import logging

from .telegram_trader import bot
from .config import Config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('transaction.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

with open('transaction.log', 'r') as f:
    transactions = f.readlines()

transactions_status = []
for transaction in transactions:
    if 'Buy' in transaction:
        transactions_status.append(f'{transaction.strip()} - Открыто')
    else:
        transactions_status.append(f'{transaction.strip()} - Закрыто')

text = '\\n'.join(transactions_status)
bot.send_message(chat_id=Config.TELEGRAM_CHAT_ID, text=text)
