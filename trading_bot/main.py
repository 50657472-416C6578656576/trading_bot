import argparse
from algotrade_classes import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api_key', type=str, help='Binance API Key')
    parser.add_argument('--secret_key', type=str, help='Binance Secret Key')
    parser.add_argument('--strategy', type=str, help='Trading strategy (ema, rsi, boll)')
    parser.add_argument('--symbol', type=str, help='Symbol to trade (e.g. BTCUSDT)')
    parser.add_argument('--timeframe', type=str, default='1m', help='Kline timeframe (default: 1m)')
    parser.add_argument('--strategy_papam', type=str, default='boll', help='Model of trading (default: boll)')
    args = parser.parse_args()

    # Initialize trading objects
    trader = Trader(api_key=args.api_key, secret_key=args.secret_key, symbol=args.symbol, timeframe=args.timeframe, strategy_param=args.strategy_param)

    # Start trading
    trader.start_trading()
