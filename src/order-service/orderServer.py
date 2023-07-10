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
#Check if database file exists in current folder, if it does load the json to a dict
if os.path.exists('./order.txt'):
    with open('./order.txt') as file:
        transactions = json.loads(file.read())
    #Continue the transaction number by finding the maximum key in the dict
    transactionNum = int(max(transactions, key=int))
else:
    transactions = {}
    transactionNum = -1

class OrderServicer(stockbazaar_pb2_grpc.OrderServicer):
    #Takes the string stockName and returns the price of the stock and the trading volume so far.
    def Request(self, request, context):
        global transactions
        global transactionNum
        tradeType = request.tradeType
        stockName = request.stockName
        stockTradeQuantity = request.stockTradeQuantity
        #Connect to the catalog server
        with grpc.insecure_channel(cataloghost + ':56892') as channel:
            stub = stockbazaar_pb2_grpc.CatalogStub(channel)
            #Lookup the given stock
            res = stub.Lookup(stockbazaar_pb2.lookupStockName(stockName = stockName))
            #Stock not found
            if res.stockPrice == -1 and res.stockQuantity == -1:
                return stockbazaar_pb2.requestResult(transactionNum = -1)
            #Invalid request i.e. not "buy" or "sell"
            elif tradeType not in ['buy','sell']:
                return stockbazaar_pb2.requestResult(transactionNum = -2)
            #Trying to buy or sell an invalid number of stocks
            elif stockTradeQuantity < 1:
                return stockbazaar_pb2.requestResult(transactionNum = -3)
            #Trying to buy more stocks than available
            elif tradeType =='buy' and stockTradeQuantity > res.stockQuantity:
                return stockbazaar_pb2.requestResult(transactionNum = -4)
            else:
                #Connect to the catalog server s.t. it can update quantity and volume
                res = stub.Trade(stockbazaar_pb2.tradeStockName(stockName = stockName, stockTradeQuantity = stockTradeQuantity, tradeType = tradeType))
                transactionNum += 1
                #Write to database in memory
                transactions[transactionNum]={'name':stockName,'type':tradeType,'quantity':stockTradeQuantity}
                #Write the current order database to a txt file in json format
                with open('./order.txt', 'w') as file:
                     file.write(json.dumps(transactions)) # use `json.loads` to do the reverse
                return stockbazaar_pb2.requestResult(transactionNum = transactionNum)

def serve():
    #Implement server with 5 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    stockbazaar_pb2_grpc.add_OrderServicer_to_server(
        OrderServicer(), server)
    print("Server started on: " + socket.gethostbyname(socket.gethostname())+':56891')
    server.add_insecure_port(socket.gethostbyname(socket.gethostname())+':56891')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    cataloghost = os.getenv("CATALOG_HOST", socket.gethostbyname(socket.gethostname()))
    logging.basicConfig()
    serve()
