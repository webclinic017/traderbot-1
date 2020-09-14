from ibapi.client import EClient
from ibapi.wrapper import EWrapper

import threading
import time

# TODO 
# Make a base class of ibAPI with the generic function names in case we 
# switch to a differnt platform in the future
#class Platform():

#Empty 'struct' for Contracts and Orders
class Contract():
    pass

class Order():
    pass

class ibAPI(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def connectPlatform(self):
        self.connect('127.0.0.1', 7497, 1) # Change port no to match port no in IB settings

    def disconnecPlatform(self):
        self.disconnect()

    def isConnected(self):
        return self.isConnected()

    #General fn
    def Start(self):
        while not self.isConnected():
            print("Connecting to IB Host...")
            self.connectPlatform()
            time.sleep(1)
        print("Starting IB API Thread...")
        ibAPIthread = threading.Thread(target=self.run, daemon=True)
        ibAPIthread.start()
        
    # Market Orders

    def CreateContract(self, security, securityType='STK', exchange='IDEALPRO', currency='USD'):
        contract = Contract()
        contract.symbol = security
        contract.secType = securityType
        contract.exchange = exchange
        contract.currency = currency
        return contract

    # Orders
    # https://interactivebrokers.github.io/tws-api/basic_orders.html

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

    #! Trailing Stop
    def TrailingStopOrder(self, action, quantity, isPercentage:bool, trailingAmount, trailStopPrice):
        order = Order()
        order.action = action
        order.orderType = "TRAIL"
        order.totalQuantity = quantity
        order.trailStopPrice = trailStopPrice
        if isPercentage:
            order.trailingPercent = trailingAmount
        else:
            order.auxPrice = trailingAmount
        return order
    
    #! Trailing Stop Limit
    def TrailingStopLimitOrder(self, action, quantity, isPercentage:bool, trailingAmount, trailStopPrice, lmtPriceOffset):
        order = Order()
        order.action = action
        order.orderType = "TRAIL LIMIT"
        order.totalQuantity = quantity
        order.trailStopPrice = trailStopPrice
        order.lmtPriceOffset = lmtPriceOffset
        if isPercentage:
            order.trailingPercent = trailingAmount
        else:
            order.auxPrice = trailingAmount
        return order

    # IB does not directly have an order that can set a buy/sell price, stop loss price and take profit price at once
    # so we need to chain 3 orders together
    # TODO Check that once one of the child orders execute, the other child order cancells automatically

    #! Bracket Limit Order with Stop Loss and Take Profit
    def BracketLimitStopLossTakeProfit(self, action, quantity, limitPrice, takeProfitPrice, stopLossPrice):
        oppAction = "BUY" if action == "SELL" else "SELL"
        # Create Limit Order
        ParentOrder = self.LimitOrder(action=action, quantity=quantity, limitPrice=limitPrice)
        ParentOrder.orderID = self.reqIds(1)
        ParentOrder.transmit = False

        # Create Take Profit (Limit Order)
        TakeProfit = self.LimitOrder(action=oppAction, quantity=quantity, limitPrice=takeProfitPrice)
        TakeProfit.orderID = ParentOrder.orderID + 1
        TakeProfit.transmit = False

        # Create Stop Loss (Stop Order)
        StopLoss = self.StopOrder(action=oppAction, quantity=quantity, stopPrice=stopLossPrice)
        StopLoss.orderID = ParentOrder.orderID + 2
        StopLoss.transmit = True

        bracketOrder = [ParentOrder, TakeProfit, StopLoss]
        return bracketOrder

    #! Custom Bracket Order
    def CustomBracketOrder(self, Parent, Child1, Child2):
        Parent.orderID = self.reqIds(1)
        Parent.transmit = False
        Child1.orderID = Parent.orderID + 1
        Child1.transmit = False
        Child2.orderID = Parent.orderID + 2
        Child2.transmit = True
        bracketOrder = [Parent, Child1, Child2]
        return bracketOrder
