import time
import indicators.macdRSI as macdRSI
import indicators.ichimoku200 as ichimoku200
import indicators.ATRcalc as atrCalc

from comparator import Comparator
from analyser import Analyser

class StrategyCalculator():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.comparator = Comparator(self.tickerName)
        self.analyser = Analyser(self.tickerName, self.comparator)
        self.analyser.inform("timeStamp")
    
    def inform(self, timeStamp, df):
        # print("Calculating Strategy for " + str(self.tickerName) + " at " + str(timeStamp) + "...")
        ### TO-DO: Develop strategies to calculate
        #1. Calculate ATR for potential trade

        atr = atrCalc.ATRcalc(df)
        # print("atr\n", atr)

        mrResults = macdRSI.macdRSI(df)
        # print("mrResults\n", mrResults)
        
        if mrResults != 0:
            self.analyser.PseudoTrade(timeStamp, 0, mrResults, atr)
            
        i2Results = ichimoku200.ichimoku200(df)
        # print("i2Results\n", i2Results)
        if i2Results != 0:
            self.analyser.PseudoTrade(timeStamp, 1, i2Results, atr)

        ### END TO-DO
        results = [mrResults, i2Results]
        print("Calculated Strategy for " + str(self.tickerName) + " at " + str(timeStamp))
        self.comparator.compare(results, atr)
        
        