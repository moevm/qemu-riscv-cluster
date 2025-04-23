# Examples
## gRPC
### [simple-grpc](./simple_grpc/)

This directory contains a simple gRPC example consisting of a client and server implementation.

The gRPC server provides a service that sums two numbers. When the client establishes a connection, it sends a request containing two numbers to the server. The server processes the request by adding the numbers and returns the result to the client.

* Server: Listens on port `50051` and implements the Sum service
* Client: Connects to the server and makes requests with numbers to be summed

The example demonstrates basic gRPC communication patterns including service definition, server implementation, and client invocation.


[**INSTRUCTION FOR RUN**](./simple_grpc/README.md)

## Node Replicas

### [Docker compose with replicas](./docker_compose_with_replicas/)

Docker Compose runs one container -- `central_node` on which all network traffic is listened to via the `tcpdump` utility, as well as several (the number is set via the `replicas` variable in the `.env` file) containers -- `replicated_nodes`, each of which pings via a python script `central_node` and, if successful, terminates with an `exit code 0` after 60 seconds. All traffic coming into `central_node` is saved in the `logs_volume` in the .pcap file format.

[**INSTRUCTION FOR RUN**](./docker_compose_with_replicas/README.md)


## Logging

### [Log server](./log_collector/log_service/)

Stack Components:
* Loki - Log aggregation system
* Grafana - Visualization and analytics

Configuration:
1) Loki
    * Port: `3100`
    * IP: `172.29.0.2`
    * Config: [loki.yml](./log_collector/log_service/configs/loki/loki.yml)
2) Grafana
    * Port: `3000`
    * IP: `172.29.0.3`
    * Config: [datasource.yml](./log_collector/log_service/configs/grafana/datasource.yml) (auto-connects to Loki)

[**INSTRUCTION FOR RUN**](./log_collector/log_service/README.md)

### [Log client](./log_collector/client/)
This setup deploys 3 containers with Loki logging driver to send logs to a Loki instance at `172.29.0.2:3100`:
* cpp-app
    * C++ application logging messages via std::cout/std::cerr
    * Loki labels: Static: `container_name`, `host`; Dynamic: Auto-populates `container_name={{.Name}}`
* err-cpp
    * C++ application generating runtime errors (invalid operations)
    * Basic Loki config (no additional labels)
* logging_app
    * Python application with structured logging
    * Log processing pipeline:
        * Extracts level from log patterns `(level=, lvl=)`
        * Adds dynamic level label to Loki entries

[**INSTRUCTION FOR RUN**](./log_collector/client/README.md)

## Metrics collection

### [metrics server](./metrics/metrics-server/)

1) Apps send metrics to Pushgateway (port `9091`)
2) Prometheus scrapes them every `15s`
3) Pushgateway temporarily stores metrics until collected
4) Web Interfaces Prometheus UI (port `9090`)


[prometheus.yml](./metrics/metrics-server/prometheus.yml):
* Scrape interval: `15s`
* Target: `localhost:9091` (Pushgateway)
* honor_labels: `true` – preserves original metric labels

[entry.sh](./metrics/metrics-server/entry.sh)
* Runs Pushgateway (background process)
* Runs Prometheus (main process)



[**INSTRUCTION FOR RUN**](./metrics/metrics-server/README.md)

### [metrics client](./metrics/metrics-client/)
This is a C++ application that collects and sends metrics to Prometheus via Pushgateway.

What it does:
1) Collects system metrics:
    * CPU usage - reads from `/proc/stat`
    * Memory usage - reads from `/proc/meminfo`
    * Request count - manually incremented via `incrementRequestCount()`
2) Pushes metrics to Pushgateway:
    * Updates metrics every 5 seconds (`mainLoop()`)
    * Uses Pushgateway as intermediate storage for Prometheus

[**INSTRUCTION FOR RUN**](./metrics/metrics-client/README.md)