import helper
import time

"""
Creates the proxy instance on EC2

parameters :
    client (Client)      -> The EC2 client object
    ec2 (Resource)       -> The EC2 resource object
    sg_id (String)       -> Id of the security groupe
"""


def create_proxy(client,ec2,sg_id) :

    print("Getting the the subnet id ...")
    subnet_id = helper.get_subnet_id(client,'us-east-1c')
    time.sleep(1)
    print('Creating Proxy instance ...')
    pr = ec2.create_instances(
        ImageId='ami-08c40ec9ead489470',
        InstanceType='t2.large',
        KeyName='vockey',
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=[
            sg_id,
        ],
        SubnetId = subnet_id,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value':'Proxy',
                    },
                ],
            },
        ],
    )[0]

    #source : https://stackoverflow.com/questions/34728477/retrieving-public-dns-of-ec2-instance-with-boto3
    pr.wait_until_running()
    pr.load()