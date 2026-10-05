import time
from queue import Queue

from PySide6.QtCore import Signal, QObject


class CommunicationSignals(QObject):
    # ??????,str??????????????
    data_received = Signal(int)

    def emit_(self, data):
        print('??????', data)
        self.data_received.emit(data)


class QueueSender:
    _instance = None
    _is_init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, queue=None):
        if not hasattr(self, 'queue'):  # ???????
            self.queue = queue or Queue()

    def send_data(self, data):
        print(f"Sender: ???? {data}")
        self.queue.put(data)


class QueueReceiver(QObject):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, queue, signal):
        super().__init__()
        self.queue = queue
        self.signal = signal
        self._running = True

    def receive_data(self):
        while self._running:
            if not self.queue.empty():
                data = self.queue.get()
                print(f"Receiver: ????? {type(data), data}")
                # ????
                self.signal.emit_(data)
                # self.signal.data_received.emit(data)
                self.queue.task_done()
            time.sleep(0.1)  # ??CPU????

    def set_stop(self):
        self._running = False

    def set_start(self):
        self._running = True


# ????????,????????
# ???????????
shared_queue = Queue()
signals_communication = CommunicationSignals()

# ??????
queue_sender = QueueSender(shared_queue)
queue_receiver = QueueReceiver(shared_queue, signals_communication)


# ??????
# receiver_thread = Thread(target=queue_receiver.receive_data)


# ??????
def get_sender():
    """???????"""
    return queue_sender


def get_receiver():
    """???????"""
    return queue_receiver


# def get_receiver_thread():
#     """??????"""
#     return receiver_thread
def get_signals():
    """??????"""
    return signals_communication
