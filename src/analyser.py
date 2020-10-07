import pandas as pd

class Analyser():
    def __init__(self, tickerName, comparator, execType):
        self.tickerName = tickerName
        self.comparator = comparator
        if execType == 0:
            self.path = './backtestdatabase/'
        elif execType == 1:
            self.path = './database/'
    
    def intervalAnalysis(self, update):
        # TO-DO: Looks through currently trading file
        df = pd.read_csv(self.path + self.tickerName + '/analysis.csv', index_col= 0)
        for index,row in df.iterrows():
            if row['Outcome'] == 'Pending':
                if row['Position'] == 1:
                    if update['high'].values[0] > row['Take Profit']:
                        df.loc[index, 'Outcome'] = 'Success'
                        weightsChange = df.loc[index, 'Confidence']
                        df.loc[index, 'Points Gained/Lost'] = weightsChange
                        df.loc[index, 'Profits'] = (df.loc[index,'Take Profit'] - df.loc[index, 'Entry']) / df.loc[index, 'Entry'] * df.loc[index, 'Amount']
                        df.to_csv(self.path + self.tickerName + '/analysis.csv')
                        self.comparator.updateWeightage(row['Strategy'], weightsChange)

                    elif update['low'].values[0] < row['Stop Loss']:
                        df.loc[index, 'Outcome'] = 'Fail'
                        weightsChange = -1 * df.loc[index, 'Confidence']
                        df.loc[index, 'Points Gained/Lost'] = weightsChange
                        df.loc[index, 'Profits'] = (df.loc[index,'Stop Loss'] - df.loc[index,'Entry']) / df.loc[index, 'Entry'] * df.loc[index,'Amount']
                        df.to_csv(self.path + self.tickerName + '/analysis.csv')
                        self.comparator.updateWeightage(row['Strategy'], weightsChange)

                elif row['Position'] == -1:
                    if update['low'].values[0] < row['Take Profit']:
                        df.loc[index, 'Outcome'] = 'Success'
                        weightsChange = df.loc[index, 'Confidence']
                        df.loc[index, 'Points Gained/Lost'] = weightsChange
                        df.loc[index, 'Profits'] = (df.loc[index,'Take Profit'] - df.loc[index,'Entry']) / df.loc[index, 'Entry'] * (-1) * df.loc[index,'Amount']
                        df.to_csv(self.path + self.tickerName + '/analysis.csv')
                        self.comparator.updateWeightage(row['Strategy'], weightsChange)

                    elif update['high'].values[0] > row['Stop Loss']:
                        df.loc[index, 'Outcome'] = 'Fail'
                        weightsChange = -1 * df.loc[index, 'Confidence']
                        df.loc[index, 'Points Gained/Lost'] = weightsChange
                        df.loc[index, 'Profits'] = (df.loc[index,'Stop Loss'] - df.loc[index, 'Entry']) / df.loc[index, 'Entry'] * (-1) * df.loc[index, 'Amount']
                        df.to_csv(self.path + self.tickerName + '/analysis.csv')
                        self.comparator.updateWeightage(row['Strategy'], weightsChange)

        # TO-DO: If ticker is currently trading, do intervalAnalysis
        pass
    
    def PseudoTrade(self, df, strategy, tradeDetails):

        df = df.head(1)
        dfDate = df['date'].values[0]


        df = pd.read_csv(self.path + self.tickerName + '/analysis.csv',index_col=0)

        df = df.append({'Time Stamp' : dfDate, 'Strategy' : strategy, 'Position' : tradeDetails['position'], 'Amount': tradeDetails['amount'], 'Entry': tradeDetails['entry'], 'Stop Loss' : tradeDetails['stoploss'], 'Take Profit' : tradeDetails['takeprofit'], 'Confidence' : tradeDetails['confidence'], 'Outcome' : 'Pending', 'Profits' : 0, 'Points Gained/Lost' : 0}, ignore_index = True)
        df.to_csv(self.path + self.tickerName + '/analysis.csv')

        pass
        ### TO-DO: Save information into a CSV database full of pseudotrades