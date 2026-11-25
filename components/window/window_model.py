# 主窗口的模型组件

from PySide6.QtCore import QObject

from common.class_7zip import ModelArchive
from common.class_file_info import FileInfoList
from common.class_setting import ModelSetting
from components.window.thread_7zip import ThreadExtract, ThreadTest
from components.window.window_signals import WindowSignals, relay_signals


class TemplateModelSignal(WindowSignals, QObject):
    """模型模板，添加通用的信号中转能力"""

    def transfer_signals(self, child):
        """把子对象的信号中转给当前对象"""
        relay_signals(child, self)


class ModelTask(TemplateModelSignal):
    """测试模型和解压模型的通用逻辑"""

    def __init__(self, thread):
        super().__init__()
        self.thread = thread
        self.passwords = []
        self.transfer_signals(thread)

    def set_passwords(self, passwords: list):
        """设置密码列表"""
        self.passwords = passwords

    def stop_task(self):
        """终止任务"""
        self.thread.stop_task()

    def process_file(self, file_info: FileInfoList):
        """把任务和密码交给子线程执行"""
        self.thread.set_task(file_info)
        self.thread.set_passwords(self.passwords)
        self.thread.load_setting()
        self.thread.start()


class ModelTestFile(ModelTask):
    """测试模式的模型"""

    def __init__(self):
        super().__init__(ThreadTest())


class ModelExtractFile(ModelTask):
    """解压模式的模型"""

    def __init__(self):
        super().__init__(ThreadExtract())


class WindowModel(TemplateModelSignal):
    """主窗口的模型组件"""

    def __init__(self):
        super().__init__()
        self.model_test_file = ModelTestFile()
        self.model_extract_file = ModelExtractFile()

        # 中转两个子模型的信号
        self.transfer_signals(self.model_test_file)
        self.transfer_signals(self.model_extract_file)

    def accept_files(self, file_info: FileInfoList):
        """接收文件信息类，执行测试或解压操作"""
        archive_model = ModelSetting().get_model_archive()
        if isinstance(archive_model, ModelArchive.Test):
            self.model_test_file.process_file(file_info)
        elif isinstance(archive_model, ModelArchive.Extract):
            self.model_extract_file.process_file(file_info)

    def stop_task(self):
        """终止所有任务"""
        self.model_test_file.stop_task()
        self.model_extract_file.stop_task()

    def set_passwords(self, passwords: list):
        """给两个子模型设置密码"""
        self.model_test_file.set_passwords(passwords)
        self.model_extract_file.set_passwords(passwords)
