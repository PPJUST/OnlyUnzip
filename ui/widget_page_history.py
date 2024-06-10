# 历史记录页
import os
import time

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QListWidget, QApplication, QMenu, QListWidgetItem

from module import function_normal, function_password
from module.function_7zip import Result7zip, Collect7zipResult


class ListWidgetHistory(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setWordWrap(True)
        self.customContextMenuRequested.connect(self._context_menu)  # 右键菜单
        self._last_state_class = None  # 上一个状态类，用于防止同一文件添加重复状态项

        self.collect_result = Collect7zipResult()

    def reset_class(self):
        """重置"""
        self._last_state_class = None

    def insert_item(self, state_class):
        """插入行项目"""
        # 只在当前状态类与上个状态类不同时，才进行插入操作，防止插入同一文件的同一状态项
        if self._last_state_class and state_class.file == self._last_state_class.file and state_class.text == self._last_state_class.text:
            return

        # 收集结果
        self.collect_result.collect(state_class)

        # 生成文本
        text_time = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())
        text_filetitle = os.path.basename(state_class.file)
        text_result = state_class.text
        color = state_class.color
        text_line = '----------'

        # 创建行项目
        item = QListWidgetItem()
        text_item = text_line + '\n■' + text_time + '\n■' + text_filetitle + '\n■' + text_result
        item.setText(text_item)
        item.setForeground(QColor(color[0], color[1], color[2]))
        # 如果状态类时“成功”，则额外添加密码文本，并设置UserRole属性
        # 单独处理成功的记录，添加右键菜单，设置UserRole由于右键获取密码
        if isinstance(state_class, Result7zip.Success):
            text_password = state_class.password
            text_item += '\n■' + text_password
            item.setText(text_item)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setData(Qt.UserRole, text_password)
            # 正确密码在数据库中的使用次数+1
            if text_password:
                function_password.update_password(text_password)

        self.addItem(item)
        self.scrollToBottom()  # 滚动到底部
        self._last_state_class = state_class

        # 保存历史记录
        function_normal.save_history(text_item)

    def copy_password(self):
        """复制密码到剪切板"""
        selected_item = self.currentItem()
        password = selected_item.data(Qt.UserRole)
        QApplication.clipboard().setText(password)

    def _context_menu(self, pos):
        """右键菜单"""
        selected_item = self.currentItem()
        if selected_item and selected_item.data(Qt.UserRole):
            menu = QMenu()
            menu.adjustSize()
            copy_action = QAction('复制解压密码', menu)
            copy_action.triggered.connect(self.copy_password)
            menu.addAction(copy_action)
            menu.exec(self.mapToGlobal(pos))
