import grpc
from concurrent import futures
import sum_pb2
import sum_pb2_grpc

SERVER_PORT = 50051


class SumService(sum_pb2_grpc.SumServiceServicer):
    def Sum(self, request, context):
        result = request.a + request.b
        return sum_pb2.SumResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sum_pb2_grpc.add_SumServiceServicer_to_server(SumService(), server)
    server.add_insecure_port(f'0.0.0.0:{SERVER_PORT}')
    server.start()
    print(f"The server is running on the port {SERVER_PORT}")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()