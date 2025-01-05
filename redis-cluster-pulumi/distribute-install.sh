#!/bin/bash

# List of EC2 instances private IPs/hostnames
SERVERS=(
    "ubuntu@13.250.12.204"
    "ubuntu@13.215.46.122"
    "ubuntu@18.139.117.129"
    "ubuntu@18.140.98.188"
    "ubuntu@13.214.152.47"
    "ubuntu@18.142.161.58"
)

# SSH key path
KEY_PATH="/root/code/redis-cluster-pulumi/MyKeyPair2.pem"

# Copy and execute installation script on all servers
for server in "${SERVERS[@]}"
do
    echo "Installing on $server..."
    # Copy the script
    scp -i $KEY_PATH -o StrictHostKeyChecking=no redis-setup.sh $server:~/
    # Execute without sudo prompt
    ssh -i $KEY_PATH -o StrictHostKeyChecking=no $server 'bash -s' < redis-setup.sh
done