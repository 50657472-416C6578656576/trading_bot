import telebot
from telebot import types
from algotrade_classes import Trader

from config import Config

bot = telebot.TeleBot(Config.BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для торговли на Binance. Чтобы начать торговать, нажмите на кнопку ниже:",
        reply_markup=start_markup(),
    )


def start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    trade_button = types.KeyboardButton("/trade")
    markup.add(trade_button)
    return markup


@bot.message_handler(commands=["trade"])
def trade_message(message):
    bot.send_message(
        message.chat.id,
        "Выберите стратегию:",
        reply_markup=strategy_markup(),
    )


def strategy_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ema_button = types.KeyboardButton("ema")
    rsi_button = types.KeyboardButton("rsi")
    boll_button = types.KeyboardButton("boll")
    macd_button = types.KeyboardButton("macd")
    markup.add(ema_button, rsi_button, boll_button, macd_button)
    return markup


@bot.message_handler(func=lambda message: True)
def select_symbol(message):
    strategy = message.text.lower()
    if strategy in ["ema", "rsi", "boll", "macd"]:
        bot.send_message(
            message.chat.id, "Введите пару, например BTCUSDT:"
        )
        bot.register_next_step_handler(message, select_timeframe, strategy)
    else:
        bot.send_message(
            message.chat.id,
            "Неверная стратегия. Выберите одну из четырех стратегий (ema, rsi, boll или macd):",
            reply_markup=strategy_markup(),
        )


def select_timeframe(message, strategy):
    symbol = message.text.upper()
    bot.send_message(
        message.chat.id, "Введите временной интервал (например, 1h):",
    )
    bot.register_next_step_handler(message, start_trading, strategy, symbol)


def start_trading(message, strategy, symbol):
    timeframe = message.text.lower()
    bot.send_message(
        message.chat.id,
        f"Вы выбрали стратегию {strategy}, пару {symbol} и временной интервал {timeframe}. Начинаю торговлю!",
    )
    trader = Trader(
        Config.BINANCE_KEY, Config.BINANCE_SECRET, strategy, symbol, timeframe
    )
    trader.start_trading()


if __name__ == "__main__":
    bot.polling(none_stop=True)
