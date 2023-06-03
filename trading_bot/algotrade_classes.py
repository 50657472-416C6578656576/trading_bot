from trading_bot.Strategy import Strategy
import time
import logging
import pandas as pd
from binance.client import Client


class Trader:
    def __init__(self, *args):
        self.args = args

    def start_trading(self):
        while True:
            print(', '.join(list(map(str, self.args))))

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

    def get_open_orders(self):
        return self.client.get_open_orders()

    def get_closed_orders(self):
        return self.client.get_closed_orders()

#     def stop_trading(self):
#         self.client.cancel_all_orders()
#         self.logger.info('Trading stopped')

    def trade(self):
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
        if signal.iloc[-1] == 1:  # Buy
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

        elif signal.iloc[-1] == -1:  # Sell
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

        # Print current balance
        self.logger.debug(f'Current balance of {self.symbol}: {self.balance}')
        time.sleep(30)  # Wait 30 seconds before checking again

    def start_trading(self, predicate: bool = True):
        while (predicate): # predicate such as True. Example: if balance < 1000 USBT
            try:
                self.trade()
            except Exception as ex:
                logging.warning(f'Caught exception: {ex}')
