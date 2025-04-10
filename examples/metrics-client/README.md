# Client for metrics collection

Uses [prometheus-cpp](https://github.com/jupp0r/prometheus-cpp) library. Collects basic metrics: `cpu_usage`,
`memory_used` and `request_count`.

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
