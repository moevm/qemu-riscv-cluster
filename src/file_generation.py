import sys
import os
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
main_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(main_dir, "protobuf"))

from controller.controller import serve
from client.client import test_file_upload

if __name__ == "__main__":
    server_thread = threading.Thread(target=serve)
    server_thread.start()

    test_file_upload()
