import time
import indicators.macdRSI as macdRSI
import indicators.ichimoku200 as ichimoku200

from comparator import Comparator
from analyser import Analyser

class StrategyCalculator():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.comparator = Comparator(self.tickerName)
        self.analyser = Analyser(self.tickerName, self.comparator)
        self.analyser.inform("timeStamp")
    
    def inform(self, timeStamp):
        print("Calculating Strategy for " + str(self.tickerName) + " at " + str(timeStamp) + "...")
        ### TO-DO: Develop strategies to calculate
        mrResults = macdRSI.macdRSI()
        
        ''' if mrResults[0] != 0:
            self.analyser.PseudoTrade(timeStamp, 0) '''
            
        i2Results = ichimoku200.ichimoku200()
        
        ''' if i2Results[0] != 0:
            self.analyser.PseudoTrade(timeStamp, 1) '''

        ### END TO-DO
        results = [mrResults, i2Results]
        self.comparator.compare(results)
        print("Calculated Strategy for " + str(self.tickerName) + " at " + str(timeStamp))
        