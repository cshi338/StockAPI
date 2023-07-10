To run stock services:

Ensure that port 56893 is listening to outside requests.
1.) Run the catalog service as follows: python3 catalogServer.py  
  
2.) Do the following to create 3 order service replicas:  
2a.) Run the order service as follows: python3 orderServer.py REPLICA_PORT_NUM REPLICA_ID FRONT_END_IP_ADDRESS CACHE  
2b.) Run the order service as follows: python3 orderServer.py REPLICA_PORT_NUM REPLICA_ID FRONT_END_IP_ADDRESS CACHE  
2c.) Run the order service as follows: python3 orderServer.py REPLICA_PORT_NUM REPLICA_ID FRONT_END_IP_ADDRESS CACHE  
Where REPLICA_PORT_NUM is the port number assigned to the given replica, REPLICA_ID is the ID assigned to the given replica, FRONT_END_IP_ADDRESS is the IP address of the front end service, CACHE is 0 for no cache, and 1 for cache enabled.  
  
3.) Run the front end service as follows: python3 frontEnd.py REPLICA_ID REPLICA_ADDRESS REPLICA_ID REPLICA_ADDRESS REPLICA_ID REPLICA_ADDRESS CACHE  
Where REPLICA_ID and REPLICA_ADDRESS are the replica IDs and corresponding replica addresses of the 3 order service replicas. REPLICA_ADDRESS is in the form "ip_address:port". CACHE is 0 for no cache, and 1 for cache enabled.  
  
Connect to the front end service with any number of clients as follows: python3 HTTPClient.py IP_ADDRESS 56893 PROBABILITY VERBOSE   
where: IP_ADDRESS is the public ip address of the front end service. PROBABILITY is the probability p at which the client will send another order request using the same connection. VERBOSE is a value of 0 or 1 where 0 is a verbose output and 1 is a non-verbose/latency only output.  
All three services will share the same local ip. Catalog service will be hosted on port 56892. Front end service will be hosted on port 56893.

e.g.  
py catalogserver.py  
py orderserver.py 56891 3 10.0.0.246 56893 1  
py orderserver.py 56890 2 10.0.0.246 56893 1  
py orderserver.py 56889 1 10.0.0.246 56893 1  
py frontend.py 3 10.0.0.246:56891 2 10.0.0.246:56890 1 10.0.0.246:56889 1  

To run test cases:  
1.) Run the test cases as follows: python3 testCases.py FRONT_END_IP FRONT_END_PORT  
where FRONT_END_IP is the ip address of the front end service and FRONT_END_PORT is the port of the front end service.  
NOTE: test cases utilize the subprocess.Popen() function in order to control the opening and termination of the various microservices. This is in order to test for fault tolerance. As such, all microservices are ran in the background and the stdout of the services will not be seen when running testCases.py  
  
Use delete.sh to delete catalog.txt and all order replica output files. 
