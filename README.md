# Final project log8415

## Creating all of the instances and benchmarking

#### The first step is to run the `main.py` file where :
- `The stand alone is created, fully set up with the `stand_alone.sh` and benchmarked`
- `The proxy is created`
- `The cluster is created and partially set up`
- `The ec2-keypair.pem is created and the key is captured in it`

#### Then the the master and the slaves need to be completly set up using this <a href="https://www.digitalocean.com/community/tutorials/how-to-create-a-multi-node-mysql-cluster-on-ubuntu-18-04">tutorial</a> (mainly all the configuration files).

#### To benchmark the cluster, do the same steps found in `stand_alone.sh` regarding the sakila set up and the SysBench commands. Then the benchmark file of the cluster can be fetched.

## Proxy set up
#### For the proxy to be properly working, certain steps must be completed beforehand : 
- `In the master's my.cnf file add : ` <em>`bind-address=0.0.0.0 `</em> `under the [mysqld] section`
- `Create a MySQL user on the cluster named : "proxy"@"the.proxy.ip.address" with the password "pass" and grant him all permisions on sakila`
- `Update all the ips in the proxy_server.py file`
- `Make sure that the pem file is in the same directory as the proxy_server.py file on the proxy instance`

## Running the proxy and the client

#### Client set up :
- `Change the ip you want to connect to the proxy's`

#### Run the proxy and then run the `client.py`

#### Here are a list of commands you can run to test the system :
- `"0 'SELECT COUNT(*) FROM actor'" To try the direct hit mode`
- `"1 'INSERT INTO actor(first_name, last_name) VALUES ("EMMA", "WATSON")'" To try the random mode`
- `"2 'SELECT * FROM actor WHERE first_name="EMMA"'" To try the customized mode`
