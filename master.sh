#!/bin/bash
sudo apt-get update
sudo apt install -y libncurses5
sudo apt install -y libaio1 libmecab2

#downloads
sudo wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-management-server_7.6.6-1ubuntu18.04_amd64.deb

#creating the config.ini files
sudo mkdir /var/lib/mysql-cluster
cd /var/lib/mysql-cluster/
sudo touch config.ini
sudo chmod 777 config.ini
sudo cat <<< '
[ndbd default]
# Options affecting ndbd processes on all data nodes:
NoOfReplicas=1	# Number of replicas

[ndb_mgmd]
# Management process options:
hostname=172.31.29.189 # Hostname of the manager
datadir=/var/lib/mysql-cluster 	# Directory for the log files

[ndbd]
hostname=172.31.31.40# Hostname/IP of the first data node
NodeId=2			# Node ID for this data node
datadir=/usr/local/mysql/data	# Remote directory for the data files

[mysqld]
# SQL node options:
hostname=172.31.29.189
' > config.ini

cd /home/ubuntu/

#downloads
sudo wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar

sudo mkdir install
sudo tar -xvf mysql-cluster_7.6.6-1ubuntu18.04_amd64.deb-bundle.tar -C install/
cd install
sudo dpkg -i mysql-common_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-client_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-client_7.6.6-1ubuntu18.04_amd64.deb