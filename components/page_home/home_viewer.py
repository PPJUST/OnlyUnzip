# 主页模块的界面组件
from typing import Union

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox

from components.page_home.res.icon_base64 import *
from components.page_home.res.label_icon import LabelIcon
from components.page_home.res.ui_page_home import Ui_Form


class HomeViewer(QWidget):
    """主页模块的界面组件"""
    Stop = Signal(name="停止")
    DropFiles = Signal(list, name="拖入文件")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        # 初始化
        self.default_icon: bytes = b''  # 对应模式的图标，用于拖放文件后复原

        # 添加自定义Label
        self.label_icon = LabelIcon()
        self.ui.verticalLayout_label_drop.addWidget(self.label_icon)

        # 绑定信号
        self.ui.toolButton_stop.clicked.connect(self._click_stop_button)

    def set_progress_total(self, progress: str):
        """设置总进度 -/-
        :param progress: "-/-"格式的字符串"""
        self.ui.label_progress_total.setText(progress)

    def set_current_file(self, filename: str,tooltip:str=''):
        """设置当前处理的文件名"""
        self.ui.label_current_file.setText(filename)
        if tooltip:
            self.ui.label_current_file.setToolTip(tooltip)

    def set_runtime_total(self, runtime: str):
        """设置总运行时间 0:00:00
        :param runtime: "0:00:00"格式的字符串"""
        self.ui.label_runtime_total.setText(runtime)

    def set_runtime_current(self, runtime: str):
        """设置当前文件的运行时间 0:00:00
        :param runtime: "0:00:00"格式的字符串"""
        self.ui.label_runtime_current.setText(runtime)

    def set_progress_test(self, progress: str):
        """设置测试密码的进度 -/-
        :param progress: "-/-"格式的进度字符串"""
        self.ui.label_progress_test.setText(progress)

    def set_current_password(self, password: str):
        """设置当前测试的密码"""
        self.ui.label_current_password.setText(password)
        self.ui.label_right_password.setText(password)  # 将正确密码label也设置为当前密码，切换到解压页时即说明密码正确

    def set_progress_extract(self, progress: int):
        """设置解压的进度 1%
        :param progress: 0~100的整数"""
        self.ui.progressBar_progress_extract.setValue(progress)

    def _click_stop_button(self):
        """点击停止按钮"""
        reply = QMessageBox.question(self, '是否终止', '是否终止当前任务', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._stop_progress()

    def _stop_progress(self):
        """终止当前任务"""
        self.Stop.emit()

    def set_page_test(self):
        """切换运行信息页为测试模式"""
        self.ui.stackedWidget.setCurrentIndex(0)

    def set_page_extract(self):
        """切换运行信息页为解压模式"""
        self.ui.stackedWidget.setCurrentIndex(1)

    """icon方法"""

    def set_icon(self, icon: Union[bytes, str]):
        """设置显示的图标"""
        self.label_icon.set_icon(icon)

    def set_gif_icon(self, icon: Union[bytes, str]):
        """设置显示的图标"""
        self.label_icon.set_gif_icon(icon)

    def set_default_icon(self, icon: Union[bytes, str]):
        """设置默认图标"""
        self.default_icon = icon

    def set_icon_drop(self):
        """设置拖入文件图标"""
        self.set_icon(ICON_DROP)

    def _set_icon_default(self):
        """设置默认图标"""
        self.set_icon(self.default_icon)

    """拖入事件"""

    def _drop_files(self, paths: list):
        """拖入文件/文件夹"""
        self.DropFiles.emit(paths)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            paths = [url.toLocalFile() for url in urls]
            self._drop_files(paths)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.set_icon_drop()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._set_icon_default()


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = HomeViewer()
    program_ui.show()
    app_.exec()
