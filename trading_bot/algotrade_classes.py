import pandas as pd
import talib
import time
import logging
import subprocess
from binance.client import Client

from .bot import bot
from .config import Config


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
    
    def macd_boll(self, period, width = 20):
        """ Moving Average Convergence Divergence and Bollinger Bands strategy """
        macd, macdsignal, macdhist = talib.MACD(self.data['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        upperband, middleband, lowerband = talib.BBANDS(self.data['close'], timeperiod=period, matype=talib.MA_Type.SMA, nbdev=width)
        # Check for buy and sell signals
        self.data['signal'] = 0
        self.data.loc[(macdhist > 0) & (self.data['close'] > upperband) & (macdsignal < 0), 'signal'] = 1
        self.data.loc[(macdhist < 0) & (self.data['close'] < lowerband) & (macdsignal > 0), 'signal'] = -1
        return self.data['signal']

class Trader:
    def __init__(self, API_KEY, SECRET_KEY, strategy, symbol, timeframe):
        self.client = Client(API_KEY, SECRET_KEY)
        self.strategy = strategy
        self.symbol = symbol
        self.timeframe = timeframe
        self.balance = self.get_balance()
        self.last_balance = self.balance
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('transaction.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_balance(self):
        account = self.client.get_account()
        for balance in account['balances']:
            if balance['asset'] == self.symbol.split('USDT')[0]:
                return float(balance['free'])
            
    def get_logs(self):
        return self.client.get_logs()
    
    def stop_trading(self):
        self.client.cancel_all_orders()
        self.logger.info('Trading stopped')

    def start_trading(self, predicate : bool = True):
        while (predicate): # predicate such as True. Example: if balance < 1000 USBT 
            try:
                # Get historical klines data
                klines = self.client.get_historical_klines(self.symbol, self.timeframe, "1000 minutes ago UTC")
                data = pd.DataFrame(
                    klines, columns=[
                        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close time',
                        'quote asset volume', 'number of trades', 'taker buy base asset volume',
                        'taker buy quote asset volume', 'ignore'
                    ],
                )
                data = data.astype(float)
                data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
                data.set_index('timestamp', inplace=True)

                # Calculate signal
                if self.strategy == 'ema':
                    signal = Strategy(data).ema(period=20)
                elif self.strategy == 'rsi':
                    signal = Strategy(data).rsi(period=14)
                elif self.strategy == 'boll':
                    signal = Strategy(data).boll(period=20)
                elif self.strategy == 'rsi_or_boll':
                    signal = Strategy(data).rsi_or_boll(period=14)
                elif self.strategy == 'macd':
                    signal = Strategy(data).macd(period=20)
                elif self.strategy == 'macd_boll':
                    signal = Strategy(data).macd_boll(period=20, width=20)
                elif self.strategy == 'ema_boll':
                    signal = Strategy(data).ema_boll(period=20, width=20)
                elif self.strategy == 'sma_boll':
                    signal = Strategy(data).sma_boll(period=20, width=20)
                elif self.strategy == 'rsi_ema_boll':
                    signal = Strategy(data).rsi_ema_boll(period=14, ema_period=20, boll_period=20)
                elif self.strategy == 'sma':
                    signal = Strategy(data).sma(period=20)
                elif self.strategy == 'rsi_or_sma':
                    signal = Strategy(data).rsi_or_sma(period=14)
                elif self.strategy == 'boll_or_sma':
                    signal = Strategy(data).boll_or_sma(period=20)
                else:
                    raise ValueError('Invalid strategy!')

                # Check for buy and sell
                if signal.iloc[-1] == 1:        # Buy
                    balance = self.get_balance()
                    if balance > 0:
                        order = self.client.create_order(
                            symbol=self.symbol,
                            side=Client.SIDE_BUY,
                            type=Client.ORDER_TYPE_MARKET,
                            quantity=balance
                        )
                        self.last_balance = self.balance
                        self.balance -= balance
                        self.logger.info(f'Buy {balance} {self.symbol} at {order.get("price")}')
                        bot.send_message(
                            chat_id=Config.telegram_chat_id,
                            text=f'Buy {balance} {self.symbol} at {order.get("price")}',
                        )

                elif signal.iloc[-1] == -1:     # Sell
                    if self.balance > 0:
                        order = self.client.create_order(
                            symbol=self.symbol,
                            side=Client.SIDE_SELL, 
                            type=Client.ORDER_TYPE_MARKET,
                            quantity=self.balance
                        )
                        self.last_balance = self.balance
                        self.balance = 0
                        self.logger.info(f'Sell {self.last_balance} {self.symbol} at {order.get("price")}')
                        bot.send_message(
                            chat_id=Config.TELEGRAM_CHAT_ID,
                            text=f'Sell {self.last_balance} {self.symbol} at {order.get("price")}',
                        )

                # Print current balance
                self.logger.debug(f'Current balance of {self.symbol}: {self.balance}')
                # Get transaction status
                subprocess.run(['python', 'transaction_status.py'])
                time.sleep(30)  # Wait 30 seconds before checking again

            except Exception as ex:
                logging.warning(f'Caught exception: {ex}')
                bot.send_message(
                    chat_id=Config.telegram_chat_id,
                    text=f'Caught exception: {ex}',
                )
