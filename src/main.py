import json
import time
import pandas as pd
import numpy as np
from yahooquery import Ticker
import multiprocessing as mp

from scraper import Scraper

if __name__ == '__main__':
    #############################################
    # 1. TO-DO: REPLACE THIS STATIC tickerName LIST WITH ONE THAT READS A CSV FILE FOR THE tickerNameS
    USTickerName = ['TSLA','AAPL','DOCU','ZM','FB','GOOG','AVGO','ADBE','EEE','EIE','TY']
    ############################################

    # Multiprocessing
    processes = []
    
    print("Fetching Data from US Stocks")
    
    for tickerName in USTickerName:
        scraper = Scraper(tickerName)
        process = mp.Process(target=scraper.update, args=())
        process.start()
        processes.append(process)
        
    for process in processes:
        process.join()
        
    