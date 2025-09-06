# 临时密码模块的模型组件

from PySide6.QtWidgets import QApplication

from common import function_password
from common.function_password import DBPassword  # 必须添加DBPassword, Password类


class TempPasswordModel:
    """密码模块的模型组件"""

    def __init__(self):
        self.password_db: DBPassword = function_password.read_db()

    @staticmethod
    def read_clipboard():
        """读取剪切板，并返回读取的内容"""
        clipboard = QApplication.clipboard()
        return clipboard.text()

    def drop_files(self, files):
        """处理拖入的文件"""
        passwords_in_files = function_password.read_passwords_from_files(files)
        return passwords_in_files
