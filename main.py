import boto3
import stand_alone
import cluster
import time
import os
import helper

client = boto3.client('ec2')
ec2 = boto3.resource('ec2')


VPC_ID = client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')
SG_NAME_STANDALONE = 'sa_sg'
SG_NAME_CLUSTER = 'cluster_sg'

def main() :

    # public_dns = stand_alone.create_stand_alone(client,ec2,'./stand_alone.sh',SG_NAME_STANDALONE,VPC_ID)
    # print(public_dns)

    # #waiting for the benchmarking to end
    # time.sleep(220)

    # print('Fetching the benchmark file')
    # os.system('scp -i key.pem ubuntu@'+public_dns+':/home/ubuntu/bm_st.txt ./')
    cluster.create_cluster(ec2,client,SG_NAME_CLUSTER,VPC_ID,'./master.sh','./slave.sh')

main()