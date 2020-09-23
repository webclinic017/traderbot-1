import pandas as pd
from talib import MACDFIX, RSI, EMA, SAR, SMA, TRIX
import indicators.ATRcalc as atrcalc
import os
#1. Calculate ATR for potential trade
#####PLACEHOLDER
df = pd.read_csv('./database/AAPL/temp2.csv')
#####END_PLACEHOLDER
#1. Calculate ATR for potential trade
#####PLACEHOLDER
# df = pd.read_csv('./database/AAPL.csv')
#####END_PLACEHOLDER
df = df.dropna()

#1. Calculate ATR for potential trade
atr = atrcalc.ATRcalc(df)

trixInput = df.head(60)
trixInput = trixInput.iloc[::-1]
trixOutput = TRIX(trixInput['close'].values, timeperiod = 14)

##c. 200EMA
emaInput = df.head(200)
emaInput = emaInput.iloc[::-1]
EMAclose = emaInput['close'].values
ema = EMA(EMAclose, timeperiod=200)

# print("EMA\n", ema[-1])

##d. current price action
priceaction = df.head(1)
pricehigh = priceaction['high'].values[0]
pricelow = priceaction['low'].values[0]
priceclose = priceaction['close'].values[0]
# print("pricehigh\n", pricehigh)
# print("pricelow\n", pricelow)

if trixOutput[-2] < 0 and trixOutput[-1] > 0:
    crossover = 1
elif trixOutput[-2] > 0 and trixOutput[-1] < 0:
    crossover = -1
else: crossover = 0


if pricelow > ema[-1]: marketEMA = 1
elif pricehigh < ema[-1]: marketEMA = -1
else: marketEMA = 0

##OUTPUT
if marketEMA == 1 and crossover > 0: position = 1
elif marketEMA == -1 and crossover < 0: position = -1
else: position = 0

if position == 1:
    stoploss = priceclose - 1.05 * atr
    takeprofit = priceclose + 1.45 * atr
    amount = priceclose / (priceclose - stoploss)
elif position == -1:
    stoploss = priceclose + 1.05*atr
    takeprofit = priceclose - 1.45 * atr
    amount = priceclose / (stoploss - priceclose)
else:
    stoploss = 0
    takeprofit = 0
    amount = 0

##For test
# position = 1