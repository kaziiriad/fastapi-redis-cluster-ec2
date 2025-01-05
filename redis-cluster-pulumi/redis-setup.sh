#!/bin/bash

# Update system
sudo apt-get update
# Install Redis
sudo apt-get install -y redis-server

sudo systemctl start redis-server
sudo systemctl enable redis-server


# Configure Redis for cluster mode
sudo tee /etc/redis/redis.conf << EOF
bind 0.0.0.0
protected-mode no
port 6379
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
EOF



# Restart Redis service
sudo systemctl restart redis-server