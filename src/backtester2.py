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

if not os.path.exists('./database/' + "AAPL"):
    tickers = Ticker("AAPL")
    df = tickers.history(period='max', interval='1d')
    print("Creating and Updating " + "AAPL" + " at " + datetime.fromtimestamp(time.time()).strftime('%H:%M'))
    os.makedirs('./database/' + "AAPL" + '/')
    analysisColumnNames = ['Time Stamp', 'Strategy', 'Position', 'Amount', 'Entry', 'Stop Loss', 'Take Profit', 'Confidence', 'Outcome', 'Profits', 'Points Gained/Lost']
    analysisFrame = pd.DataFrame(columns=analysisColumnNames)
    analysisFrame.to_csv('./database/' + "AAPL" + '/analysis.csv')
    tradeColumnNames = ['Time Stamp', 'Position', 'Amount', 'Entry', 'Stop Loss', 'Target', 'Confidence', 'Leverage', 'Outcome', 'Profits']
    tradeFrame = pd.DataFrame(columns=tradeColumnNames)
    tradeFrame.to_csv('./database/' + "AAPL" + '/trades.csv')
    df.to_csv('./database/' + "AAPL" + '/temp.csv')