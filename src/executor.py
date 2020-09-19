import Pyro4
from datetime import datetime
import time

## RUN THIS FIRST on command line
## for namespace
## pyro4-ns [options]
 ##


class Executor():
    def __init__(self):
        pass
    
    @Pyro4.expose
    @Pyro4.oneway
    def execute(self, tickerName, buySell, amount, stopLoss, takeProfit, leverage):
        
        print("(" + datetime.fromtimestamp(time.time()).strftime('%H:%M') + ") " + "Executed " + str(buySell) + " " + tickerName + " for $" + str(amount) + " at x" + str(leverage) + " leverage. Stop Loss = " + str(stopLoss) + ", Take Profit = " + str(takeProfit) + ".")


### MAIN CODE EXECUTION
Pyro4.config.MAX_RETRIES = 200
Pyro4.config.THREADPOOL_SIZE = 3000

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(Executor)   # register the greeting maker as a Pyro object
ns.register("executor", uri)
print("Server Created.")
daemon.requestLoop()