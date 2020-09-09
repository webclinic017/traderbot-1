import Pyro4

class Comparator():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.executor = Pyro4.Proxy("PYRONAME:executor")

    def updateWeightage(self, strategy, points):
        # TO-DO: Updates strategy weightage file
        pass
    
    def compare(self, results, atr):
        # TO-DO: Compare results and output final decision
        if(results[0] != 0 or results[1] != 0):
            self.executor.execute(self.tickerName,results,atr, 1)
        
        