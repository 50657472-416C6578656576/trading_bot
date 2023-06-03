import threading
import uuid


class TaskThread(threading.Thread):
    THREADS = dict()

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.id = str(uuid.uuid4())

    def run(self, *args, **kwargs):
        threading.Thread.start(self)

    # def stop(self):
    #     threading.

    def get_id(self) -> str:
        return self.id
