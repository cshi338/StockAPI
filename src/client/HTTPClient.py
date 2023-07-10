#!/usr/bin/env python
import logging
import random
import time

import http.client
import sys
import json

#get http server ip
http_server = sys.argv[1]
port = sys.argv[2]
probability = float(sys.argv[3])
mode = int(sys.argv[4]) #0 for verbose 1 for non-verbose/only latency shows
#create a connection
conn = http.client.HTTPConnection(http_server, port)
stockNames = ["tesla","ford","apple","amazon","nvidia","intel","meta","imaginarycompany"]
start_time = time.time()
#Running total of number of requests sent s.t. we can calculate average latency
numRequests = 0
for _ in range(100):
    stockName = random.choice(stockNames)
    if mode == 0: print("-------------- Lookup --------------") 
    if mode == 0: print("Input: " + stockName)
    conn.request('GET','/stocks/' + stockName)
    #get response from server
    rsp = conn.getresponse()
    data_received = rsp.read()
    #Convert data to dict
    data_received = json.loads(data_received)
    numRequests += 1
    if mode == 0: print("Output: " + str(data_received))

    order = random.uniform(0,1)
    if order > probability:
        if mode == 0: print("-------------- Trade --------------")
        data = {}
        data['name']=stockName
        #Randomly choose to buy or sell or invalid option
        tradeTypes = ["buy", "sell","trade"]
        tradeType = random.choice(tradeTypes)
        data['type']=tradeType
        #Randomly select how many stocks to buy sell within range of 1 to 100
        stockQuantity = random.randint(-10,100)
        data['quantity']=stockQuantity
        json_data = json.dumps(data)
        if mode == 0: print("Input: " + str(json_data))
        conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
        #get response from server
        rsp = conn.getresponse()
        data_received = rsp.read()
        #Convert data to dict
        data_received = json.loads(data_received)
        numRequests += 1
        if mode == 0: print("Output: " + str(data_received))
    if mode == 0: print("\n")
print("Average Latency: " + str((time.time() - start_time)/numRequests))
conn.close()
