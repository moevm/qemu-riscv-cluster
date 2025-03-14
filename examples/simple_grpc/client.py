import grpc
import sum_pb2
import sum_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = sum_pb2_grpc.SumServiceStub(channel)
    
    response = stub.Sum(sum_pb2.SumRequest(a=22, b=2332))
    print(f"The result of the addition: {response.result}")

if __name__ == '__main__':
    run()