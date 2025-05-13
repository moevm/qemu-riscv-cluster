# System deployment instructions

## System architecture

The system consists of the following components:
1. Several virtual machines with Linux
2. Controller - the central control component (Go)
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
- Docker and Docker Compose

### 2. Creating base images using Yocto

1. Preparing Yocto layers: Creating a custom layer for our components
2. Setting up a layer for the controller
3. Setting up a layer for the worker
4. Building images

### 3. Launching virtual machines

1. The ports.conf file specifies ports for each VM (one port per line)
2. The run.sh script reads this file and starts the corresponding number of VMs
3. SSH port forwarding is configured for each VM
4. The first VM (the first port in the list) will be used for the controller
5. The remaining VMs will be used for workers

### 4. Starting the monitoring system

The monitoring stack is launched on the host machine (using docker-compose):
1. Grafana - for visualization
2. Prometheus - for collecting metrics
3. Loki - for collecting logs

### 5. Deploying the controller

The controller is launched on the first VM via docker-compose:
* Compiling Go code via Bazel in a container
* Using a prepared Yocto image for launching
* Setting up a volume for a Unix socket
* Exporting metrics for Prometheus
* Sending logs to Loki

### 6. Deploying workers

Launch a worker on each VM via docker-compose:
* Compiling C++ code via Bazel in a container
* Using a prepared Yocto image to launch
* Connecting to the controller's Unix socket
* Exporting metrics for Prometheus
* Sending logs to Loki

### 7. Checking health

1. Checking Grafana for:
- Controller status
- Status of each worker
- Performance metrics
- System resources

2. Checking controller logs for:
- Creating a Unix socket
- ​​Connecting workers
- No interaction errors

### 8. System management

Basic management operations:
1. Stopping/starting individual workers
2. Restarting the controller if necessary
3. Stopping the system completely in the following order:
- Stopping all workers
- Stopping the controller
- Stopping virtual machines
- Stopping the monitoring system

### 9. Troubleshooting

If problems occur, the following is checked:
1. Availability of SSH for VM management
2. Availability and access rights to the Unix socket
3. Controller logs for IPC errors
4. Worker logs to check the connection
5. Metrics in Prometheus
6. Docker container status

## Important notes

1. The order of startup is important: first the controller, then the workers
2. Base images are built using Yocto for optimization and size minimization
3. Docker images use minimal base images from Yocto
4. Communication between the controller and workers is via Unix sockets
5. SSH is used only for VM management
6. Monitoring is performed centrally via Grafana
7. Components are built via Bazel inside Docker using optimized Yocto images
8. When updating the code:
- Rebuild the corresponding Docker image
- Update containers in the system