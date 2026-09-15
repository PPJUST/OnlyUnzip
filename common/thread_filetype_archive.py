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
        self.is_ignore_exclude = False  # 是否忽略内置排除列表（GUI 线程传入）

    def set_files(self, files: list, is_ignore_exclude: bool = False):
        self.files = files
        self.is_ignore_exclude = is_ignore_exclude

    def run(self):
        archive_files = []
        for file in self.files:
            if self.is_ignore_exclude or not is_exclude_file_extension(file):
                if lzytools_archive.is_archive_by_filename(os.path.basename(file)):
                    archive_files.append(file)
                elif os.path.exists(file) and lzytools_archive.is_archive(file):
                    archive_files.append(file)

        self.files.clear()

        self.Archives.emit(archive_files)


def is_exclude_file_extension(filename: str):
    """在识别压缩文件时，排除指定文件扩展名"""
    _exclude_file_extension = [
        'exe', 'apk', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'ppt',
        # Office OOXML 及宏/模板文档（zip 容器）
        'pptx', 'docm', 'xlsm', 'pptm', 'dotx', 'xltx', 'potx', 'thmx', 'vsdx', 'vsdm', 'one',
        # OpenDocument（zip 容器）
        'odt', 'ods', 'odp', 'odg', 'odf',
        # Apple iWork（zip 容器）
        'pages', 'numbers', 'key',
        # 游戏存档/资源（内容为 zip 容器时会被 filetype 误判）
        'sav', 'dat', 'pak', 'rpgsave', 'mcworld', 'mcpack', 'slot', 'profile', 'quicksave', 'autosave',
        # 应用包/电子书（本质是 zip，解压破坏功能）
        'jar', 'war', 'ear', 'aab', 'xapk', 'nupkg', 'vsix', 'appx', 'msix', 'ipa', 'whl', 'egg', 'xpi', 'crx', 'epub', 'cbz', 'kmz',
    ]

    file_extension = os.path.splitext(filename)[1].strip().strip('.').strip()
    if file_extension.lower() in _exclude_file_extension:
        return True

    return False
