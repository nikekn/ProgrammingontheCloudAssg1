import fetch_pb2_grpc
import fetch_pb2
import requests

rfw_id = input("Enter the RFW ID\n")
benchmark_type = str(input('Choose benchmark type you require:\n 1: DVD testing \n 2: DVD training\n 3: NDBench testing\n 4: NDBench training\n '))
workload_metric = input("Choose workload metric you require?:\n 1: Cpu utilization average\n 2: Network in average\n 3: Network out average\n 4: Memory utilization average\n 5: Final target \n")
batch_unit = input('How many units do you want in one batch?\n')
batch_size = input('How many batches do you require?\n')
batch_id = input('Which batch of data do you want? \n')

info_req = fetch_pb2.Request()

info_req.req_id = rfw_id
info_req.benchmark_type = benchmark_type
info_req.workload_metric = workload_metric
info_req.batch_unit = int(batch_unit)
info_req.batch_size = int(batch_size)
info_req.batch_id = int(batch_id)


info_result = requests.get("http://172.31.53.44:5000/serve?",
                      headers={'Content-Type': 'application/protobuf'},
                      data= info_req.SerializeToString())

print(info_result.content)
info_response = fetch_pb2.Response.FromString(info_result.content)

print(info_response)
