import Pyro4
import pandas as pd

class Comparator():
    def __init__(self, tickerName, execType):
        self.tickerName = tickerName
        self.executor = Pyro4.Proxy("PYRONAME:executor")
        self.execType = execType
        if execType == 0:
            self.path = './backtestatabase/'
        elif execType == 1:
            self.path = './database/'

    def updateWeightage(self, strategy, points):
        df = pd.read_csv(self.path + self.tickerName + '/IndicatorScore.csv', index_col=0)

        # if points < 0:
        #     df.loc[0,strategy] = (1+(0.1*points)) * df.loc[0,strategy]
        # elif points > 0:
        #     df.loc[0, strategy] = (1+(0.1*points)) * df.loc[0,strategy]
        if points > 0:
            points = 2.0 * points
        df.loc[0,strategy] = points + df.loc[0,strategy]
        # if points < 0:
        #     df.loc[0, strategy] = 0.9 * df.loc[0, strategy]
        #     # fibonacci increment strategy
        #     # if df.loc[2,strategy] > 0:
        #     #     df.loc[2,strategy] = -1
        #     #     df.loc[1,strategy] = 0
        #     # else:
        #     #     temp = df.loc[2,strategy]
        #     #     df.loc[2,strategy] = df.loc[2,strategy] + df.loc[1,strategy]
        #     #     df.loc[1,strategy] = temp
        # else:
        #     df.loc[0, strategy] = 1.1 * df.loc[0,strategy]
        #     # fibonacci decrement strategy
        #     # if df.loc[2,strategy] < 0:
        #     #     df.loc[2,strategy] = 1
        #     #     df.loc[1,strategy] = 0
        #     # else:
        #     #     temp = df.loc[2, strategy]
        #     #     df.loc[2,strategy] = df.loc[2,strategy] + df.loc[1,strategy]
        #     #     df.loc[1,strategy] = temp

        # fibonacci strategy
        # df.loc[0,strategy] = df.loc[0,strategy] + df.loc[2,strategy]
        df.to_csv(self.path + self.tickerName + '/IndicatorScore.csv')
        pass
    
    def compare(self, results, timestamp):
        # TO-DO: Compare results and output final decision
        df = pd.read_csv(self.path + self.tickerName + '/IndicatorScore.csv', index_col=0)

        # 1. Get the weightage
        init = False

        for i in results:
            if init == False:
                highest = df.loc[0,i] * (results[i])["position"] * (results[i])["confidence"]
                lowest = df.loc[0,i] * (results[i])["position"] * (results[i])["confidence"]
                highestIndicator = i
                lowestIndicator = i
                init = True
            else:
                if df.loc[0,i] * (results[i])["position"] * (results[i])["confidence"] > highest:
                    highest = df.loc[0,i] * (results[i])["position"] * (results[i])["confidence"]
                    highestIndicator = i
                if df.loc[0,i] * (results[i])["position"] * (results[i])["confidence"] < lowest:
                    lowest = df.loc[0,i] * (results[i])["position"] * (results[i])["confidence"]
                    lowestIndicator = i
            
            df.loc[0,i] = df.loc[0,i] * (results[i])["position"] * (results[i])["confidence"]

        total = df.sum(axis = 1)

        if total[0] > 100:
            if total[0] > 500: leverage = 5
            elif total[0] > 200: leverage = 2
            else: leverage = 1
            tradeWindow = pd.read_csv(self.path + self.tickerName + '/trades.csv', index_col= 0)
            tradeWindow = tradeWindow.append({'Time Stamp' : timestamp, 'Position': 1, 'Amount': results[highestIndicator]["amount"], 'Entry': results[highestIndicator]["entry"], 'Stop Loss': results[highestIndicator]["stoploss"], 'Target': results[highestIndicator]["takeprofit"], 'Confidence': results[highestIndicator]["confidence"], 'Leverage': leverage, 'Outcome': 'Pending', 'Profits': 0}, ignore_index = True)
            tradeWindow.to_csv(self.path + self.tickerName + '/trades.csv')
            if self.execType == 1:
                instructionWindow = pd.read_csv('./tradeInstructions/tradeInstructions.csv', index_col= 0)
                instructionWindow = instructionWindow.append({'Day' : str(timestamp), 'Action': 'Buy ' + self.tickerName + " StopLoss: " + str(results[highestIndicator]["stoploss"]) + " Target: " + str(results[highestIndicator]["takeprofit"]) + " Leverage " + str(leverage)}, ignore_index = True)
                instructionWindow.to_csv('./tradeInstructions/tradeInstructions.csv')
            # print("Indicator Selected: " + highestIndicator + " , Confidence: " + str(results[highestIndicator]["confidence"]) + ", Position: " + str(results[highestIndicator]["position"]))
            # self.executor.execute(self.tickerName, 1, results[highestIndicator]["amount"], results[highestIndicator]["entry"], results[highestIndicator]["stoploss"], results[highestIndicator]["takeprofit"], leverage)
        elif total[0] < -100:
            if total[0] < -500: leverage = 5
            elif total[0] < -200: leverage = 2
            else: leverage = 1
            tradeWindow = pd.read_csv(self.path + self.tickerName + '/trades.csv', index_col= 0)
            tradeWindow = tradeWindow.append({'Time Stamp' : timestamp, 'Position': -1, 'Amount': results[lowestIndicator]["amount"], 'Entry': results[lowestIndicator]["entry"], 'Stop Loss': results[lowestIndicator]["stoploss"], 'Target': results[lowestIndicator]["takeprofit"], 'Confidence': results[lowestIndicator]["confidence"], 'Leverage': leverage, 'Outcome': 'Pending', 'Profits': 0}, ignore_index = True)
            tradeWindow.to_csv(self.path + self.tickerName + '/trades.csv')
            if self.execType == 1:
                instructionWindow = pd.read_csv('./tradeInstructions/tradeInstructions.csv', index_col= 0)
                instructionWindow = instructionWindow.append({'Day' : str(timestamp), 'Action': 'Sell ' + self.tickerName + " StopLoss: " + str(results[lowestIndicator]["stoploss"]) + " Target: " + str(results[lowestIndicator]["takeprofit"]) + " Leverage " + str(leverage)}, ignore_index = True)
                instructionWindow.to_csv('./tradeInstructions/tradeInstructions.csv')
            # print("Indicator Selected: " + lowestIndicator + " , Confidence: " + str((results[lowestIndicator])["confidence"]) + ", Position: " + str((results[lowestIndicator])["position"]))
            # self.executor.execute(self.tickerName, -1, results[lowestIndicator]["amount"], results[highestIndicator]["entry"], results[lowestIndicator]["stoploss"], results[lowestIndicator]["takeprofit"], leverage)
        pass

    def intervalAnalysis(self, update):
        df = pd.read_csv(self.path + self.tickerName + '/trades.csv', index_col= 0)
        for index,row in df.iterrows():
            if row['Outcome'] == 'Pending':
                if row['Position'] == 1:
                    if update['close'].values[0] > row['Target']:
                        oldPriceDifference = abs(row['Target'] - row['Entry'])
                        newPriceDifference = 1.5 * oldPriceDifference
                        cap = 1.2 * update['low'].values[0]
                        capPriceDifference = abs(cap - update['low'].values[0])
                        if abs(row['Entry'] + newPriceDifference) > abs(capPriceDifference):
                            df.loc[index, 'Target'] = cap
                            updatee = cap
                        else:
                            df.loc[index, 'Target'] = row['Entry'] + newPriceDifference
                            updatee = row['Entry'] + newPriceDifference
                        df.loc[index, 'Stop Loss'] = update['low'].values[0]
                        df.loc[index, 'Profits'] = (update['close'].values[0] - df.loc[index, 'Entry']) / df.loc[index,'Entry'] * df.loc[index, 'Amount'] * df.loc[index, 'Leverage']
                        df.to_csv(self.path + self.tickerName + '/trades.csv')
                        if self.execType == 1:
                            instructionWindow = pd.read_csv('./tradeInstructions/tradeInstructions.csv', index_col= 0)
                            instructionWindow = instructionWindow.append({'Day' : str(update['date'].values[0]), 'Action': 'Update ' + self.tickerName + " StopLoss: " + str(update['low'].values[0]) + " Target: " + str(updatee)}, ignore_index = True)
                            instructionWindow.to_csv('./tradeInstructions/tradeInstructions.csv')

                    elif update['low'].values[0] < row['Stop Loss']:
                        df.loc[index, 'Outcome'] = 'Closed'
                        df.loc[index, 'Profits'] = (df.loc[index,'Stop Loss'] - df.loc[index,'Entry']) / df.loc[index,'Entry'] * df.loc[index,'Amount'] * df.loc[index, 'Leverage']
                        df.to_csv(self.path + self.tickerName + '/trades.csv')

                elif row['Position'] == -1:
                    if update['close'].values[0] < row['Target']:
                        oldPriceDifference = abs(row['Entry'] - row['Target'])
                        newPriceDifference = 1.5 * oldPriceDifference
                        cap = 0.8 * update['high'].values[0]
                        capPriceDifference = abs(cap - update['low'].values[0])
                        if (row['Entry'] - newPriceDifference) < cap:
                            df.loc[index, 'Target'] = cap
                            updatee = cap
                        else:
                            df.loc[index, 'Target'] = row['Entry'] - newPriceDifference
                            updatee = row['Entry'] - newPriceDifference
                        df.loc[index, 'Stop Loss'] = update['high'].values[0]
                        df.loc[index, 'Profits'] = (update['close'].values[0] - df.loc[index,'Entry']) / df.loc[index,'Entry'] * (-1) * df.loc[index,'Amount'] * df.loc[index, 'Leverage']
                        df.to_csv(self.path + self.tickerName + '/trades.csv')
                        if self.execType == 1:
                            instructionWindow = pd.read_csv('./tradeInstructions/tradeInstructions.csv', index_col= 0)
                            instructionWindow = instructionWindow.append({'Day' : str(update['date'].values[0]), 'Action': 'Update ' + self.tickerName + " StopLoss: " + str(update['high'].values[0]) + " Target: " + str(updatee)}, ignore_index = True)
                            instructionWindow.to_csv('./tradeInstructions/tradeInstructions.csv')


                    elif update['high'].values[0] > row['Stop Loss']:
                        df.loc[index, 'Outcome'] = 'Closed'
                        df.loc[index, 'Profits'] = (df.loc[index,'Stop Loss'] - df.loc[index, 'Entry']) / df.loc[index,'Entry'] * (-1) * df.loc[index, 'Amount'] * df.loc[index, 'Leverage']
                        df.to_csv(self.path + self.tickerName + '/trades.csv')

        # TO-DO: If ticker is currently trading, do intervalAnalysis
        pass