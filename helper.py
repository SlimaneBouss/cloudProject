import subprocess

"""
Creates the security group

parameters :
    client (Client)      -> The EC2 client object
    ec2 (Resource)       -> The EC2 resource object
    sg_name (String)     -> Name of the security groupe
    vpc_id (String)      -> The vpc id

return :
    sg_id (String) -> The id of the security group
"""

def create_sg(client,ec2,sg_name,vpc_id) :

    #create security group
    sg_payload = client.create_security_group(GroupName = sg_name,VpcId = vpc_id,Description = 'simple group')
    
    #Getting the id
    sg_id = sg_payload['GroupId']

    #Ingress
    sg = ec2.SecurityGroup(sg_id)
    sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=22, ToPort=22)
    sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=80, ToPort=80)
    sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=3306, ToPort=3306)
    sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=1186, ToPort=1186)
    sg.authorize_ingress(CidrIp='0.0.0.0/0', IpProtocol='tcp', FromPort=5001, ToPort=5001)


    #returning the id
    return sg_id

#----------------------------------------------------------------------
"""
Fetches the subnet id for a specific subnet

parameters :
    client (Client)          -> The EC2 client object
    subnet_name (String)     -> Name of the subnet

return : 
    The subnet id
"""

def get_subnet_id(client,subnet_name) :
    sb_list = client.describe_subnets()['Subnets']

    for sb in sb_list :
        if sb['AvailabilityZone'] == subnet_name :
            return sb['SubnetId']
 
#----------------------------------------------------------------------
"""
Creates a key pair

parameters :
    client (Client) -> The EC2 client object
"""
def create_key(ec2) : 
    # create a file to store the key locally
    outfile = open('ec2-keypair.pem','w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)