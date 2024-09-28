import ctypes
import os
import sys

from PySide6.QtGui import QPalette, QColor, QIcon
from PySide6.QtWidgets import QApplication, QMessageBox

from constant import _ICON_APP
from module import function_normal
from ui.OnlyUnzip import OnlyUnzip

paths = []
try:  # 提取拖入路径
    cmd_args = sys.argv[1:]
    _folder = os.getcwd()
    for i in cmd_args:
        if os.path.isabs(i):
            paths.append(i)
        else:  # 组合相对路径
            paths.append(os.path.normpath(os.path.join(_folder, i)))
except IndexError:
    pass


def main():
    app_ = QApplication()
    app_.setStyle('Fusion')
    # 设置白色背景色
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    app_.setPalette(palette)

    program_ui = OnlyUnzip(paths)
    program_ui.setWindowIcon(QIcon(_ICON_APP))
    program_ui.setFixedSize(262, 232)
    program_ui.show()
    app_.exec()


def check_software_is_running():
    """使用互斥体检查是否已经打开了一个实例"""
    mutex_name = 'OnlyUnzip'
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        ctypes.windll.kernel32.CloseHandle(mutex)
        return True
    return False


if __name__ == "__main__":
    if check_software_is_running():
        app = QApplication([])
        messagebox = QMessageBox()
        messagebox.setText('程序已经运行，请勿重复打开')
        messagebox.exec()
        sys.exit(1)
    else:
        function_normal.check_default_files()
        main()
