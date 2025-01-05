#!/bin/bash

# List of EC2 instances
INSTANCES=(
    "ubuntu@ec2-ip-1"
    "ubuntu@ec2-ip-2"
    # Add more instances as needed
)

KEY_PATH="path/to/your-key.pem"

for instance in "${INSTANCES[@]}"
do
    echo "Deploying to $instance..."
    
    # Copy files
    scp -i $KEY_PATH -r fastapi-redis/* $instance:~/fastapi-redis/
    
    # Execute deployment script
    ssh -i $KEY_PATH $instance 'bash ~/fastapi-redis/deploy.sh'
done