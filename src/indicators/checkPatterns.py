from talib import CDLIDENTICAL3CROWS, CDL3BLACKCROWS, CDL3WHITESOLDIERS, CDLMORNINGSTAR, CDLEVENINGSTAR
from talib import CDL3LINESTRIKE, CDLMORNINGDOJISTAR, CDLEVENINGDOJISTAR, CDL3OUTSIDE, CDLENGULFING
from talib import CDLBELTHOLD, CDLABANDONEDBABY, CDL3INSIDE, CDLPIERCING, CDLDARKCLOUDCOVER
from talib import CDLBREAKAWAY,CDLXSIDEGAP3METHODS, CDLHAMMER, CDLSHOOTINGSTAR, CDLCONCEALBABYSWALL
from talib import CDLDOJISTAR, CDLRISEFALL3METHODS, CDLSEPARATINGLINES, CDLADVANCEBLOCK, CDLHANGINGMAN
from talib import CDLINVERTEDHAMMER, CDLMATCHINGLOW, CDLSTICKSANDWICH, CDLUNIQUE3RIVER, CDLUPSIDEGAP2CROWS

def check(df):
    ## a. checkpatterns
    cdlInput = df
    cdlInput = cdlInput.iloc[::-1]
    aa = cdlInput['open'].values
    ab = cdlInput['high'].values
    ac = cdlInput['low'].values
    ad = cdlInput['close'].values

    # Strong Candlestick Patterns
    output3BC = CDL3BLACKCROWS(aa,ab,ac,ad)
    output3WS = CDL3WHITESOLDIERS(aa,ab,ac,ad)
    outputCBS = CDLCONCEALBABYSWALL(aa,ab,ac,ad)
    outputES = CDLEVENINGSTAR(aa,ab,ac,ad)
    outputI3C = CDLIDENTICAL3CROWS(aa,ab,ac,ad)
    outputMS = CDLMORNINGSTAR(aa,ab,ac,ad)

    #Reliable Candlestick Patterns
    output3LS = CDL3LINESTRIKE(aa,ab,ac,ad)
    output3O = CDL3OUTSIDE(aa,ab,ac,ad)
    outputAB = CDLABANDONEDBABY(aa,ab,ac,ad)
    outputBH = CDLBELTHOLD(aa,ab,ac,ad)
    outputDS = CDLDOJISTAR(aa,ab,ac,ad)
    outputE = CDLENGULFING(aa,ab,ac,ad)
    outputMDS = CDLMORNINGDOJISTAR(aa,ab,ac,ad)
    outputEDS = CDLEVENINGDOJISTAR(aa,ab,ac,ad)
    outputRF3M = CDLRISEFALL3METHODS(aa,ab,ac,ad)
    outputSL = CDLSEPARATINGLINES(aa,ab,ac,ad)

    #Weak Candlestick Patterns
    output3I = CDL3INSIDE(aa,ab,ac,ad)
    outputADVB = CDLADVANCEBLOCK(aa,ab,ac,ad)
    outputB = CDLBREAKAWAY(aa,ab,ac,ad)
    outputDCC = CDLDARKCLOUDCOVER(aa,ab,ac,ad)
    outputH = CDLHAMMER(aa,ab,ac,ad)
    outputHM = CDLHANGINGMAN(aa,ab,ac,ad)
    outputIH = CDLINVERTEDHAMMER(aa,ab,ac,ad)
    outputML = CDLMATCHINGLOW(aa,ab,ac,ad)
    outputP = CDLPIERCING(aa,ab,ac,ad)
    outputSS = CDLSHOOTINGSTAR(aa,ab,ac,ad)
    outputSSW = CDLSTICKSANDWICH(aa,ab,ac,ad)
    outputU3R = CDLUNIQUE3RIVER(aa,ab,ac,ad)
    outputUG2C = CDLUPSIDEGAP2CROWS(aa,ab,ac,ad)
    outputXSG3M = CDLXSIDEGAP3METHODS(aa,ab,ac,ad)

    if output3LS[-1] > 0:
        pattern = 1.84*1.3
        patterntype = -1
    elif output3LS[-1] < 0:
        pattern = -1.65*1.3
        patterntype = -1
    elif output3O[-1] > 0:
        pattern = 1.75*1.3
        patterntype = -1
    elif output3O[-1] < 0:
        pattern = -1.69*1.3
        patterntype = -1
    elif outputAB[-1] > 0:
        pattern = 1.7*1.3
        patterntype = -1
    elif outputAB[-1] < 0:
        pattern = -1.69*1.3
        patterntype = -1
    elif outputBH[-1] >0:
        pattern = 1.71*1.3
        patterntype = -1
    elif outputBH[-1] <0:
        pattern = -1.68*1.3
        patterntype = -1
    elif outputDS[-1] >0:
        pattern = 1.69*1.3
        patterntype = 1
    elif outputDS[-1] < 0:
        pattern = -1.64*1.3
        patterntype = 1
    elif outputE[-1] >0:
        pattern = 1.63*1.3
        patterntype = -1
    elif outputE[-1] <0:
        pattern = 1.79*1.3
        patterntype = -1
    elif outputEDS[-1] <0:
        pattern = -1.71*1.3
        patterntype = -1
    elif outputMDS[-1] >0:
        pattern = 1.76*1.3
        patterntype = -1
    elif outputRF3M[-1] >0:
        pattern = 1.74*1.3
        patterntype = 1
    elif outputRF3M[-1] <0:
        pattern = -1.71*1.3
        patterntype = 1
    elif outputSL[-1] >0:
        pattern = 1.72*1.3
        patterntype = 1
    elif outputSL[-1] < 0:
        pattern = -1.63*1.3
        patterntype = 1
    elif output3BC[-1] < 0:
        pattern = -1.78*1.5
        patterntype = -1
    elif output3WS[-1] >0:
        pattern = 1.83*1.5
        patterntype = -1
    elif outputCBS[-1] <0:
        pattern = -1.75*1.5
        patterntype = 1
    elif outputES[-1] <0:
        pattern = -1.72*1.5
        patterntype = -1
    elif outputI3C[-1] < 0:
        pattern = -1.79*1.5
        patterntype = -1
    elif outputMS[-1] >0:
        pattern = 1.78*1.5
        patterntype = -1
    elif output3I[-1] >0:
        pattern = 1.65*1.1
        patterntype = -1
    elif output3I[-1] <0:
        pattern = 1.6*1.1
        patterntype = -1
    elif outputADVB[-1] >0:
        pattern = 1.64*1.1
        patterntype = 1
    elif outputB[-1] >0:
        pattern = 1.59*1.1
        patterntype = -1
    elif outputB[-1]<0:
        pattern = -1.63*1.1
        patterntype = -1
    elif outputDCC[-1] <0:
        pattern = -1.6*1.1
        patterntype = -1
    elif outputH[-1] >0:
        pattern = 1.6*1.1
        patterntype = -1
    elif outputHM[-1] >0:
        pattern = 1.59*1.1
        patterntype = 1
    elif outputIH[-1] <0:
        pattern = -1.65*1.1
        patterntype = 1
    elif outputML[-1] < 0:
        pattern = -1.61*1.1
        patterntype = 1
    elif outputP[-1] >0:
        pattern = 1.64*1.1
        patterntype = -1
    elif outputSS[-1] <0:
        pattern = -1.59*1.1
        patterntype = -1
    elif outputSSW[-1] <0:
        pattern = -1.62*1.1
        patterntype = 1
    elif outputU3R[-1] < 0:
        pattern = -1.6*1.1
        patterntype = 1
    elif outputUG2C[-1] >0:
        pattern = 1.6*1.1
        patterntype = 1
    elif outputXSG3M[-1] > 0:
        pattern = 1.62*1.1
        patterntype = -1
    elif outputXSG3M[-1] <0:
        pattern = -1.59*1.1
        patterntype = -1
    else: 
        pattern = 0
        patterntype = 0

    return [pattern,patterntype]
    # if output3BC[-1] > 0 or output3WS[-1] > 0 + outputCBS[-1] > 0 or outputES[-1] > 0 or outputI3C[-1] > 0 or outputMS[-1] > 0:
    #     pattern = 1.5
    # elif output3BC[-1] < 0 or output3WS[-1] < 0 + outputCBS[-1] < 0 or outputES[-1] < 0 or outputI3C[-1] < 0 or outputMS[-1] < 0:
    #     pattern = -1.5
    # elif output3LS[-1] > 0 or output3O[-1] > 0 or outputAB[-1] > 0 or outputBH[-1] > 0 or outputDS[-1] > 0 or outputE[-1] > 0 or outputMDS[-1] > 0 or outputEDS[-1] > 0 or outputRF3M[-1] > 0 or outputSL[-1] > 0:
    #     pattern = 1.3
    # elif output3LS[-1] < 0 or output3O[-1] < 0 or outputAB[-1] < 0 or outputBH[-1] < 0 or outputDS[-1] < 0 or outputE[-1] < 0 or outputMDS[-1] < 0 or outputEDS[-1] < 0 or outputRF3M[-1] < 0 or outputSL[-1] < 0:
    #     pattern = -1.3
    # elif output3I[-1] > 0 or outputADVB[-1] > 0 or outputB[-1] > 0 or outputDCC[-1] > 0 or outputH[-1] > 0 or outputHM[-1] > 0 or outputIH[-1] > 0 or outputML[-1] > 0 or outputP[-1] > 0 or outputSS[-1] > 0 or outputSSW[-1] > 0 or outputU3R[-1] > 0 or outputUG2C[-1] > 0 or outputXSG3M[-1] > 0:
    #     pattern = 1.1
    # elif output3I[-1] < 0 or outputADVB[-1] < 0 or outputB[-1] < 0 or outputDCC[-1] < 0 or outputH[-1] < 0 or outputHM[-1] < 0 or outputIH[-1] < 0 or outputML[-1] < 0 or outputP[-1] < 0 or outputSS[-1] < 0 or outputSSW[-1] < 0 or outputU3R[-1] < 0 or outputUG2C[-1] < 0 or outputXSG3M[-1] < 0:
    #     pattern = -1.1
    # else: pattern = 0