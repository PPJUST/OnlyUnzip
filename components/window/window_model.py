# 主窗口的模型组件

from PySide6.QtCore import Signal, QObject

from common.class_7zip import ModelExtract, ModelBreakFolder, ModelCoverFile, ModelArchive, \
    TYPES_MODEL_EXTRACT, TYPES_MODEL_COVER_FILE, TYPES_MODEL_BREAK_FOLDER, TYPES_POSITION, TYPES_MODEL_ARCHIVE
from common.class_file_info import FileInfoList, FileInfo
from components.window.thread_7zip import ThreadTest, ThreadExtract, TemplateThread


class TemplateModelSignal(QObject):
    """模式模版，用于添加通用信号"""
    SignalCurrentFile = Signal(str, name='当前处理的文件名')
    SignalTaskCount = Signal(int, name='需要处理的文件总数')
    SignalTaskIndex = Signal(int, name='当前处理的文件索引')
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
        child_thread.SignalPwCount.connect(self.SignalPwCount)
        child_thread.SignalPwIndex.connect(self.SignalPwIndex)
        child_thread.SignalResult.connect(self.SignalResult)
        child_thread.SignalStart.connect(self.SignalStart)
        child_thread.SignalFinish.connect(self.SignalFinish)


class WindowModel(QObject):
    """主窗口的模型组件"""
    SignalCurrentFile = Signal(str, name='当前处理的文件名')
    SignalTaskCount = Signal(int, name='需要处理的文件总数')
    SignalTaskIndex = Signal(int, name='当前处理的文件索引')
    SignalPwCount = Signal(int, name='待测试密码总数')
    SignalPwIndex = Signal(int, name='当前使用的密码索引')
    SignalResult = Signal(FileInfo, name='自定义文件信息类')
    SignalStart = Signal(name='开始')
    SignalFinish = Signal(FileInfoList, name='结束，传递最终的文件信息类清单')

    def __init__(self):
        super().__init__()
        self.model_test_file = ModelTestFile()
        self.model_extract_file = ModelExtractFile()
        self.archive_model = None  # 压缩文件处理模式

        # 中转信号
        self._transfer_signal(self.model_test_file)
        self._transfer_signal(self.model_extract_file)

    def accept_files(self, file_info: FileInfoList):
        """接收文件信息类，执行解压/测试操作"""
        print('接受处理后的文件信息')
        if isinstance(self.archive_model, ModelArchive.Test):
            print('执行测试操作')
            self.model_test_file.process_file(file_info)
        elif isinstance(self.archive_model, ModelArchive.Extract):
            print('执行解压操作')
            self.model_extract_file.process_file(file_info)

    def set_passwords(self, passwords: list):
        self.model_extract_file.set_passwords(passwords)
        self.model_test_file.set_passwords(passwords)

    def set_archive_model(self, archive_model: TYPES_MODEL_ARCHIVE):
        self.archive_model = archive_model

    def set_is_read_password_from_filename(self, value: bool):
        self.model_test_file.set_is_read_password_from_filename(value)
        self.model_extract_file.set_is_read_password_from_filename(value)

    def set_extract_model(self, extract_model: TYPES_MODEL_EXTRACT):
        self.model_extract_file.set_extract_model(extract_model)

    def set_is_delete_file(self, value: bool):
        self.model_extract_file.set_is_delete_file(value)

    def set_is_recursive_extract(self, value: bool):
        self.model_extract_file.set_is_recursive_extract(value)

    def set_cover_model(self, cover_model: TYPES_MODEL_COVER_FILE):
        self.model_extract_file.set_cover_model(cover_model)

    def set_is_break_folder(self, value: bool):
        self.model_extract_file.set_is_break_folder(value)

    def set_break_folder_model(self, break_folder_model: TYPES_MODEL_BREAK_FOLDER):
        self.model_extract_file.set_break_folder_model(break_folder_model)

    def set_is_extract_to_folder(self, value: bool):
        self.model_extract_file.set_is_extract_to_folder(value)

    def set_extract_output_folder(self, value: str):
        self.model_extract_file.set_extract_output_folder(value)

    def set_is_filter(self, value: bool):
        self.model_extract_file.set_is_filter(value)

    def set_filter_rules(self, value: str):
        self.model_extract_file.set_filter_rules(value)

    def set_is_write_filename(self, value: bool):
        self.model_test_file.set_is_write_filename(value)

    def set_write_filename_left_word(self, value: str):
        self.model_test_file.set_write_filename_left_word(value)

    def set_write_filename_right_word(self, value: str):
        self.model_test_file.set_write_filename_right_word(value)

    def set_write_filename_position(self, value: TYPES_POSITION):
        self.model_test_file.set_write_filename_position(value)

    def _transfer_signal(self, child_thread: TemplateModelSignal):
        """中转信号"""
        child_thread.SignalCurrentFile.connect(self.SignalCurrentFile)
        child_thread.SignalTaskCount.connect(self.SignalTaskCount)
        child_thread.SignalTaskIndex.connect(self.SignalTaskIndex)
        child_thread.SignalPwCount.connect(self.SignalPwCount)
        child_thread.SignalPwIndex.connect(self.SignalPwIndex)
        child_thread.SignalResult.connect(self.SignalResult)
        child_thread.SignalStart.connect(self.SignalStart)
        child_thread.SignalFinish.connect(self.SignalFinish)


