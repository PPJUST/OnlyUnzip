# 历史模块的界面组件
from typing import Tuple

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QMenu

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

    def add_record(self, record_text: str, color: Tuple[int, int, int], password: str = None):
        """添加记录"""
        item = QListWidgetItem()
        item.setText(record_text)
        if color:
            item.setForeground(QColor(color[0], color[1], color[2]))
        if password:  # 如果显示了密码，则将密码设置为UserRole属性，用于右键提取
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setData(Qt.UserRole, password)

        self.ui.listWidget_records.addItem(item)
        self.ui.listWidget_records.scrollToBottom()  # 滚动到底部

    def _context_menu(self, pos):
        """右键菜单"""
        selected_item = self.ui.listWidget_records.currentItem()
        if selected_item and selected_item.data(Qt.UserRole):
            menu = QMenu()
            menu.adjustSize()
            copy_action = QAction('复制密码', menu)
            copy_action.triggered.connect(self._copy_password)
            menu.addAction(copy_action)
            menu.exec(self.mapToGlobal(pos))

    def _copy_password(self):
        """复制行项目中的密码到剪切板"""
        selected_item = self.ui.listWidget_records.currentItem()
        password = selected_item.data(Qt.UserRole)
        QApplication.clipboard().setText(password)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = HistoryViewer()
    program_ui.show()
    app_.exec()
