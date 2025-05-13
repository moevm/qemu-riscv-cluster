# System Deployment Guide

## System Architecture

The system consists of the following components:

1. Multiple Linux virtual machines
2. Controller – the central management component (Go)

   * Manages workers via Unix sockets
   * Distributes tasks among workers
3. Workers – processing components (C++)

   * Connect to the controller via Unix sockets
   * Perform hash computations
4. Monitoring stack (Grafana, Prometheus, Loki)

## Deployment Procedure

### 1. Environment Preparation

The host machine must have:

* Linux with KVM support
* Docker and Docker Compose
* Git to work with the repository

### 2. Component Preparation

1. Controller preparation:

   * Build and create Docker image:

     ```bash
     cd controller
     docker build -f Dockerfile.controller -t controller:latest .
     ```
   * Build notes:

     * Uses a Bazel-based base image
     * Go code is built inside the container via Bazel
     * A volume is created for the Unix socket

2. Worker preparation:

   * Build and create Docker image:

     ```bash
     cd controller
     docker build -f Dockerfile.worker -t worker:latest .
     ```
   * Build notes:

     * Uses a Bazel-based base image
     * C++ code is built inside the container
     * Environment is configured for the worker

3. Key build notes:

   * Bazel is used for both Go and C++ code
   * Build happens entirely inside the Docker container
   * All dependencies are defined in WORKSPACE and BUILD files
   * Docker images contain only the necessary runtime files

4. Verification:

   * Run tests via Bazel
   * Verify Docker image correctness
   * Test functionality on the target system

### 3. Launching Virtual Machines

1. The `ports.conf` file lists ports for each VM (one port per line)
2. The `run.sh` script reads this file and launches the required number of VMs
3. SSH port forwarding is set up for each VM
4. The first VM (first port in the list) is used for the controller
5. The remaining VMs are used for the workers

### 4. Launching the Monitoring Stack

The monitoring stack is launched on the host using Docker Compose:

1. Grafana – for visualization
2. Prometheus – for metrics collection
3. Loki – for log collection

### 5. Deploying the Controller

1. The controller is launched on the first VM using Docker Compose
2. In `docker-compose.controller.yml`, configure:

   * Path to the Unix socket for communication with workers
   * Port for Prometheus metrics
   * Loki log forwarding settings
3. The Unix socket is mounted into the container via a volume

### 6. Deploying the Workers

1. Each VM runs a worker via Docker Compose
2. Each worker has its own configuration:

   * The same Unix socket path is mounted in `docker-compose.yml`
   * CPU binding is configured via Docker
   * Metrics and log forwarding parameters are set

### 7. Verifying Functionality

1. In Grafana, verify:

   * Controller status
   * Status of each worker
   * Performance metrics
   * System resource usage

2. In controller logs, verify:

   * Unix socket creation
   * Worker connections
   * No IPC communication errors

### 8. System Management

Main management operations:

1. Start/stop individual workers
2. Restart the controller if necessary
3. Full system shutdown in the following order:

   * Stop all workers
   * Stop the controller
   * Stop the virtual machines
   * Stop the monitoring stack

### 9. Troubleshooting

In case of issues, check:

1. SSH availability for VM management
2. Presence and permissions of the Unix socket
3. Controller logs for IPC errors
4. Worker logs for connection issues
5. Metrics in Prometheus
6. Docker container status

## Important Notes

1. Startup order is important: controller first, then workers
2. All components run inside Docker containers
3. Communication between controller and workers is via Unix sockets
4. SSH is used only for managing VMs
5. Centralized monitoring via Grafana
6. All components are built with Bazel inside Docker
7. When updating code:

   * Rebuild the corresponding Docker image
   * Update the containers in the system