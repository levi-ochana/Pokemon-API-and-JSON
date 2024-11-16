import boto3

# Initialize EC2 client
client = boto3.client('ec2')

# Retrieves the default VPC ID.
# If no default VPC is found, raises an exception.
def get_default_vpc():
    response = client.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
    if response['Vpcs']:
        vpc_id = response['Vpcs'][0]['VpcId']
        print(f"Using default VPC: {vpc_id}")
        return vpc_id
    raise Exception("No default VPC found.")

# Checks if the security group exists. If not, creates a new one.
# Adds inbound rules for SSH (port 22) and HTTP (port 80).
def check_or_create_security_group(vpc_id, group_name="PokemonAppSecurityGroup"):
    try:
        response = client.describe_security_groups(GroupNames=[group_name])
        security_group_id = response['SecurityGroups'][0]['GroupId']
        print(f"Security group {group_name} already exists with ID {security_group_id}.")
        return security_group_id
    except client.exceptions.ClientError as e:
        if 'InvalidGroup.NotFound' in str(e):
            print(f"Security group {group_name} not found. Creating a new one.")
            security_group = client.create_security_group(
                GroupName=group_name,
                Description='Security group for the Pokemon App',  # Removed the accent
                VpcId=vpc_id
            )
            security_group_id = security_group['GroupId']
            print(f"Created security group {group_name} with ID {security_group_id}.")
            
            # Add inbound rules
            client.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[{
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Allow SSH from anywhere
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]  # Allow HTTP traffic
                } ]
            )
            print(f"Inbound rules added to the security group {group_name}.")
            return security_group_id
        else:
            raise e


# Retrieves the first available subnet ID from the given VPC.
def get_subnet_id(vpc_id):
    response = client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    if response['Subnets']:
        subnet_id = response['Subnets'][0]['SubnetId']
        print(f"Using subnet ID: {subnet_id}")
        return subnet_id
    raise Exception("No available subnets in the specified VPC.")

# Finds the latest Amazon Linux 2 AMI for a free-tier eligible instance.
def get_latest_ami():
    response = client.describe_images(
        Owners=['amazon'],
        Filters=[
            {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']},
            {'Name': 'state', 'Values': ['available']}
        ]
    )
    amis = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    ami_id = amis[0]['ImageId']
    print(f"Using the latest AMI: {ami_id}")
    return ami_id

# Launches an EC2 instance with the given parameters.
# Includes a user data script to set up the Pokémon app.
def launch_instance(ami_id, key_name, security_group_id, subnet_id):
    ec2 = boto3.resource('ec2')
    user_data_script = '''#!/bin/bash
    sudo yum update -y
    sudo yum install -y python3 python3-pip git
    sudo alternatives --set python /usr/bin/python3 
    sudo yum install openssl11
    pip3 install urllib3==1.25.11
    pip3 install --upgrade pip
    pip3 install requests
    cd /home/ec2-user
    git clone https://github.com/levi-ochana/Pokemon-API-and-JSON.git
    '''
    instance = ec2.create_instances(
        ImageId=ami_id,
        InstanceType='t2.micro',
        KeyName=key_name,
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=[security_group_id],
        SubnetId=subnet_id,
        UserData=user_data_script
    )[0]
    print(f"Launching instance {instance.id}...")
    instance.wait_until_running()
    instance.load()  # Refresh instance attributes
    print(f"Instance {instance.id} is running.")

    # Get the public IP address of the instance
    public_ip = instance.public_ip_address
    print(f"Instance public IP address: {public_ip}")
    return instance, public_ip

# Main workflow to provision an EC2 instance for the Pokémon app.
def main():
    # Define key pair name
    key_name = "vockey"

    # Get default VPC ID
    vpc_id = get_default_vpc()

    # Check or create the security group
    security_group_id = check_or_create_security_group(vpc_id)

    # Get a valid subnet ID
    subnet_id = get_subnet_id(vpc_id)

    # Get the latest Amazon Linux 2 AMI
    ami_id = get_latest_ami()

    # Launch an EC2 instance
    instance, public_ip = launch_instance(ami_id, key_name, security_group_id, subnet_id)

    # Return the public IP address
    return public_ip

if __name__ == "__main__":
    public_ip = main()
    print(f"Access your Pokémon app at http://{public_ip}")
