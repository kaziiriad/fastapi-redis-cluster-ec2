#!/bin/bash

# Update system packages
sudo apt update
sudo apt upgrade -y

# Install Python and virtualenv
sudo apt install -y python3 python3-pip python3-venv

# Create project directory
mkdir -p ~/fastapi-redis
cd ~/fastapi-redis

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Copy systemd service file
sudo cp fastapi-redis.service /etc/systemd/system/

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl start fastapi-redis
sudo systemctl enable fastapi-redis

# Check status
sudo systemctl status fastapi-redis