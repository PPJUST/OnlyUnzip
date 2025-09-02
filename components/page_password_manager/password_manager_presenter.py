# 密码管理器模块的桥梁组件
from PySide6.QtCore import QObject, Signal

from components.page_password_manager.password_manager_model import PasswordManagerModel
from components.page_password_manager.password_manager_viewer import PasswordManagerViewer


class PasswordManagerPresenter(QObject):
    """密码管理器模块的桥梁组件"""
    SignalDeleted = Signal(name="删除密码")

    def __init__(self, viewer: PasswordManagerViewer, model: PasswordManagerModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        self.viewer.SignalFilterUpdated.connect(self.set_passwords_need_delete)
        self.viewer.SignalDeleted.connect(self.delete_passwords)

    def update_count(self):
        """更新计数"""
        self.set_count_100()
        self.set_count_10()
        self.set_count_1()
        self.set_count_0()

    def set_count_100(self):
        """显示使用次数>100的密码数量"""
        count = len(self.model.filter_use_count(100, 10000))
        self.viewer.set_count_100(count)

    def set_count_10(self):
        """显示10<使用次数<100的密码数量"""
        count = len(self.model.filter_use_count(10, 100))
        self.viewer.set_count_10(count)

    def set_count_1(self):
        """显示1<使用次数<10的密码数量"""
        count = len(self.model.filter_use_count(1, 10))
        self.viewer.set_count_1(count)

    def set_count_0(self):
        """显示未使用过的密码数量"""
        count = len(self.model.filter_use_count(0, 0))
        self.viewer.set_count_0(count)

    def set_passwords_need_delete(self):
        """传递需要删除的密码给viewer控件"""
        passwords = self.get_passwords_need_delete()
        self.viewer.set_passwords_need_delete(passwords)

    def get_passwords_need_delete(self):
        """获取符合条件，会被删除的密码"""
        # 提取所有密码，后续用交集获取符合条件的密码
        passwords = set(self.model.get_passwords())
        is_filter = False

        # 使用次数
        if self.viewer.ui.checkBox_delete_use_count.isChecked():
            min_use_count = self.viewer.ui.spinBox_use_count.value()
            passwords_delete_use_count = self.model.filter_use_count(0, min_use_count)
            passwords.intersection_update(passwords_delete_use_count)
            is_filter = True

        # 添加时间
        if self.viewer.ui.checkBox_delete_add_date.isChecked():
            max_add_date = self.viewer.ui.spinBox_add_date.value()
            passwords_delete_add_date = self.model.filter_add_time(max_add_date, is_inside=False)
            passwords.intersection_update(passwords_delete_add_date)
            is_filter = True

        # 最后使用时间
        if self.viewer.ui.checkBox_delete_use_date.isChecked():
            max_use_date = self.viewer.ui.spinBox_use_date.value()
            passwords_delete_use_date = self.model.filter_last_use_time(max_use_date, is_inside=False)
            passwords.intersection_update(passwords_delete_use_date)
            is_filter = True

        if is_filter:
            return passwords
        else:
            return []

    def delete_passwords(self, delete_passwords: list):
        """删除密码本中的指定密码"""
        self.model.delete_passwords(delete_passwords)
        self.SignalDeleted.emit()

    def show_preview(self):
        """显示预览密码清单"""
        self.viewer.show_preview()

    def hidden_preview(self):
        """隐藏预览密码清单"""
        self.viewer.hidden_preview()
