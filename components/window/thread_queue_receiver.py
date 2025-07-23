# 接受queue的子线程
from PySide6.QtCore import QThread, Signal

from common import function_queue


class ThreadQueueReceiver(QThread):
    Data = Signal(int)

    def __init__(self):
        super().__init__()
        self.receiver = function_queue.get_receiver()
        self.signal = function_queue.get_signals()

        self.signal.data_received.connect(self.emit_)

    def run(self):
        self.receiver.receive_data()

    def stop(self):
        self.receiver.set_stop()

    def start_(self):
        self.receiver.set_start()
        self.run()

    def emit_(self, data):
        self.Data.emit(data)
