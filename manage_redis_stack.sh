#!/bin/bash

# Function to check if the redis-stack container exists
container_exists() {
    docker container inspect redis-stack > /dev/null 2>&1
}

# Function to check if the redis-stack container is running
container_is_running() {
    [ "$(docker container inspect -f '{{.State.Running}}' redis-stack 2>/dev/null)" == "true" ]
}

# Function to start redis-stack
start_redis_stack() {
    if container_exists; then
        if container_is_running; then
            echo "Redis Stack is already running."
        else
            echo "Starting existing Redis Stack container..."
            docker start redis-stack
            echo "Redis Stack started."
        fi
    else
        echo "Creating and starting Redis Stack container..."
        docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
        echo "Redis Stack started."
    fi
    echo "Redis command line interface available on port 6379."
    echo "Redis Stack UI available at http://localhost:8001"
}

# Function to stop redis-stack
stop_redis_stack() {
    if container_exists; then
        if container_is_running; then
            echo "Stopping redis-stack..."
            docker stop redis-stack && docker rm redis-stack
            echo "Redis Stack stopped."
        else
            echo "Redis Stack is not running, removing container..."
            docker rm redis-stack
            echo "Redis Stack container removed."
        fi
    else
        echo "Redis Stack container does not exist."
    fi
}

# Check the command-line argument
case "$1" in
    start)
        start_redis_stack
        ;;
    stop)
        stop_redis_stack
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac
