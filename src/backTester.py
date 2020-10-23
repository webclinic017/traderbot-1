import json
import time
import pandas as pd
import numpy as np
import multiprocessing as mp
from backTestFn import backTestFn

def backTester():
    TickerNames = pd.read_csv('./src/tickerNames/TickerNames.csv')
        
    TickerNames = TickerNames.values

    print("Fetching data from Stocks")
    concurrency = 16
    processes = []
    sema = mp.Semaphore(concurrency)
    for tickerName in TickerNames:
        sema.acquire()
        process = mp.Process(target=backTestFn, args=(tickerName[0],sema))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
        
if __name__ == '__main__':
    backTester()