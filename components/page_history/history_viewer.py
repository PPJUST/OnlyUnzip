# 历史模块的界面组件
import os.path
from typing import Tuple

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QMenu

from common.class_file_info import FileInfo
from components.page_history.res.ui_page_history import Ui_Form


class HistoryViewer(QWidget):
    """历史模块的界面组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 初始化
        self.ui.listWidget_records.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.ui.listWidget_records.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget_records.setWordWrap(True)
        self.ui.listWidget_records.customContextMenuRequested.connect(self._context_menu)  # 右键菜单
        self.ui.listWidget_records.setSpacing(3)

    def add_record(self, record_text: str, color: Tuple[int, int, int], password: str = None,
                   file_info: FileInfo = None):
        """添加记录"""
        item = QListWidgetItem()
        record_text = record_text + '\n' + '-' * 20
        item.setText(record_text)
        if color:
            item.setForeground(QColor(color[0], color[1], color[2]))
        if password:  # 如果显示了密码，则将密码设置为UserRole属性，用于右键提取
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setData(Qt.UserRole, password)
        if file_info:  # 将对于的FileInfo写入item中，用于提取其他数据
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setData(Qt.UserRole + 1, file_info)

        self.ui.listWidget_records.addItem(item)
        self.ui.listWidget_records.scrollToBottom()  # 滚动到底部

    def _context_menu(self, pos):
        """右键菜单"""
        selected_item = self.ui.listWidget_records.currentItem()
        file_info: FileInfo = selected_item.data(Qt.UserRole + 1)
        is_show_action_password = True if file_info and file_info.password else False
        is_show_action_open_origin = True if file_info and file_info.filepath and os.path.exists(
            file_info.filepath) else False
        is_show_action_open_extract = True if file_info and file_info.extract_path and os.path.exists(
            file_info.extract_path) else False

        if selected_item and selected_item.data(Qt.UserRole):
            menu = QMenu()
            menu.adjustSize()

            if is_show_action_password:
                copy_action = QAction('复制密码', menu)
                copy_action.triggered.connect(self._copy_password)
                menu.addAction(copy_action)

            if is_show_action_open_origin:
                open_origin_path_action = QAction('打开原文件路径', menu)
                open_origin_path_action.triggered.connect(self._open_origin_path)
                menu.addAction(open_origin_path_action)

            if is_show_action_open_extract:
                open_extract_result_path_action = QAction('打开文件解压结果路径', menu)
                open_extract_result_path_action.triggered.connect(self._open_extract_result_path)
                menu.addAction(open_extract_result_path_action)

            menu.exec(self.mapToGlobal(pos))

    def _copy_password(self):
        """复制行项目中的密码到剪切板"""
        selected_item = self.ui.listWidget_records.currentItem()
        password = selected_item.data(Qt.UserRole)
        QApplication.clipboard().setText(password)

    def _open_origin_path(self):
        """打开行项目中的原文件路径"""
        selected_item = self.ui.listWidget_records.currentItem()
        file_info = selected_item.data(Qt.UserRole + 1)
        origin_filepath = file_info.filepath
        os.startfile(origin_filepath)

    def _open_extract_result_path(self):
        """打开行项目中的解压结果路径"""
        selected_item = self.ui.listWidget_records.currentItem()
        file_info = selected_item.data(Qt.UserRole + 1)
        extract_result = file_info.extract_path
        os.startfile(extract_result)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = HistoryViewer()
    program_ui.show()
    app_.exec()
