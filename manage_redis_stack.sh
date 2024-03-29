#!/bin/bash

# Function to start redis-stack
start_redis_stack() {
    echo "Starting redis-stack..."
    docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
    echo "Redis Stack started."
    echo "Redis command line interface available on port 6379."
    echo "Redis Stack UI available at http://localhost:8001"
}

# Function to stop redis-stack
stop_redis_stack() {
    echo "Stopping redis-stack..."
    docker stop redis-stack && docker rm redis-stack
    echo "Redis Stack stopped."
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

