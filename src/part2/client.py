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
    start_time = time.time()
    for _ in range(1000):
        #Randomly choose to Lookup or Trade
        requestType = random.randint(0,1)
        with grpc.insecure_channel('128.119.243.168:56897') as channel:
            stub = stockbazaar_pb2_grpc.StockBazaarStub(channel)
            #Randomly select which stock to use for this request
            stockName = random.choice(stockNames)
            if requestType == 0:
                print("-------------- Lookup --------------")
                #Send lookup request
                res = stub.Lookup(stockbazaar_pb2.lookupStockName(stockName = stockName))
                if res.stockPrice == -1 and res.tradingVolume == -1:
                    print(stockName + ' not found in lookup.\n')
                else:
                    print("Price of " + stockName + ": " + str(res.stockPrice) + ". \nVolume of " + stockName + ": " + str(res.tradingVolume) + '\n')

            elif requestType == 1:
                print("-------------- Trade --------------")
                #Randomly choose to buy or sell
                tradeTypes = ["Buy", "Sell"]
                tradeType = random.choice(tradeTypes)
                #Randomly select how many stocks to buy sell within range of 1 to 100
                stockQuantity = random.randint(1,100)
                #Send trade request
                res = stub.Trade(stockbazaar_pb2.tradeStockName(stockName = stockName, stockQuantity = stockQuantity, tradeType = tradeType))

                if res.resultTrade == 1:
                    if tradeType == "Buy":
                        print("Successfully bought " + str(stockQuantity) + " " + stockName + " stocks.\n")
                    else:
                        print("Successfully sold " + str(stockQuantity) + " " + stockName + " stocks.\n")
                elif res.resultTrade == -1:
                    print(stockName + ' not found in lookup.\n')
                elif res.resultTrade == 0:
                    print("Trade suspended for " + stockName + ".\n")

    print("Average Latency: " + str((time.time() - start_time)/1000))
if __name__ == '__main__':
    logging.basicConfig()
    run()
