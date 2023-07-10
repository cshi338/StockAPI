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
#create a connection
conn = http.client.HTTPConnection(http_server, port)
stockNames = ["tesla","ford","apple","amazon","nvidia","intel","meta"]

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


conn.close()
