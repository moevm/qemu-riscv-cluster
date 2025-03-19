# Разработка docker-compose с зеркалированием контейнеров

## Структура

```
deploy
├── compose.yaml
├── Dockerfile
├── example_logs
│   └── traffic.pcap
└── src
    ├── ping.py
    └── entrypoint.sh
```

- Compose file: [compose.yaml](./deploy/compose.yaml)

- Dockerfile: [Dockerfile](./deploy/Dockerfile)

- Python script: [ping.py](./deploy/src/ping.py)

- Entrypoint script: [entrypoint.sh](./deploy/src/entrypoint.sh)

- Env. file: [.env](./deploy/.env)

## Сборка и запуск

Для сборки и запуска необходимо перейти в директорию `deploy` и выполнить следующую команду:

```
docker compose build && docker compose up
```

Для остановки контейнеров необходимо в директории `deploy` выполнить следующую команду:

```
docker compose down
```

## Резюме

`docker compose` запускает один `central_node` с `alpine linux` на котором прослушивает весь сетевой трафик через `tcpdump`, а также несколько (количество задается через переменную `replicas` в `.env` файле) `replicated_nodes` с `alpine linux`, каждый из которых пингует через python-скрипт `central_node` и в случае успеха завешается с `exit code 0` через 60 секунд. Весь трафик поступающий в `central_node` сохраняется в `logs_volume` в формате .pcap файла, в директории `deploy/example_logs` можно найти [пример такого файла](./deploy/example_logs/traffic.pcap).
