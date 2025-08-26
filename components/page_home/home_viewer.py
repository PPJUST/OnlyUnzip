# 主页模块的界面组件
from typing import Union

import lzytools._qt_pyside6
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from lzytools._qt_pyside6 import base64_to_pixmap

from common.function_7zip import FAKE_PASSWORD
from components.page_home.res.icon_base64 import *
from components.page_home.res.label_icon import LabelIcon
from components.page_home.res.ui_page_home import Ui_Form


class HomeViewer(QWidget):
    """主页模块的界面组件"""
    UserStop = Signal(name="用户主动停止")
    DropFiles = Signal(list, name="拖入文件")
    OpenAbout = Signal(name="打开关于页")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setAcceptDrops(True)

        # 初始化
        self.last_icon: bytes = None  # 上一个显示的图标，用于拖放文件后复原
        self.last_icon_gif: bytes = None  # 上一个显示的gif图标，用于拖放文件后复原
        self.turn_page_welcome()
        self._set_stop_icon()
        self.ui.label_step_notice.setOpenExternalLinks(True)
        self.ui.label_about.setOpenExternalLinks(False)
        self.ui.label_about.linkActivated.connect(self._open_about)

        # 添加自定义Label
        self.label_icon = LabelIcon(self)
        self.ui.verticalLayout_label_drop.addWidget(self.label_icon)
        self.label_current_file = lzytools._qt_pyside6.TabelWidgetHiddenOverLengthText(self)
        self.ui.layout_current_file.addWidget(self.label_current_file)
        self.label_current_password = lzytools._qt_pyside6.TabelWidgetHiddenOverLengthText(self)
        self.ui.layout_current_password.addWidget(self.label_current_password)
        self.label_right_password = lzytools._qt_pyside6.TabelWidgetHiddenOverLengthText(self)
        self.ui.layout_right_password.addWidget(self.label_right_password)

        # 绑定信号
        self.ui.toolButton_stop.clicked.connect(self._click_stop_button)

    """欢迎页"""

    def turn_page_welcome(self):
        """切换到欢迎页"""
        self.ui.stackedWidget.setCurrentIndex(0)

    def _open_about(self):
        self.OpenAbout.emit()

    """步骤提示页"""

    def turn_page_step(self):
        """切换到步骤提示页"""
        self.ui.stackedWidget.setCurrentIndex(1)

    def set_step_notice(self, notice: str):
        """设置步骤提示"""
        self.turn_page_step()
        self.ui.label_step_notice.setText(notice)

    def _set_stop_icon(self):
        """设置停止按钮的图标"""
        self.ui.toolButton_stop.setIcon(base64_to_pixmap(ICON_STOP))

    """测试和解压页"""

    def turn_page_test_and_extract(self):
        """切换到测试和解压页"""
        self.ui.stackedWidget.setCurrentIndex(2)

    def set_progress_total(self, progress: str):
        """设置总进度 -/-
        :param progress: "-/-"格式的字符串"""
        self.turn_page_test_and_extract()
        self.ui.label_progress_total.setText(progress)

    def set_current_file(self, filename: str, tooltip: str = ''):
        """设置当前处理的文件名"""
        self.turn_page_test_and_extract()
        self.label_current_file.set_text(filename)
        if tooltip:
            self.label_current_file.setToolTip(tooltip)

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
        self.set_child_page_test()
        self.ui.label_progress_test.setText(progress)

    def set_current_password(self, password: str):
        """设置当前测试的密码"""
        if password == FAKE_PASSWORD:  # 如果是虚拟密码，则显示省略号
            password = '...'

        self.label_current_password.set_text(password)
        self.label_right_password.set_text(password)

    def set_progress_extract(self, progress: int):
        """设置解压的进度 1%
        :param progress: 0~100的整数"""
        self.set_child_page_extract()
        self.ui.progressBar_progress_extract.setValue(progress)

    def set_current_file_step_tip(self, tip: str):
        """设置当前处理的文件的步骤提示"""
        self.set_child_page_step_tip()
        self.ui.label_current_file_step_tip.setText(tip)

    def _click_stop_button(self):
        """点击停止按钮"""
        reply = QMessageBox.question(self, '是否终止', '是否终止当前任务', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._stop_progress()

    def _stop_progress(self):
        """终止当前任务"""
        self.UserStop.emit()

    def set_child_page_test(self):
        """切换运行信息页为测试模式"""
        self.ui.stackedWidget_2.setCurrentIndex(0)

    def set_child_page_extract(self):
        """切换运行信息页为解压模式"""
        self.ui.stackedWidget_2.setCurrentIndex(1)

    def set_child_page_step_tip(self):
        """切换运行信息页为当前步骤提示"""
        self.ui.stackedWidget_2.setCurrentIndex(2)

    """结果页"""

    def turn_page_result(self):
        """切换到结果页"""
        self.ui.stackedWidget.setCurrentIndex(3)

    def show_time_final(self):
        """设置全部任务结束后的总耗时"""
        time = self.ui.label_runtime_total.text()  # 直接读取另一个label的文本即可
        self.ui.label_time_final.setText(time)

    def show_process_count(self, count: Union[int, str]):
        """设置处理的文件数量"""
        self.ui.label_process_file_count.setText(str(count))

    def show_result_count(self, result_info: str, result_info_tip: str = ''):
        """设置处理结果的统计"""
        self.turn_page_result()
        self.ui.label_result_count.setText(result_info)
        if result_info_tip:
            self.ui.label_result_count.setToolTip(result_info_tip)

    """icon方法"""

    def set_icon(self, icon: Union[bytes, str]):
        """设置显示的图标"""
        self.label_icon.set_icon(icon)

        # 赋值给变量，用于拖放后复原
        self.last_icon = icon
        self.last_icon_gif = None

    def set_gif_icon(self, icon: Union[bytes, str]):
        """设置显示的图标"""
        self.label_icon.set_gif_icon(icon)

        # 赋值给变量，用于拖放后复原
        self.last_icon = None
        self.last_icon_gif = icon

    def _show_last_icon(self):
        """设置默认图标"""
        if self.last_icon:
            print('显示静态图标')
            self.set_icon(self.last_icon)
        elif self.last_icon_gif:
            print('显示动态图标')
            self.set_gif_icon(self.last_icon_gif)

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
            self.label_icon.set_icon(ICON_DROP)  # 显示拖入图标
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._show_last_icon()

    """缩放事件，用于修改icon控件的尺寸"""

    def resizeEvent(self, event):
        # icon控件以短边为基准，按比例缩放
        frame = self.size()
        icon_width = frame.width()
        icon_height = frame.width()
        resize_width = min(icon_width, icon_height)
        resize_height = min(icon_width, icon_height)
        self.label_icon.resize(resize_width, resize_height)
        super().resizeEvent(event)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = HomeViewer()
    program_ui.show()
    app_.exec()
