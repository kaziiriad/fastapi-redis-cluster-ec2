import pulumi
import pulumi_aws as aws

# Create a VPC
vpc = aws.ec2.Vpc("redis-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": "redis-vpc",
    })
pulumi.export("vpcId", vpc.id)

# Create public subnets in three availability zones
public_subnet1 = aws.ec2.Subnet("subnet-1",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone="ap-southeast-1a",
    map_public_ip_on_launch=True,
    tags={
        "Name": "subnet-1",
    })
pulumi.export("publicSubnet1Id", public_subnet1.id)

public_subnet2 = aws.ec2.Subnet("subnet-2",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="ap-southeast-1b",
    map_public_ip_on_launch=True,
    tags={
        "Name": "subnet-2",
    })
pulumi.export("publicSubnet2Id", public_subnet2.id)

public_subnet3 = aws.ec2.Subnet("subnet-3",
    vpc_id=vpc.id,
    cidr_block="10.0.3.0/24",
    availability_zone="ap-southeast-1c",
    map_public_ip_on_launch=True,
    tags={
        "Name": "subnet-3",
    })
pulumi.export("publicSubnet3Id", public_subnet3.id)

# Create an Internet Gateway
internet_gateway = aws.ec2.InternetGateway("redis-igw",
    vpc_id=vpc.id,
    tags={
        "Name": "redis-igw",
    })
pulumi.export("igwId", internet_gateway.id)

# Create a Route Table
public_route_table = aws.ec2.RouteTable("redis-rt",
    vpc_id=vpc.id,
    tags={
        "Name": "redis-rt",
    })
pulumi.export("publicRouteTableId", public_route_table.id)

# Create a route in the Route Table for the Internet Gateway
route = aws.ec2.Route("igw-route",
    route_table_id=public_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    gateway_id=internet_gateway.id)

# Associate Route Table with Public Subnets
rt_association1 = aws.ec2.RouteTableAssociation("rt-association-1",
    subnet_id=public_subnet1.id,
    route_table_id=public_route_table.id)
rt_association2 = aws.ec2.RouteTableAssociation("rt-association-2",
    subnet_id=public_subnet2.id,
    route_table_id=public_route_table.id)
rt_association3 = aws.ec2.RouteTableAssociation("rt-association-3",
    subnet_id=public_subnet3.id,
    route_table_id=public_route_table.id)

# Create a Security Group for the Node.js and Redis Instances
redis_security_group = aws.ec2.SecurityGroup("redis-secgrp",
    vpc_id=vpc.id,
    description="Allow SSH, Redis, and Node.js traffic",
    ingress=[
        {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]},  # SSH
        {"protocol": "tcp", "from_port": 6379, "to_port": 6379, "cidr_blocks": ["10.0.0.0/16"]},  # Redis
        {"protocol": "tcp", "from_port": 16379, "to_port": 16379, "cidr_blocks": ["10.0.0.0/16"]},  # Redis Cluster
        {"protocol": "tcp", "from_port": 3000, "to_port": 3000, "cidr_blocks": ["0.0.0.0/0"]},  # Node.js (Port 3000)
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}  # Allow all outbound traffic
    ],
    tags={
        "Name": "redis-secgrp",
    })
pulumi.export("redisSecurityGroupId", redis_security_group.id)

# Define an AMI for the EC2 instances
ami_id = "ami-01811d4912b4ccb26"  # Ubuntu 24.04 LTS

# Create a Node.js Instance in the first subnet (ap-southeast-1a)
fastapi_instance = aws.ec2.Instance("fastapi-instance",
    instance_type="t2.micro",
    vpc_security_group_ids=[redis_security_group.id],
    ami=ami_id,
    subnet_id=public_subnet1.id,
    key_name="MyKeyPair4",  # Update with your key pair
    associate_public_ip_address=True,
    tags={
        "Name": "fastapi-instance",
        "Environment": "Development",
        "Project": "RedisSetup"
    })
pulumi.export("fastapiInstanceId", fastapi_instance.id)
pulumi.export("fastapiInstancePublicIp", fastapi_instance.public_ip)  # Output Node.js public IP

