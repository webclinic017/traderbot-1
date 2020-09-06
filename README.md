# TraderBot
Simple algorithmic trading bot

## Introduction
This program attempts to retrieve trading data on user-determined timeframes and intervals, then applies several indicators on the dataset to trade the market. 

## Architectural Overview Diagram
![alt text](https://github.com/cwlroda/traderbot/blob/master/img/AOD.png)

## Explanation of Components
### 1. Scraper
a.	Collects data from Yahoo! Finance at every user-determined timeframe and interval\
b.	Updates the Database of each ticker\
c.	To improve efficiency, can attempt to pipeline by informing Strategy Calculators immediately after completion of each ticker.

### 2. Ticker Database
a.	CSV/JSON form of all the tickers

### 3. Strategy Calculators (Multi-thread)
a.	Made up of many modules, each module uses their own set of indicators to calculate if a position should be made, and the TP/SL.\
b.	Extracts (read only) data from the Database to commence calculation.\
c.	Interface for Scraper: __Inform(String TickerName, String TimeStamp)__

### 4. Analyser
a.	Assumes at all position advices are taken regardless of Strategy weightage.\
b.	Tracks these positions to identify if it has succeeded or failed.\
c.	Successful positions will result in the improvement of strategy’s weight in future decisions by the Comparator\
d.	Failed positions will result in the decrease in the strategy’s weight in future decisions by the Comparator\
e.	Interface for Strategy Calculators: __StrategyOutput(Int BuySell, Float TP, Float SL)__

### 5. Comparator
a.	Each Strategy Calculator is given a rating due to their past performances\
b.	Outputs from the respective Strategy Calculators are imported given a weighted score based on their rating.\
c.	A high overall score could pass through and carried out, while low overall score will be disposed.\
d.	The ratings of the Strategy Calculators can be updated by the Analyser\
e.	Interface for Strategy Calculators: __StrategyOutput(Int BuySell, Float TP, Float SL)__\
f.	Interface for Analyser: __UpdateWeightage(String StrategyCalculator, Int WeightageChange)__

### 6. Executor
a.	Performs the execution of the Comparator on the Brokerage Platform\
b.	Interface for Comparator: __Execute(Int BuySell, Float TP, FloatSL, Int Leverage)__



