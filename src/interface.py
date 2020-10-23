from datetime import datetime
from backTester import backTester
from main import mainfn
from createFolders import createFolders
import time

if __name__ == '__main__':
    while(1):
        print("This is the interface for traderBot.")
        print("1. backTest")
        print("2. Transfer indicator Scores to Swing Trade")
        command = input("What function do you want to call?")
        if command == "1":
            print("Running backTest")
            createFolders(0)
            backTester()
        elif command == "2":
            print("Are you sure?! This will remove all data from previous swingTrades")
            print("Transferring Indicator Scores to Swing Trade")
        else: print("Invalid Command")


    
