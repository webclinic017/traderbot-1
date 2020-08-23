import os
import json
import pandas as pd
import numpy as np
from yahooquery import Ticker

''' aapl = Ticker('aapl')
print(aapl.summary_detail) '''

tickers = Ticker('fb')
df = tickers.history(period='2y', interval='1d')

# ['adjclose', 'close', 'high', 'low', 'open', 'volume']
df = df.reindex(sorted(df.columns), axis=1)

df['10ma'] = df.iloc[:,1].rolling(window=10).mean()
df['20ma'] = df.iloc[:,1].rolling(window=20).mean()
df['50ma'] = df.iloc[:,1].rolling(window=50).mean()
df['200ma'] = df.iloc[:,1].rolling(window=200).mean()

print(df.columns)
print(df)

''' with open(os.path.dirname(__file__)+"query.json", "r+") as file:
    data = json.load(file)
    data.update(aapl.summary_detail)
    file.seek(0)
    json.dump(data, file)
 '''