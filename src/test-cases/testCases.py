#!/usr/bin/env python
import logging
import random
import time
import timeit
import filecmp
import http.client
import sys
import json
import os
import os.path
import shutil
import subprocess
from subprocess import DEVNULL
import socket
#get http server ip
http_server = sys.argv[1]
port = sys.argv[2]
#create a connection
conn = http.client.HTTPConnection(http_server, port)
stockNames = ["tesla","ford","apple","amazon","nvidia","intel","meta","nike","amc","gamestop"]

os.chdir('..')

catalogService = subprocess.Popen(['python',os.getcwd()+'\\catalog-service\\catalogServer.py'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService1 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56891','3',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService2 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56890','2',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService3 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56889','1',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(1)
frontendService = subprocess.Popen(['python',os.getcwd()+'\\front-end\\frontEnd.py','3',str(socket.gethostbyname(socket.gethostname()))+":56891",'2',str(socket.gethostbyname(socket.gethostname()))+":56890",'1',str(socket.gethostbyname(socket.gethostname()))+":56889",'1'], stdout=DEVNULL, stderr=subprocess.STDOUT)

#Lookup functionality test case
stockName = random.choice(stockNames)
print("########################################")
print("##Test Case 1 - Lookup Functionality: ##")
print("########################################")
print("Input Request: GET /stocks/" + stockName)
conn.request('GET','/stocks/' + stockName)
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("JSON Reply: " + str(data_received))
print()

#Lookup functionality error handling test case
stockName = "imaginarycompany"
print("###########################################################")
print("##Test Case 2 - Lookup Error Handling (Stock not found): ##")
print("###########################################################")
print("Input Request: GET /stocks/" + stockName)
conn.request('GET','/stocks/' + stockName)
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("JSON Reply: " + str(data_received))
print()

#Sell functionality test case
stockName = random.choice(stockNames)
print("######################################")
print("##Test Case 3 - Sell Functionality: ##")
print("######################################")
print("Input Request: POST /orders")
print("Input JSON: ", end = "")
data = {}
data['name']=stockName
data['type']="sell"
data['quantity']=10
json_data = json.dumps(data)
print(json_data)
print("Stock Information before Request: ", end = "")
conn.request('GET','/stocks/' + stockName)
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print(str(data_received))
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("JSON Reply: " + str(data_received))
print("Stock Information after Request: ", end = "")
conn.request('GET','/stocks/' + stockName)
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print(str(data_received))
print()

#Buy functionality test case
stockName = random.choice(stockNames)
print("#####################################")
print("##Test Case 4 - Buy Functionality: ##")
print("#####################################")
print("Input Request: POST /orders")
print("Input JSON: ", end = "")
data = {}
data['name']=stockName
data['type']="buy"
data['quantity']=10
json_data = json.dumps(data)
print(json_data)
print("Stock Information before Request: ", end = "")
conn.request('GET','/stocks/' + stockName)
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print(str(data_received))
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("JSON Reply: " + str(data_received))
print("Stock Information after Request: ", end = "")
conn.request('GET','/stocks/' + stockName)
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print(str(data_received))
print()

#Buy functionality error handling test case
stockName = random.choice(stockNames)
print("#############################################################################")
print("##Test Case 5 - Buy Error Handling (Amount to buy > num of stocks avail.): ##")
print("#############################################################################")
print("Input Request: POST /orders")
print("Input JSON: ", end = "")
data = {}
data['name']=stockName
data['type']="buy"
data['quantity']=10000000
json_data = json.dumps(data)
print(json_data)
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("JSON Reply: " + str(data_received))
print()

#Buy/Sel functionality error handling test case
#PROTO already defines quantity needs to be an int. As such, the only invalid value will be negative values.
stockName = random.choice(stockNames)
print("########################################################################")
print("##Test Case 6 - Buy/Sell Error Handling (Invalid quantity of stocks): ##")
print("########################################################################")
print("Note: PROTO already defines quantity needs to be an int. As such, the only invalid value will be negative values.")
print("Input Request: POST /orders")
print("Input JSON: ", end = "")
data = {}
data['name']=stockName
data['type']="buy"
data['quantity']=-1000
json_data = json.dumps(data)
print(json_data)
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("JSON Reply: " + str(data_received))
print()
print("Input Request: POST /orders")
print("Input JSON: ", end = "")
data = {}
data['name']=stockName
data['type']="sell"
data['quantity']=-1000
json_data = json.dumps(data)
print(json_data)
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("JSON Reply: " + str(data_received))
print()

#Buy functionality error handling test case
stockName = random.choice(stockNames)
print("##################################################################")
print("##Test Case 7 - Buy/Sell Error Handling (Invalid request type): ##")
print("##################################################################")
print("Input Request: POST /orders")
print("Input JSON: ", end = "")
data = {}
data['name']=stockName
data['type']="trade"
data['quantity']=100
json_data = json.dumps(data)
print(json_data)
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("JSON Reply: " + str(data_received))
print()

#Buy functionality error handling test case
stockName = "imaginarycompany"
print("#############################################################")
print("##Test Case 8 - Buy/Sell Error Handling (Stock not found): ##")
print("#############################################################")
print("Input Request: POST /orders")
print("Input JSON: ", end = "")
data = {}
data['name']=stockName
data['type']="buy"
data['quantity']=100
json_data = json.dumps(data)
print(json_data)
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("JSON Reply: " + str(data_received))
print()

#Caching test case
stockName = random.choice(stockNames)
print("##########################################")
print("##Test Case 9 - Caching Functionality:  ##")
print("##########################################")
print("Request 1a (s.t. it is stored in local cache): GET /stocks/" + stockName)
conn.request('GET','/stocks/' + stockName)
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("Request 1b (s.t. we can retrieve from cache): GET /stocks/" + stockName)
start = timeit.default_timer()
conn.request('GET','/stocks/' + stockName)
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
cache = timeit.default_timer() - start
print("Latency with caching: " + str(cache))
print("Request 2a (trade stock so cache is invalidated): POST /orders")
data = {}
data['name']=stockName
data['type']="buy"
data['quantity']=10
json_data = json.dumps(data)
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("Request 2b (lookup stock without cache): GET /stocks/" + stockName)
start = timeit.default_timer()
conn.request('GET','/stocks/' + stockName)
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
noCache = timeit.default_timer() - start
print("Latency without caching: " + str(noCache))
print("Difference in time: " + str(noCache - cache))
print("Percent speed up: " + str(((noCache - cache) / noCache)* 100))
print()

#Order query functionality test case
stockName = random.choice(stockNames)
print("##############################################")
print("##Test Case 10 - Order Query Functionality: ##")
print("##############################################")
print("Input Request: POST /orders")
print("Input JSON: ", end = "")
data = {}
data['name']=stockName
data['type']="sell"
data['quantity']=10
json_data = json.dumps(data)
print(json_data)
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
#Locally store order information for successful trades in order to verify with backend
localOrderInfo = {}
orderNum = (data_received['data'])['transaction_number']
orderInfo = {'number':orderNum,'name':stockName,'type':'sell','quantity':10}
localOrderInfo[orderNum] = orderInfo
print("Client Locally Stored Information: "+str(localOrderInfo))
print("Input Request: GET /orders/"+str(orderNum))
conn.request('GET','/orders/' + str(orderNum))
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("Output of Order Query: "+str(data_received))
print()

#Order query error handling test case
stockName = random.choice(stockNames)
print("###############################################")
print("##Test Case 11 - Order Query Error Handling: ##")
print("###############################################")
print("Input Request: POST /orders")
print("Input JSON: ", end = "")
data = {}
data['name']=stockName
data['type']="sell"
data['quantity']=10
json_data = json.dumps(data)
print(json_data)
conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
#Locally store order information for successful trades in order to verify with backend
localOrderInfo = {}
orderNum = (data_received['data'])['transaction_number']
orderInfo = {'number':orderNum,'name':stockName,'type':'sell','quantity':10}
localOrderInfo[orderNum] = orderInfo
print("Client Locally Stored Information: "+str(localOrderInfo))
print("Input Request: GET /orders/"+str(orderNum+1))
conn.request('GET','/orders/' + str(orderNum+1))
rsp = conn.getresponse()
data_received = rsp.read()
#Convert data to dict
data_received = json.loads(data_received)
print("Output of Order Query: "+str(data_received))
print()
conn.close()


catalogService.terminate()
orderService1.terminate()
orderService2.terminate()
orderService3.terminate()
frontendService.terminate()
os.remove(os.getcwd()+'\\order1.txt')
os.remove(os.getcwd()+'\\order2.txt')
os.remove(os.getcwd()+'\\order3.txt')
os.remove(os.getcwd()+'\\catalog.txt')

catalogService = subprocess.Popen(['python',os.getcwd()+'\\catalog-service\\catalogServer.py'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService1 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56891','3',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService2 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56890','2',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService3 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56889','1',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(1)
frontendService = subprocess.Popen(['python',os.getcwd()+'\\front-end\\frontEnd.py','3',str(socket.gethostbyname(socket.gethostname()))+":56891",'2',str(socket.gethostbyname(socket.gethostname()))+":56890",'1',str(socket.gethostbyname(socket.gethostname()))+":56889",'1'], stdout=DEVNULL, stderr=subprocess.STDOUT)

#Propagation functoinality test case
stockName = random.choice(stockNames)
print("##############################################")
print("##Test Case 12 - Propagation Functionality: ##")
print("##############################################")
#os.chdir("..")
for x in range(0,2):
    print("-------- Input --------")
    print("Input Request: POST /orders")
    print("Input JSON: ", end = "")
    data = {}

    data['name']=stockName
    #Randomly choose to buy or sell or invalid option
    tradeTypes = ["buy", "sell"] #tradeTypes = ["buy", "sell","trade"]
    tradeType = random.choice(tradeTypes)
    data['type']=tradeType
    #Randomly select how many stocks to buy sell within range of 1 to 100
    stockQuantity = random.randint(1,100) #stockQuantity = random.randint(-10,100)
    data['quantity']=stockQuantity

    json_data = json.dumps(data)
    print(json_data)
    conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
    rsp = conn.getresponse()
    data_received = rsp.read()
    #Convert data to dict
    data_received = json.loads(data_received)
    print("JSON Reply: " + str(data_received))

file1 = os.getcwd() + '\\order1.txt'
print("--- Content of Replica 1 at " + str(file1)+": ---")
with open(file1) as f:
    lines = f.readlines()
    print(lines)


file2 = os.getcwd() + '\\order2.txt'
print("--- Content of Replica 2 at " + str(file2)+": ---")
with open(file2) as f:
    lines = f.readlines()
    print(lines)


file3 = os.getcwd() + '\\order3.txt'
print("--- Content of Replica 3 at " + str(file3)+": ---")
with open(file3) as f:
    lines = f.readlines()
    print(lines)
print("ALL THREE FILES ARE THE SAME: " + str(filecmp.cmp(file1,file2,file3)))
print()
conn.close()

catalogService.terminate()
orderService1.terminate()
orderService2.terminate()
orderService3.terminate()
frontendService.terminate()
os.remove(os.getcwd()+'\\order1.txt')
os.remove(os.getcwd()+'\\order2.txt')
os.remove(os.getcwd()+'\\order3.txt')
os.remove(os.getcwd()+'\\catalog.txt')

catalogService = subprocess.Popen(['python',os.getcwd()+'\\catalog-service\\catalogServer.py'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService2 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56890','2',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService3 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56889','1',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(1)
frontendService = subprocess.Popen(['python',os.getcwd()+'\\front-end\\frontEnd.py','3',str(socket.gethostbyname(socket.gethostname()))+":56891",'2',str(socket.gethostbyname(socket.gethostname()))+":56890",'1',str(socket.gethostbyname(socket.gethostname()))+":56889",'1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(6)

with open('./order3.txt', 'w') as file:
     file.write(json.dumps({}))
#Fault tolerance test case
stockName = random.choice(stockNames)
print("#######################################################")
print("##Test Case 13 - Largest Replica ID Dead on Arrival: ##")
print("#######################################################")
#os.chdir("..")
for x in range(0,3):
    print("-------- Input --------")
    print("Input Request: POST /orders")
    print("Input JSON: ", end = "")
    data = {}

    data['name']=stockName
    #Randomly choose to buy or sell or invalid option
    tradeTypes = ["buy", "sell"] #tradeTypes = ["buy", "sell","trade"]
    tradeType = random.choice(tradeTypes)
    data['type']=tradeType
    #Randomly select how many stocks to buy sell within range of 1 to 100
    stockQuantity = random.randint(1,100) #stockQuantity = random.randint(-10,100)
    data['quantity']=stockQuantity

    json_data = json.dumps(data)
    print(json_data)
    conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
    rsp = conn.getresponse()
    data_received = rsp.read()
    #Convert data to dict
    data_received = json.loads(data_received)
    print("JSON Reply: " + str(data_received))

file1 = os.getcwd() + '\\order1.txt'
print("--- Content of Replica 1 at " + str(file1)+": ---")
with open(file1) as f:
    lines = f.readlines()
    print(lines)


file2 = os.getcwd() + '\\order2.txt'
print("--- Content of Replica 2 at " + str(file2)+": ---")
with open(file2) as f:
    lines = f.readlines()
    print(lines)


file3 = os.getcwd() + '\\order3.txt'
print("--- Content of Replica 3 at " + str(file3)+": ---")
with open(file3) as f:
    lines = f.readlines()
    print(lines)

print("ALL THREE FILES ARE THE SAME: " + str(filecmp.cmp(file1,file2) and filecmp.cmp(file2,file3) and filecmp.cmp(file1,file3)))
print("REPLICAS 2 AND 1 ARE THE SAME: " + str(filecmp.cmp(file1,file2)))
print()
conn.close()


catalogService.terminate()
orderService1.terminate()
orderService2.terminate()
orderService3.terminate()
frontendService.terminate()
os.remove(os.getcwd()+'\\order1.txt')
os.remove(os.getcwd()+'\\order2.txt')
os.remove(os.getcwd()+'\\order3.txt')
os.remove(os.getcwd()+'\\catalog.txt')

catalogService = subprocess.Popen(['python',os.getcwd()+'\\catalog-service\\catalogServer.py'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService1 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56891','3',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService2 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56890','2',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService3 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56889','1',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(2)
frontendService = subprocess.Popen(['python',os.getcwd()+'\\front-end\\frontEnd.py','3',str(socket.gethostbyname(socket.gethostname()))+":56891",'2',str(socket.gethostbyname(socket.gethostname()))+":56890",'1',str(socket.gethostbyname(socket.gethostname()))+":56889",'1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(2)

#Fault tolerance test case
stockName = random.choice(stockNames)
print("####################################################")
print("##Test Case 14 - Leader Crashes During Execution: ##")
print("####################################################")
#os.chdir("..")
for x in range(0,3):
    print("-------- Input --------")
    print("Input Request: POST /orders")
    print("Input JSON: ", end = "")
    data = {}

    data['name']=stockName
    #Randomly choose to buy or sell or invalid option
    tradeTypes = ["buy", "sell"] #tradeTypes = ["buy", "sell","trade"]
    tradeType = random.choice(tradeTypes)
    data['type']=tradeType
    #Randomly select how many stocks to buy sell within range of 1 to 100
    stockQuantity = random.randint(1,100) #stockQuantity = random.randint(-10,100)
    data['quantity']=stockQuantity

    json_data = json.dumps(data)
    print(json_data)
    conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
    if x == 1:
        orderService1.terminate()
        time.sleep(5)
    rsp = conn.getresponse()
    data_received = rsp.read()
    #Convert data to dict
    data_received = json.loads(data_received)
    print("JSON Reply: " + str(data_received))


file1 = os.getcwd() + '\\order1.txt'
print("--- Content of Replica 1 at " + str(file1)+": ---")
with open(file1) as f:
    lines = f.readlines()
    print(lines)


file2 = os.getcwd() + '\\order2.txt'
print("--- Content of Replica 2 at " + str(file2)+": ---")
with open(file2) as f:
    lines = f.readlines()
    print(lines)


file3 = os.getcwd() + '\\order3.txt'
print("--- Content of Replica 3 at " + str(file3)+": ---")
with open(file3) as f:
    lines = f.readlines()
    print(lines)

print("ALL THREE FILES ARE THE SAME: " + str(filecmp.cmp(file1,file2) and filecmp.cmp(file2,file3) and filecmp.cmp(file1,file3)))
print("REPLICAS 2 AND 1 ARE THE SAME: " + str(filecmp.cmp(file1,file2)))
print()
conn.close()


catalogService.terminate()
orderService1.terminate()
orderService2.terminate()
orderService3.terminate()
frontendService.terminate()
os.remove(os.getcwd()+'\\order1.txt')
os.remove(os.getcwd()+'\\order2.txt')
os.remove(os.getcwd()+'\\order3.txt')
os.remove(os.getcwd()+'\\catalog.txt')

catalogService = subprocess.Popen(['python',os.getcwd()+'\\catalog-service\\catalogServer.py'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService1 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56891','3',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService2 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56890','2',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService3 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56889','1',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(2)
frontendService = subprocess.Popen(['python',os.getcwd()+'\\front-end\\frontEnd.py','3',str(socket.gethostbyname(socket.gethostname()))+":56891",'2',str(socket.gethostbyname(socket.gethostname()))+":56890",'1',str(socket.gethostbyname(socket.gethostname()))+":56889",'1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(2)

#Fault tolerance test case
stockName = random.choice(stockNames)
print("######################################################")
print("##Test Case 15 - Follower Crashes During Execution: ##")
print("######################################################")
#os.chdir("..")
for x in range(0,3):
    print("-------- Input --------")
    print("Input Request: POST /orders")
    print("Input JSON: ", end = "")
    data = {}

    data['name']=stockName
    #Randomly choose to buy or sell or invalid option
    tradeTypes = ["buy", "sell"] #tradeTypes = ["buy", "sell","trade"]
    tradeType = random.choice(tradeTypes)
    data['type']=tradeType
    #Randomly select how many stocks to buy sell within range of 1 to 100
    stockQuantity = random.randint(1,100) #stockQuantity = random.randint(-10,100)
    data['quantity']=stockQuantity

    json_data = json.dumps(data)
    print(json_data)
    conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})

    rsp = conn.getresponse()
    data_received = rsp.read()
    if x == 1:
        orderService2.terminate()
        time.sleep(5)
    #Convert data to dict
    data_received = json.loads(data_received)
    print("JSON Reply: " + str(data_received))


file1 = os.getcwd() + '\\order1.txt'
print("--- Content of Replica 1 at " + str(file1)+": ---")
with open(file1) as f:
    lines = f.readlines()
    print(lines)


file2 = os.getcwd() + '\\order2.txt'
print("--- Content of Replica 2 at " + str(file2)+": ---")
with open(file2) as f:
    lines = f.readlines()
    print(lines)


file3 = os.getcwd() + '\\order3.txt'
print("--- Content of Replica 3 at " + str(file3)+": ---")
with open(file3) as f:
    lines = f.readlines()
    print(lines)

print("ALL THREE FILES ARE THE SAME: " + str(filecmp.cmp(file1,file2) and filecmp.cmp(file2,file3) and filecmp.cmp(file1,file3)))
print("REPLICAS 3 AND 1 ARE THE SAME: " + str(filecmp.cmp(file1,file3)))
print()
conn.close()

catalogService.terminate()
orderService1.terminate()
orderService2.terminate()
orderService3.terminate()
frontendService.terminate()
os.remove(os.getcwd()+'\\order1.txt')
os.remove(os.getcwd()+'\\order2.txt')
os.remove(os.getcwd()+'\\order3.txt')
os.remove(os.getcwd()+'\\catalog.txt')

catalogService = subprocess.Popen(['python',os.getcwd()+'\\catalog-service\\catalogServer.py'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService1 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56891','3',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService2 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56890','2',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService3 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56889','1',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(2)
frontendService = subprocess.Popen(['python',os.getcwd()+'\\front-end\\frontEnd.py','3',str(socket.gethostbyname(socket.gethostname()))+":56891",'2',str(socket.gethostbyname(socket.gethostname()))+":56890",'1',str(socket.gethostbyname(socket.gethostname()))+":56889",'1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(2)

#Fault tolerance test case
stockName = random.choice(stockNames)
print("################################################################")
print("##Test Case 16 - Leader Crashes and Rejoins During Execution: ##")
print("################################################################")
#os.chdir("..")
for x in range(0,4):
    print("-------- Input --------")
    print("Input Request: POST /orders")
    print("Input JSON: ", end = "")
    data = {}

    data['name']=stockName
    #Randomly choose to buy or sell or invalid option
    tradeTypes = ["buy", "sell"] #tradeTypes = ["buy", "sell","trade"]
    tradeType = random.choice(tradeTypes)
    data['type']=tradeType
    #Randomly select how many stocks to buy sell within range of 1 to 100
    stockQuantity = random.randint(1,100) #stockQuantity = random.randint(-10,100)
    data['quantity']=stockQuantity

    json_data = json.dumps(data)
    print(json_data)
    conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
    if x == 1:
        orderService1.terminate()
        time.sleep(5)
        file3 = os.getcwd() + '\\order3.txt'
        print("--- Content of Replica 3 at Time of Crash: ---")
        with open(file3) as f:
            lines = f.readlines()
            print(lines)
    rsp = conn.getresponse()
    data_received = rsp.read()
    if x == 3:
        orderService1 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56891','3',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(5)
    #Convert data to dict
    data_received = json.loads(data_received)
    print("JSON Reply: " + str(data_received))


file1 = os.getcwd() + '\\order1.txt'
print("--- Content of Replica 1 at " + str(file1)+": ---")
with open(file1) as f:
    lines = f.readlines()
    print(lines)


file2 = os.getcwd() + '\\order2.txt'
print("--- Content of Replica 2 at " + str(file2)+": ---")
with open(file2) as f:
    lines = f.readlines()
    print(lines)


file3 = os.getcwd() + '\\order3.txt'
print("--- Content of Replica 3 at " + str(file3)+": ---")
with open(file3) as f:
    lines = f.readlines()
    print(lines)

print("ALL THREE FILES ARE THE SAME: " + str(filecmp.cmp(file1,file2) and filecmp.cmp(file2,file3) and filecmp.cmp(file1,file3)))
print("REPLICAS 3 AND 1 ARE THE SAME: " + str(filecmp.cmp(file1,file3)))
print()
conn.close()

catalogService.terminate()
orderService1.terminate()
orderService2.terminate()
orderService3.terminate()
frontendService.terminate()
os.remove(os.getcwd()+'\\order1.txt')
os.remove(os.getcwd()+'\\order2.txt')
os.remove(os.getcwd()+'\\order3.txt')
os.remove(os.getcwd()+'\\catalog.txt')

catalogService = subprocess.Popen(['python',os.getcwd()+'\\catalog-service\\catalogServer.py'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService1 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56891','3',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService2 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56890','2',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
orderService3 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56889','1',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(2)
frontendService = subprocess.Popen(['python',os.getcwd()+'\\front-end\\frontEnd.py','3',str(socket.gethostbyname(socket.gethostname()))+":56891",'2',str(socket.gethostbyname(socket.gethostname()))+":56890",'1',str(socket.gethostbyname(socket.gethostname()))+":56889",'1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
time.sleep(2)

#Fault tolerance test case
stockName = random.choice(stockNames)
print("##################################################################")
print("##Test Case 17 - Follower Crashes and Rejoins During Execution: ##")
print("##################################################################")
#os.chdir("..")
for x in range(0,4):
    print("-------- Input --------")
    print("Input Request: POST /orders")
    print("Input JSON: ", end = "")
    data = {}

    data['name']=stockName
    #Randomly choose to buy or sell or invalid option
    tradeTypes = ["buy", "sell"] #tradeTypes = ["buy", "sell","trade"]
    tradeType = random.choice(tradeTypes)
    data['type']=tradeType
    #Randomly select how many stocks to buy sell within range of 1 to 100
    stockQuantity = random.randint(1,100) #stockQuantity = random.randint(-10,100)
    data['quantity']=stockQuantity

    json_data = json.dumps(data)
    print(json_data)
    conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
    rsp = conn.getresponse()
    data_received = rsp.read()
    if x == 1:
        orderService2.terminate()
        time.sleep(5)
        file3 = os.getcwd() + '\\order2.txt'
        print("--- Content of Replica 2 at Time of Crash: ---")
        with open(file3) as f:
            lines = f.readlines()
            print(lines)
    if x == 3:
        orderService2 = subprocess.Popen(['python',os.getcwd()+'\\order-service\\orderServer.py','56890','2',str(socket.gethostbyname(socket.gethostname())),'56893','1'], stdout=DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(5)
    #Convert data to dict
    data_received = json.loads(data_received)
    print("JSON Reply: " + str(data_received))


file1 = os.getcwd() + '\\order1.txt'
print("--- Content of Replica 1 at " + str(file1)+": ---")
with open(file1) as f:
    lines = f.readlines()
    print(lines)


file2 = os.getcwd() + '\\order2.txt'
print("--- Content of Replica 2 at " + str(file2)+": ---")
with open(file2) as f:
    lines = f.readlines()
    print(lines)


file3 = os.getcwd() + '\\order3.txt'
print("--- Content of Replica 3 at " + str(file3)+": ---")
with open(file3) as f:
    lines = f.readlines()
    print(lines)

print("ALL THREE FILES ARE THE SAME: " + str(filecmp.cmp(file1,file2) and filecmp.cmp(file2,file3) and filecmp.cmp(file1,file3)))
print("REPLICAS 3 AND 1 ARE THE SAME: " + str(filecmp.cmp(file1,file3)))
print()
conn.close()


catalogService.terminate()
orderService1.terminate()
orderService2.terminate()
orderService3.terminate()
frontendService.terminate()
os.remove(os.getcwd()+'\\order1.txt')
os.remove(os.getcwd()+'\\order2.txt')
os.remove(os.getcwd()+'\\order3.txt')
os.remove(os.getcwd()+'\\catalog.txt')
