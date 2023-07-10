import socket
from queue import Queue
from threading import Thread
import threading

#Dict mapping company names to their respective stock price
stockPrices = {}
stockPrices["GameStart"] = 15.99
stockPrices["FishCo"] = 25.47

#Query returns the price of the meme stock (as a floating-point value, such as 15.99). It returns -1 if the company name is not found
def Lookup(companyName):
    return stockPrices.get(companyName, -1)

#Worker class on which the threads act upon
class Worker(Thread):
    def __init__(self, requests):
        Thread.__init__(self)
        #Requests stack contains a stack of (connection, address) tuples
        self.requests = requests
        self.daemon = True
        #Start the worker/thread
        self.start()

    def run(self):
        while True:
            connection, address = self.requests.get()
            try:
                while True:
                    #Receive the request from the client
                    request = connection.recv(1024).decode()
                    #Split the request string based on space s.t. we are able to extract the desired function and corresponding arguement
                    func = request.split()[0]
                    arg = request.split()[1]
                    #From the string naming the desired function eval s.t. we call the corresponding function
                    res = eval(func)(arg)
                    if res == -1:
                        message = "Could not find price for " + arg
                    else:
                        message = "Price of " + arg + ": " + str(res)
                    connection.send(message.encode())
            except Exception as e:
                continue
            finally:
                #Close the connection
                connection.close()


class ThreadPool:
    #Create threadpool of size numThreads
    def __init__(self, numThreads):
        self.requests = Queue(numThreads)
        #Create workers equal to the number of threads
        for x in range(numThreads):
            Worker(self.requests)
    #Handle client request by adding the client connection information to the threadpool
    def handle_request(self, connectionAddress):
        self.requests.put(connectionAddress)

if __name__ == '__main__':
    s = socket.socket()
    port = 56897  # Specify the port to connect to
    host = "128.119.243.168"
    print(socket.gethostbyname(socket.gethostname()))
    s.bind((socket.gethostbyname(socket.gethostname()), port))  # Bind to the port
    #Create threadpool with n number of threads
    var = input("Desired number of threads in pool: ")
    pool = ThreadPool(int(var))
    #Accept up to 10 clients
    s.listen(10)  # Now wait for client connection
    while True:
        c, addr = s.accept()  # Establish connection with client
        print(f"Connection from {addr} has been established.")
        #c.send(b"Thank you for connecting")

        pool.handle_request((c, addr)) #Add current connection information to the thread pool
    s.close()  # Close the connection
