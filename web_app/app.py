import json

from flask import Flask, request

from trading_bot import Trader

app = Flask(__name__)


@app.route('/home')
def hello_world():
    return json.dumps({
        'data': 'Hello world!'
    })


@app.route('/start_trading', methods=['POST'])
def start_trading():
    data = request.get_json(force=True)
    api_key, secret, strategy, symbol, timeframe = \
        data['api_key'], data['secret'], data['strategy'], data['symbol'], data['timeframe']
    trader = Trader(api_key, secret, strategy, symbol, timeframe)
    thread = Thread(target=trader.start_trading)
    # thread.daemon = True
    thread.start()
    return json.dumps({
        'thread': f'{thread.}',
        'data': data
    })
