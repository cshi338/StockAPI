from __future__ import print_function

import logging
import random
import time

import grpc
import stockbazaar_pb2
import stockbazaar_pb2_grpc

def run():
    #Create list of stock names including one fake stock
    stockNames = ['GameStart','FishCo','BoarCo','MenhirCo','Apple']
    for _ in range(1000):
        with grpc.insecure_channel('128.119.243.168:56897') as channel:
            stub = stockbazaar_pb2_grpc.StockBazaarStub(channel)
            #Randomly select which stock to use for this request
            stockName = random.choice(stockNames)
            print("-------------- Update --------------")
            #Choose a random stock price from -10.0-100.0 and round to 2 decimal places
            updatePrice = round(random.uniform(-10.0,100.0),2)
            #Send update request
            res = stub.Update(stockbazaar_pb2.updateStockName(stockName = stockName, stockPrice = updatePrice))
            if res.resultUpdate == 1:
                print("Successfully updated " + stockName + " price to " + str(updatePrice) + ".")
            elif res.resultUpdate == -2:
                print("Unsuccessfully updated " + stockName + " price to " + str(updatePrice) + ". \nReason: Invalid stock Price.")
            elif res.resultUpdate == -1:
                print(stockName + ' not found in lookup.')
        #Randomly sleep for 0.0-3.0 seconds
        sleepTime = round(random.uniform(0.0,3.0),2)
        print("------- Waiting " + str(sleepTime) + " Seconds -------\n")
        time.sleep(sleepTime)
if __name__ == '__main__':
    logging.basicConfig()
    run()
