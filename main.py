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
    presenter.set_default_app_title('OnlyUnzip v2.0.0')
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


def exception_hook(exc_type, exc_value, exc_traceback):
    """重写异常钩子，将错误信息显示在消息框中"""
    # 忽略KeyboardInterrupt，让用户可以正常退出
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # 格式化错误信息
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    # 显示错误消息框
    if not QApplication.instance():
        app_ = QApplication([])
    messagebox = QMessageBox()
    messagebox.setIcon(QMessageBox.Critical)
    messagebox.setText("程序发生错误，请尝试重启程序或反馈问题：")
    messagebox.setInformativeText(str(exc_value))
    messagebox.setDetailedText(error_msg)
    messagebox.setWindowTitle("错误")
    messagebox.exec()


if __name__ == "__main__":
    # 重定向异常处理
    sys.excepthook = exception_hook

    if not lzytools.common.check_mutex('OnlyUnzip'):  # 互斥体检查（单个实例）
        load_app(paths_cmd)
    else:
        if not paths_cmd:  # 重复打开，并且没有传参，则进行提示
            show_dup_info()
        else:  # 否则将参数传递给程序
            send_args(paths_cmd)
