import Pyro4
import pandas as pd

class Comparator():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.executor = Pyro4.Proxy("PYRONAME:executor")

    def updateWeightage(self, strategy, points):
        df = pd.read_csv('./database/' + self.tickerName + '/IndicatorScore.csv', index_col=0)
        print("df round 1")
        print(df)

        if points < 0:
            if df.loc[2,strategy] > 0:
                df.loc[2,strategy] = -1
                df.loc[1,strategy] = 0
            else:
                temp = df.loc[2,strategy]
                df.loc[2,strategy] = df.loc[2,strategy] + df.loc[1,strategy]
                df.loc[1,strategy] = temp
        else:
            if df.loc[2,strategy] < 0:
                df.loc[2,strategy] = 1
                df.loc[1,strategy] = 0
            else:
                temp = df.loc[2, strategy]
                df.loc[2,strategy] = df.loc[2,strategy] + df.loc[1,strategy]
                df.loc[1,strategy] = temp


        df.loc[0,strategy] = df.loc[0,strategy] + df.loc[2,strategy]
        df.to_csv('./database/' + self.tickerName + '/IndicatorScore.csv')
        print("df round 2")
        print(df)
        pass
    
    def compare(self, results, atr):
        # TO-DO: Compare results and output final decision
        df = pd.read_csv('./database/' + self.tickerName + '/IndicatorScore.csv', index_col=0)
        for i in results:
            df.loc[0,i] = df.loc[0,i] * results[i]
            total = df.sum(axis = 1)

            if total[0] > 100:
                self.executor.execute(self.tickerName, 1, atr, 1)
            elif total[0] < -100:
                self.executor.execute(self.tickerName, -1, atr, 1)
        pass
        