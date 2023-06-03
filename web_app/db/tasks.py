import logging
from threading import Thread

from trading_bot import Trader


TASKS: dict = dict()


class TraderTask:
    def __init__(self, user_id: str, api_key: str, secret: str, *args, **kwargs):
        self.user_id = user_id
        TASKS[self.user_id] = self
        self.trader: Trader = Trader(api_key, secret, *args, **kwargs)
        self.thread: Thread | None = None
        self.is_running = False

    def __run(self):
        while self.is_running:
            self.trader.trade()
        self.thread.join()

    def run(self):
        if self.thread is None:
            self.thread = Thread(target=self.__run)
            self.thread.start()

    def stop(self):
        self.is_running = False
        self.thread = None
