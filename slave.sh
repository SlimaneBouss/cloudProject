#!/bin/bash
sudo apt-get update
sudo apt install libclass-methodmaker-perl

sudo wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

cd /etc/
sudo touch my.cnf
sudo chmod 777 my.cnf
sudo cat <<< '
[mysql_cluster]
# Options for NDB Cluster processes:
ndb-connectstring=172.31.29.189
' > my.cnf
sudo chmod o-w my.cnf

cd /home/ubuntu/
sudo mkdir -p /usr/local/mysql/data