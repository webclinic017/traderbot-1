import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import os
from yahooquery import Ticker
from strategyCalculator import StrategyCalculator
from progressReport import progressReport as pr
import math

TickerNames = pd.read_csv('./src/tickerNames/TickerNames.csv')
    
TickerNames = TickerNames.values

class backTestFn():
    def __init__(self, tickerName, sema):
        self.tickerName = tickerName
        self.stratCalc = StrategyCalculator(self.tickerName,0)
        self.update(sema)

    def update(self, sema):
        stratCalc = StrategyCalculator(self.tickerName,0)
        df = pd.read_csv('./database/' + self.tickerName + '/temp.csv')
        # df = df.iloc[::-1]

        counter = 0
        totalCounter = len(df.index) - 200

        endOfBacktest = False
        oldprogress = 0
        while endOfBacktest == False:
            
            inputt = df
            inputt = inputt.head(201)
            inputt = inputt.iloc[::-1]
            
            stratCalc.inform(df=inputt, 0)
            df = df.iloc[1:]
            if len(df.index) < 201:
                endOfBacktest = True
            counter += 1
            newprogress = math.floor(counter / totalCounter * 100)
            if oldprogress != newprogress:
                print(self.tickerName + ": " + str(newprogress) + "%")
                oldprogress = newprogress
        
        sema.release()