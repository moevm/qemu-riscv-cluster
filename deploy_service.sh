#!/bin/bash
set -e

REPO_DIR="grpc_server"
REPO_URL="https://github.com/moevm/grpc_server.git"
LOG_COMPOSE_FILE="log_and_metric/docker-compose.yml"
MAIN_COMPOSE_FILE="docker-compose.manager.controller.yml"
DEFAULT_REPLICAS=5

function clone_repo() {
    if [ -d "$REPO_DIR" ]; then
        echo "Error: Repository already exists"
        exit 1
    fi
    git clone "$REPO_URL"
    echo "Repository successfully cloned"
}

function update_repo() {
    if [ ! -d "$REPO_DIR" ]; then
        echo "Error: Repository does not exist"
        exit 1
    fi
    cd "$REPO_DIR"
    git pull origin master
    cd ..
    echo "Repository successfully updated"
}

function remove_repo() {
    if [ ! -d "$REPO_DIR" ]; then
        echo "Error: Repository does not exist"
        exit 1
    fi
    rm -rf "$REPO_DIR"
    echo "Repository successfully removed"
}

function start_services() {
    local replicas=${1:-$DEFAULT_REPLICAS}
    
    if [ ! -d "$REPO_DIR" ]; then
        echo "Error: Repository does not exist"
        exit 1
    fi
    
    docker-compose -f "$LOG_COMPOSE_FILE" up -d --build
    
    REPLICAS=$replicas docker-compose -f "$MAIN_COMPOSE_FILE" up -d --build
    
    echo "All services successfully started with $replicas replicas"
}

function stop_services() {
    if [ ! -d "$REPO_DIR" ]; then
        echo "Error: Repository does not exist"
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
        remove_repo
    fi
    clone_repo
    start_services $replicas
}

function show_help() {
    echo "Usage: $0 [command] [replicas]"
    echo ""
    echo "Commands:"
    echo "  clone               - Clone repository"
    echo "  update              - Update repository"
    echo "  remove              - Remove repository"
    echo "  start [replicas]    - Start services (default: $DEFAULT_REPLICAS replicas)"
    echo "  stop                - Stop services"
    echo "  restart [replicas]  - Restart services (default: $DEFAULT_REPLICAS replicas)"
    echo "  reset [replicas]    - Full reset (stop, remove, clone, start)"
    echo "  help                - Show help message"
}

case "$1" in
    clone)
        clone_repo
        ;;
    update)
        update_repo
        ;;
    remove)
        remove_repo
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