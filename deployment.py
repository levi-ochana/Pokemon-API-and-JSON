import boto3
import os


# Initialize EC2 resource and client
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# Function to launch an EC2 instance
def launch_instance(ami_id, key_name, security_group_id, subnet_id):
    user_data_script = '''#!/bin/bash
    sudo yum install -y python3 python3-pip git
    pip3 install requests
    git clone https://github.com/levi-ochana/pokemon.git
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
    
    print(f"Instance {instance.id} launched.")
    instance.wait_until_running()
    instance.load()  # Refresh instance data
    return instance


# Function to get a valid subnet ID from the VPC
def get_subnet_id(vpc_id):
    response = client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    if response['Subnets']:
        subnet_id = response['Subnets'][0]['SubnetId']
        print(f"Using subnet: {subnet_id} from VPC: {vpc_id}")
        return subnet_id
    else:
        raise Exception("No available subnets in the specified VPC.")

# Function to get the default VPC
def get_default_vpc():
    response = client.describe_vpcs()
    for vpc in response['Vpcs']:
        if vpc['IsDefault']:
            print(f"Using default VPC: {vpc['VpcId']}")
            return vpc['VpcId']
    raise Exception("No default VPC found.")

# Function to check or create a security group
def check_or_create_security_group(vpc_id, group_name="my-security-group"):
    try:
        response = client.describe_security_groups(GroupNames=[group_name])
        security_group_id = response['SecurityGroups'][0]['GroupId']
        print(f"Security group {group_name} already exists with ID {security_group_id}.")
        return security_group_id
    except client.exceptions.ClientError as e:
        if 'InvalidGroup.NotFound' in str(e):
            print(f"Security group {group_name} not found, creating a new one.")
            security_group = client.create_security_group(GroupName=group_name, Description='My security group', VpcId=vpc_id)
            security_group_id = security_group['GroupId']
            # Add inbound rules (allow SSH and HTTP)
            client.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 22,
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    },
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            print(f"Security group {group_name} created with ID {security_group_id}.")
            return security_group_id
        else:
            raise e

# Function to get the latest Amazon Linux 2 AMI
def get_latest_ami():
    response = client.describe_images(
        Owners=['amazon'],
        Filters=[{'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']}]
    )
    amis = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    ami_id = amis[0]['ImageId']
    print(f"Using AMI: {ami_id}")
    return ami_id

# Main workflow
def main():
    # Define the key name
    key_name = "vockey"

    # Get default VPC and check/create security group
    vpc_id = get_default_vpc()
    security_group_id = check_or_create_security_group(vpc_id)

    # Get a valid subnet ID
    subnet_id = get_subnet_id(vpc_id)
    
    # Find an AMI and launch the instance
    ami_id = get_latest_ami()
    instance = launch_instance(ami_id, key_name, security_group_id, subnet_id)  

if __name__ == '__main__':
    main()
