import Pyro4
import pandas as pd

class Comparator():
    def __init__(self, tickerName):
        self.tickerName = tickerName
        self.executor = Pyro4.Proxy("PYRONAME:executor")

    def updateWeightage(self, strategy, points):
        df = pd.read_csv('./database/' + self.tickerName + '/IndicatorScore.csv')
        df.loc[0,strategy] = df.loc[0,strategy] + points
        df.to_csv('./database/' + self.tickerName + '/IndicatorScore.csv')
        pass
    
    def compare(self, results, atr):
        # TO-DO: Compare results and output final decision
        df = pd.read_csv('./database/' + self.tickerName + '/IndicatorScore.csv')
        for i in results:
            df.loc[0,i] = df.loc[0,i] * results[i]
            total = df.sum(axis = 1)

            if total[0] > 100:
                self.executor.execute(self.tickerName, 1, atr, 1)
            elif total[0] < -100:
                self.executor.execute(self.tickerName, -1, atr, 1)
        pass
        