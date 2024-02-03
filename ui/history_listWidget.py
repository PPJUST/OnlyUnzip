# 自定义历史记录控件
import os.path
import time

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QListWidget, QMenu, QListWidgetItem, QApplication

from module import function_normal
from module.class_state import State7zResult


class HistoryListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setWordWrap(True)  # 自动换行
        self.customContextMenuRequested.connect(self.context_menu)  # 右键菜单
        self.last_state_class = None  # 上一个状态类，用于防止添加同一文件的重复状态项

    def insert_item(self, state_class):
        info_time = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())
        info_file = os.path.split(state_class.file)[1]
        info_type = state_class.type_text
        color = state_class.color

        # 为了防止重复处理同一文件的密码错误状态类，做与上一个状态类的相同判断
        if type(state_class) is type(self.last_state_class) and info_file == os.path.split(self.last_state_class.file)[1]:
            pass
        else:
            item = QListWidgetItem()
            item_text = '■' + info_time + '■' + info_file + '■' + info_type
            item.setText(item_text)
            item.setForeground(QColor(color[0], color[1], color[2]))

            # 单独处理成功的记录，添加右键菜单，设置UserRole由于右键获取密码
            if type(state_class) is State7zResult.Success:
                info_password = state_class.password
                item_text += '■' + info_password
                item.setText(item_text)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setData(Qt.UserRole, info_password)

            self.addItem(item)

            # 保存记录到本地
            function_normal.save_history(item_text)

        self.last_state_class = state_class

    # 右键菜单
    def context_menu(self, pos):
        selected_item = self.currentItem()
        if selected_item and selected_item.data(Qt.UserRole):
            menu = QMenu()
            menu.adjustSize()
            copy_action = QAction('复制解压密码', menu)
            copy_action.triggered.connect(self.copy_password)
            menu.addAction(copy_action)
            menu.exec(self.mapToGlobal(pos))

    def copy_password(self):
        selected_item = self.currentItem()
        password = selected_item.data(Qt.UserRole)
        QApplication.clipboard().setText(password)
