import Pyro4
import pandas as pd

class Comparator():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.executor = Pyro4.Proxy("PYRONAME:executor")

    def updateWeightage(self, strategy, points):
        df = pd.read_csv('./database/' + self.tickerName + '/IndicatorScore.csv', index_col=0)

        if points < 0:
            df.loc[0, strategy] = 0.9 * df.loc[0, strategy]
            # fibonacci increment strategy
            # if df.loc[2,strategy] > 0:
            #     df.loc[2,strategy] = -1
            #     df.loc[1,strategy] = 0
            # else:
            #     temp = df.loc[2,strategy]
            #     df.loc[2,strategy] = df.loc[2,strategy] + df.loc[1,strategy]
            #     df.loc[1,strategy] = temp
        else:
            df.loc[0, strategy] = 1.1 * df.loc[0,strategy]
            # fibonacci decrement strategy
            # if df.loc[2,strategy] < 0:
            #     df.loc[2,strategy] = 1
            #     df.loc[1,strategy] = 0
            # else:
            #     temp = df.loc[2, strategy]
            #     df.loc[2,strategy] = df.loc[2,strategy] + df.loc[1,strategy]
            #     df.loc[1,strategy] = temp

        # fibonacci strategy
        # df.loc[0,strategy] = df.loc[0,strategy] + df.loc[2,strategy]
        df.to_csv('./database/' + self.tickerName + '/IndicatorScore.csv')
        pass
    
    def compare(self, results):
        # TO-DO: Compare results and output final decision
        df = pd.read_csv('./database/' + self.tickerName + '/IndicatorScore.csv', index_col=0)

        # 1. Get the weightage
        init = False

        for i in results:
            if init == False:
                highest = df.loc[0,i] * (results[i])["position"]
                lowest = df.loc[0,i] * (results[i])["position"]
                highestIndicator = i
                lowestIndicator = i
                init = True
            else:
                if df.loc[0,i] * (results[i])["position"] > highest:
                    highest = df.loc[0,i] * (results[i])["position"]
                    highestIndicator = i
                if df.loc[0,i] * (results[i])["position"] < lowest:
                    lowest = df.loc[0,i] * (results[i])["position"]
                    lowestIndicator = i
            
            df.loc[0,i] = df.loc[0,i] * (results[i])["position"]

        total = df.sum(axis = 1)

        if total[0] > 100:
            if total[0] > 500: leverage = 5
            elif total[0] > 200: leverage = 2
            else: leverage = 1
            self.executor.execute(self.tickerName, 1, results[highestIndicator]["amount"], results[highestIndicator]["stoploss"], results[highestIndicator]["takeprofit"], leverage)
        elif total[0] < -100:
            if total[0] < -500: leverage = 5
            elif total[0] < -200: leverage = 2
            else: leverage = 1
            self.executor.execute(self.tickerName, -1, results[lowestIndicator]["amount"], results[lowestIndicator]["stoploss"], results[lowestIndicator]["takeprofit"], leverage)
        pass
        