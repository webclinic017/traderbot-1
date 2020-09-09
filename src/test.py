import time
from yahooquery import Ticker
import pandas as pd
import os.path as path
from datetime import datetime

print("Scraping " + "AAPL" + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
        
tickers = Ticker("AAPL")
df = tickers.history(period='7d', interval='1m')
df = df[::-1]
dfFirstTwoRows = df.head(2)
dfSecondRow = dfFirstTwoRows.iloc[1:].head(1)
dflow = dfSecondRow['low'].values
dflow2 = round(dflow[0],5)
dfhigh = dfSecondRow['high'].values
dfhigh2 = round(dfhigh[0],5)


if path.exists('./database/' + 'AAPL' + '.csv'):
    database = pd.read_csv('./database/' + 'AAPL' + '.csv')
    databaseFirstTwoRow = database.head(2)
    databaseSecondRow = databaseFirstTwoRow.iloc[1:].head(1)
    dblow = databaseSecondRow['low'].values
    dblow2 = round(dblow[0],5)
    dbhigh = databaseSecondRow['high'].values
    dbhigh2 = round(dbhigh[0],5)

    if  dbhigh2 == dfhigh2 and dblow2 == dflow2:
        print("1")
        pass
    else:
        print("updating database")
        # df.to_csv('./database/' + self.tickerName + '.csv')
        # self.stratCalc.inform("timeStamp",df)
else:
    print("creating database")
    # df.to_csv('./database/' + self.tickerName + '.csv')
    # self.stratCalc.inform("timeStamp",df)