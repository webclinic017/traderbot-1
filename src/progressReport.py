import os
import pandas as pd

def progressReport():
    rootFolder = os.getcwd()
    analysisReportColumns = ['Ticker Name', 'Indicator', 'Score', 'Successful PseudoTrades', 'Failed PseudoTrades', 'Win/Loss Ratio', 'Amount Earned']
    analysisReportFrame = pd.DataFrame(columns=analysisReportColumns)
    tradesReportColumns = ['Ticker Name', 'No. of Trades', 'Profits']
    tradesReportFrame = pd.DataFrame(columns=tradesReportColumns)
    for parentFolder in os.listdir(rootFolder + '/database'):
        indicatorScore = pd.read_csv(rootFolder + '/database/' + parentFolder + '/IndicatorScore.csv', index_col= 0)
        analysis = pd.read_csv(rootFolder + '/database/' + parentFolder + '/analysis.csv', index_col= 0)
        indicators = list(indicatorScore.columns)
        trades = pd.read_csv(rootFolder + '/database/' + parentFolder + '/trades.csv', index_col= 0)
        for i in indicators:
            score = indicatorScore.loc[0,i]
            profits = 0
            success = 0
            fail = 0
            for index,row in analysis.iterrows():
                if row['Strategy'] == i:
                    if row['Outcome'] == 'Success':
                        success = success + 1
                    elif row['Outcome'] == 'Fail':
                        fail = fail + 1
                    profits = profits + row['Profits']
            if fail == 0:
                ratiofail = 1
            else: ratiofail = fail
            if success == 0:
                ratiosuccess = 1
            else: ratiosuccess = success
            analysisReportFrame = analysisReportFrame.append({'Ticker Name' : parentFolder, 'Indicator' : i, 'Score': score, 'Successful PseudoTrades' : success, 'Failed PseudoTrades': fail, 'Win/Loss Ratio':ratiosuccess/ratiofail, 'Amount Earned' : profits}, ignore_index=True)
        tradeNumber = 0
        tradeProfit = 0
        for index,row in trades.iterrows():
            tradeNumber = tradeNumber + 1
            tradeProfit = tradeProfit + row['Profits']
        tradesReportFrame = tradesReportFrame.append({'Ticker Name' : parentFolder, 'No. of Trades' : tradeNumber, 'Profits': tradeProfit}, ignore_index=True)
    analysisReportFrame.to_csv('./reports/AnalysisReport.csv')
    tradesReportFrame.to_csv('./reports/TradesReport.csv')
    pass
        


