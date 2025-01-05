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
nodejs_instance = aws.ec2.Instance("nodejs-instance",
    instance_type="t2.micro",
    vpc_security_group_ids=[redis_security_group.id],
    ami=ami_id,
    subnet_id=public_subnet1.id,
    key_name="MyKeyPair2",  # Update with your key pair
    associate_public_ip_address=True,
    tags={
        "Name": "nodejs-instance",
        "Environment": "Development",
        "Project": "RedisSetup"
    })
pulumi.export("nodejsInstanceId", nodejs_instance.id)
pulumi.export("nodejsInstancePublicIp", nodejs_instance.public_ip)  # Output Node.js public IP

# Helper function to create Redis instances
def create_redis_instance(name, subnet_id):
    return aws.ec2.Instance(name,
        instance_type="t2.micro",
        vpc_security_group_ids=[redis_security_group.id],
        ami=ami_id,
        subnet_id=subnet_id,
        key_name="MyKeyPair2",  # Update with your key pair
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


  + redisInstance1PrivateIp: "10.0.2.182"
  ~ redisInstance1PublicIp : "10.0.2.182" => "13.250.12.204"
    redisInstance2Id       : "i-0730040501bef3fb8"
  + redisInstance2PrivateIp: "10.0.2.16"
  ~ redisInstance2PublicIp : "10.0.2.16" => "13.215.46.122"
    redisInstance3Id       : "i-0bf9406c505adaf3d"
  + redisInstance3PrivateIp: "10.0.2.13"
  ~ redisInstance3PublicIp : "10.0.2.13" => "18.139.117.129"
    redisInstance4Id       : "i-0dfc84a58a21b6306"
  + redisInstance4PrivateIp: "10.0.3.131"
  ~ redisInstance4PublicIp : "10.0.3.131" => "18.140.98.188"
    redisInstance5Id       : "i-0bfd49e5466753af4"
  + redisInstance5Privatep : "10.0.3.115"
  ~ redisInstance5PublicIp : "10.0.3.115" => "13.214.152.47"
    redisInstance6Id       : "i-06c0e957854f9a596"
  + redisInstance6PrivateIp: "10.0.3.95"
  ~ redisInstance6PublicIp : "10.0.3.95" => "18.142.161.58"
    redisSecurityGroupId   : "sg-07be23746912d5adc"
    vpcId                  : "vpc-00a2faa99f72cb855"