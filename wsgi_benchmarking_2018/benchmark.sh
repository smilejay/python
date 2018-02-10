#!/bin/bash

IP=192.168.122.140
PORTS=(8000 8100 8200 8300 8400)
CONNECTIONS=(100 500 1000 5000 10000)
THREADS=8
DURATION=30
BASE=$1

ulimit -n 10240


function perf() {
    echo "    Testing with $1 threads and $2 connections ..."
    ./wrk --duration $DURATION --threads $1 --connections "$2" "http://$IP:$3" > "$3_$1_$2.log"
}

for connections in "${CONNECTIONS[@]}"; do
    for port in "${PORTS[@]}"; do
        perf "$THREADS" "$connections" "$port"
        sleep 1
    done
done
