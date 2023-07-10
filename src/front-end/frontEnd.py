from concurrent.futures import ThreadPoolExecutor
from socketserver import ThreadingMixIn
from threading import Lock

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json
import sys

import socket
import grpc
import stockbazaar_pb2
import stockbazaar_pb2_grpc

from grpc._channel import _InactiveRpcError
import time

#Read ID numbers and address of replica 1
oneOrderID = sys.argv[1]
oneOrderAdd = sys.argv[2]
#Read ID numbers and address of replica 2
twoOrderID = sys.argv[3]
twoOrderAdd = sys.argv[4]
#Read ID numbers and address of replica 3
threeOrderID = sys.argv[5]
threeOrderAdd = sys.argv[6]
#Determine if cache should be off/on 0/1 respectively.
cache = int(sys.argv[7])

#Map replicas to a dict
replicas = {oneOrderID:oneOrderAdd,twoOrderID:twoOrderAdd,threeOrderID:threeOrderAdd}
#Create Lock
lock = Lock()



def ping(ipAdd,port):
    #First check to see if the given addres and port even has an existing gRPC server
    try:
        channel = grpc.insecure_channel(str(ipAdd) + ':'+str(port))
        #If the server exists at the address, check if the server is responsive
        try:
            grpc.channel_ready_future(channel).result(timeout=5)
            channel.close()
            return True
        except grpc.FutureTimeoutError:
            print(" Connection to "+str(ipAdd)+":"+str(port) + " timed out.")
            channel.close()
            return False
    except grpc._channel._InactiveRpcError:
        print(" Address does not exist "+str(ipAdd)+":"+str(port))
        return False

def leaderElection(replicas, currLeaderID):
    #Sort replica ID numbers from largest to smallest
    replicaIDs = list(replicas.keys())
    replicaIDs.sort(reverse=True)
    #Iterate down through list of replica ID numbers
    for x in range(0,len(replicaIDs)):
        leader = replicaIDs[x]
        #If currLeaderID=-1, which means a leader has not been elected, then the if statement will never be called
        if leader == currLeaderID:
            continue
        else:
            currReplicaIP = replicas[leader].split(':')[0]
            currReplicaPort = replicas[leader].split(':')[1]
            #If leader is able to be succesfully pinged
            if ping(currReplicaIP, currReplicaPort):
                #Once we have determined who the leader is, we assign their followers by sending their followers in the following format "ip_address:port"
                with grpc.insecure_channel(currReplicaIP + ':' +str(currReplicaPort)) as channel:
                    stub = stockbazaar_pb2_grpc.OrderStub(channel)
                    #If the leader is the largest ID, then the two smaller ID's will be the followers
                    if x == 0:
                        followerOne, followerTwo = replicas[replicaIDs[x+1]], replicas[replicaIDs[x+2]]
                    #If the leader is the second largest ID, the the smallest ID will be the follower. (We assume that the second largest ID will only ever be the leader when the largest ID cannot be reached)
                    elif x == 1:
                        followerOne, followerTwo = replicas[replicaIDs[x+1]], ""
                    #If the leader is the third largest ID, we assume that both the largest and second largest IDs cannot be reached and as such no followers
                    else:
                        followerOne, followerTwo = "", ""
                    res = stub.AssignFollowers(stockbazaar_pb2.followersAssigned(followerOne = followerOne, followerTwo = followerTwo))
                return leader, currReplicaIP, currReplicaPort


class StockHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global orderhost
        global orderport
        global currLeaderID
        global cachedStockData
        #Extract GET request type i.e. /REQUEST/<input> we extract "REQUEST"
        type = self.path.split('/')[1]
        if type == 'stocks':
            #Extract the name of the stock from the HTTP request
            stockName = self.path.split('/')[2]
            #First check local cache to see if the stock is present
            if len(cachedStockData.get(stockName, {})) > 0:
                cachedStock = cachedStockData.get(stockName, {})
                #send code 200 response
                self.send_response(200)
                response = {}
                data = {'name':stockName,'price':cachedStock['price'] ,'quantity':cachedStock['quantity']}
                response['data']=data
            #If the stock is not located in the cache, query the catalog service
            else:
                with grpc.insecure_channel(cataloghost + ':56892') as channel:
                    stub = stockbazaar_pb2_grpc.CatalogStub(channel)
                    res = stub.Lookup(stockbazaar_pb2.lookupStockName(stockName = stockName))
                    if res.stockPrice == -1 and res.stockQuantity == -1:
                        #send code 404 response
                        self.send_response(404)
                        response = {}
                        error = {'code':404,'message':"stock not found"}
                        response['error']=error
                    else:
                        #send code 200 response
                        self.send_response(200)
                        response = {}
                        data = {'name':stockName,'price':round(res.stockPrice,2) ,'quantity':res.stockQuantity}
                        if cache == 1:
                            #Add the retrieved data to the local cache
                            cachedStockData[stockName] = {'price':round(res.stockPrice,2) ,'quantity':res.stockQuantity}
                        response['data']=data

        elif type == 'orders':
            #Extract the order num of the stock from the HTTP request
            orderNum = self.path.split('/')[2]
            orderNum = int(orderNum)
            def getorders():
                with grpc.insecure_channel(orderhost + ':' + str(orderport)) as channel:
                    stub = stockbazaar_pb2_grpc.OrderStub(channel)
                    res = stub.Lookup(stockbazaar_pb2.lookupOrderNum(orderNum = orderNum))
                    if res.orderNum == -1:
                        #send code 404 response
                        self.send_response(404)
                        response = {}
                        error = {'code':404,'message':"transaction not found"}
                        response['error']=error
                    else:
                        #send code 200 response
                        self.send_response(200)
                        response = {}
                        data = {'number':res.orderNum,'name':res.stockName,'type':res.tradeType,'quantity':res.stockTradeQuantity}
                        response['data']=data
                return response

            with lock:
                try:
                    response = getorders()
                #If the current order service replica crashes/timesout, elect a new leader, and execute the GET request with a connection to the new leader
                except grpc._channel._InactiveRpcError:
                    print("OLD LEADER REMOVED DURING GET /ORDERS/: " + str(currLeaderID), end = '')
                    currLeaderID, orderhost, orderport = leaderElection(replicas, currLeaderID)
                    print("/NEW LEADER ELECTED DURING GET /ORDERS/: " + str(currLeaderID))
                    response = getorders()

        elif type == 'cache':
            #Extract the name of the stock from the HTTP request
            stockName = self.path.split('/')[2]
            if cache == 1:
                #On successful trade, we must remove the stock with given stock name from the local cache
                cachedStockData.pop(stockName, None)
            #send code 200 response
            self.send_response(200)
            response = {}
            data = {}
            response['data']=data


        elif type == 'leader':
            #send code 200 response
            self.send_response(200)
            response = {}
            data = {'leader':replicas[currLeaderID]}
            response['data']=data


        json_data = json.dumps(response)
        #send header first
        self.send_header("Connection", "keep-alive")
        self.send_header("Content-Length", str(len(bytes(json_data, 'utf-8'))))
        self.end_headers()

        self.wfile.write(json_data.encode())
        return

    def do_POST(self):
        global orderhost
        global orderport
        global currLeaderID

        #Read input json
        content_length = int(self.headers['Content-Length'])
        inputData = self.rfile.read(content_length)
        #Convert bytes to a dict object
        inputData = json.loads(inputData)
        stockName = inputData['name']

        def post():
            with grpc.insecure_channel(orderhost + ':' + str(orderport)) as channel:
                stub = stockbazaar_pb2_grpc.OrderStub(channel)
                res = stub.Request(stockbazaar_pb2.requestStockName(stockName = stockName, stockTradeQuantity = inputData['quantity'], tradeType = inputData['type']))
                res = res.transactionNum
                #Stock not found
                if res == -1:
                    #send code 404 response
                    self.send_response(404)
                    response = {}
                    error = {'code':404,'message':"stock not found"}
                    response['error']=error
                #Invalid request i.e. not "buy" or "sell"
                elif res == -2:
                    #send code 400 response
                    self.send_response(400)
                    response = {}
                    error = {'code':400,'message':"invalid request type"}
                    response['error']=error
                #Trying to buy or sell an invalid number of stocks
                elif res == -3:
                    #send code 400 response
                    self.send_response(400)
                    response = {}
                    error = {'code':404,'message':"invalid number of stocks"}
                    response['error']=error
                #Trying to buy more stocks than available
                elif res == -4:
                    #send code 400 response
                    self.send_response(400)
                    response = {}
                    error = {'code':404,'message':"not enough stocks available to buy"}
                    response['error']=error
                else:
                    #send code 200 response
                    self.send_response(200)
                    response = {}
                    data = {'transaction_number':res}
                    response['data']=data
            return response

        with lock:
            try:
                response = post()
            #If the current order service replica crashes/timesout, elect a new leader, and execute the POST request with a connection to the new leader
            except grpc._channel._InactiveRpcError:
                print("OLD LEADER REMOVED DURING POST: " + str(currLeaderID), end = '')
                currLeaderID, orderhost, orderport = leaderElection(replicas, currLeaderID)
                print("/NEW LEADER ELECTED DURING POST: " + str(currLeaderID))
                response = post()

        json_data = json.dumps(response)
        #send header first
        self.send_header("Connection", "keep-alive")
        self.send_header("Content-Length", str(len(bytes(json_data, 'utf-8'))))
        self.end_headers()
        self.wfile.write(json_data.encode())
        return

#Create pool mix in that allows for requests to be submitted to pool.
class PoolMixIn(ThreadingMixIn):
    def process_request(self, request, client_address):
        self.pool.submit(self.process_request_thread, request, client_address)

def run():
    print('http server is starting...')
    print("Front-end server started on: " + socket.gethostbyname(socket.gethostname())+':56893')
    #Define the pooled http server.
    class PoolHTTPServer(PoolMixIn, HTTPServer):
        pool = ThreadPoolExecutor(max_workers=10)

    server = PoolHTTPServer((socket.gethostbyname(socket.gethostname()), 56893), StockHTTPRequestHandler)
    print('http server is running...')
    server.serve_forever()

if __name__=="__main__":
    cataloghost = os.getenv("CATALOG_HOST", socket.gethostbyname(socket.gethostname()))
    orderhost = os.getenv("ORDER_HOST", socket.gethostbyname(socket.gethostname()))
    #Create local cache
    cachedStockData = {}
    #Perform leader election for order service replicas
    currLeaderID = -1
    currLeaderID, orderhost, orderport = leaderElection(replicas, currLeaderID)
    run()
