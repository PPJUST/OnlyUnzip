import ctypes
import os
import sys
import traceback

import lzytools.common
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMessageBox

from components import window

paths_cmd = []  # 通过命令行或者程序直接打开的文件路径
try:  # 提取路径
    cmd_args = sys.argv[1:]
    _folder = os.getcwd()
    for i in cmd_args:
        if os.path.isabs(i):  # 如果是绝对路径，则直接添加
            paths_cmd.append(i)
        else:  # 如果是相对路径，则添加程序路径头
            paths_cmd.append(os.path.normpath(os.path.join(_folder, i)))
except IndexError:
    pass


def load_app(paths: list = None):
    """:param paths: 通过命令行或者程序直接打开的文件路径"""
    app_ = QApplication()
    app_.setStyle('Fusion')
    # 设置白色背景色
    # palette = QPalette()
    # palette.setColor(QPalette.Window, QColor(255, 255, 255))
    # app_.setPalette(palette)

    # 设置全局字体
    font = QFont("Microsoft YaHei", 10)  # 字体名称和大小
    app_.setFont(font)

    presenter = window.get_presenter()
    viewer = presenter.viewer
    model = presenter.model
    viewer.setWindowTitle('OnlyUnzip v2.0.0')
    viewer.show()
    if paths:
        presenter.accept_paths_from_cmd(paths)
    app_.exec()


def send_args(path: list):
    """:param path: 通过命令行或者程序直接打开的文件路径"""
    presenter = window.get_presenter()
    presenter.accept_paths_from_cmd(path)


def show_dup_info():
    app_ = QApplication([])
    messagebox = QMessageBox()
    messagebox.setText('OnlyUnzip已经运行了一个实例，请勿重复运行。')
    messagebox.exec()
    sys.exit(1)


def show_error_info(error):
    # 确保有应用实例来显示消息框
    if not QApplication.instance():
        app_ = QApplication([])
    messagebox = QMessageBox()
    messagebox.setText(f'程序发生错误：\n{error}')
    messagebox.exec()
    sys.exit(1)


def create_console():
    """创建临时控制台窗口用于显示错误信息"""
    # 分配控制台
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    result = kernel32.AllocConsole()

    if result == 0:
        return False

    # 将标准输出重定向到新控制台
    sys.stdout = open('CONOUT$', 'w', encoding='utf-8')
    sys.stderr = open('CONOUT$', 'w', encoding='utf-8')
    return True


if __name__ == "__main__":
    if not lzytools.common.check_mutex('OnlyUnzip'):  # 互斥体检查（单个实例）
        try:
            load_app(paths_cmd)
        except Exception as e:
            # 尝试创建控制台显示错误
            console_created = create_console()
            print(f"程序发生错误: {str(e)}")
            print("详细错误信息:")
            traceback.print_exc()

            # 如果无法创建控制台，使用QMessageBox显示
            if not console_created:
                show_error_info(e)


    else:
        if not paths_cmd:  # 重复打开，并且没有传参，则进行提示
            show_dup_info()
        else:  # 否则将参数传递给程序
            send_args(paths_cmd)
