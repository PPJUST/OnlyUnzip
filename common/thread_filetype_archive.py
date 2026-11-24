"""检查文件类型是否为压缩文件的子线程。"""

import os

import lzytools_archive
from PySide6.QtCore import QThread, Signal

# 这些格式即使带有压缩包特征（如自解压 exe），也不按压缩包处理
EXCLUDED_EXTENSIONS = frozenset(
    {"xls", "xlsx", "xlsm", "doc", "docx", "docm", "ppt", "pptx", "pptm", "csv", "odt", "ods", "odp", "epub", "kmz",
     "cbz", "ipa", "jar", "war", "ear", "aar", "xpi", "crx", "vsix", "nupkg", "whl", "apk", "exe", "appx", "msix",
     "aab", "xapk", "vpk", "pck", "ba2", "love", "mcpack", "mcworld", "bsa", "mpq", "sav", "dat", "pak", "quicksave",
     "autosave"})


class ThreadCheckFiletype(QThread):
    """在子线程中筛选压缩文件，避免阻塞界面线程。"""

    Archives = Signal(list, name='压缩文件列表')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.files: list[str] = []  # 需要检查的文件列表

    def set_files(self, files: list[str]) -> None:
        """设置待检查的文件列表（复制一份，避免修改调用方的数据）。"""
        self.files = list(files)

    def run(self) -> None:
        archive_files = [file for file in self.files if is_archive_file(file)]

        self.files.clear()  # 及时释放文件列表的引用
        self.Archives.emit(archive_files)


def is_archive_file(path: str) -> bool:
    """判断单个文件是否为需要处理的压缩文件。"""
    if is_exclude_file_extension(path):
        return False

    # 分卷压缩包的文件头无法被 filetype 正确识别，优先按文件名判断
    if lzytools_archive.is_archive_by_filename(os.path.basename(path)):
        return True

    # 文件名无法判断时，再读取文件头判断
    return os.path.isfile(path) and lzytools_archive.is_archive(path)


def is_exclude_file_extension(filename: str) -> bool:
    """在识别压缩文件时，排除指定扩展名的文件。"""
    extension = os.path.splitext(filename)[1].lstrip('.').lower()
    return extension in EXCLUDED_EXTENSIONS
