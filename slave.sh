#!/bin/bash
sudo apt-get update
sudo apt install libclass-methodmaker-perl

sudo wget https://dev.mysql.com/get/Downloads/MySQL-Cluster-7.6/mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb
sudo dpkg -i mysql-cluster-community-data-node_7.6.6-1ubuntu18.04_amd64.deb

cd /home/ubuntu/
sudo mkdir -p /usr/local/mysql/data