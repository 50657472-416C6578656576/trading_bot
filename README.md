# trading_bot
### Бот для гребения денег лопатой


## О проекте
### Фронт, подключенный к АПИ, [захощен, можно потыкать](http://158.160.28.97:3000/) его, но осторожно - подключение возможно пока что только по http :)

**Данный проект реализует торговлю на Binance с использованием различных стратегий, таких как *RSI, BOLL, EMA, MACD.*** 

**В файле `algotrade_classes` определены классы `Strategy` и `Trader`.**

Класс `Strategy` содержит в себе индикаторы технического анализа, стратегии торговли.

Класс `trader` по сути является виртуальным менеджером торговли.

## Планы
1. ~~Индикаторы и их комбинации~~
2. Интерфейс *в процессе разработки*
3. Предсказание цены актива нейросетью
4. Возможность вести торговл на нескольких валютных парах
5. Добавление новых бирж
6. Рынок фьючерсов
7. Тикер-инфо (валотильность пар, комиссионные пары, пары с высоким/низким риском)
8. Рекомендательная система

## Уставновка и запуск
### Основной флоу
1. Установка зависимостей производится командой в директории проекта: 
   ```bash
   $ poetry install
   ```
2. Запуск бэкенда (АПИ):
   ```bash
   $ python3 web_app
   ```
3. Запуск фронтенда (веб-клиента) из директории `web_app_fron/`:
   ```bash
   $ npm install && npm start
   ```
### Установка ta-lib (если возникают проблемы)
1. Перейти в директорию [ta-lib](./ta-lib)
2. Выполнить следующие действия:
    ```bash
    $ ./configure && make && sudo make install && pip install ta-lib
    ```
