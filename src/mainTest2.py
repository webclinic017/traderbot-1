import json
import time
import pandas as pd
import numpy as np
from yahooquery import Ticker
import multiprocessing as mp

## start the nameserver pyro4-ns [options]

from scraper import Scraper

if __name__ == '__main__':
    #############################################
    # 1. TO-DO: REPLACE THIS STATIC tickerName LIST WITH ONE THAT READS A CSV FILE FOR THE tickerNameS
    TickerNames = ['ETH-USD', 'BTC-USD', 'XRP-USD', 'BCH-USD', 'LTC-USD', 'EOS-USD']
    
    # TickerNames = TickerNames.values
    ############################################

    # Multiprocessing
    processes = []
    
    print("Fetching Data from Stocks")
    
    for tickerName in TickerNames:
        scraper = Scraper(tickerName)
        process = mp.Process(target=scraper.update, args=())
        process.start()
        processes.append(process)
        
    for process in processes:
        process.join()
        
    