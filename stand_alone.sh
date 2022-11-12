#!/bin/bash
sudo apt-get update

sudo apt-get install mysql-server -y

#set up the password
sudo mysql <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'sql';
exit
EOF

#do the secure installation
sudo mysql_secure_installation <<EOF
sql
n
n
n
n
EOF

#connect 
sudo mysql -u root -p <<EOF 
sql 
EOF

