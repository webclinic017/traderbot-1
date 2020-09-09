import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import os.path as path
from yahooquery import Ticker
from strategyCalculator import StrategyCalculator


class Scraper():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.stratCalc = StrategyCalculator(self.tickerName)
    
    def update(self):
        while True:
            self.scrape()
            t = datetime.utcnow()
            sleeptime = 60 - (t.second + t.microsecond/1000000.0)
            time.sleep(sleeptime)

            

    def scrape(self):
        
        tickers = Ticker(self.tickerName)
        df = tickers.history(period='7d', interval='1m')
        df = df.iloc[::-1]
        dfFirstTwoRows = df.head(2)
        dfSecondRow = dfFirstTwoRows.iloc[1:].head(1)
        dflow = dfSecondRow['low'].values
        dflow2 = round(dflow[0],5)
        dfhigh = dfSecondRow['high'].values
        dfhigh2 = round(dfhigh[0],5)

        if path.exists('./database/' + self.tickerName + '.csv'):
            database = pd.read_csv('./database/' + self.tickerName + '.csv')
            databaseFirstTwoRow = database.head(2)
            databaseSecondRow = databaseFirstTwoRow.iloc[1:].head(1)
            dblow = databaseSecondRow['low'].values
            dblow2 = round(dblow[0],5)
            dbhigh = databaseSecondRow['high'].values
            dbhigh2 = round(dbhigh[0],5)

            if  dbhigh2 == dfhigh2 and dblow2 == dflow2:
                pass
            else:
                print("Updating " + self.tickerName + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
                df.to_csv('./database/' + self.tickerName + '.csv')
                self.stratCalc.inform("timeStamp",df.iloc[1:])
        else:
            print("Updating " + self.tickerName + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
            df.to_csv('./database/' + self.tickerName + '.csv')
            self.stratCalc.inform("timeStamp",df.iloc[1:])

        
        
        
    
