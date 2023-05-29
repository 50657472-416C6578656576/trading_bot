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

    def start_trading(self):
        while True:
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
