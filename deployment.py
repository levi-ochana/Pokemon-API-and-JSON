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
    cd pokemon
    python3 game.py
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

# (The rest of the functions remain unchanged)

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
