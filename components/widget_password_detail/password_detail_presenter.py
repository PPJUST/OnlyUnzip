# 密码详情表的桥梁组件
from typing import Tuple

from PySide6.QtCore import QObject

from components.widget_password_detail.password_detail_model import PasswordDetailModel
from components.widget_password_detail.password_detail_viewer import PasswordDetailViewer


class PasswordDetailPresenter(QObject):
    """密码详情表的桥梁组件"""

    def __init__(self, viewer: PasswordDetailViewer, model: PasswordDetailModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

    def add_record(self, password_info: Tuple[str, int, str, str]):
        """添加记录"""
        self.viewer.add_record(password_info)

    def add_records(self, password_infos: list):
        """添加多条记录"""
        for password_info in password_infos:
            self.add_record(password_info)
