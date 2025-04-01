# Client for metrics collection (Telegraf)

Collects basic metrics (CPU time and memory) and custom metric `custom-metric.sh`.
It does't actually measure anything, it just calculates a sine function.

## How to run?

In a real scenario, the clients-collectors will be launched on different machines with different IP addresses, but for demonstration purposes, we will launch several clients on one machine:

* Create a network:
```sh
docker network create example-network
```

* Build docker image:
```sh
./build.sh
```

* Run docker container for first client:
```sh
docker run --network example-network -e WORKER_NAME=client1 -e PROMETHEUS_GATEWAY_ADDRESS=server -e PROMETHEUS_GATEWAY_PORT=9091 --rm -d qemu-riscv-cluster/metrics-client
```

* Run docker container for second client:

```sh
docker run --network example-network -e WORKER_NAME=name_it_however_you_want -e PROMETHEUS_GATEWAY_ADDRESS=server -e PROMETHEUS_GATEWAY_PORT=9091 --rm -d qemu-riscv-cluster/metrics-client
```
