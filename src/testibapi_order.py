from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time

class IBapi(EWrapper, EClient):
	
	def __init__(self):
		EClient.__init__(self, self)
	
	def nextValidId(self, orderId: int):
		super().nextValidId(orderId)
		self.nextorderId = orderId
		print('The next valid order id is: ', self.nextorderId)

	def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
		print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
	
	def openOrder(self, orderId, contract, order, orderState):
		print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

	def execDetails(self, reqId, contract, execution):
		print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

	def error(self, reqId, errorCode: int, errorString: str):
		super().error(reqId, errorCode, errorString)
		print("Error. Id:", reqId, "Code:", errorCode, "Msg:", errorString)

def run_loop():
	app.run()

def stock_order(symbol):
	contract = Contract()	
	contract.symbol = symbol
	contract.secType = "STK"
	contract.currency = "USD"
	contract.exchange = "SMART"
	contract.primaryExchange = "ISLAND"
	return contract

app = IBapi()
app.connect('127.0.0.1', 7497, 123)

app.nextorderId = None

#Start the socket in a thread
api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

#Check if the API is connected via orderid
while True:
	if isinstance(app.nextorderId, int):
		print('connected')
		print()
		break
	else:
		print('waiting for connection')
		time.sleep(1)

#Create order object
def BracketOrder(parentOrderId:int, action:str, quantity:float, 
				limitPrice:float, takeProfitLimitPrice:float, 
				stopLossPrice:float):
    #This will be our main or "parent" order
	parent = Order()
	parent.orderId = parentOrderId
	parent.action = action
	parent.orderType = "LMT"
	parent.totalQuantity = quantity
	parent.lmtPrice = limitPrice
	#The parent and children orders will need this attribute set to False to prevent accidental executions.
	#The LAST CHILD will have it set to True, 
	parent.transmit = False
	takeProfit = Order()
	takeProfit.orderId = parent.orderId + 1
	takeProfit.action = "SELL" if action == "BUY" else "BUY"
	takeProfit.orderType = "LMT"
	takeProfit.totalQuantity = quantity
	takeProfit.lmtPrice = takeProfitLimitPrice
	takeProfit.parentId = parentOrderId
	takeProfit.transmit = False
	stopLoss = Order()
	stopLoss.orderId = parent.orderId + 2
	stopLoss.action = "SELL" if action == "BUY" else "BUY"
	stopLoss.orderType = "STP"
	#Stop trigger price
	stopLoss.auxPrice = stopLossPrice
	stopLoss.totalQuantity = quantity
	stopLoss.parentId = parentOrderId
	#In this case, the low side order will be the last child being sent. Therefore, it needs to set this attribute to True 
	#to activate all its predecessors
	stopLoss.transmit = True
	bracketOrder = [parent, takeProfit, stopLoss]
	return bracketOrder

# order = Order()
# order.action = 'BUY'
# order.totalQuantity = 100
# order.orderType = 'LMT'
# order.lmtPrice = '200'
# order.orderId = app.nextorderId
# app.nextorderId += 1
# order.transmit = False

# #Create stop loss order object
# stop_order = Order()
# stop_order.action = 'SELL'
# stop_order.totalQuantity = 100
# stop_order.orderType = 'STP'
# stop_order.auxPrice = '198'
# stop_order.orderId = app.nextorderId
# app.nextorderId += 1
# stop_order.parentId = order.orderId
# order.transmit = True

#Place orders
bracket = BracketOrder(app.nextorderId, "BUY", 100, 200, 210, 180)
for o in bracket:
	app.placeOrder(o.orderId, stock_order('MSFT'), o)
	
time.sleep(3)

#Cancel order 
# print('cancelling order')
# app.cancelOrder(order.orderId)
# time.sleep(3)

app.disconnect()