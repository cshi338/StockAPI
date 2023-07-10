from concurrent import futures
from threading import Lock

import logging
import math
import time
import socket
import json

import os
import grpc
import stockbazaar_pb2
import stockbazaar_pb2_grpc

#Load the database json txt if it exists
if os.path.exists('./catalog.txt'):
    with open('./catalog.txt') as file:
        stockData = json.loads(file.read())
else:
    #Create initial on disk data file
    stockData = {}
    tesla = {'price':183.26,'volume':0,'quantity':1000}
    ford = {'price':11.93,'volume':0,'quantity':1000}
    apple = {'price':152.59,'volume':0,'quantity':1000}
    amazon = {'price':94.88,'volume':0,'quantity':1000}
    nvidia = {'price':240.63,'volume':0,'quantity':1000}
    intel = {'price':28.01,'volume':0,'quantity':1000}
    meta = {'price':194.02,'volume':0,'quantity':1000}

    stockData['apple']=apple
    stockData['tesla']=tesla
    stockData['ford']=ford
    stockData['amazon']=amazon
    stockData['nvidia']=nvidia
    stockData['intel']=intel
    stockData['meta']=meta
    with open('./catalog.txt', 'w') as file:
         file.write(json.dumps(stockData)) # use `json.loads` to do the reverse


class CatalogServicer(stockbazaar_pb2_grpc.CatalogServicer):
    #Takes the string stockName and returns the price of the stock and the trading volume so far.
    def Lookup(self, request, context):
        global stockData
        #Get stock price for the given stock name
        stockInfo = stockData.get(request.stockName, {})
        #If the name cannot be found in dict, return -1/-1
        if len(stockInfo) == 0:
            return stockbazaar_pb2.lookupResult(stockPrice=-1,stockQuantity=-1)
        #If found, return stock price and stock volume
        else:
            return stockbazaar_pb2.lookupResult(stockPrice=stockInfo['price'],stockQuantity=stockInfo['quantity'])

    #Buys or sells N items of the stock and increments the trading volume of that item by N.
    def Trade(self, request, context):
        global stockData
        tradeType = request.tradeType
        stockName = request.stockName
        stockTradeQuantity = request.stockTradeQuantity

        #If the trade type is Buy, increment stock volume
        if tradeType == "buy":
            (stockData[stockName])['quantity'] -= stockTradeQuantity
            (stockData[stockName])['volume'] += stockTradeQuantity
        #If the trade type is Sell, increment stock volume
        elif tradeType == "sell":
            (stockData[stockName])['quantity'] += stockTradeQuantity
            (stockData[stockName])['volume'] += stockTradeQuantity
        with open('./catalog.txt', 'w') as file:
             file.write(json.dumps(stockData)) # use `json.loads` to do the reverse
        #Successfully buy/sell returns 1
        return stockbazaar_pb2.tradeResult(resultTrade = 1)

def serve():
    #Implement server with 5 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    stockbazaar_pb2_grpc.add_CatalogServicer_to_server(
        CatalogServicer(), server)
    print("Server started on: " + socket.gethostbyname(socket.gethostname())+':56892')
    server.add_insecure_port(socket.gethostbyname(socket.gethostname())+':56892')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
