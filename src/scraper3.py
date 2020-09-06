import json
import time
import pandas as pd
import numpy as np
from yahooquery import Ticker
import Pyro4


start = time.time()
symbol = ['TSLA','AAPL','DOCU']
strategyCalculator = Pyro4.Proxy("PYRONAME:strategy.calculator")
generationtime = time.time()-start
print("Generation Time:")
print(generationtime)
for i in symbol:
    tickers = Ticker(i)
    df = tickers.history(period='60d', interval='1h')
    df.to_csv('./database/' + i + '.csv')
    print("Calculating " + i)
    strategyCalculator.calculateStrategy(i,1234)
    total = time.time()-start
print("total time elapsed:")
print(total)