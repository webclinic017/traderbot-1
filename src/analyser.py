class Analyser():
    def __init__(self, tickerName, comparator):
        self.tickerName = tickerName
        self.comparator = comparator
    
    def inform(self, timeStamp):
        # TO-DO: Looks through currently trading file
        # TO-DO: If ticker is currently trading, do intervalAnalysis
        pass
    
    def PseudoTrade(self, timeStamp, strategy, result, atr):
        # print("Adding pseudo trade for " + self.tickerName + " at " + timeStamp + " (" + strategy + ")")
        # TO-DO: Create new unique ID (ticker name + counter)
        pass
        ### TO-DO: Save information into a CSV database full of pseudotrades

    def intervalAnalysis(self):
        # TO-DO: Read from pseudotrades database
        for trade in pseudoTrades:
            # TO-DO: Analyses whether the trade has succeeded or failed for each trade
            if successfulTrade:
                self.comparator.updateWeightage("strategy (placeholder)", "+1 point (placeholder)")
            elif failedTrade:
                self.comparator.updateWeightage("strategy (placeholder)", "-1 point (placeholder)")

