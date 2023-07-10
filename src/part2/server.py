from concurrent import futures
from threading import Lock
import logging
import math
import time
import socket

import grpc
import stockbazaar_pb2
import stockbazaar_pb2_grpc

#Dict mapping company names to their respective stock price
stockPrices = {}
stockPrices["GameStart"] = 15.99
stockPrices["FishCo"] = 25.47
stockPrices["BoarCo"] = 5.28
stockPrices["MenhirCo"] = 22.58
#Dict mapping company names to the trading volume of their respective stock
stockVolume = {}
stockVolume["GameStart"] = 0
stockVolume["FishCo"] = 0
stockVolume["BoarCo"] = 0
stockVolume["MenhirCo"] = 0
#Dict mapping company names to the maximum trade volume of their respective stock
stockMaxVolume = {}
def setMaxVolume(gameStart, fishCo, boarCo, menhirCo):
    stockMaxVolume["GameStart"] = int(gameStart)
    stockMaxVolume["FishCo"] = int(fishCo)
    stockMaxVolume["BoarCo"] = int(boarCo)
    stockMaxVolume["MenhirCo"] = int(menhirCo)

#Multithreaded lock for synchronization purposes
lock = Lock()
class StockBazaarServicer(stockbazaar_pb2_grpc.StockBazaarServicer):
    #Takes the string stockName and returns the price of the stock and the trading volume so far.
    def Lookup(self, request, context):
        global stockPrices
        global stockVolume
        #Enable read-lock
        with lock:
            #Get stock price for the given stock name
            stockPrice = stockPrices.get(request.stockName, -1)
            #If the name cannot be found in dict, return -1/-1
            if stockPrice == -1:
                return stockbazaar_pb2.lookupResult(stockPrice=-1,tradingVolume=-1)
            #If found, return stock price and stock volume
            else:
                return stockbazaar_pb2.lookupResult(stockPrice=stockPrice,tradingVolume=stockVolume[request.stockName])
    #Buys or sells N items of the stock and increments the trading volume of that item by N.
    def Trade(self, request, context):
        global stockPrices
        global stockVolume
        global stockMaxVolume
        #Enable write-lock
        with lock:
            tradeType = request.tradeType
            stockName = request.stockName
            stockQuantity = request.stockQuantity
            currVolume = stockVolume.get(stockName,-1)
            #If stock cannot be found, return -1
            if currVolume == -1:
                return stockbazaar_pb2.tradeResult(resultTrade = -1)
            #If the stock is suspended, return 0
            elif currVolume >= stockMaxVolume[stockName]:
                return stockbazaar_pb2.tradeResult(resultTrade = 0)
            #If the trade type is Buy, increment stock volume
            elif tradeType == "Buy":
                stockVolume[stockName] += stockQuantity
            #If the trade type is Sell, increment stock volume
            elif tradeType == "Sell":
                stockVolume[stockName] += stockQuantity
            #Successfully buy/sell returns 1
            return stockbazaar_pb2.tradeResult(resultTrade = 1)
    #Updates the stock price
    def Update(self, request, context):
        global stockPrices
        global stockVolume
        #Enable write-lock
        with lock:
            stockName = request.stockName
            stockPrice = request.stockPrice
            currVolume = stockVolume.get(stockName,-1)
            #If stock cannot be found, return -1
            if currVolume == -1:
                return stockbazaar_pb2.updateResult(resultUpdate = -1)
            #If the updated stock price is invalid, return -2
            elif stockPrice <= 0:
                return stockbazaar_pb2.updateResult(resultUpdate= -2)
            #Update stock price and return 1
            else:
                stockPrices[stockName] = stockPrice
                return stockbazaar_pb2.updateResult(resultUpdate = 1)

def serve():
    #Implement server with 5 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    stockbazaar_pb2_grpc.add_StockBazaarServicer_to_server(
        StockBazaarServicer(), server)
    print(socket.gethostbyname(socket.gethostname())+':56897')
    server.add_insecure_port(socket.gethostbyname(socket.gethostname())+':56897')
    #server.add_insecure_port('128.119.243.168:56897')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    gameStart = input("Maximum trade volume for Game Start: ")
    fishCo = input("Maximum trade volume for Fish Co: ")
    boarCo = input("Maximum trade volume for Boar Co: ")
    menhirCo = input("Maximum trade volume for Menhir Co: ")
    setMaxVolume(gameStart, fishCo, boarCo, menhirCo)


    logging.basicConfig()
    serve()
