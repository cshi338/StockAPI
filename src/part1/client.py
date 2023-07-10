import socket
import time
import random

#List of stock names including one fake stock
stockNames = ['GameStart','FishCo','Apple']

start_time = time.time()
#Send 1000 requests
for _ in range(1000):
    #Randomly select which stock to use for current request
    stockName = random.choice(stockNames)
    a = socket.socket()
    port = 56897  # Specify the port to connect to
    host = "128.119.243.168"
    a.connect((host, port))

    print("-------------- Lookup --------------")
    #Create request string
    message = "Lookup " + stockName
    #Send request to server
    a.send(message.encode())
    #Receive and decode reply
    reply = a.recv(1024).decode()
    print(reply + "\n")
    a.close()  # Close the socket when done
print("Average Latency: " + str((time.time() - start_time)/1000))
