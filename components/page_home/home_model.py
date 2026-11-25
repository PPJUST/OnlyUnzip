# 主页模块的模型组件
import time

import lzytools
from PySide6.QtCore import QObject, QTimer, Signal

from common.class_archive_spliter import ArchiveSpliter

TIMER_INTERVAL_MS = 500


class HomeModel(QObject):
    """主页模块的模型组件"""

    RuntimeTotal = Signal(str, name="总运行时间")
    RuntimeCurrent = Signal(str, name="当前文件运行时间")

    def __init__(self):
        super().__init__()
        self.archive_spliter = ArchiveSpliter()  # 压缩文件分类对象

        self._timer = QTimer()
        self._timer.timeout.connect(self._update_runtime)
        self._timer.setInterval(TIMER_INTERVAL_MS)
        self._start_time_total = 0
        self._start_time_current = 0

    @staticmethod
    def get_files(paths: list):
        """提取路径内包含的文件"""
        return lzytools.file.get_files_in_paths(paths)

    def split_volume_archive(self, files: list) -> ArchiveSpliter:
        """分组压缩文件"""
        self.archive_spliter.analyse_files(files)
        return self.archive_spliter

    def start_timing(self):
        """开始计时"""
        now = time.time()
        self._start_time_total = now
        self._start_time_current = now
        self._timer.start()

        self.RuntimeTotal.emit('0:00:00')
        self.RuntimeCurrent.emit('0:00:00')

    def reset_current_time(self):
        """重置当前文件运行时间"""
        self._start_time_current = time.time()

    def stop_timing(self):
        """停止计时"""
        self._timer.stop()

    @staticmethod
    def _format_runtime(seconds: float) -> str:
        """把秒数格式化为 0:00:00"""
        return lzytools.time.convert_time_hms(seconds)

    def _update_runtime(self):
        """更新运行时间"""
        time_now = time.time()

        runtime_total = time_now - self._start_time_total
        self.RuntimeTotal.emit(self._format_runtime(runtime_total))

        runtime_current = time_now - self._start_time_current
        self.RuntimeCurrent.emit(self._format_runtime(runtime_current))
