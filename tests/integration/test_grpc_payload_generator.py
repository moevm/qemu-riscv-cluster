import subprocess
import time
import pytest
import grpc
import sys
import os

from src.utils.payload_generator import PayloadGenerator

@pytest.mark.integration
def test_text_file_upload(tmpdir, grpc_server, grpc_client):
    text_size = 10
    generator = PayloadGenerator(size=text_size, file_type="text", unit="MB")
    file_path = generator.generate(output_dir=tmpdir, filename="test_text_file.txt")
    response = grpc_client.upload_and_validate(file_path, "text")

    assert response.size == text_size * 1024 *1024
    assert response.is_valid is True
    assert response.message == "Validation successful"

@pytest.mark.integration
def test_binary_file_upload(tmpdir, grpc_server, grpc_client):
    text_size = 2048
    generator = PayloadGenerator(size=text_size, file_type="binary")
    file_path = generator.generate(output_dir=tmpdir, filename="test_binary_file.bin")
    response = grpc_client.upload_and_validate(file_path, "binary")

    assert response.size == text_size
    assert response.is_valid is True
    assert response.message == "Validation successful"