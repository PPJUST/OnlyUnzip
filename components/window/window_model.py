# 主窗口的模型组件

from PySide6.QtCore import Signal, QObject

from common.class_7zip import ModelArchive
from common.class_file_info import FileInfoList, FileInfo
from common.class_setting import ModelSetting
from components.window.thread_7zip import ThreadTest, ThreadExtract, TemplateThread


class TemplateModelSignal(QObject):
    """模式模版，用于添加通用信号"""
    StepInfo = Signal(str, name='步骤信息')
    SignalCurrentFile = Signal(str, name='当前处理的文件名')
    SignalTaskCount = Signal(int, name='需要处理的文件总数')
    SignalTaskIndex = Signal(int, name='当前处理的文件索引')
    SignalCurrentPw = Signal(str, name='当前使用的密码')
    SignalPwCount = Signal(int, name='待测试密码总数')
    SignalPwIndex = Signal(int, name='当前使用的密码索引')
    SignalResult = Signal(FileInfo, name='自定义文件信息类')
    SignalStart = Signal(name='开始')
    SignalFinish = Signal(FileInfoList, name='结束，传递最终的文件信息类清单')

    def __init__(self):
        super().__init__()

    def _transfer_signal(self, child_thread: TemplateThread):
        """中转信号"""
        child_thread.SignalCurrentFile.connect(self.SignalCurrentFile)
        child_thread.SignalTaskCount.connect(self.SignalTaskCount)
        child_thread.SignalTaskIndex.connect(self.SignalTaskIndex)
        child_thread.SignalCurrentPw.connect(self.SignalCurrentPw)
        child_thread.SignalPwCount.connect(self.SignalPwCount)
        child_thread.SignalPwIndex.connect(self.SignalPwIndex)
        child_thread.SignalResult.connect(self.SignalResult)
        child_thread.SignalStart.connect(self.SignalStart)
        child_thread.SignalFinish.connect(self.SignalFinish)
        child_thread.StepInfo.connect(self.StepInfo)


class WindowModel(QObject):
    """主窗口的模型组件"""
    StepInfo = Signal(str, name='步骤信息')
    SignalCurrentFile = Signal(str, name='当前处理的文件名')
    SignalTaskCount = Signal(int, name='需要处理的文件总数')
    SignalTaskIndex = Signal(int, name='当前处理的文件索引')
    SignalCurrentPw = Signal(str, name='当前使用的密码')
    SignalPwCount = Signal(int, name='待测试密码总数')
    SignalPwIndex = Signal(int, name='当前使用的密码索引')
    SignalResult = Signal(FileInfo, name='自定义文件信息类')
    SignalStart = Signal(name='开始')
    SignalFinish = Signal(FileInfoList, name='结束，传递最终的文件信息类清单')

    def __init__(self):
        super().__init__()
        self.model_test_file = ModelTestFile()
        self.model_extract_file = ModelExtractFile()

        # 中转信号
        self._transfer_signal(self.model_test_file)
        self._transfer_signal(self.model_extract_file)

    def accept_files(self, file_info: FileInfoList):
        """接收文件信息类，执行解压/测试操作"""
        print('接受处理后的文件信息')
        archive_model = ModelSetting().get_model_archive()  # 压缩文件处理模式
        if isinstance(archive_model, ModelArchive.Test):
            print('执行测试操作')
            self.model_test_file.process_file(file_info)
        elif isinstance(archive_model, ModelArchive.Extract):
            print('执行解压操作')
            self.model_extract_file.process_file(file_info)

    def stop_task(self):
        """终止任务"""
        self.model_test_file.stop_task()
        self.model_extract_file.stop_task()

    def set_passwords(self, passwords: list):
        self.model_extract_file.set_passwords(passwords)
        self.model_test_file.set_passwords(passwords)

    def _transfer_signal(self, child_thread: TemplateModelSignal):
        """中转信号"""
        child_thread.SignalCurrentFile.connect(self.SignalCurrentFile)
        child_thread.SignalTaskCount.connect(self.SignalTaskCount)
        child_thread.SignalTaskIndex.connect(self.SignalTaskIndex)
        child_thread.SignalCurrentPw.connect(self.SignalCurrentPw)
        child_thread.SignalPwCount.connect(self.SignalPwCount)
        child_thread.SignalPwIndex.connect(self.SignalPwIndex)
        child_thread.SignalResult.connect(self.SignalResult)
        child_thread.SignalStart.connect(self.SignalStart)
        child_thread.SignalFinish.connect(self.SignalFinish)
        child_thread.StepInfo.connect(self.StepInfo)


class ModelTestFile(TemplateModelSignal):
    """测试模式的模型"""

    def __init__(self):
        super().__init__()
        self.thread_test = ThreadTest()
        self.passwords = list()

        # 中转子线程信号
        self._transfer_signal(self.thread_test)

    def set_passwords(self, passwords: list):
        """设置密码"""
        self.passwords = passwords

    def stop_task(self):
        """终止任务"""
        self.thread_test.stop_task()

    def process_file(self, file_info: FileInfoList):
        """测试文件"""
        print('传递参数给测试子线程，并执行')
        self.thread_test.set_task(file_info)
        self.thread_test.set_passwords(self.passwords)
        self.thread_test.load_setting()
        self.thread_test.start()


class ModelExtractFile(TemplateModelSignal):
    """解压模式的模型"""

    def __init__(self):
        super().__init__()
        self.thread_extract = ThreadExtract()
        self.passwords = list()

        # 中转子线程信号
        self._transfer_signal(self.thread_extract)

    def set_passwords(self, passwords: list):
        self.passwords = passwords

    def stop_task(self):
        """终止任务"""
        self.thread_extract.stop_task()

    def process_file(self, file_info: FileInfoList):
        """解压文件"""
        print('传递参数给解压子线程，并执行')
        self.thread_extract.set_task(file_info)
        self.thread_extract.set_passwords(self.passwords)
        self.thread_extract.load_setting()
        self.thread_extract.start()
