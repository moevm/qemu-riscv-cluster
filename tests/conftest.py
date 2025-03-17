import pytest
import subprocess
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.client.client import FileClient

@pytest.fixture(scope="module")
def grpc_server():
    controller_path = os.path.join(
        os.path.dirname(__file__), '..', 'src', 'controller', 'controller.py'
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