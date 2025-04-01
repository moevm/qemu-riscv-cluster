import pytest
import os
from src.utils.payload_generator import PayloadGenerator


@pytest.mark.integration
def test_text_file_upload(tmpdir, grpc_server, grpc_client):
    text_size = 10
    file_path = os.path.join(tmpdir, "test_text_file.txt")

    generator = PayloadGenerator(size=text_size, file_type="text", unit="MB")
    generated_path = generator.generate(path=file_path)
    response = grpc_client.upload_and_validate(generated_path, "text")

    assert response.size == text_size * 1024 * 1024 
    assert response.is_valid is True
    assert response.message == "Validation successful"


@pytest.mark.integration
def test_binary_file_upload(tmpdir, grpc_server, grpc_client):
    binary_size = 2048
    file_path = os.path.join(tmpdir, "test_binary_file.bin")

    generator = PayloadGenerator(size=binary_size, file_type="binary")
    generated_path = generator.generate(path=file_path)
    response = grpc_client.upload_and_validate(generated_path, "binary")

    assert response.size == binary_size
    assert response.is_valid is True
    assert response.message == "Validation successful"
