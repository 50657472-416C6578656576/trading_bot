# trading_bot
### Бот для гребения денег лопатой


## О проекте
**Данный проект реализует торговлю на Binance с использованием различных стратегий, таких как *RSI, BOLL, EMA, MACD.*** 

В файле `algotrade_classes` определены классы `Strategy` и `Trader`, которые содержат реализации различных торговых стратегий и торговую логику соответственно.

*coming soon...*

## Планы
1. ~~Индикаторы и их комбинации~~
2. Интерфейс
3. Более гибкий менеджер торговли
4. Возможность получения сигнала от нейросети


## Уставновка и запуск
1. Установка зависимостей производится командой в директории проекта: `$ poetry install`
2. Создайте файл `.env` и запишите туда необходимые данные для запуска бота и клиента бинанс (их список можно найти в [config.py](trading_bot/config.py))
3. Запуск бота: `$ python3 trading_bot/telegram_trader.py`
