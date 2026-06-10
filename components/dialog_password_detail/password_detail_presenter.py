# 密码详情表的桥梁组件
from typing import Tuple

from PySide6.QtCore import QObject

from components.dialog_password_detail.password_detail_model import PasswordDetailModel
from components.dialog_password_detail.password_detail_viewer import PasswordDetailViewer


class PasswordDetailPresenter(QObject):
    """密码详情表的桥梁组件"""

    def __init__(self, viewer: PasswordDetailViewer, model: PasswordDetailModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

    def add_record(self, password_info: Tuple[str, int, str, str]):
        """添加记录
        :param password_info: 密码，使用次数，添加时间，最后使用时间"""
        self.viewer.add_record(password_info)

    def add_records(self, password_infos: list):
        """添加多条记录"""
        for password_info in password_infos:
            self.add_record(password_info)

    def exec(self):
        self.viewer.exec()

    def clear(self):
        self.viewer.clear()
