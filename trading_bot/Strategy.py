import pandas as pd
import talib

class Strategy:
    def __init__(self, data):
        self.data = data

    def ema(self, period):
        """ Exponential Moving Average strategy """
        ema = talib.EMA(self.data['close'], timeperiod=period)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[self.data['close'] > ema, 'signal'] = 1
        self.data.loc[self.data['close'] < ema, 'signal'] = -1
        return self.data['signal']

    def rsi(self, period):
        """ Relative Strength Index strategy """
        rsi = talib.RSI(self.data['close'], timeperiod=period)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[rsi < 30, 'signal'] = 1
        self.data.loc[rsi > 70, 'signal'] = -1
        return self.data['signal']

    def boll(self, period):
        """ Bollinger Bands strategy """
        upperband, middleband, lowerband = talib.BBANDS(self.data['close'], timeperiod=period)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[self.data['close'] > upperband, 'signal'] = -1
        self.data.loc[self.data['close'] < lowerband, 'signal'] = 1
        return self.data['signal']

    def macd(self, period):
        """ Moving Average Convergence Divergence strategy """
        macd, macdsignal, macdhist = talib.MACD(self.data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[macdhist > 0, 'signal'] = 1
        self.data.loc[macdhist < 0, 'signal'] = -1
        return self.data['signal']
    
    def sma(self, period):
        """ Simple Moving Average strategy """
        sma = talib.SMA(self.data['close'], timeperiod=period)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[self.data['close'] > sma, 'signal'] = 1
        self.data.loc[self.data['close'] < sma, 'signal'] = -1
        return self.data['signal']

    def mae(self, period, width = 20):
        """ Moving Average Envelope strategy """
        upperband, lowerband = talib.MAEnvelopes(self.data['close'], timeperiod=period, matype=talib.MA_Type.SMA, nbdev=width)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[self.data['close'] > upperband, 'signal'] = -1
        self.data.loc[self.data['close'] < lowerband, 'signal'] = 1
        return self.data['signal']

    def rsi_ema(self, rsi_period = 14, ema_period = 20):
        """ RSI and EMA strategy """
        rsi = talib.RSI(self.data['close'], timeperiod=rsi_period)
        ema = talib.EMA(self.data['close'], timeperiod=ema_period)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[(self.data['close'] > ema) & (rsi < 30), 'signal'] = 1
        self.data.loc[(self.data['close'] < ema) & (rsi > 70), 'signal'] = -1
        return self.data['signal']

    def rsi_or_ema(self, rsi_period = 14, ema_period = 20):
        """ RSI or EMA strategy """
        rsi = talib.RSI(self.data['close'], timeperiod=rsi_period)
        ema = talib.EMA(self.data['close'], timeperiod=ema_period)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[(self.data['close'] > ema) | (rsi < 30), 'signal'] = 1
        self.data.loc[(self.data['close'] < ema) | (rsi > 70), 'signal'] = -1
        return self.data['signal']
    
    def rsi_boll(self, rsi_period = 14, boll_period = 20):
        """ RSI and Bollinger Bands strategy """
        rsi = talib.RSI(self.data['close'], timeperiod=rsi_period)
        upperband, middleband, lowerband = talib.BBANDS(self.data['close'], timeperiod=boll_period)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[(self.data['close'] > upperband) & (rsi < 30), 'signal'] = 1
        self.data.loc[(self.data['close'] < lowerband) & (rsi > 70), 'signal'] = -1
        return self.data['signal']
    
    def rsi_or_boll(self, rsi_period = 14, boll_period = 20):
        """ RSI or Bollinger Bands strategy """
        rsi = talib.RSI(self.data['close'], timeperiod=rsi_period)
        upperband, middleband, lowerband = talib.BBANDS(self.data['close'], timeperiod=boll_period)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[(self.data['close'] > upperband) | (rsi < 30), 'signal'] = 1
        self.data.loc[(self.data['close'] < lowerband) | (rsi > 70), 'signal'] = -1
        return self.data['signal']
    
    def rsi_ema_boll(self, rsi_period = 14, ema_period = 20, boll_period = 20):
        """ RSI and EMA and Bollinger Bands strategy """
        rsi = talib.RSI(self.data['close'], timeperiod=rsi_period)
        ema = talib.EMA(self.data['close'], timeperiod=ema_period)
        upperband, middleband, lowerband = talib.BBANDS(self.data['close'], timeperiod=boll_period)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[(self.data['close'] > ema) & (self.data['close'] > upperband) & (rsi < 30), 'signal'] = 1
        self.data.loc[(self.data['close'] < ema) & (self.data['close'] < lowerband) & (rsi > 70), 'signal'] = -1
        return self.data['signal']
    
    def macd_boll(self, period = 20, width = 20):
        """ Moving Average Convergence Divergence and Bollinger Bands strategy """
        macd, macdsignal, macdhist = talib.MACD(self.data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        upperband, middleband, lowerband = talib.BBANDS(self.data['close'], timeperiod=period, matype=talib.MA_Type.SMA, nbdev=width)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[(macdhist > 0) & (self.data['close'] > upperband) & (macdsignal < 0), 'signal'] = 1
        self.data.loc[(macdhist < 0) & (self.data['close'] < lowerband) & (macdsignal > 0), 'signal'] = -1
        return self.data['signal']
