# trading_bot
## Бот для гребения денег лопатой

**Данный проект реализует торговлю на Binance с использованием различных стратегий, таких как *RSI, BOLL, EMA, MACD.* В файле `algotrade_classes` определены классы `Strategy` и `Trader`, которые содержат реализации различных торговых стратегий и торговую логику соответственно.

В файле `transaction_status` происходит чтение лог-файла `transaction.log`, где хранятся все сделки, и отправка их статуса в Telegram.

В файле `telegrambot` определены функции для работы с Telegram API, которые позволяют пользователю выбрать стратегию, пару и временной интервал и начать торговлю.**
