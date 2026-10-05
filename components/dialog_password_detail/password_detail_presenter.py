# ??????????
from typing import Tuple

from PySide6.QtCore import QObject

from components.dialog_password_detail.password_detail_model import PasswordDetailModel
from components.dialog_password_detail.password_detail_viewer import PasswordDetailViewer


class PasswordDetailPresenter(QObject):
    """??????????"""

    def __init__(self, viewer: PasswordDetailViewer, model: PasswordDetailModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

    def add_record(self, password_info: Tuple[str, int, str, str]):
        """????
        :param password_info: ??,????,????,??????"""
        self.viewer.add_record(password_info)

    def add_records(self, password_infos: list):
        """??????"""
        for password_info in password_infos:
            self.add_record(password_info)

    def exec(self):
        self.viewer.exec()

    def clear(self):
        self.viewer.clear()
