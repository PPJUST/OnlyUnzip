# 密码详情表的桥梁组件
from PySide6.QtCore import QObject

from components.dialog_password_detail.password_detail_model import PasswordDetailModel
from components.dialog_password_detail.password_detail_viewer import PasswordDetailViewer


class PasswordDetailPresenter(QObject):
    """密码详情表的桥梁组件"""

    def __init__(self, viewer: PasswordDetailViewer, model: PasswordDetailModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

    def add_record(self, password_info: tuple):
        """添加一条记录

        :param password_info: 一条记录，依次为密码str、使用次数int、添加时间str、最后使用时间str
        """
        self.add_records([password_info])

    def add_records(self, password_infos: list):
        """添加多条记录

        :param password_infos: 记录列表，每条记录为四元元组
        """
        values_list = []
        for password_info in password_infos:
            values = self.model.get_display_values(password_info)
            values_list.append(values)
        self.viewer.add_records(values_list)

    def clear(self):
        """清空表格中的记录"""
        self.viewer.clear()

    def exec(self):
        """显示密码详情对话框"""
        self.viewer.exec()
