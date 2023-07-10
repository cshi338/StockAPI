To run stock services on NATIVE host:
1) Ensure that port 56893 is listening to outside requests.
2) Run the order service as follows: python3 orderServer.py
3) Run the catalog service as follows: python3 catalogServer.py
4) Run the front end service as follows: python3 frontEnd.py
5) Connect to the front end service with any number of clients as follows: python3 HTTPClient.py IP_ADDRESS 56893 PROBABILITY VERBOSE
where: IP_ADDRESS is the public ip address of the front end service. PROBABILITY is the probability p at which the client will send another order request using the same connection. VERBOSE is a value of 0 or 1 where 0 is a verbose output and 1 is a non-verbose/latency only output.
All three services will share the same local ip. Order service will be hosted on port 56891. Catalog service will be hosted on port 56892. Front end service will be hosted on port 56893.

To run stock services on docker containers:
1) Ensure that port 56893 is listening to outside requests.
2) Execute: sudo bash build.sh
3) Execute: docker-compose up
4) Connect to the front end service with any number of clients as follows: python3 HTTPClient.py IP_ADDRESS 56893 PROBABILITY VERBOSE
where: IP_ADDRESS is the public ip address of the front end service. PROBABILITY is the probability p at which the client will send another order request using the same connection. VERBOSE is a value of 0 or 1 where 0 is a verbose output and 1 is a non-verbose/latency only output.
5) Close the docker containers with: docker-compose down

Order service will be hosted on 10.0.0.241:56891. Catalog service will be hosted on 10.0.0.242:56892. Front end service will be hosted on 10.0.0.243:56983. A network is created with subnet of 10.0.0.0/24 s.t. any incoming connection with 10.0.0.xxx:56893 is accepted.
