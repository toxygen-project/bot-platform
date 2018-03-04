import threading
import queue
from core.util import log


class FileTransfersThread(threading.Thread):

    def __init__(self):
        self._queue = queue.Queue()
        self._timeout = 0.1
        self._continue = True
        super().__init__()

    def execute(self, func, *args, **kwargs):
        self._queue.put((func, args, kwargs))

    def stop(self):
        self._continue = False

    def run(self):
        while self._continue:
            try:
                func, args, kwargs = self._queue.get(timeout=self._timeout)
                func(*args, **kwargs)
            except queue.Empty:
                pass
            except queue.Full:
                log('Queue is full in ft thread')
            except Exception as ex:
                log('Exception in ft thread: ' + str(ex))


_thread = FileTransfersThread()


def start():
    _thread.start()


def stop():
    _thread.stop()
    _thread.join()


def execute(func, *args, **kwargs):
    _thread.execute(func, *args, **kwargs)
