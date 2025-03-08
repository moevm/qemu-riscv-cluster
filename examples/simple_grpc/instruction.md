# Simple gRPC

- Создать виртуальное окружение ``python3 -m venv venv``
- Активировать ВО ``source venv/bin/activate``
- Установить нужные зависимости ``pip install -r requirements.txt``
- Сгенерируйте Python-код из .proto файла 
``python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. sum.proto``
- Запустите сервер python ``server.py``
- Запустите клиент (в другом терминале) python ``client.py``