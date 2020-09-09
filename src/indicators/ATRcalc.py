from talib import ATR

import pandas as pd

def ATRcalc(df):
    df = df.dropna()
    ##d. ATR
    priceaction = df.head(15)
    pricehigh = priceaction['high'].values
    pricelow = priceaction['low'].values
    priceclose = priceaction['close'].values
    atr = ATR(pricehigh, pricelow, priceclose, timeperiod=14)
    # print("ATR\n", atr[-1])
    return atr[-1]