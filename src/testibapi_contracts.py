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

	def error(self, reqId, errorCode: int, errorString: str):
		super().error(reqId, errorCode, errorString)
		print("Error. Id:", reqId, "Code:", errorCode, "Msg:", errorString)
	
	def contractDetails(self, reqId: int, contractDetails):
		self.contract_details[reqId] = contractDetails

	def get_contract_details(self, reqId, contract):
		self.contract_details[reqId] = None
		self.reqContractDetails(reqId, contract)
		#Error checking loop - breaks from loop once contract details are obtained
		for err_check in range(50):
			if not self.contract_details[reqId]:
				time.sleep(0.1)
			else:
				break
		#Raise if error checking loop count maxed out (contract details not obtained)
		if err_check == 49:
			raise Exception('error getting contract details')
		#Return contract details otherwise
		return app.contract_details[reqId].contract
		
	def symbolSamples(self, reqId: int,contractDescriptions):
		super().symbolSamples(reqId, contractDescriptions)
		print("Symbol Samples. Request Id: ", reqId)

		for contractDescription in contractDescriptions:
			derivSecTypes = ""
			for derivSecType in contractDescription.derivativeSecTypes:
				derivSecTypes += derivSecType
				derivSecTypes += " "
			print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, "
					"currency:%s, derivativeSecTypes:%s" % (
				contractDescription.contract.conId,
				contractDescription.contract.symbol,
				contractDescription.contract.secType,
				contractDescription.contract.primaryExchange,
				contractDescription.contract.currency, derivSecTypes))

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

if __name__ == '__main__':
	app = IBapi()
	app.connect('127.0.0.1', 7497, 123)

	#Start the socket in a thread
	api_thread = threading.Thread(target=run_loop, daemon=True)
	api_thread.start()

	#Check if the API is connected via orderid
	app.reqMatchingSymbols(211, "IB")
	time.sleep(1)
	app.disconnect()