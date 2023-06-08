from trading_bot.Strategy import Strategy
import time
import logging
import pandas as pd
from binance.client import Client


class Trader:
    def __init__(
            self, 
            api_key: str, 
            secret_key: str, 
            symbol: str, 
            timeframe: str, 
            strategy_param: str, 
            balance: float | None = None
    ):
        self.client = Client(api_key, secret_key)
        self.strategy = Strategy()
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategy_param = strategy_param
        self.balance = balance
        self.profit = 0
        if balance is None:
            self.balance = self.get_balance_from_binance()

    def set_balance(self, new_balance):
        if self.client.get_asset_balance(asset=self.symbol)['free'] >= new_balance > 0:
            self.balance = new_balance
        else:
            self.balance = round(self.client.get_asset_balance(asset=self.symbol)['free'] / 2, 5)
            logging.warning(f'{self.symbol} balance is {self.balance}')

    def get_open_orders(self):
        return self.client.get_open_orders()

    def get_balance_from_binance(self):
        return self.client.get_asset_balance(asset=self.symbol)

    def get_closed_orders(self):
        return self.client.get_closed_orders()

    def get_balance(self):
        return self.balance

    def get_profit(self):
        return self.profit

    def cancel_all_orders(self):
        orders = self.client.get_open_orders()
        for order in orders:
            self.client.cancel_order(symbol=order['symbol'], orderId=order['orderId'])

    def set_strategy_param(self, param: str):
        self.strategy_param = param

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
        self.strategy.update_data(data)
        # Calculate signal
        signal = self.strategy.run_strategy(strategy_name=self.strategy_param)
        self.set_balance(self.balance)

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
                self.profit -= balance
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
                self.profit += self.balance
                self.balance = 0

        # Print current balance
        time.sleep(30)  # Wait 30 seconds before checking again

    def start_trading(self, predicate: bool = True):
        while True:
            try:
                self.trade()
            except Exception as ex:
                logging.warning(f'Caught exception: {ex}')
