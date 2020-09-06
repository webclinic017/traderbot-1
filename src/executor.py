import Pyro4

class Executor():
    def __init__(self):
        pass
    
    @Pyro4.expose
    @Pyro4.oneway
    def execute(self, buySell, amount, stopLoss, takeProfit, leverage):
        print("lelolulalil")
        

### MAIN CODE EXECUTION

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(Executor)   # register the greeting maker as a Pyro object
ns.register("executor", uri)
print("Server Created.")
daemon.requestLoop()