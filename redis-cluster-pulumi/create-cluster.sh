#!/bin/bash

# Replace these with your actual EC2 private IPs
REDIS_NODES=(
    "10.0.2.182:6379"
    "10.0.2.16:6379"
    "10.0.2.13:6379"
    "10.0.3.131:6379"
    "10.0.3.115:6379"
    "10.0.3.95:6379"
)

sudo apt install redis-tools -y


# Join all IPs with spaces
NODES_STRING=$(printf "%s " "${REDIS_NODES[@]}")

# Create cluster
redis-cli --cluster create $NODES_STRING --cluster-replicas 1