import socket
import pymysql
import os
import random
from sshtunnel import SSHTunnelForwarder

#Set up our data structures
ping_vals = {}
nodes ={'3.81.94.210': 'MASTER' ,'54.210.202.75':'SLAVE1','18.215.234.129 ':'SLAVE2'}
for k in nodes.keys():
    ping_vals[k] = 0

#Connect to our master node
host_conn = pymysql.connect(host='3.81.94.210',user='localuser',password='local',db='sakila',port=3306,autocommit=True)
curr = host_conn.cursor()

#----------------------------------------------------------------------

#pings all the machines in the cluster and checks the fastest response
def ping() : 
    for key in ping_vals.keys() :
        var = os.popen('ping -c 2 ' + key).read()
        ping_vals[key] = float(var.splitlines()[-1].split(' ')[3].split('/')[1])

    return min(ping_vals.items(),key=lambda x: x[1])[0]

#----------------------------------------------------------------------

#Get random node to query to
def get_random_node() :
    k = random.choice(list(nodes.keys()))
    return k, nodes[k]

#----------------------------------------------------------------------

#executes a command intended for the master node
def execute_master(cmd,clientsocket) : 
    curr.execute(cmd[2:])
    output = curr.fetchall()
    if 'SELECT' in cmd :
     for o in output :
        clientsocket.send(bytes("FROM MASTER : " + str(o), "utf-8"))
    else :
        clientsocket.send(bytes("MASTER : OK !", "utf-8"))

#----------------------------------------------------------------------

#executes a command intended for one of the slave nodes
def execute_in_slave(cmd,clientsocket,ip,name) : 
    with SSHTunnelForwarder(ip, ssh_username='ubuntu',ssh_pkey='ec2-keypair.pem',remote_bind_address=('3.81.94.210',3306)) as tunnel:

        slave_conn = pymysql.connect(host='3.81.94.210',user='localuser',password='local',db='sakila',port=3306,autocommit=True)
        slave_curr = slave_conn.cursor()
        slave_curr.execute(cmd[2:])
        output = slave_curr.fetchall()
        if 'SELECT' in cmd :
         for o in output :
            clientsocket.send(bytes("FROM "+name+" : " + str(o), "utf-8"))
        else :
             clientsocket.send(bytes(name + ": OK !", "utf-8"))
        slave_conn.close()

#----------------------------------------------------------------------

#routes to different modes
def route(cmd,clientsocket) : 
    if cmd[0] == '0' :
        execute_master(cmd,clientsocket)
    
    elif cmd[0] == '1' :
        ip , name = get_random_node()
        if name == 'MASTER' :
            execute_master(cmd,clientsocket)
        else :
            execute_in_slave(cmd,clientsocket,ip,name)
        
    elif cmd[0] == '2' :
        ip = ping()
        if nodes[ip]=='MASTER' :
            execute_master(cmd,clientsocket)
        else :
            execute_in_slave(cmd,clientsocket,ip,nodes[ip])

#----------------------------------------------------------------------

def main():
    host = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, 5001))
        s.listen(1)
        clientsocket, address = s.accept()
        print("Connection: ", address)
        with clientsocket:
            while True:
                data = clientsocket.recv(1024)
                if not data:
                    break
                cmd = data.decode('utf-8')
                route(cmd,clientsocket)

main()