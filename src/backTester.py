import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import os
from yahooquery import Ticker
from strategyCalculator import StrategyCalculator
from progressReport import progressReport as pr

TickerNames = pd.read_csv('./src/tickerNames/TickerNames.csv')
    
TickerNames = TickerNames.values

for i in TickerNames:
    stratCalc = StrategyCalculator(i[0])
    tickers = Ticker(i[0])
    df = tickers.history(period='max', interval='1d')
    # df = df.iloc[::-1]
    endOfBacktest = False
    
    while endOfBacktest == False:
        if os.path.exists('./database/' + i[0]):
            initialbool = False
            if initialbool == False:
                df.to_csv('./database/' + i[0] + '/temp.csv')
                df = pd.read_csv('./database/' + i[0] + '/temp.csv', index_col=0)
                initialbool = True            
            inputt = df
            inputt = inputt.head(201)
            inputt = inputt.iloc[::-1]
            stratCalc.inform(df=inputt)
            df = df.iloc[1:]
            if len(df.index) < 201:
                endOfBacktest = True
        else:
            print("Creating and Updating " + i[0] + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
            os.makedirs('./database/' + i[0] + '/')
            analysisColumnNames = ['Time Stamp', 'Strategy', 'Position', 'Amount', 'Entry', 'Stop Loss', 'Take Profit', 'Confidence', 'Outcome', 'Profits', 'Points Gained/Lost']
            analysisFrame = pd.DataFrame(columns=analysisColumnNames)
            analysisFrame.to_csv('./database/' + i[0] + '/analysis.csv')
            tradeColumnNames = ['Time Stamp', 'Position', 'Amount', 'Entry', 'Stop Loss', 'Target', 'Confidence', 'Leverage', 'Outcome', 'Profits']
            tradeFrame = pd.DataFrame(columns=tradeColumnNames)
            tradeFrame.to_csv('./database/' + i[0] + '/trades.csv')
            df.to_csv('./database/' + i[0] + '/temp.csv')
            df = pd.read_csv('./database/' + i[0] + '/temp.csv')