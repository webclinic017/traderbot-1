
from talib import MACDFIX, RSI, EMA
import os

import pandas as pd
class Indicator:

    
    # indicatorlist = ['ichimoku200', 'macdRSI']    
    def beginCalc(self, df, tickerName, atr):
        ## FILL THIS IN AS MORE INDICATORS ARE ADDED
        indicatorlist = ['ichimoku200','macdRSI']

        # Step 1: Find out if analysis csv exists
        if not os.path.exists('./database/' + tickerName + '/analysis.csv'):
            columnNames = ['Time Stamp', 'Strategy', 'Position', 'Stop Loss', 'Take Profit', 'Outcome', 'Points Gained/Lost']
            frame = pd.DataFrame(columns=columnNames)
            frame.to_csv('./database/' + tickerName + '/analysis.csv')
        
        if not os.path.exists('./database/' + tickerName + '/IndicatorScore.csv'):
            columnNames = indicatorlist
            frame = pd.DataFrame(columns=columnNames)
            frame.loc[len(frame)] = 100
            frame.to_csv('./database/' + tickerName + '/IndicatorScore.csv')
        else:
            columnCheck = pd.read_csv('./database/' + tickerName + '/IndicatorScore.csv')
            for i in indicatorlist:
                if not i in columnCheck.columns:
                    avg = columnCheck.mean(axis = 1)
                    columnCheck.insert(len(columnCheck.columns), i, avg)
            columnCheck.to_csv('./database/' + tickerName + '/IndicatorScore.csv')
        resultsDict = {}

        for i in indicatorlist:
            fnRun = getattr(self, i)
            output = fnRun(df)
            resultsDict[i] = output
            
        return resultsDict
    

    def ichimoku200(self,df):
        ## Step 1: 
        #####PLACEHOLDER
        # df = pd.read_csv('./database/AAPL.csv')
        #####END_PLACEHOLDER
        df = df.dropna()
        ###1. Getting Parameters

        ##a. Senkou Span B Ahead
        Currentfifty_two = df.head(52)
        Currentfifty_two_high = Currentfifty_two['high'].max()
        Currentfifty_two_low = Currentfifty_two['low'].min()
        AheadSenkouB = (Currentfifty_two_high + Currentfifty_two_low) / 2
        # print("SenkouBAhead\n", AheadSenkouB)

        ##b. Current Kijun-Sen
        Currenttwenty_six = Currentfifty_two.head(26)
        Currenttwenty_six_high = Currenttwenty_six['high'].max()
        Currenttwenty_six_low = Currenttwenty_six['low'].min()
        CurrentKijun = (Currenttwenty_six_high + Currenttwenty_six_low) / 2
        # print("Kijun-Sen\n" , CurrentKijun)

        ##c. Current Tenkan-Sen
        Currentnine = Currenttwenty_six.head(9)
        Currentnine_high = Currentnine['high'].max()
        Currentnine_low = Currentnine['low'].min()
        CurrentTenkan = (Currentnine_high + Currentnine_low)/2

        # print("Tenkan-Sen\n", CurrentTenkan)

        ##d. Senkou Span A Ahead
        AheadSenkouA = (CurrentKijun + CurrentTenkan) / 2
        # print("SenkouAAhead\n", AheadSenkouA)

        ##e. Senkou Span B Current
        Pastfifty_two = df.iloc[26:].head(52)
        Pastfifty_two_high = Pastfifty_two['high'].max()
        Pastfifty_two_low = Pastfifty_two['low'].min()
        CurrentSenkouB = (Pastfifty_two_high + Pastfifty_two_low) / 2
        # print("SenkouBCurrent\n", CurrentSenkouB)

        ##f. Past Kijun-Sen
        Pasttwenty_six = Pastfifty_two.head(26)
        Pasttwenty_six_high = Pasttwenty_six['high'].max()
        Pasttwenty_six_low = Pasttwenty_six['low'].min()
        PastKijun = (Pasttwenty_six_low + Pasttwenty_six_high) / 2
        # print("PastKijun-Sen\n",PastKijun)

        ##g. Past Tenkan-Sen
        Pastnine = Pasttwenty_six.head(9)
        Pastnine_high = Pastnine['high'].max()
        Pastnine_low = Pastnine['low'].min()
        PastTenkan = (Pastnine_high + Pastnine_low) / 2
        # print("PastTenkan-Sen\n", PastTenkan)

        ##h. Senkou Span A Current
        CurrentSenkouA = (PastKijun + PastTenkan) / 2
        # print("SenkouACurrent\n", CurrentSenkouA)

        ##i. 200EMA
        emaInput = df.head(200)
        EMAclose = emaInput['close'].values
        ema = EMA(EMAclose, timeperiod=200)
        # print("EMA\n", ema[-1])

        ##j. current price action
        priceaction = df.head(1)
        pricehigh = priceaction['high'].values[0]
        pricelow = priceaction['low'].values[0]
        # print("pricehigh\n", pricehigh)
        # print("pricelow\n", pricelow)
        
        ### 2. Analysing using Data Provided
        ##tenkan-kijun crossover type
            ## -1 means negative crossover
            ## 1 means positive crossover
            ## 0 means both

        if CurrentTenkan > CurrentKijun: crossover = 1
        elif CurrentTenkan < CurrentKijun: crossover = -1
        else: crossover = 0

        ##current cloud colour
            ## -1 means red cloud
            ## 1 means green cloud
            ## 0 means both

        if CurrentSenkouA > CurrentSenkouB: CurrentCloud = 1
        elif CurrentSenkouA < CurrentSenkouB: CurrentCloud = -1
        else: CurrentCloud = 0

        ##ahead cloud colour
            ## -1 means red cloud
            ## 1 means green cloud
            ## 0 means both

        if AheadSenkouA > AheadSenkouB: AheadCloud = 1
        elif AheadSenkouA < AheadSenkouB: AheadCloud = -1
        else: AheadCloud = 0

        ##market-ema type
            ## 1 means low > 200EMA
            ## -1 means high < 200EMA
            ## 0 means otherwise

        if pricelow > ema[-1]: marketEMA = 1
        elif pricehigh < ema[-1]: marketEMA = -1
        else: marketEMA = 0

        ##market-cloud type
            ## 1 means low is above current green cloud
            ## -1 means high is below current red cloud
            ## 0 means otherwise (absolutely no trading)

        if CurrentCloud >= 0 and pricelow > CurrentSenkouA:
            marketCloud = 1
        elif CurrentCloud <= 0 and pricehigh < CurrentSenkouB:
            marketCloud = -1
        else: marketCloud = 0



        if marketCloud == 1 and marketEMA >= 0 and AheadCloud >= 0 and crossover >= 0:
            position = 1
        elif marketCloud == -1 and marketEMA <=0 and AheadCloud <= 0 and crossover <= 0:
            position = -1
        else: position = 0

        return position


    def macdRSI(self,df):
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
