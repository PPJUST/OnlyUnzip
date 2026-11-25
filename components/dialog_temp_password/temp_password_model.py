# 临时密码模块的模型组件
import lzytools
from PySide6.QtWidgets import QApplication

from common import function_password


class TempPasswordModel:
    """临时密码模块的模型组件，负责读取和处理密码数据。"""

    @staticmethod
    def read_clipboard() -> str:
        """读取剪贴板内容

        :return: 剪贴板中的文本
        """
        clipboard = QApplication.clipboard()
        return clipboard.text()

    @staticmethod
    def read_passwords_from_files(files: list) -> list:
        """从拖入的文件中提取密码

        :param files: 拖入的文件路径列表
        :return: 文件中的密码列表（已去重）
        """
        return function_password.read_passwords_from_files(files)

    @staticmethod
    def dedup_passwords(passwords: list) -> list:
        """去除密码列表中的重复项

        :param passwords: 待处理的密码列表
        :return: 去重后的密码列表
        """
        return lzytools.common.dedup_list(passwords)
