import boto3
import stand_alone
import cluster
import proxy
import time
import os
import helper

client = boto3.client('ec2')
ec2 = boto3.resource('ec2')


VPC_ID = client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
SG_NAME_STANDALONE = 'sa_sg'
SG_NAME_CLUSTER_PROXY = 'cluster_sg'

"""
Creating all the instances and fetches the benchmark file for the stand alone
"""

def main() :

    #Creating the standalone
    public_dns = stand_alone.create_stand_alone(client,ec2,'./stand_alone.sh',SG_NAME_STANDALONE,VPC_ID)
    print(public_dns)
    #waiting for the benchmarking to end
    time.sleep(220)
    #fetching from the standAlone
    print('Fetching the benchmark file')
    os.system('scp -i key.pem ubuntu@'+public_dns+':/home/ubuntu/bm_st.txt ./')

    #Creating security group for cluster + proxy
    sg_id = helper.create_sg(client,ec2,SG_NAME_CLUSTER_PROXY,VPC_ID)
    #Creating the cluster (semi-automatic set up)
    cluster.create_cluster(ec2,client,sg_id,'./master.sh','./slave.sh')
    #create proxy
    proxy.create_proxy(client,ec2,sg_id)
main()