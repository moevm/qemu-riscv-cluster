#!/bin/bash
set -e

# Load environment variables
if [ -f log_and_metric/.env ]; then
    source log_and_metric/.env
else
    echo "Error: .env file not found"
    exit 1
fi

# Default configuration
TEST_DURATION=60
CONCURRENT_USERS=3
TEST_FILE_SIZE="10KB"
TEST_FILE_TYPE="text"

# Parse CLI arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -d|--duration) TEST_DURATION="$2"; shift ;;
        -c|--concurrent) CONCURRENT_USERS="$2"; shift ;;
        -s|--size) TEST_FILE_SIZE="$2"; shift ;;
        -t|--type) TEST_FILE_TYPE="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

function check_dependencies() {
    echo "Checking dependencies..."
    for dep in python3 pip3 curl; do
        if ! command -v $dep &> /dev/null; then
            echo "Missing dependency: $dep"
            exit 1
        fi
    done
}

function check_service() {
    local name=$1
    local url=$2
    local retries=30
    local wait=2

    echo "Checking $name at $url..."
    for ((i=1; i<=retries; i++)); do
        if curl -s "$url" > /dev/null; then
            echo "$name is available."
            return 0
        fi
        echo "Waiting for $name... ($i/$retries)"
        sleep $wait
    done
    echo "Failed to reach $name"
    return 1
}

function check_services() {
    check_service "Grafana" "$GRAFANA_URL" || return 1
    check_service "Prometheus" "$PROMETHEUS_URL" || return 1
    check_service "Loki" "$LOKI_URL" || return 1
}

function setup_virtualenv() {
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
    else
        echo "Using existing virtual environment."
        source venv/bin/activate

        if [ requirements.txt -nt venv/requirements.timestamp ]; then
            echo "Requirements changed. Updating..."
            pip install -r requirements.txt
            touch venv/requirements.timestamp
        fi
    fi
}

function generate_protobuf() {
    if [ ! -f "src/protobuf/file_service_pb2.py" ]; then
        echo "Generating gRPC code..."
        python -m grpc_tools.protoc -Iprotos/ --python_out=src/protobuf/ --grpc_python_out=src/protobuf/ protos/file_service.proto
    fi
    export PYTHONPATH="src/protobuf:$PYTHONPATH"
}

function generate_test_file() {
    case "$TEST_FILE_TYPE" in
        text)
            base64 /dev/urandom | head -c "$TEST_FILE_SIZE" > testfile.txt ;;
        binary)
            head -c "$TEST_FILE_SIZE" /dev/urandom > testfile.bin ;;
        *)
            echo "Unknown file type: $TEST_FILE_TYPE"; exit 1 ;;
    esac
}

function run_load_test() {
    echo "Running load test for $TEST_DURATION sec with $CONCURRENT_USERS users on $TEST_FILE_TYPE file of $TEST_FILE_SIZE"
    python3 load_test.py "$CONCURRENT_USERS" "$TEST_DURATION" "$TEST_FILE_SIZE" "$TEST_FILE_TYPE"
}

function collect_metrics() {
    echo "Collecting Prometheus metrics..."
    curl -s "$PROMETHEUS_URL/api/v1/query?query=grpc_requests_total" > metrics_requests.json
    curl -s "$PROMETHEUS_URL/api/v1/query?query=grpc_request_latency_seconds_count" > metrics_latency.json
    curl -s "$PROMETHEUS_URL/api/v1/query?query=grpc_request_size_bytes_sum" > metrics_size.json
    curl -s "$PROMETHEUS_URL/api/v1/query?query=grpc_request_errors_total" > metrics_errors.json
}

function cleanup_files() {
    rm -f testfile.txt testfile.bin
}

function main() {
    check_dependencies
    check_services || { echo "One or more services are unavailable."; exit 1; }
    setup_virtualenv
    generate_protobuf
    generate_test_file
    run_load_test
    collect_metrics
    cleanup_files
    echo "Test finished. Check Grafana dashboard for results."
}

main
