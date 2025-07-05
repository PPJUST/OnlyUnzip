import time
from queue import Queue
from threading import Thread

from PySide6.QtCore import Signal, QObject


class CommunicationSignals(QObject):
    # 定义一个信号，str类型参数用于传递接收到的数据
    data_received = Signal(int)

    def emit_(self, data):
        print('发送信号数据', data)
        self.data_received.emit(data)



class QueueSender:
    _instance = None
    _is_init = False


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, queue=None):
        if not hasattr(self, 'queue'):  # 防止重复初始化
            self.queue = queue or Queue()


    def send_data(self, data):
        print(f"Sender: 发送数据 {data}")
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
                print(f"Receiver: 接收到数据 {type(data), data}")
                # 发射信号
                self.signal.emit_(data)
                # self.signal.data_received.emit(data)
                self.queue.task_done()
            time.sleep(0.1)  # 避免CPU占用过高

    def stop(self):
        self._running = False


# 模块级别创建单例，用于其他模块调用
# 创建共享队列和信号对象
shared_queue = Queue()
signals_communication = CommunicationSignals()

# 创建通信实例
queue_sender = QueueSender(shared_queue)
queue_receiver = QueueReceiver(shared_queue, signals_communication)

# 创建接收线程
receiver_thread = Thread(target=queue_receiver.receive_data)


# 提供访问接口
def get_sender():
    """获取发送器对象"""
    return queue_sender
def get_receiver():
    """获取接收器对象"""
    return queue_receiver
def get_receiver_thread():
    """获取接收线程"""
    return receiver_thread
def get_signals():
    """获取信号对象"""
    return signals_communication