import os
import re
import time

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QMovie, QPalette
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMenu, QFileDialog, QMessageBox

import module.function_archive
import module.function_file
import module.function_filetype
import module.function_password
from constant import _ICON_TEST_GIF, _ICON_EXTRACT_GIF, _ICON_MAIN, _ICON_DEFAULT, _ICON_DEFAULT_WITH_OUTPUT, _ICON_ERROR, \
    _ICON_FINISH
from module import function_config
from module import function_static
from module.function_config import Config
from qthread_7zip import ExtractQthread
from ui import Ui_MainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)










    def update_ui(self, code: str, data: list = None):
        """根据传入的list，分不同情况更新ui
        type_list格式：['更新类型', '相关数据']"""
        function_static.print_function_info()
        if code == '1-1':  # 初始状态
            self.ui.label_drop_file.setPixmap(_ICON_DEFAULT)
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮

        elif code == '1-2':  # 启动子线程
            self.ui.button_stop.setVisible(True)  # 显示停止按钮
            self.movie_label_icon = None
            if self.ui.checkBox_mode_test.isChecked():  # 按选项设置不同图标
                # self.ui.label_drop_file.setPixmap(icon_test)
                self.movie_label_icon = QMovie(_ICON_TEST_GIF)
            else:
                # self.ui.label_drop_file.setPixmap(icon_extract)
                self.movie_label_icon = QMovie(_ICON_EXTRACT_GIF)
            self.ui.label_drop_file.setMovie(self.movie_label_icon)
            self.movie_label_icon.start()  # 开始动图
        elif code == '1-3':  # 完成全部任务
            self.ui.label_drop_file.setPixmap(_ICON_FINISH)
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('全部完成')
            self.ui.label_schedule_finish.setText(data[0])
            self.set_widget_enable(mode=True)
            self.ui.stackedWidget_schedule.setCurrentIndex(0)
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮
            self.movie_label_icon.stop()  # 停止动图
        elif code == '1-4':  # 中止任务
            self.ui.label_schedule_file.setText('等待当前文件完成执行')
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮
            self.set_widget_enable(mode=True)  # 启用被禁用的ui
            self.movie_label_icon.stop()  # 停止动图






    def stop_qthread(self):
        """中止解压子线程"""
        function_static.print_function_info()
        reply = QMessageBox.question(self, '确认对话框',
                                     f'是否中止当前任务\n（不终止当前正在执行的文件，\n仅中止之后的任务）',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.update_ui('1-4')
            self.qthread.signal_stop.emit()


def main():
    app = QApplication()
    app.setStyle('Fusion')
    # 设置白色背景色
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    app.setPalette(palette)

    show_ui = Main()
    show_ui.setWindowIcon(QIcon(_ICON_MAIN))
    show_ui.setFixedSize(262, 232)
    show_ui.show()
    app.exec_()


if __name__ == "__main__":
    main()
