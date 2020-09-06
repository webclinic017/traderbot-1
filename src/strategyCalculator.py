import Pyro4
import time
import indicators.macdRSI as macdRSI
import indicators.ichimoku200 as ichimoku200


@Pyro4.expose
class StrategyCalculator(object):

    @Pyro4.oneway
    def inform(self,tickerName,timeStamp):
        print("Calculating Strategy for " + tickerName + " at " + timeStamp + "...")
        ### INSERT CODE HERE
        mrResults = macdRSI.macdRSI()
        if mrResults[0] != 0:
            analyser.PseudoTrade(tickerName, timeStamp, 0)
        i2Results = ichimoku200.ichimoku200()

        ### END INSERT
        print("Calculated Strategy for " + tickerName + " at " + timeStamp + "...")

#SETTING UP OWN SERVER
daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(StrategyCalculator)   # register the greeting maker as a Pyro object
ns.register("strategy.calculator", uri)   # register the object with a name in the name server
print("Server Created.")
#CONNECTING TO ANALYSER
analyser = Pyro4.Proxy("PYRONAME:analyser")
print("Connected to Analyser.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls