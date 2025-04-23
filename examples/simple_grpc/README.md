# Simple gRPC

- Create a virtual environment 
```
python3 -m venv venv
```
- Activate VE 
```
source venv/bin/activate
```
- Install the necessary dependencies 
``` 
pip install -r requirements.txt
```
- Generate Python code from the .proto file 
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. sum.proto
```
- Start the python server 
```
python3 server.py
```
- Launch the client (in another terminal) 
```
python3 client.py
```