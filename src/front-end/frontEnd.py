from concurrent.futures import ThreadPoolExecutor
from socketserver import ThreadingMixIn

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

import socket
import grpc
import stockbazaar_pb2
import stockbazaar_pb2_grpc

class StockHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with grpc.insecure_channel(cataloghost + ':56892') as channel:
            stub = stockbazaar_pb2_grpc.CatalogStub(channel)
            #Extract the name of the stock from the HTTP request
            stockName = self.path.split('/')[2]
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
                response['data']=data

            json_data = json.dumps(response)
            #send header first
            self.send_header("Connection", "keep-alive")
            self.send_header("Content-Length", str(len(bytes(json_data, 'utf-8'))))
            self.end_headers()

            self.wfile.write(json_data.encode())
        return

    def do_POST(self):
        with grpc.insecure_channel(orderhost + ':56891') as channel:
            stub = stockbazaar_pb2_grpc.OrderStub(channel)
            #Read input json
            content_length = int(self.headers['Content-Length'])
            inputData = self.rfile.read(content_length)
            #Convert bytes to a dict object
            inputData = json.loads(inputData)
            stockName = inputData['name']

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
    print("Server started on: " + socket.gethostbyname(socket.gethostname())+':56893')
    #Define the pooled http server.
    class PoolHTTPServer(PoolMixIn, HTTPServer):
        pool = ThreadPoolExecutor(max_workers=5)

    server = PoolHTTPServer((socket.gethostbyname(socket.gethostname()), 56893), StockHTTPRequestHandler)
    print('http server is running...')
    server.serve_forever()

if __name__=="__main__":
    cataloghost = os.getenv("CATALOG_HOST", socket.gethostbyname(socket.gethostname()))
    orderhost = os.getenv("ORDER_HOST", socket.gethostbyname(socket.gethostname()))
    run()
