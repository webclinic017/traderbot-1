import json
import time
import pandas as pd
import numpy as np
from yahooquery import Ticker

start = time.time()
symbol = ['TSLA','AAPL','DOCU']
for i in symbol:
    tickers = Ticker(i)
    df = tickers.history(period='1h', interval='1h')
    df.to_csv('./database/' + i + '.csv')

print(time.time()-start)