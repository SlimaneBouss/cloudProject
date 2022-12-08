import helper
import time

def create_cluster(ec2,client, sg_id,master_script, slave_script) :


    with open(master_script, 'r') as r:
        ms = r.read()

    with open(slave_script, 'r') as r:
        ss = r.read()

    #Set up
    print("Creating key pair")
    helper.create_key(ec2)
    time.sleep(1)
    print("Getting the the subnet id for the cluster...")
    subnet_id = helper.get_subnet_id(client,'us-east-1b')
    time.sleep(1)

    dns_list = []
    ips_list = []

    #create master
    master = create_master(ec2,sg_id,subnet_id,'Master',ms)[0]
    master.wait_until_running()
    master.reload()
    dns_list.append(master.public_dns_name)
    ips_list.append(master.private_dns_name)

    #create slaves
    slaves = []
    for i in range(3) :
        slaves.append(create_slaves(ec2,sg_id,subnet_id,'Slave ' + str(i+1),ss)[0])
    
    for slave in slaves :
        slave.wait_until_running()
        slave.reload()
        dns_list.append(slave.public_dns_name)
        ips_list.append(slave.private_dns_name)

    print(dns_list)
    print(ips_list)

    return master

#----------------------------------------------------------------------

def create_master(ec2,sg_id,subnet_id,name,script) :
    return ec2.create_instances(
        ImageId='ami-0149b2da6ceec4bb0',
        InstanceType='t2.micro',
        KeyName='vockey',
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=[
            sg_id,
        ],
        SubnetId = subnet_id,
        #UserData=script,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value':name,
                    },
                ],
            },
        ],
    )

#----------------------------------------------------------------------

def create_slaves(ec2,sg_id,subnet_id,name,script) :

    return ec2.create_instances(
        ImageId='ami-0149b2da6ceec4bb0',
        InstanceType='t2.micro',
        KeyName='vockey',
        MaxCount=1,
        MinCount=1,
        SecurityGroupIds=[
            sg_id,
        ],
        SubnetId = subnet_id,
        #SUserData=script,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value':name,
                    },
                ],
            },
        ],
    )