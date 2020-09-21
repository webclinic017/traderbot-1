import pandas as pd
df = pd.read_csv('./database/' + 'BTC-USD' + '/analysis.csv', index_col= 0)
for index,row in df.iterrows():
    print(row['Stop Loss'])