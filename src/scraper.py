import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import os
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
            print(str(sleeptime) + " Seconds to next scrape")
            time.sleep(sleeptime + 2)
            print("Starting Next Scrape")

            

    def scrape(self):

        tickers = Ticker(self.tickerName)
        df = tickers.history(period='7d', interval='1m')
        df = df.iloc[::-1]
        

        if os.path.exists('./database/' + self.tickerName):

            ## This saving then re-reading is necessary to prevent the buggy header issues
            df.to_csv('./database/' + self.tickerName + '/temp.csv')
            df = pd.read_csv('./database/' + self.tickerName + '/temp.csv')
            ###########################
            dfFirstTwoRows = df.head(2)
            dfSecondRow = dfFirstTwoRows.iloc[1:].head(1)
            dfDate = dfSecondRow['date'].values[0]
            print("DfDate = " + str(dfDate))

            database = pd.read_csv('./database/' + self.tickerName + '/query.csv', index_col=0)
            databaseFirstTwoRow = database.head(2)
            databaseSecondRow = databaseFirstTwoRow.iloc[1:].head(1)
            dbDate = databaseSecondRow['date'].values[0]
            print("DbDate = " + dbDate)

            if not (dbDate == dfDate):
                print("Updating " + self.tickerName + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
                df.to_csv('./database/' + self.tickerName + '/query.csv')
                self.stratCalc.inform(df.iloc[1:])
        else:
            print("Creating and Updating " + self.tickerName + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
            os.makedirs('./database/' + self.tickerName + '/')
            columnNames = ['Time Stamp', 'Strategy', 'Position', 'Stop Loss', 'Take Profit', 'Outcome', 'Points Gained/Lost']
            frame = pd.DataFrame(columns=columnNames)
            frame.to_csv('./database/' + self.tickerName + '/analysis.csv')
            df.to_csv('./database/' + self.tickerName + '/query.csv')
            df.to_csv('./database/' + self.tickerName + '/temp.csv')
            df = pd.read_csv('./database/' + self.tickerName + '/temp.csv')        
            self.stratCalc.inform(df.iloc[1:])

        
        
        
    
