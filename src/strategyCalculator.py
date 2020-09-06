import Pyro4
import time
@Pyro4.expose
class StrategyCalculator(object):

    @Pyro4.oneway
    def calculateStrategy(self,name,date):
        print("Calculating Strategy for " + name + "...")
        ### INSERT CODE HERE
        
        time.sleep(10)

        ### END INSERT
        print("Calculated Strategy for " + name + "...")

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(StrategyCalculator)   # register the greeting maker as a Pyro object
ns.register("strategy.calculator", uri)   # register the object with a name in the name server

print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls