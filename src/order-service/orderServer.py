from concurrent import futures
from threading import Lock

import logging
import socket
import json
import sys

import os
import grpc
import stockbazaar_pb2
import stockbazaar_pb2_grpc
import http.client
#import requests

#Assign port number to this order service replica
port = sys.argv[1]
#Assign id number to this order service replica
replicaID = sys.argv[2]
#Assign front end server ip
frontendAdd = sys.argv[3]
#Assign front end server port
frontendPort = sys.argv[4]
#Determine if cache should be off/on 0/1 respectively.
cache = int(sys.argv[5])


#Check if database file exists in current folder, if it does load the json to a dict
if os.path.exists('./order'+str(replicaID)+'.txt'):
    with open('./order'+str(replicaID)+'.txt') as file:
        transactions = json.loads(file.read())
    #Continue the transaction number by finding the maximum key in the dict
    transactionNum = int(max(transactions, key=int))
else:
    transactions = {}
    transactionNum = -1

#Create Lock
lock = Lock()
#List of the current replicas followers. Will only be populated when the current replica is the leader
followers = {}

class OrderServicer(stockbazaar_pb2_grpc.OrderServicer):
    #Takes the int orderNum and returns the order number, name of stock, type of trade, and quantity of stock traded.
    def Lookup(self, request, context):
        global transactions
        #Get stock price for the given stock name
        stockInfo = transactions.get(request.orderNum, {})
        #If the name cannot be found in dict, return -1 as order num
        if len(stockInfo) == 0:
            return stockbazaar_pb2.lookupOrderNumResult(orderNum = -1, stockName = "", tradeType = "", stockTradeQuantity = -1)
        #If found, return the order number, name of stock, type of trade, and quantity of stock traded.
        else:
            return stockbazaar_pb2.lookupOrderNumResult(orderNum = request.orderNum, stockName = stockInfo['name'], tradeType = stockInfo['type'], stockTradeQuantity = stockInfo['quantity'])
    #Takes the string stockName and returns the price of the stock and the trading volume so far.
    def Request(self, request, context):
        global transactions
        global transactionNum
        global followers
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

                with lock: #Without locking, sometimes different clients are given the same transaction number
                    if cache == 1:
                        #Server-push technique to tell frontend service to delete the stock from its local cache
                        conn = http.client.HTTPConnection(frontendAdd, frontendPort)
                        conn.request('GET','/cache/' + stockName)
                        rsp = conn.getresponse()
                        data_received = rsp.read()
                        conn.close()
                    #Iterate transaction number
                    transactionNum += 1
                    #Write to database in memory
                    transactions[transactionNum]={'name':stockName,'type':tradeType,'quantity':stockTradeQuantity}
                    print("Written on Replica " + str(replicaID) + ": "+str({transactionNum:transactions[transactionNum]}))

                    #propagate to all of the followers (given the current replica is the leader, since if it was not the leader than this function would never even be called)
                    for followerNum in list(followers):
                        followerAdd = followers[followerNum]
                        #First check to see if the given addres and port even has an existing gRPC server
                        try:
                            #If the follower can be connected to, propagate the information
                            replicaChannel = grpc.insecure_channel(str(followerAdd['ip']) + ':'+str(followerAdd['port']))
                            stub = stockbazaar_pb2_grpc.OrderStub(replicaChannel)
                            res = stub.Propagate(stockbazaar_pb2.propagateOrderNum(orderNum = transactionNum, stockName = stockName,tradeType=tradeType,stockTradeQuantity = stockTradeQuantity))
                        except grpc._channel._InactiveRpcError:
                            print("Follower address does not exist "+str(followerAdd['ip'])+":"+str(followerAdd['port']))
                            #If we cannot connect to a follower, delete it from the follower list (We assume that is has crashed)
                            del followers[followerNum]

                    #Write the current order database to a txt file in json format
                    with open('./order'+str(replicaID)+'.txt', 'w') as file:
                         file.write(json.dumps(transactions)) # use `json.loads` to do the reverse

                    return stockbazaar_pb2.requestResult(transactionNum = transactionNum)

    def Propagate(self, request, context):
        global transactions
        global transactionNum
        #propagate increase in transaction number
        transactionNum += 1
        #propagate data into local memory
        transactions[transactionNum]={'name':request.stockName,'type':request.tradeType,'quantity':request.stockTradeQuantity}
        #propagate data into the respective database file
        with open('./order'+str(replicaID)+'.txt', 'w') as file:
             file.write(json.dumps(transactions)) # use `json.loads` to do the reverse
        print("Propagated on Replica " + str(replicaID) + ": "+str({transactionNum:transactions[transactionNum]}))
        return stockbazaar_pb2.propagateResult(resultPropagate = 1)

    #Front end sends a list of the addresses of the follower replicas
    def AssignFollowers(self, request, context):
        global followers
        #Check if first follower exists. If so, add to list of followers
        if len(request.followerOne) > 0:
            followers['followerOne'] = {'ip':request.followerOne.split(':')[0],'port':request.followerOne.split(':')[1]}
        #Check if second follower exists. If so, add to list of followers
        if len(request.followerTwo) > 0:
            followers['followerTwo'] = {'ip':request.followerTwo.split(':')[0],'port':request.followerTwo.split(':')[1]}
        print("Followers Assigned: " + str(followers))
        return stockbazaar_pb2.followersResult(resultFollowers = 1)

    #Synchronize the transaction list of the leader with the rejoining replica
    def Synchronize(self, request, context):
        global transactions
        global transactionNum
        global followers
        print("Replica " + str(replicaID) + " Synchornizing with " + str(request.synchronizedAdd))
        print("Followers Before Synchronization: " + str(followers))
        #Add replica to be synchronzied to the list of the leaders followers
        if len(followers.get('followerOne', {})) == 0:
            followers['followerOne'] = {'ip':request.synchronizedAdd.split(':')[0],'port':request.synchronizedAdd.split(':')[1]}
        elif len(followers.get('followerTwo', {})) == 0:
            followers['followerTwo'] = {'ip':request.synchronizedAdd.split(':')[0],'port':request.synchronizedAdd.split(':')[1]}
        print("Followers After Synchronization: " + str(followers))
        orderNeedsSynchronize = request.orderNum
        #Iterate through transactions s.t. we stream all order numbers (rejoin replica max order num, leader max order num]
        for orderNum in list(transactions):
            if int(orderNum) > orderNeedsSynchronize:
                yield stockbazaar_pb2.transNumInfo(orderNum = int(orderNum), stockName = transactions[orderNum]['name'], tradeType = transactions[orderNum]['type'], stockTradeQuantity = transactions[orderNum]['quantity'])



def serve():
    global transactions
    global transactionNum
    #Implement server with 5 threads
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stockbazaar_pb2_grpc.add_OrderServicer_to_server(
        OrderServicer(), server)
    print("Order server started on: " + socket.gethostbyname(socket.gethostname())+':'+str(port))
    server.add_insecure_port(socket.gethostbyname(socket.gethostname())+':'+str(port))
    server.start()
    #Try to ping the front end service. In normal operating conditions, the front end service should not be able to be pinged. If a replica is being restarted, then the front end service will already be running and can be pinged.
    try:
        #Gets leader information from the frontend service.
        #Server-push technique to get the leader replica from the front end service
        conn = http.client.HTTPConnection(frontendAdd, frontendPort)
        conn.request('GET','/leader/' + socket.gethostbyname(socket.gethostname())+':'+str(port))
        rsp = conn.getresponse()
        data_received = rsp.read()
        data_received = json.loads(data_received)
        leaderAdd = data_received['data']['leader']
        conn.close()
        #Extract the ip address and port of the leader order service
        leaderIP, leaderPort = leaderAdd.split(':')[0], leaderAdd.split(':')[1]
        #Connect to the leader order service
        with grpc.insecure_channel(leaderIP + ':'+str(leaderPort)) as channel:
            stub = stockbazaar_pb2_grpc.OrderStub(channel)
            #Get the address of the replica that needs synchronization
            synchronizedAdd = socket.gethostbyname(socket.gethostname())+':'+str(port)
            #Pass the latest order number and address of the rejoining replica to the leader.
            for transaction in stub.Synchronize(stockbazaar_pb2.synchronizeTransNum(orderNum = transactionNum, synchronizedAdd = synchronizedAdd)):
                #propagate data into local memory
                transactionNum = transaction.orderNum
                transactions[transactionNum]={'name':transaction.stockName,'type':transaction.tradeType,'quantity':transaction.stockTradeQuantity}
                print("Synchronized on Replica " + str(replicaID) + ": "+str({transactionNum:transactions[transactionNum]}))
                #propagate data into the respective database file
                with open('./order'+str(replicaID)+'.txt', 'w') as file:
                     file.write(json.dumps(transactions)) # use `json.loads` to do the reverse
    except ConnectionRefusedError:
        pass
    server.wait_for_termination()


if __name__ == '__main__':
    cataloghost = os.getenv("CATALOG_HOST", socket.gethostbyname(socket.gethostname()))
    logging.basicConfig()
    #Choose and print the unique ID of this order service replica
    print("Unique ID of this order service: " + str(replicaID))
    serve()
