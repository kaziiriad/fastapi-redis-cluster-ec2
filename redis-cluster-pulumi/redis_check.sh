#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color


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

# # Copy and execute installation script on all servers
# for server in "${SERVERS[@]}"
# do
#     echo "Checking redis on $server..."
#     # Copy the script
#     # scp -i $KEY_PATH -o StrictHostKeyChecking=no redis-setup.sh $server:~/
#     # Execute without sudo prompt
#     ssh -i $KEY_PATH -o StrictHostKeyChecking=no $server 'bash -c' < sudo systemctl status redis-server
# done

fix_redis() {
    local server=$1
    echo -e "\n${YELLOW}Fixing Redis on $server...${NC}"

    ssh -i $KEY_PATH -o StrictHostKeyChecking=no $server '
        # Ensure Redis is installed
        if ! command -v redis-server &> /dev/null; then
            echo "Installing Redis..."
            sudo apt-get update
            sudo apt-get install -y redis-server
        fi

        # Configure Redis for cluster mode
        echo "Configuring Redis..."
        sudo tee /etc/redis/redis.conf > /dev/null << EOF
bind 0.0.0.0
protected-mode no
port 6379
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
EOF

        # Restart Redis service
        echo "Starting Redis service..."
        sudo systemctl restart redis-server
        sudo systemctl enable redis-server

        # Check status
        echo "Service status:"
        sudo systemctl status redis-server --no-pager
    '

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Redis fixed successfully on $server${NC}"
    else
        echo -e "${RED}❌ Failed to fix Redis on $server${NC}"
    fi
}

# Main execution
echo "Starting Redis fix across all servers..."
for server in "${SERVERS[@]}"; do
    fix_redis "$server"
done

echo -e "\n${YELLOW}Fix attempt complete! Running configuration check...${NC}"

# Wait a moment for services to fully start
sleep 5