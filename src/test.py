import pandas as pd
from yahooquery import Ticker

tickers = Ticker('AAPL')
df = tickers.history(period='7d', interval='1m')
df = df.iloc[::-1]
df = df.head(2)
print(df)
# a = df['date'].values(0)
df.to_csv('./database/' + 'AAPL' + '/temp.csv')
df = pd.read_csv('./database/' + 'AAPL' + '/temp.csv')
print(df)
a = df['date'][0]
print(a)

