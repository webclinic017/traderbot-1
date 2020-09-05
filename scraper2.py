from alpha_vantage.timeseries import TimeSeries

symbol = ['TSLA','AAPL','DOCU']

ts = TimeSeries(key='S0Z9P2SO2GK2MROJ',output_format = 'pandas')

for i in symbol:
    data, meta_data = ts.get_intraday(symbol='TSLA',interval = '5min', outputsize = 'compact')
    data.to_csv('./database/' + i + '.csv', index = False)