# Helper function to create Redis instances
def create_redis_instance(name, subnet_id):
    return aws.ec2.Instance(name,
        instance_type="t2.micro",
        vpc_security_group_ids=[redis_security_group.id],
        ami=ami_id,
        subnet_id=subnet_id,
        key_name="MyKeyPair4",  # Update with your key pair
        associate_public_ip_address=True,
        tags={
            "Name": name,
            "Environment": "Development",
            "Project": "RedisSetup"
        })

# Create Redis Cluster Instances across the remaining two subnets
redis_instance1 = create_redis_instance("redis-instance-1", public_subnet2.id)
redis_instance2 = create_redis_instance("redis-instance-2", public_subnet2.id)
redis_instance3 = create_redis_instance("redis-instance-3", public_subnet2.id)
redis_instance4 = create_redis_instance("redis-instance-4", public_subnet3.id)
redis_instance5 = create_redis_instance("redis-instance-5", public_subnet3.id)
redis_instance6 = create_redis_instance("redis-instance-6", public_subnet3.id)

# Export Redis instance IDs and public IPs
pulumi.export("redisInstance1Id", redis_instance1.id)
pulumi.export("redisInstance1PublicIp", redis_instance1.public_ip)
pulumi.export("redisInstance1PrivateIp", redis_instance1.private_ip)
pulumi.export("redisInstance2Id", redis_instance2.id)
pulumi.export("redisInstance2PublicIp", redis_instance2.public_ip)
pulumi.export("redisInstance2PrivateIp", redis_instance2.private_ip)
pulumi.export("redisInstance3Id", redis_instance3.id)
pulumi.export("redisInstance3PublicIp", redis_instance3.public_ip)
pulumi.export("redisInstance3PrivateIp", redis_instance3.private_ip)
pulumi.export("redisInstance4Id", redis_instance4.id)
pulumi.export("redisInstance4PublicIp", redis_instance4.public_ip)
pulumi.export("redisInstance4PrivateIp", redis_instance4.private_ip)
pulumi.export("redisInstance5Id", redis_instance5.id)
pulumi.export("redisInstance5PublicIp", redis_instance5.public_ip)
pulumi.export("redisInstance5Privatep", redis_instance5.private_ip)
pulumi.export("redisInstance6Id", redis_instance6.id)
pulumi.export("redisInstance6PublicIp", redis_instance6.public_ip)
pulumi.export("redisInstance6PrivateIp", redis_instance6.private_ip)

"""
Outputs:
    fastapiInstanceId      : "i-06a6ab30a05072579"
    fastapiInstancePublicIp: "13.250.15.202"
    igwId                  : "igw-0b6cf6001852b7258"
    publicRouteTableId     : "rtb-0f0d0a1da786d1363"
    publicSubnet1Id        : "subnet-0079f722f34b72544"
    publicSubnet2Id        : "subnet-0aaec29574b6c9413"
    publicSubnet3Id        : "subnet-0592cee06294ef5ec"
    redisInstance1Id       : "i-01c99eae268faa1e7"
    redisInstance1PrivateIp: "10.0.2.5"
    redisInstance1PublicIp : "47.129.44.128"
    redisInstance2Id       : "i-057679bdb4d54ac43"
    redisInstance2PrivateIp: "10.0.2.208"
    redisInstance2PublicIp : "54.169.82.0"
    redisInstance3Id       : "i-0f99bdbd8a2226bb8"
    redisInstance3PrivateIp: "10.0.2.186"
    redisInstance3PublicIp : "54.251.178.164"
    redisInstance4Id       : "i-0eac3cadcdd6ade49"
    redisInstance4PrivateIp: "10.0.3.53"
    redisInstance4PublicIp : "13.212.226.119"
    redisInstance5Id       : "i-074bf3a4c6f0a7dcd"
    redisInstance5Privatep : "10.0.3.149"
    redisInstance5PublicIp : "18.138.233.156"
    redisInstance6Id       : "i-051c2c9ad230b7c2a"
    redisInstance6PrivateIp: "10.0.3.83"
    redisInstance6PublicIp : "47.128.234.202"
    redisSecurityGroupId   : "sg-04f8a5d351b4b5e33"
    vpcId                  : "vpc-0f93dc7ddfa5632d9
"""