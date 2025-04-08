# Docker compose with replicas 

## Tree

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

## Build and run

To build and run, go to the `deploy` directory and run the following command:

```
docker compose build && docker compose up
```

To stop, run the command:

```
docker compose down
```

## Resume

Docker Compose runs one container -- `central_node` on which all network traffic is listened to via the `tcpdump` utility, as well as several (the number is set via the `replicas` variable in the `.env` file) containers -- `replicated_nodes`, each of which pings via a python script `central_node` and, if successful, terminates with an `exit code 0` after 60 seconds. All traffic coming into `central_node` is saved in the `logs_volume` in the .pcap file format [(example)](./deploy/example_logs/traffic.pcap).
