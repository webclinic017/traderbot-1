import Pyro4

@Pyro4.expose
class Analyser(object):
    
    @Pyro4.oneway
    def PseudoTrade(self,TickerName,timeStamp,strategy):
        print("Adding pseudo trade for " + TickerName + " at " + timeStamp + " (" + strategy + ")")
        ### Save information into a CSV database full of pseudotrades

    @Pyro4.oneway
    def intervalAnalysis(self):
        a = 1


### MAIN CODE EXECUTION
daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(Analyser)   # register the greeting maker as a Pyro object
ns.register("analyser", uri)
print("Server Created.")
Comparator = Pyro4.Proxy("PYRONAME:comparator")
print("Connected to Analyser.")
daemon.requestLoop()