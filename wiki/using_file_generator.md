# payload generation gRPC

## initialization and generation
- create a virtual environment at the root ``python3 -m venv venv``
- activate VE ``source venv/bin/activate``
- install the necessary dependencies ``pip install -r requirements.txt``
- generate Python code from the .proto file ``python -m grpc_tools.protoc -Iprotos/ --python_out=src/protobuf/ --grpc_python_out=src/protobuf/ protos/file_service.proto``

## Launch Options
### file launch
- in the src folder, run the file file_generation.py ``python3 file_generation.py``
- this file runs the test_file_upload() function, which is defined on the client, where you can enter your tests and see how the program works.
### launching via the terminal
- it is necessary to add several paths to PYTHONPATH through the console so that the imports work normally ``export PYTHONPATH="/home/ravendexter/Desktop/code/project/new_repo_yadro/qemu-riscv-cluster/qemu-riscv-cluster/src/protobuf:/home/ravendexter/Desktop/code/project/new_repo_yadro/qemu-riscv-cluster/qemu-riscv-cluster:$PYTHONPATH"``
- you must run this command in another terminal where the client will be launched.
- in the controller directory, you need to run ``python3 controller.py``
- in another terminal in the client directory, you need to run ``python3 client.py``