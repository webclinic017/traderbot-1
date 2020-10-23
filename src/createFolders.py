import json
import time
from datetime import datetime
import pandas as pd
import numpy as np
import os
from yahooquery import Ticker
from strategyCalculator import StrategyCalculator
from progressReport import progressReport as pr
import math

# TickerNames = [["ZM"]]
def createFolders(execType):
    TickerNames = pd.read_csv('./src/tickerNames/TickerNames.csv')
    TickerNames = TickerNames.values
    if execType == 0:
        pathName = './backtestdatabase/'
    else:
        pathName = './database'
    for tickerName in TickerNames:
        if not os.path.exists(pathName + tickerName[0]):
            tickers = Ticker(tickerName[0])
            df = tickers.history(period='max', interval='1d')
            print("Creating and Updating " + tickerName[0] + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
            os.makedirs(pathName + tickerName[0] + '/')
            analysisColumnNames = ['Time Stamp', 'Strategy', 'Position', 'Amount', 'Entry', 'Stop Loss', 'Take Profit', 'Confidence', 'Outcome', 'Profits', 'Points Gained/Lost']
            analysisFrame = pd.DataFrame(columns=analysisColumnNames)
            analysisFrame.to_csv(pathName + tickerName[0] + '/analysis.csv')
            tradeColumnNames = ['Time Stamp', 'Position', 'Amount', 'Entry', 'Stop Loss', 'Target', 'Confidence', 'Leverage', 'Outcome', 'Profits']
            tradeFrame = pd.DataFrame(columns=tradeColumnNames)
            tradeFrame.to_csv(pathName + tickerName[0] + '/trades.csv')
            df.to_csv(pathName + tickerName[0] + '/temp.csv')