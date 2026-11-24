"""工作线程与界面线程之间的数据通道。

数据流：工作线程 -> QueueSender -> Queue -> QueueReceiver -> Qt 信号 -> 界面。
共享实例在模块底部创建，其他模块通过 get_sender/get_receiver/get_signals 获取。
"""

from __future__ import annotations

from queue import Empty, Queue
from threading import Event

from PySide6.QtCore import QObject, Signal

# 等待队列数据的最长时间（秒）：既避免空轮询占用 CPU，也能及时响应停止请求
QUEUE_TIMEOUT = 0.1


class CommunicationSignals(QObject):
    """将队列中的数据转发为 Qt 信号。"""

    data_received = Signal(int)

    def emit_(self, data: int) -> None:
        """发射数据接收信号。"""
        self.data_received.emit(data)


class QueueSender:
    """数据发送端：线程安全地把数据写入共享队列。"""

    def __init__(self, queue: Queue[int]) -> None:
        self.queue = queue

    def send_data(self, data: int) -> None:
        """向队列写入一条数据。"""
        self.queue.put(data)


class QueueReceiver(QObject):
    """数据接收端：在调用方线程中循环读取队列并发射信号。"""

    def __init__(self, queue: Queue[int], signal: CommunicationSignals) -> None:
        super().__init__()
        self.queue = queue
        self.signal = signal
        self._stop_event = Event()

    def receive_data(self) -> None:
        """持续接收数据，直到调用 set_stop()。"""
        while not self._stop_event.is_set():
            try:
                data = self.queue.get(timeout=QUEUE_TIMEOUT)
            except Empty:
                continue

            try:
                self.signal.emit_(data)
            finally:
                self.queue.task_done()

    def set_stop(self) -> None:
        """请求停止接收循环。"""
        self._stop_event.set()

    def set_start(self) -> None:
        """允许接收循环继续运行。"""
        self._stop_event.clear()


# 模块级共享实例：整个进程内通过下方的 getter 访问同一组对象
shared_queue: Queue[int] = Queue()
signals_communication = CommunicationSignals()
queue_sender = QueueSender(shared_queue)
queue_receiver = QueueReceiver(shared_queue, signals_communication)


def get_sender() -> QueueSender:
    """获取共享的数据发送器。"""
    return queue_sender


def get_receiver() -> QueueReceiver:
    """获取共享的数据接收器。"""
    return queue_receiver


def get_signals() -> CommunicationSignals:
    """获取共享的信号对象。"""
    return signals_communication
