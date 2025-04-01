# Prometheus server

## How to run?

* Create a network if you haven't already done so, following the instructions in `metrics-client/README.md`:
```sh
docker network create example-network
```

* Build docker image:
```sh
./build.sh
```

* Run docker container:
```
docker run --network example-network --rm -p 9090:9090 --name server qemu-riscv-cluster/metrics-server
```

Now you can open the Prometheus frontend in your browser at `localhost:9090`.
