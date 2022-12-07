import helper
import time

def create_stand_alone(client,ec2,script_file, sg_name, vpc_id) :

    print("creating security group ...")
    sg_id = helper.create_sg(client,ec2,sg_name,vpc_id)
    time.sleep(1)
    print("Getting the the subnet id ...")
    subnet_id = helper.get_subnet_id(client,'us-east-1a')
    time.sleep(1)

    script = ''

    with open(script_file, 'r') as r:
        script = r.read()
    
    print('Creating standalone instance ...')
    sa = ec2.create_instances(
        ImageId='ami-08c40ec9ead489470',
        InstanceType='t2.micro',
        KeyName='vockey',
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=[
            sg_id,
        ],
        SubnetId = subnet_id,
        UserData=script,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value':'standalone',
                    },
                ],
            },
        ],
    )[0]

    #source : https://stackoverflow.com/questions/34728477/retrieving-public-dns-of-ec2-instance-with-boto3
    sa.wait_until_running()
    sa.load()
    return(sa.public_dns_name)
 
