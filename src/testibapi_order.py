from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time

class IBapi(EWrapper, EClient):
	
	def __init__(self):
		EClient.__init__(self, self)
		self.nextorderId = None
	
	def nextValidId(self, orderId: int):
		self.nextorderId = orderId
		print('The next valid order id is: ', self.nextorderId)
	
	def connectPlatform(self):
		self.connect('127.0.0.1', 7497, 123) # Change port no to match port no in IB settings

	# General fn
	def Start(self):
		while not self.isConnected():
			print("Connecting to IB Host...")
			self.connectPlatform()
			time.sleep(1)
		print("Starting IB API Thread...")
		ibAPIthread = threading.Thread(target=self.run, daemon=True)
		ibAPIthread.start()

	'''    
    Market Orders
    '''

	def orderStatus(self, orderId, status, filled, remaining, avgFullPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice):
		print('orderStatus - orderid:', orderId, 'status:', status, 'filled', filled, 'remaining', remaining, 'lastFillPrice', lastFillPrice)
	
	def openOrder(self, orderId, contract, order, orderState):
		print('openOrder id:', orderId, contract.symbol, contract.secType, '@', contract.exchange, ':', order.action, order.orderType, order.totalQuantity, orderState.status)

	def execDetails(self, reqId, contract, execution):
		print('Order Executed: ', reqId, contract.symbol, contract.secType, contract.currency, execution.execId, execution.orderId, execution.shares, execution.lastLiquidity)

	#! Limit Order
	# A Limit order is an order to buy or sell at a specified price or better. The Limit order ensures that if the order fills, 
	# it will not fill at a price less favorable than your limit price, but it does not guarantee a fill. 
	def LimitOrder(self, action, quantity, limitPrice):
		order = Order()
		order.action = action
		order.orderType = "LMT"
		order.totalQuantity = quantity
		order.lmtPrice = limitPrice
		return order

	#! Stop Order
	#? Will immediately try and buy/sell if the market hits that price,
	#? but will also execute even if it overshoots by a lot
	#? i.e. If the price suddenly falls by a lot past the price, it will execute the order at a very low price
	# A Stop order is an instruction to submit a buy or sell market order if and when the user-specified stop trigger price is attained or penetrated. 
	# A Stop order is not guaranteed a specific execution price and may execute significantly away from its stop price. 
	# A Sell Stop order is always placed below the current market price and is typically used to limit a loss or protect a profit on a long stock position. 
	# A Buy Stop order is always placed above the current market price. 
	# It is typically used to limit a loss or help protect a profit on a short sale. 
	def StopOrder(self, action, quantity, stopPrice):
		order = Order()
		order.action = action
		order.orderType = "STP"
		order.totalQuantity = quantity
		order.auxPrice = stopPrice
		return order

	#! Stop Limit Order
	#? Will try to execute the order at the limit price executed, but no guarentees
	#? i.e. If the price drops a lot suddenly, it may not be able to stop loss/take profit at all
	def StopLimitOrder(self, action, quantity, stopPrice, limitPrice):
		order = Order()
		order.action = action
		order.orderType = "STP LMT"
		order.totalQuantity = quantity
		order.auxPrice = stopPrice
		order.lmtPrice = limitPrice
		return order

	#! Bracket Limit Order with Stop Loss and Take Profit
	def BracketLimitStopLossTakeProfit(self, action, quantity, limitPrice, takeProfitPrice, stopLossPrice):

		oppAction = "BUY" if action == "SELL" else "SELL"
		# Create Limit Order
		ParentOrder = self.LimitOrder(action=action, quantity=quantity, limitPrice=limitPrice)
		ParentOrder.orderId = self.nextorderId
		ParentOrder.transmit = False

		# Create Take Profit (Limit Order)
		TakeProfit = self.LimitOrder(action=oppAction, quantity=quantity, limitPrice=takeProfitPrice)
		TakeProfit.orderId = ParentOrder.orderId + 1
		TakeProfit.transmit = False
		TakeProfit.parentId = ParentOrder.orderId

		# Create Stop Loss (Stop Order)
		StopLoss = self.StopOrder(action=oppAction, quantity=quantity, stopPrice=stopLossPrice)
		StopLoss.orderId = ParentOrder.orderId + 2
		StopLoss.transmit = True
		StopLoss.parentId = ParentOrder.orderId

		bracketOrder = [ParentOrder, TakeProfit, StopLoss]
		return bracketOrder	

	def error(self, reqId, errorCode: int, errorString: str):
		super().error(reqId, errorCode, errorString)
		print("Error. Id:", reqId, "Code:", errorCode, "Msg:", errorString)

	def Stock_contract(self, symbol, secType='STK', exchange='SMART', currency='USD'):
		contract = Contract()
		contract.symbol = symbol
		contract.secType = secType
		contract.exchange = exchange
		contract.currency = currency
		return contract

	def buyOrder(self, tickerName, buySell, amount, takeProfit, stopLoss):
		bracket = self.BracketLimitStopLossTakeProfit("BUY", buySell, amount, takeProfit, stopLoss)
		for o in bracket:
			print("place order")
			app.placeOrder(o.orderId, self.Stock_contract(tickerName), o)
		time.sleep(3)
		print('Finished buy order')

if __name__ == '__main__':
	app = IBapi()
	app.Start()
	
	#Check if the API is connected via orderid
	while True:
		if isinstance(app.nextorderId, int):
			print('connected')
			print()
			break
		else:
			print('waiting for connection')
			time.sleep(1)
	print(app.nextorderId)

	# #Place orders
	app.buyOrder("MSFT", 100, 200, 210, 190)

	# #Cancel order 
	print('cancelling order')
	app.cancelOrder(app.nextorderId)
	time.sleep(3)

	app.disconnect()