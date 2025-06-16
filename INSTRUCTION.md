# Project Launch Guide

## 1. Clone the Repositories

```bash
# Clone the main repository
git clone https://github.com/moevm/qemu-riscv-cluster.git
cd qemu-riscv-cluster

# Initialize and update submodules
git submodule init
git submodule update
```

## 2. Dependencies for Running on Host

### System Dependencies

```bash
# Install required packages
sudo apt-get install -y \
    docker.io \
    docker-compose \
    python3 \
    python3-pip
```

## 3. Project Management

The project management script supports the following commands:

```bash
# Update submodules
./deploy_service.sh update

# Start services (default: 5 replicas)
./deploy_service.sh start [number_of_replicas]

# Stop services
./deploy_service.sh stop

# Restart services
./deploy_service.sh restart [number_of_replicas]

# Full reset (stop, remove, initialize, start)
./deploy_service.sh reset [number_of_replicas]

# Show help
./deploy_service.sh help
```

The script will launch:

* Grafana
* Prometheus
* Loki
* gRPC server
* Docker Compose with the controller
* Worker containers (specified number of replicas)

## 4. Running Tests

### Test Preparation

1. Make sure all system components are up and running
2. Verify the availability of all services:

   * Grafana (port 3000)
   * Prometheus (port 9090)
   * Loki (port 3100)
   * gRPC server

### Load Test Description

The load test validates the performance of the load distribution system and includes:

1. File upload testing:

   * Generating test files of a specified size and type
   * Sending files through the gRPC server
   * Validating file uploads and correctness

2. Load distribution testing:

   * Simulating multiple concurrent users
   * Checking task distribution balance across workers
   * Monitoring individual worker load

3. Performance metrics collection:

   * System response time
   * Number of processed requests
   * Size of processed files
   * Number of errors

### Running the Load Test

```bash
# Run the test with default parameters
./run_load_test.sh

# Or with custom parameters
./run_load_test.sh -d 60 -c 3 -s 10KB -t text
```

Test parameters:

* `-d, --duration` – duration of the test in seconds (default: 60)
* `-c, --concurrent` – number of concurrent users (default: 3)
* `-s, --size` – size of the test file (default: 10KB)
* `-t, --type` – type of the test file (text or binary)

### Test Results

After running the test, you'll see:

* Total number of requests
* Average response time
* 95th percentile response time
* 99th percentile response time
* Total test duration

Metrics are also available in:

* Prometheus (port 9090)
* Grafana dashboards (port 3000)
* Loki logs (port 3100)

## 5. Monitoring

Once all components are running, you can access:

* Grafana: [http://localhost:3000](http://localhost:3000)
* Prometheus: [http://localhost:9090](http://localhost:9090)
* Loki: [http://localhost:3100](http://localhost:3100)

## 6. Stopping the Project

```bash
./deploy_service.sh stop
```