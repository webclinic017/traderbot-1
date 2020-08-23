import json
import time
import pandas as pd
import numpy as np
from yahooquery import Ticker

start = time.time()

tickers = Ticker('fb')
df = tickers.history(period='2y', interval='1d')

# Columns: ['adjclose', 'close', 'high', 'low', 'open', 'volume']
df = df.reindex(sorted(df.columns), axis=1)

# Moving averages
df['10ma'] = df.iloc[:,1].rolling(window=10).mean()
df['20ma'] = df.iloc[:,1].rolling(window=20).mean()
df['50ma'] = df.iloc[:,1].rolling(window=50).mean()
df['200ma'] = df.iloc[:,1].rolling(window=200).mean()
df['grad10'] = df['10ma'].diff(periods=2)/2

# Average true range
df['tr0'] = abs(df['high']-df['low'])
df['tr1'] = abs(df['high']-df['close'].shift())
df['tr2'] = abs(df['low']-df['close'].shift())
df['tr'] = df[['tr0', 'tr1', 'tr2']].max(axis=1)
df['atr'] = df.iloc[:,14].rolling(window=14).mean()

# Chaikin money flow
df['mf0'] = df['close']-df['low']
df['mf1'] = df['high']-df['close']
df['mf'] = (df['mf0']-df['mf1'])/df['tr0']*df['volume']
df['vsum'] = df.iloc[:,5].rolling(window=21).sum()
df['cmf'] = df.iloc[:,18].rolling(window=21).sum()/df['vsum']

# Calculated stop loss
x = 1
df['csl'] = df['close']-(df['atr']*x)
df['usl'] = df['csl']

for i in range(1, len(df)):
    if (df.iloc[i, 1] < df.iloc[i, 6]) or i == 0:
        continue
        
    else:
        df.iloc[i, 22] = df.iloc[i-1, 22]

print(time.time()-start)
print(df.columns)
print(df)

df.to_csv(r'fb.csv')