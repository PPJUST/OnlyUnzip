# 接收 queue 的子线程
from PySide6.QtCore import QThread, Signal

from common import function_queue


class ThreadQueueReceiver(QThread):
    """从队列接收解压进度并发送信号"""

    Data = Signal(int)

    def __init__(self):
        super().__init__()
        self.receiver = function_queue.get_receiver()
        self.signal = function_queue.get_signals()
        self.signal.data_received.connect(self.emit_data)

    def run(self):
        self.receiver.receive_data()

    def stop(self):
        self.receiver.set_stop()

    def start_receiving(self):
        self.receiver.set_start()
        self.run()

    def emit_data(self, data):
        self.Data.emit(data)
