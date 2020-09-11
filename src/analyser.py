import pandas as pd

class Analyser():
    def __init__(self, tickerName, comparator):
        self.tickerName = tickerName
        self.comparator = comparator
    
    def intervalAnalysis(self, update):
        # TO-DO: Looks through currently trading file
        df = pd.read_csv('./database/' + self.tickerName + '/analysis.csv')
        for index,row in df.iterrows():
            if row['Outcome'] == 'Pending':
                if row['Position'] == 1:
                    if update['high'].values[0] > row['Take Profit']:
                        df.loc[index, 'Outcome'] = 'Success'
                        df.loc[index, 'Points Gained/Lost'] = 1
                        df.to_csv('./database/' + self.tickerName + '/analysis.csv')
                        self.comparator.updateWeightage(row['Strategy'], 1)

                    elif update['low'].values[0] < row['Stop Loss']:
                        df.loc[index, 'Outcome'] = 'Fail'
                        df.loc[index, 'Points Gained/Lost'] = -1
                        df.to_csv('./database/' + self.tickerName + '/analysis.csv')
                        self.comparator.updateWeightage(row['Strategy'], -1)

                elif row['Position'] == -1:
                    if update['low'].values[0] < row['Take Profit']:
                        df.loc[index, 'Outcome'] = 'Success'
                        df.loc[index, 'Points Gained/Lost'] = 1
                        df.to_csv('./database/' + self.tickerName + '/analysis.csv')
                        self.comparator.updateWeightage(row['Strategy'], 1)

                    elif update['high'].values[0] > row['StopLoss']:
                        df.loc[index, 'Outcome'] = 'Fail'
                        df.loc[index, 'Points Gained/Lost'] = -1
                        df.to_csv('./database/' + self.tickerName + '/analysis.csv')
                        self.comparator.updateWeightage(row['Strategy'], -1)

        # TO-DO: If ticker is currently trading, do intervalAnalysis
        pass
    
    def PseudoTrade(self, df, strategy, position, atr):
        # print("Adding pseudo trade for " + self.tickerName + " at " + timeStamp + " (" + strategy + ")")
        df = df.head(2).iloc[1:]
        dfDate = df['date'].values[0]
        dfHigh = df['high'].values[0]
        dfLow = df['low'].values[0]

        if position == -1:
            stopLoss = dfHigh + atr
            takeProfit = dfLow - (1.5 * atr)
        elif position == 1:
            stopLoss = dfLow - atr
            takeProfit = dfHigh + (1.5*atr)

        df = pd.read_csv('./database/' + self.tickerName + '/analysis.csv')

        df = df.append({'Time Stamp' : dfDate, 'Strategy' : strategy, 'Position' : position, 'Stop Loss' : stopLoss, 'Take Profit' : takeProfit, 'Outcome' : 'Pending', 'Points Gained/Lost' : 0}, ignore_index = True)
        df.to_csv('./database/' + self.tickerName + '/analysis.csv')

        pass
        ### TO-DO: Save information into a CSV database full of pseudotrades