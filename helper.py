import subprocess

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


    #returning the id
    return sg_id

#----------------------------------------------------------------------

def get_subnet_id(client,subnet_name) :
    sb_list = client.describe_subnets()['Subnets']

    for sb in sb_list :
        if sb['AvailabilityZone'] == subnet_name :
            return sb['SubnetId']
 
#----------------------------------------------------------------------

