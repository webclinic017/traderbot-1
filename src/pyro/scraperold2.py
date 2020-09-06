import json
import time
import pandas as pd
import numpy as np
from yahooquery import Ticker
import Pyro4

start = time.time()
#############################################
# 1. REPLACE THIS STATIC SYMBOL LIST WITH ONE THAT READS A CSV FILE FOR THE SYMBOLS
USsymbol = ['TSLA','AAPL','DOCU']
UKsymbol = []
ASIAsymbol = []
############################################

strategyCalculator = Pyro4.Proxy("PYRONAME:strategy.calculator")
generationtime = time.time()-start
print("Fetching Data from US Stocks")
for i in USsymbol:
    tickers = Ticker(i)
    df = tickers.history(period='60d', interval='1h')
    ##############################
    # 2. CREATE A CODE HERE THAT EXITS THE LOOP IF LAST ROW OF DF = LAST ROW OF DATABASE
    ##############################
    df.to_csv('./database/' + i + '.csv')
    print("Calculating " + i)
    strategyCalculator.inform(i,1234)

print("Fetching Data from UK Stocks")
for i in UKsymbol:
    tickers = Ticker(i)
    df = tickers.history(period='60d', interval='1h')
    ##############################
    # 3. CREATE A CODE HERE THAT EXITS THE LOOP IF LAST ROW OF DF = LAST ROW OF DATABASE
    ##############################
    df.to_csv('./database/' + i + '.csv')
    print("Calculating " + i)
    strategyCalculator.inform(i,1234)

print("Fetching Data from ASIA Stocks")
for i in ASIAsymbol:
    tickers = Ticker(i)
    df = tickers.history(period='60d', interval='1h')
    ##############################
    # 4. CREATE A CODE HERE THAT EXITS THE LOOP IF LAST ROW OF DF = LAST ROW OF DATABASE
    ##############################
    df.to_csv('./database/' + i + '.csv')
    print("Calculating " + i)
    strategyCalculator.inform(i,1234)

total = time.time()-start
print("total time elapsed:")
print(total)