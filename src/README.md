
 Add your source code to this directory. Part 1 should go to a directory called *part1* and Part 2 should go to a directory called *part2*
 
 At the time of writing this, the IP address assigned to my edLab machine is 128.119.243.168. Therefore 128.119.243.168 is utilized as the host for all files in the lab. I have confirmed that hosting the server on the edlab machine, I am able to connect from my local machine to the server. I have also confirmed that hosting the server on the edlab machine, I am able to connect from another edlab machine. I am not sure if the IP is going to change when grading. 
 
 UPDATE:
For both parts, when running the code, execute the server.py files first. The server.py file will output a string. For part 1, replace the "host" value with this string. For part 2, replace the string in grpc.insecure_channel() on line 18 in client.py and line 15 in updateClient.py with the displayed string. 
