# 检查文件类型是否是压缩文件的子线程
import os

import lzytools_archive
from PySide6.QtCore import QThread, Signal


class ThreadFiletypeArchive(QThread):
    """检查文件类型是否是压缩文件的子线程"""
    Archives = Signal(list, name='压缩文件列表')

    def __init__(self, ):
        super().__init__()
        self.files = []  # 需要检查的文件列表

    def set_files(self, files: list):
        self.files = files

    def run(self):
        archive_files = []
        for file in self.files:
            if not is_exclude_file_extension(file):
                if lzytools_archive.is_archive_by_filename(os.path.basename(file)):
                    archive_files.append(file)
                elif lzytools_archive.is_archive(file):
                    archive_files.append(file)

        self.files.clear()

        self.Archives.emit(archive_files)


def is_exclude_file_extension(filename: str):
    """在识别压缩文件时，排除指定文件扩展名"""
    _exclude_file_extension = ['exe', 'apk', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'ppt']

    file_extension = os.path.splitext(filename)[1].strip().strip('.').strip()
    if file_extension.lower() in _exclude_file_extension:
        return True

    return False
