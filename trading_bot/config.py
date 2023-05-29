from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    BINANCE_KEY = os.getenv('BINANCE_KEY')
    BINANCE_SECRET = os.getenv('BINANCE_SECRET')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
