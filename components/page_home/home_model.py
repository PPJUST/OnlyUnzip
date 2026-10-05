# ?????????
import time

import lzytools
from PySide6.QtCore import QTimer, Signal, QObject

from common.class_archive_spliter import ArchiveSpliter


class HomeModel(QObject):
    """?????????"""
    RuntimeTotal = Signal(str, name='?????')
    RuntimeCurrent = Signal(str, name='????????')

    def __init__(self):
        super().__init__()
        self.archive_spliter = ArchiveSpliter()  # ????????

        # ???,????????
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_runtime)
        self._timer.setInterval(500)
        self._start_time_total = 0
        self._start_time_current = 0

    @staticmethod
    def get_files(paths: list):
        """??????????"""
        return lzytools.file.get_files_in_paths(paths)

    def split_volume_archive(self, files: list) -> ArchiveSpliter:
        """??????"""
        self.archive_spliter.analyse_files(files)
        return self.archive_spliter

    def start_timing(self):
        """????"""
        self._start_time_total = time.time()
        self._start_time_current = time.time()
        self._timer.start()

        self.RuntimeTotal.emit('0:00:00')
        self.RuntimeCurrent.emit('0:00:00')

    def reset_current_time(self):
        """??????????"""
        self._start_time_current = time.time()

    def stop_timing(self):
        """????"""
        self._timer.stop()

    def _update_runtime(self):
        """??????"""
        time_now = time.time()

        runtime_total = time_now - self._start_time_total
        runtime_total_text = lzytools.time.convert_time_hms(runtime_total)
        self.RuntimeTotal.emit(runtime_total_text)

        runtime_current = time_now - self._start_time_current
        runtime_current_text = lzytools.time.convert_time_hms(runtime_current)
        self.RuntimeCurrent.emit(runtime_current_text)
