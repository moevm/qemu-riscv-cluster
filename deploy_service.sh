#!/bin/bash
set -e

REPO_DIR="external/grpc_server"
LOG_COMPOSE_FILE="log_and_metric/docker-compose.yml"
MAIN_COMPOSE_FILE="docker-compose.manager.controller.yml"
DEFAULT_REPLICAS=5

function update_submodule() {
    if [ ! -d "$REPO_DIR" ]; then
        echo "Error: Submodule does not exist"
        exit 1
    fi
    git submodule update --init --recursive
    echo "Submodule successfully updated"
}

function start_services() {
    local replicas=${1:-$DEFAULT_REPLICAS}
    
    if [ ! -d "$REPO_DIR" ]; then
        echo "Error: Submodule does not exist"
        exit 1
    fi
    
    docker-compose -f "$LOG_COMPOSE_FILE" up -d --build
    
    REPLICAS=$replicas docker-compose -f "$MAIN_COMPOSE_FILE" up -d --build
    
    echo "All services successfully started with $replicas replicas"
}

function stop_services() {
    if [ ! -d "$REPO_DIR" ]; then
        echo "Error: Submodule does not exist"
        exit 1
    fi
    
    docker-compose -f "$MAIN_COMPOSE_FILE" down || true
    
    docker-compose -f "$LOG_COMPOSE_FILE" down || true
    
    echo "All services successfully stopped"
}

function restart_services() {
    local replicas=${1:-$DEFAULT_REPLICAS}
    stop_services
    start_services $replicas
}

function full_reset() {
    local replicas=${1:-$DEFAULT_REPLICAS}
    stop_services
    if [ -d "$REPO_DIR" ]; then
        remove_submodule
    fi
    init_submodule
    start_services $replicas
}

function show_help() {
    echo "Usage: $0 [command] [replicas]"
    echo ""
    echo "Commands:"
    echo "  update              - Update submodule"
    echo "  start [replicas]    - Start services (default: $DEFAULT_REPLICAS replicas)"
    echo "  stop                - Stop services"
    echo "  restart [replicas]  - Restart services (default: $DEFAULT_REPLICAS replicas)"
    echo "  reset [replicas]    - Full reset (stop, remove, init, start)"
    echo "  help                - Show help message"
}

case "$1" in
    update)
        update_submodule
        ;;
    start)
        start_services "$2"
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services "$2"
        ;;
    reset)
        full_reset "$2"
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac