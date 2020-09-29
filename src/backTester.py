import json
import time
import pandas as pd
import numpy as np
from yahooquery import Ticker
import multiprocessing as mp
from backTestFn import backTestFn


if __name__ == '__main__':
    TickerNames = pd.read_csv('./src/tickerNames/TickerNames.csv')
        
    TickerNames = TickerNames.values

    processes = []

    print("Fetching data from Stocks")

    for tickerName in TickerNames:
        backtestfn = backTestFn(tickerName[0])
        process = mp.Process(target=backtestfn.update, args=())
        process.start()
        processes.append(process)

    for process in processes:
        process.join()