class ModelTestFile(TemplateModelSignal):
    """测试模式的模型"""

    def __init__(self):
        super().__init__()
        self.thread_test = ThreadTest()
        self.passwords = list()
        self.is_read_password_from_filename = False  # 是否从文件名中读取密码

        # 中转子线程信号
        self._transfer_signal(self.thread_test)

    def set_passwords(self, passwords: list):
        """设置密码"""
        self.passwords = passwords

    def set_is_read_password_from_filename(self, value: bool):
        """设置是否从文件名中读取密码"""
        self.is_read_password_from_filename = value

    def process_file(self, file_info: FileInfoList):
        """测试文件"""
        print('传递参数给测试子线程，并执行')
        self.thread_test.set_task(file_info)
        self.thread_test.set_passwords(self.passwords)
        self.thread_test.set_is_read_pw_from_filename(self.is_read_password_from_filename)
        self.thread_test.start()

    def set_is_write_filename(self, value: bool):
        self.thread_test.is_write_filename = value

    def set_write_filename_left_word(self, value: str):
        self.thread_test.write_left_part = value

    def set_write_filename_right_word(self, value: str):
        self.thread_test.write_right_part = value

    def set_write_filename_position(self, value: TYPES_POSITION):
        self.thread_test.write_position = value


class ModelExtractFile(TemplateModelSignal):
    """解压模式的模型"""

    def __init__(self):
        super().__init__()
        self.thread_extract = ThreadExtract()
        self.passwords = list()
        # 初始化参数项
        self.is_read_password_from_filename = False  # 是否从文件名中读取密码
        self.extract_model = ModelExtract.Smart()  # 解压模式
        self.is_delete_file = False  # 完成后是否删除原文件
        self.is_recursive_extract = False  # 是否递归解压
        self.cover_model = ModelCoverFile.Overwrite()  # 重名文件覆盖模式
        self.is_break_folder = False  # 是否解散文件夹
        self.break_folder_model = ModelBreakFolder.MoveToTop()  # 解散文件夹的模式
        self.is_extract_to_folder = False  # 是否解压至指定文件夹
        self.extract_output_folder = ''  # 解压输出文件夹
        self.is_filter = False  # 是否过滤文件
        self.filter_rules = ''  # 过滤规则

        # 中转子线程信号
        self._transfer_signal(self.thread_extract)

    def set_passwords(self, passwords: list):
        self.passwords = passwords

    def set_is_read_password_from_filename(self, value: bool):
        """设置是否从文件名中读取密码"""
        self.is_read_password_from_filename = value

    def process_file(self, file_info: FileInfoList):
        """解压文件"""
        print('传递参数给解压子线程，并执行')
        self.thread_extract.set_task(file_info)
        self.thread_extract.set_passwords(self.passwords)
        self.thread_extract.set_is_read_pw_from_filename(self.is_read_password_from_filename)
        self.thread_extract.start()

    def set_extract_model(self, extract_model: TYPES_MODEL_EXTRACT):
        self.extract_model = extract_model

    def set_is_delete_file(self, value: bool):
        self.is_delete_file = value

    def set_is_recursive_extract(self, value: bool):
        self.is_recursive_extract = value

    def set_cover_model(self, cover_model: TYPES_MODEL_COVER_FILE):
        self.cover_model = cover_model
        self._set_thread_args()

    def set_is_break_folder(self, value: bool):
        self.is_break_folder = value

    def set_break_folder_model(self, break_folder_model: TYPES_MODEL_BREAK_FOLDER):
        self.break_folder_model = break_folder_model

    def set_is_extract_to_folder(self, value: bool):
        self.is_extract_to_folder = value
        self._set_thread_args()

    def set_extract_output_folder(self, value: str):
        self.extract_output_folder = value
        self._set_thread_args()

    def set_is_filter(self, value: bool):
        self.is_filter = value
        self._set_thread_args()

    def set_filter_rules(self, value: str):
        self.filter_rules = value
        self._set_thread_args()

    def _set_thread_args(self):
        """设置子线程的参数"""
        # 测试子线程

        # 解压子线程
        self.thread_extract.cover_model = self.cover_model.switch
        self.thread_extract.is_extract_to_folder = self.is_extract_to_folder
        self.thread_extract.extract_output_path = self.extract_output_folder
        self.thread_extract.is_filter = self.is_filter
        self.thread_extract.filter_rules = self.filter_rules
        self.thread_extract.extract_model = self.extract_model
        self.thread_extract.is_break_folder = self.is_break_folder
        self.thread_extract.break_folder_model = self.break_folder_model
        self.thread_extract.is_delete_file = self.is_delete_file
