import Pyro4

class Comparator():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.executor = Pyro4.Proxy("PYRONAME:executor")

    def updateWeightage(self, strategy, points):
        # TO-DO: Updates strategy weightage file
        pass
    
    def compare(self, results):
        # TO-DO: Compare results and output final decision
        finalDecision = 1 # Placeholder
        if abs(finalDecision) == 1:
            self.executor.execute(1,1,1,1,1)
        
        