from concurrent import futures
import time

import grpc
import fetch_pb2
import fetch_pb2_grpc
import pandas as pd
import json
import statistics as st
import numpy as np
from flask import Flask, request, json

app = Flask(__name__)

@app.route('/serve', methods=['GET'])
def serve():
    
    dict_bench = {
        '1': 'DVD-testing.csv',
        '2': 'DVD-training.csv',
        '3': 'NDBench-testing.csv',
        '4' : 'NDBench-training.csv'
    }

    dict_metric = {
        '1': 'CPUUtilization_Average',
        '2': 'NetworkIn_Average',
        '3': 'NetworkOut_Average',
        '4': 'MemoryUtilization_Average',
        '5': 'Final_Target'
    }

    info_req = fetch_pb2.Request.FromString(request.data)
    info_result = fetch_pb2.Response()
    rfw_id = info_req.req_id
    benchmark_type = info_req.benchmark_type
    metric = info_req.workload_metric
    batch_unit = info_req.batch_unit
    batch_id = info_req.batch_id
    batch_size = info_req.batch_size
    


    request_size = int(batch_unit)*int(batch_size)
    k = int(batch_id)
    j = k*int(batch_unit)
    df = pd.read_csv(dict_bench[benchmark_type])
    requested_data = df[dict_metric[metric]][j+1:request_size+j+1]
    print(requested_data)

    list = []
    for line in requested_data:
        list.append(line)

    analytics = {
        'avg' : np.average(list),
        'max' : max(list),
        'min' : min(list),
        'std' : round(st.stdev(list),2),
        '10p' : round(np.percentile(list, 10),2),
        '50p' : round(np.percentile(list, 50),2),
        '95p' : round(np.percentile(list, 90),2),
        '99p': round(np.percentile(list, 99),2),
        }

    print(analytics)

    final = [list[i * int(batch_unit):(i + 1) * int(batch_unit)] for i in range((len(list) + int(batch_unit) - 1) // int(batch_unit))]

    
    abc = str(j+int(batch_size)-1)

    dict_request = {
    'RFW ID':" ",
    'Last batch ID' : " ",
    'Requested data': " ",
    'Analytics': " ",
    }
    dict_request['RFW ID'] = rfw_id
    dict_request['Last batch ID'] = abc
    dict_request['Requested data']= list
    dict_request['Analytics'] = analytics

    info_result.rfw_id = dict_request['RFW ID']
    info_result.last_batch_id = dict_request['Last batch ID']
    info_result.request_data.extend(dict_request['Requested data'])
    #for num in dict_request['Requested data']:
        #info_result.requested_data.append(num)

    info_result.average = dict_request['Analytics']['avg']
    info_result.maximum = dict_request['Analytics']['max']
    info_result.minimum = dict_request['Analytics']['min']
    info_result.stdeviation = dict_request['Analytics']['std']
    info_result.percentile10 = dict_request['Analytics']['10p']
    info_result.percentile50 = dict_request['Analytics']['50p']
    info_result.percentile95 = dict_request['Analytics']['95p']
    info_result.percentile99 = dict_request['Analytics']['99p']

    if info_result is not None:
        serialized_data = info_result.SerializeToString()
        return serialized_data


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)


