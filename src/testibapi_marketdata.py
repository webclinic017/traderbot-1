from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time
import datetime
import pandas as pd

class IBapi(EWrapper, EClient):
	def __init__(self):
		EClient.__init__(self, self)
		self.data = [] #Initialize variable to store candle
	def historicalData(self, reqId, bar):
		print("HistoricalData. ReqId:", reqId, "BarData.", bar)
		self.data.append([bar.date, bar.close])
	def historicalDataEnd(self, reqId, start, end):
		super().historicalDataEnd(reqId, start, end)
		print("HistoricalDataEnd. ReqId:", reqId, "from", start, "to", end)
	def historicalDataUpdate(self, reqId, bar):
		print("HistoricalDataUpdate. ReqId:", reqId, "BarData.", bar)

def run_loop():
	app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 123)

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

time.sleep(1) #Sleep interval to allow time for connection to server

#Create contract object
eurusd_contract = Contract()
eurusd_contract.symbol = 'EUR'
eurusd_contract.secType = 'CASH'
eurusd_contract.exchange = 'IDEALPRO'
eurusd_contract.currency = 'USD'

#Request historical candles
"""
	tickerId: A unique identifier which will serve to identify the incoming data.
	contract: The IBApi.Contract you are interested in.
	endDateTime: The request's end date and time (the empty string indicates current present moment).
	durationString: The amount of time (or Valid Duration String units) to go back from the request's given end date and time.
	barSizeSetting: The data's granularity or Valid Bar Sizes
	whatToShow: The type of data to retrieve. See Historical Data Types
	useRTH: Whether (1) or not (0) to retrieve data generated only within Regular Trading Hours (RTH)
	formatDate: The format in which the incoming bars' date should be presented. Note that for day bars, only yyyyMMdd format is available.
	keepUpToDate" Whether a subscription is made to return updates of unfinished real time bars as they are available (True), 
		or all data is returned on a one-time basis (False). Available starting with API v973.03+ and TWS v965+. If True, and endDateTime cannot be specified.
"""

queryTime = (datetime.datetime.today() - datetime.timedelta(days=180)).strftime("%Y%m%d %H:%M:%S")
app.reqHistoricalData(1, eurusd_contract, '', '60 S', '1 secs', 'BID', 1, 2, False, [])

time.sleep(20) #sleep to allow enough time for data to be returned

df = pd.DataFrame(app.data, columns=['DateTime', 'Close'])
df['DateTime'] = pd.to_datetime(df['DateTime'],unit='s') 
df.to_csv('EURUSD_secs.csv')  

print(df)

app.disconnect()