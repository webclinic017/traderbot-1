import pandas as pd
from yahooquery import Ticker

columnNames = ["Ichimoku", "MACD"]

frame = pd.DataFrame(columns=columnNames)
frame.loc[len(frame)] = 100
frame.loc[len(frame)] = 0
frame.loc[len(frame)] = 1
print(frame)

