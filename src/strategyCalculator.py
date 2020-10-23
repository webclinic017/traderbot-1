import time

import indicators.indicators as ind

import os.path as path
import pandas as pd
import importlib

from comparator import Comparator
from analyser import Analyser

class StrategyCalculator():
    def __init__(self, tickerName, execType):
        self.tickerName = tickerName
        self.comparator = Comparator(self.tickerName, execType)
        self.analyser = Analyser(self.tickerName, self.comparator, execType)
    
    def inform(self, df, execType):
        # print("Calculating Strategy for " + str(self.tickerName) + " at " + str(timeStamp) + "...")
        ### TO-DO: Develop strategies to calculate
        
        ##
        ## Inform Analyser to do the interval Analysis first
        ## This is before the pseudotrades to ensure no clashes
        self.analyser.intervalAnalysis(df.head(1))
        self.comparator.intervalAnalysis(df.head(1))

        
        indi = ind.Indicator()
        
        Results = indi.beginCalc(df, self.tickerName, execType)

        for i in Results:
            # print('Indicator: ' + i)
            # print('Position: ' + str((Results[i])['position']))
            if (Results[i])["position"] != 0:
                # print("Indicator: " + i + ", Position: " + str((Results[i])["position"]) + ", Confidence: " + str((Results[i])["confidence"]))
                self.analyser.PseudoTrade(df,i, Results[i])

            ### for testing
            # self.analyser.PseudoTrade(df,i, Results[i], atr)
            ###
        ### END TO-DO
        # print("Calculated Strategy for " + str(self.tickerName) + " at " + str(timeStamp))
        self.comparator.compare(Results,df["date"].values[0])
        
        