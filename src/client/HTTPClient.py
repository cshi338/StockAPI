#!/usr/bin/env python
import logging
import random
import time
import timeit

import http.client
import sys
import json

#Locally store order information for successful trades in order to verify with backend
localOrderInfo = {}

#get http server ip
http_server = sys.argv[1]
port = sys.argv[2]
probability = float(sys.argv[3]) #Set the probability p at which it will send another order request using the same connection.
mode = int(sys.argv[4]) #0 for verbose 1 for non-verbose/latency and verification shows
#create a connection
conn = http.client.HTTPConnection(http_server, port)
stockNames = ["tesla","ford","apple","amazon","nvidia","intel","meta","nike","amc","gamestop"] #stockNames = ["tesla","ford","apple","amazon","nvidia","intel","meta","nike","amc","gamestop","imaginarycompany"]


#Counts of times for each request
catalogLookup = 0.0
orderLookup = 0.0
orderTrade = 0.0
#Running total of number of requests sent s.t. we can calculate average latency
numCatalogLookup = 0
numOrderLookup = 0
numOrderTrade = 0

for _ in range(100):
    stockName = random.choice(stockNames)
    if mode == 0: print("-------------- Lookup --------------")
    if mode == 0: print("Input: " + stockName)
    start_time = timeit.default_timer()
    conn.request('GET','/stocks/' + stockName)
    #get response from server
    rsp = conn.getresponse()
    data_received = rsp.read()
    #Convert data to dict
    data_received = json.loads(data_received)
    catalogLookup += (timeit.default_timer() - start_time)
    numCatalogLookup += 1
    if mode == 0: print("Output: " + str(data_received))

    order = random.uniform(0,1)
    if probability > order:

        if mode == 0: print("-------------- Trade --------------")
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
        if mode == 0: print("Input: " + str(json_data))
        start_time = timeit.default_timer()
        conn.request('POST', '/orders', body = json_data.encode(), headers={'Content-Length':str(len(bytes(json_data, 'utf-8')))})
        #get response from server
        rsp = conn.getresponse()
        data_received = rsp.read()
        #Convert data to dict
        data_received = json.loads(data_received)
        orderTrade += (timeit.default_timer() - start_time)
        numOrderTrade += 1

        #Verify that the trade was successful s.t. we can add it to our local record
        if(len(data_received.get('error',{})) == 0):
            orderNum = (data_received['data'])['transaction_number']
            orderInfo = {'number':orderNum,'name':stockName,'type':tradeType,'quantity':stockQuantity}
            localOrderInfo[orderNum] = orderInfo
        if mode == 0: print("Output: " + str(data_received))
    if mode == 0: print("\n")


#Perform order verification comparing local info to server info
print("----- Order Query Verification -----")
print("Successful Trades Made: " + str(len(localOrderInfo)))
count = 0
for orderNum, orderInfo in localOrderInfo.items():
    if mode == 0: print("------- Verifying Order " + str(orderNum) + " -------")
    start_time = timeit.default_timer()
    conn.request('GET','/orders/' + str(orderNum))
    #get response from server
    rsp = conn.getresponse()
    data_received = rsp.read()
    #Convert data to dict
    data_received = json.loads(data_received)
    orderLookup += (timeit.default_timer() - start_time)
    numOrderLookup += 1
    if mode == 0: print("Local: " + str(orderInfo))
    if mode == 0: print("Server: " + str(data_received['data']))
    #Verify that the two dicts match
    if orderInfo == data_received['data']:
        if mode == 0: print("MATCH")
        pass
    else:
        if mode == 0: print("NO MATCH")
        pass
        count += 1
    if mode == 0: print()
if count != 0:
    print("A NON-MATCH WAS FOUND")
else:
    print("ALL ORDERS VERIFIED")
print("---- Average Latency of Requests ----")
print("Average Latency of Catalog Lookup Request: " + str(catalogLookup/numCatalogLookup))
if numOrderTrade == 0:
    print("Average Latency of Order Trade Request: N/A")
else:
    print("Average Latency of Order Trade Request: " + str(orderTrade/numOrderTrade))
if numOrderLookup == 0:
    print("Average Latency of Order Trade Request: N/A")
else:
    print("Average Latency of Order Query Lookup: " + str(orderLookup/numOrderLookup))

conn.close()
