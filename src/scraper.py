import json
import time
import pandas as pd
import numpy as np
from yahooquery import Ticker
from strategyCalculator import StrategyCalculator

class Scraper():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.stratCalc = StrategyCalculator(self.tickerName)
    
    def update(self):
        while True:
            self.scrape()
            time.sleep(10)
            

    def scrape(self):
        print("Scraping " + self.tickerName)
        
        tickers = Ticker(self.tickerName)
        df = tickers.history(period='60d', interval='1h')
        ##############################
        # 2. TO-DO: CREATE A CODE HERE THAT EXITS THE LOOP IF LAST ROW OF DF = LAST ROW OF DATABASE
        ##############################
        
        df.to_csv('./database/' + self.tickerName + '.csv')
        
        self.stratCalc.inform("timeStamp")
        
        
    
