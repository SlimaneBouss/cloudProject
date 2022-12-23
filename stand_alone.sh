#!/bin/bash
sudo apt-get update
sudo apt-get install mysql-server -y

#secure install source : https://bertvv.github.io/notes-to-self/2015/11/16/automating-mysql_secure_installation/#:~:text=One%20approach%20to%20automating%20mysql_secure_installation,typically%20not%20installed%20by%20default.
sudo mysql -e "UPDATE mysql.user SET Password=PASSWORD('sql') WHERE User='root';"
sudo mysql -e "DELETE FROM mysql.user WHERE User='';"
sudo mysql -e "DROP DATABASE IF EXISTS test;"
sudo mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
sudo mysql -e "FLUSH PRIVILEGES;"

#Get sakila
wget https://downloads.mysql.com/docs/sakila-db.tar.gz
tar -xf sakila-db.tar.gz --directory /home/ubuntu/

#add sakila to mysql
sudo mysql -u root -p <<EOF
sql
EOF
sudo mysql -e "SOURCE /home/ubuntu/sakila-db/sakila-schema.sql;"
sudo mysql -e "SOURCE /home/ubuntu/sakila-db/sakila-data.sql;"

#create local user because acces is denied with root user source : https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql
sudo mysql -e "CREATE USER 'localuser'@'localhost' IDENTIFIED BY 'local';"
sudo mysql -e "GRANT ALL PRIVILEGES on sakila.* TO 'localuser'@'localhost';"

#getting sysbench
sudo apt-get install sysbench -y

#testbenching
sysbench \
--db-driver=mysql \
--mysql-user=localuser \
--mysql_password=local \
--mysql-db=sakila \
--tables=16 \
--table-size=10000 \
/usr/share/sysbench/oltp_read_write.lua prepare

sudo sh -c "sysbench \
--db-driver=mysql \
--mysql-user=localuser \
--mysql_password=local \
--mysql-db=sakila \
--tables=8 \
--table-size=10000 \
--threads=6 \
--time=60 \
--events=0 \
--report-interval=1 \
/usr/share/sysbench/oltp_read_write.lua run > /home/ubuntu/bm_st.txt"
