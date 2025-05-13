# System deployment instructions

## System architecture

The system consists of the following components:
1. Several RISC-V virtual machines created with QEMU
2. Controller - central control component (Go)
- Manages workers via Unix sockets
- Provides task distribution
3. Workers - processing components (C++)
- Connect to the controller via Unix sockets
- Perform hash calculations
4. Monitoring system (Grafana, Prometheus, Loki)

## Deployment procedure

### 1. Preparing the environment

The host machine must have the following installed:
- Linux with KVM support
- QEMU for RISC-V emulation

### 2. Preparing components

1. Preparing base images:
- Creating an image for the controller via Yocto:
* Optimized image for RISC-V
* Includes the necessary dependencies for Go
* Configured for operation with metrics and logs
- Creating an image for a worker via Yocto:
* Optimized image for RISC-V
* Includes the necessary C++ runtime dependencies
* Configured to work with metrics and logs

2. Compiling and deploying the controller:

- Process:
* Compiling Go code via Bazel in a container
* Using a prepared Yocto image to run
* Setting up a volume for a Unix socket
* Exporting metrics for Prometheus
* Sending logs to Loki

3. Compiling and deploying workers:

- Process:
* Compiling C++ code via Bazel in a container
* Using a prepared Yocto image to run
* Connecting to the controller's Unix socket
* Exporting metrics for Prometheus
* Sending logs to Loki

4. Important points:
- Compilation occurs in separate containers with Bazel
- Launching is performed on images built via Yocto
- Each component has its own docker-compose.yml
- Collection of metrics and logs for monitoring is configured

### 3. Monitoring

1. Prometheus:
- Collection of metrics from the controller and workers
- Setting up goals via service discovery
- Storing historical data

2. Loki:
- Centralized log collection
- Aggregation of logs from all components
- Structured storage

3. Grafana:
- Visualization of metrics from Prometheus
- Viewing logs from Loki
- Configured dashboards for monitoring

## Important notes

1. The order of launch is important: first the controller, then the workers
2. All components are launched via Docker Compose
3. Communication via Unix sockets
4. SSH is used only for VM management
5. Base images are created via Yocto
6. Compilation occurs via Bazel in a container
7. When updating the code:
- Stopping the corresponding service
- Rebuild via docker-compose up --build
- Logs and metrics are saved in the monitoring system

### 7. Health check

1. Grafana checks:
- Controller status
- Status of each worker
- Performance metrics
- System resources

2. Controller logs check:
- Creating a Unix socket
- ​​Connecting workers
- No interaction errors

### 8. System management

Basic management operations:
1. Stopping/starting individual workers
2. Restarting the controller if necessary
3. Completely stopping the system in the following order:
- Stopping all workers
- Stopping the controller
- Stopping virtual machines
- Stopping the monitoring system

### 9. Troubleshooting

If problems arise, the following is checked:
1. SSH availability for VM management
2. Availability and access rights to the Unix socket
3. Controller logs for errors IPC
4. Worker logs to check the connection
5. Metrics in Prometheus
6. Docker container status

## Important notes

1. The order of startup is important: first the controller, then the workers
2. All components run in Docker containers
3. Communication between the controller and workers is via Unix sockets
4. SSH is used only for VM management
5. Monitoring is performed centrally via Grafana
6. Code is built via Bazel in the container
7. When updating the code:
- Rebuild via Bazel in the container
- Restart updated components