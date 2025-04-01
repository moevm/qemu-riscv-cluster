import pytest
import subprocess
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(main_dir, "src", "protobuf"))

from src.client.client import FileClient


@pytest.fixture(scope="module")
def grpc_server():
    controller_path = os.path.join(
        os.path.dirname(__file__), '..', 'src', 'server_tests', 'payload_generator_server.py'
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(sys.path)

    server_process = subprocess.Popen(
        ['python3', controller_path],
        env=env
    )
    time.sleep(2)
    yield
    server_process.terminate()


@pytest.fixture(scope="module")
def grpc_client():
    client = FileClient()
    return client
