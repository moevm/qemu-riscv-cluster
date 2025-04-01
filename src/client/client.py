import grpc
from dotenv import load_dotenv
import os
from src.utils.payload_generator import PayloadGenerator
from src.protobuf import file_service_pb2
from src.protobuf import file_service_pb2_grpc

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "env", ".grpc.env"))


class FileClient:
    def __init__(self):
        self.host: str = os.environ["GRPC_CLIENT_HOST"]
        self.port: str = os.environ["GRPC_PORT"]
        max_message_length: int = int(os.environ["GRPC_MAX_MESSAGE_LENGTH"])

        options = [
            ("grpc.max_receive_message_length", max_message_length),
            ("grpc.max_send_message_length", max_message_length),
        ]

        self.channel: grpc.Channel = grpc.insecure_channel(f"{self.host}:{self.port}", options=options)

        self.stub: file_service_pb2_grpc.FileServiceStub = file_service_pb2_grpc.FileServiceStub(self.channel)

    def upload_and_validate(self, file_path: str, file_type: str) -> file_service_pb2.FileResponse:
        """
        Uploads the file to the server and verifies its validity.

        Arguments:

        `file_path: str` - File path

        `file_type: str` - File type ("text" or "binary")

        Output data:

        `file_service_pb2.FileResponse` - Server response with validation result
        """
        with open(file_path, "rb") as f:
            content: bytes = f.read()

        request: file_service_pb2.FileRequest = file_service_pb2.FileRequest(
            filename=file_path, content=content, file_type=file_type
        )

        return self.stub.UploadFile(request)


def test_file_upload():
    client = FileClient()

    valid_text = PayloadGenerator(size=10, file_type="text", unit="MB").generate(path="data/files/hello_text.txt")
    response = client.upload_and_validate(valid_text, "text")
    print(f"Valid text: Size={response.size}, Valid={response.is_valid}, Msg={response.message}")

    binary_file = PayloadGenerator(size=2048, file_type="binary").generate(path="data/files/hello_bin.bin")
    response = client.upload_and_validate(binary_file, "binary")
    print(f"Binary file: Size={response.size}, Valid={response.is_valid}, Msg={response.message}")


if __name__ == "__main__":
    test_file_upload()
