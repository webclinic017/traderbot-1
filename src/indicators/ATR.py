from talib import ATR

import pandas as pd

def ATR(df):
    #####PLACEHOLDER
    df = pd.read_csv('./database/AAPL.csv')
    #####END_PLACEHOLDER
    df = df.dropna()
    ##d. ATR
    priceaction = df.iloc[::-1].head(15)
    pricehigh = priceaction['high'].values
    pricelow = priceaction['low'].values
    priceclose = priceaction['close'].values
    atr = ATR(pricehigh, pricelow, priceclose)
    print("ATR\n", atr[-1])
    return atr[-1]