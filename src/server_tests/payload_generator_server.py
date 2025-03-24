import grpc
import os
import traceback
from concurrent import futures
from dotenv import load_dotenv
from typing import Set
from src.protobuf import file_service_pb2
from src.protobuf import file_service_pb2_grpc

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', 'env', '.grpc.env'))
AVAILABLE_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !?.,\n"


class FileValidator:
    @staticmethod
    def validate_text(content: bytes, charset: Set[str]) -> bool:
        """
        Checks that the file contents consist of only valid characters.

        Arguments:

        `content: bytes` - The byte content of the file.

        `charset: Set[str]` - A set of valid characters.

        Output data:

        `bool` - True if the content is valid, otherwise False.
        """
        try:
            decoded: str = content.decode('utf-8')
            return all(c in charset for c in decoded)
        except UnicodeDecodeError:
            return False

    @staticmethod
    def validate_binary(content: bytes) -> bool:
        """
        Verification for binary files.

        Arguments:

        `content: bytes` - The byte content of the file.

        Output data:

        `bool` - True if the content is valid, otherwise False.
        """
        return True


class FileService(file_service_pb2_grpc.FileServiceServicer):
    def __init__(self, text_charset: str) -> None:
        self.text_charset: Set[str] = set(text_charset)

    def UploadFile(self, request: file_service_pb2.FileRequest,
                   context: grpc.ServicerContext) -> file_service_pb2.FileResponse:
        """
        Processes a request to upload a file.

        Arguments:

        `request: file_service_pb2.FileRequest` - A request with the contents of the file and its type.

        `context: grpc.ServicerContext` - The gRPC Context

        Output data:

        `file_service_pb2.FileResponse` - The response with the validation result.
        """
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
            error_trace = traceback.format_exc()
            print(f"Error trace: {error_trace}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error: {e}")
            return file_service_pb2.FileResponse()


def serve():
    """
    Starts the gRPC server.
    """
    max_message_length = int(os.environ['GRPC_MAX_MESSAGE_LENGTH'])
    port = os.environ['GRPC_PORT']
    host = os.environ['GRPC_SERVER_HOST']

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
