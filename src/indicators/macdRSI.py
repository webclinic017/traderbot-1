from talib import MACDFIX, RSI, EMA

import pandas as pd
def macdRSI(df):
    #####PLACEHOLDER
    # df = pd.read_csv('./database/AAPL.csv')
    #####END_PLACEHOLDER
    df = df.dropna()

    ###1. Getting Parameters
    ##a. RSI
    rsiInput = df.head(15)
    RSIclose = rsiInput['close'].values
    rsi = RSI(RSIclose,timeperiod=14)
    # print("RSI\n", rsi[-1])

    ##b. MACD
    macdInput = df.head(34)
    MACDclose = macdInput['close'].values
    macd, macdsignal, macdhist = MACDFIX(MACDclose, signalperiod = 9)
    # print("MACD\n", macd[-1])
    # print("Signal\n", macdsignal[-1])

    ##c. 200EMA
    emaInput = df.head(200)
    EMAclose = emaInput['close'].values
    ema = EMA(EMAclose, timeperiod=200)

    # print("EMA\n", ema[-1])

    ##d. current price action
    priceaction = df.head(1)
    pricehigh = priceaction['high'].values[0]
    pricelow = priceaction['low'].values[0]
    # print("pricehigh\n", pricehigh)
    # print("pricelow\n", pricelow)


    ###2. Analysing using the data provided

    ##macd-signal crossover type
    ## -1 means negative crossover
    ## 1 means positive crossover
    ## 0 means both
    if macd[-1] > macdsignal[-1]: crossover = 1
    elif macd[-1] < macdsignal[-1]: crossover = -1
    else: crossover = 0

    ##market-ema type
    ## 1 means low > 200EMA
    ## -1 means high < 200EMA
    ## 0 means otherwise

    if pricelow > ema[-1]: marketEMA = 1
    elif pricehigh < ema[-1]: marketEMA = -1
    else: marketEMA = 0



    ##RSI-TYPE
    ##TO-DO


    ##OUTPUT
    if marketEMA == 1 and crossover >= 0: position = 1
    elif marketEMA == -1 and crossover <=0: position = -1
    else: position = 0

    return position
