import grpc
import os
from concurrent import futures
from dotenv import load_dotenv
import sys
from src.protobuf import file_service_pb2
from src.protobuf import file_service_pb2_grpc

# python -m grpc_tools.protoc -Iprotos/ --python_out=src/protobuf/ --grpc_python_out=src/protobuf/ protos/file_service.proto
# export PYTHONPATH="/home/ravendexter/Desktop/code/project/new_repo_yadro/qemu-riscv-cluster/qemu-riscv-cluster/src/protobuf:/home/ravendexter/Desktop/code/project/new_repo_yadro/qemu-riscv-cluster/qemu-riscv-cluster:$PYTHONPATH"
load_dotenv(os.path.join(os.path.dirname(__file__), '../../env/.grpc.env'))
AVAILABLE_CHARACTERS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !?.,\n"

class FileValidator:
    @staticmethod
    def validate_text(content, charset):
        try:
            decoded = content.decode('utf-8')
            return all(c in charset for c in decoded)
        except UnicodeDecodeError:
            return False

    @staticmethod
    def validate_binary(content):
        return True

class FileService(file_service_pb2_grpc.FileServiceServicer):
    def __init__(self, text_charset):
        self.text_charset = text_charset
        
    def UploadFile(self, request, context):
        try:
            actual_size = len(request.content)
            is_valid = False
            if request.file_type == "text":
                is_valid = FileValidator.validate_text(request.content, self.text_charset)
            elif request.file_type == "binary":
                is_valid = FileValidator.validate_binary(request.content)
            
            return file_service_pb2.FileResponse(
                size=actual_size,
                is_valid=is_valid,
                message="Validation successful" if is_valid else "Invalid file content"
            )
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {str(e)}")
            return file_service_pb2.FileResponse()

def serve():
    max_message_length = int(os.getenv('GRPC_MAX_MESSAGE_LENGTH'))
    port = os.getenv('GRPC_PORT')
    host = os.getenv('GRPC_SERVER_HOST')

    options = [
        ('grpc.max_receive_message_length', max_message_length), 
        ('grpc.max_send_message_length', max_message_length), 
    ]
    
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=options
    )
    
    file_service_pb2_grpc.add_FileServiceServicer_to_server(
        FileService(text_charset=AVAILABLE_CHARACTERS), 
        server
    )
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    print(f"Server started on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()