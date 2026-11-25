# 密码管理器模块的桥梁组件
# 接收 Viewer 的信号，按条件查询密码本，并把统计和预览结果交给 Viewer 显示
from PySide6.QtCore import QObject, Signal

from components import dialog_password_detail
from components.page_password_manager.password_manager_model import PasswordManagerModel
from components.page_password_manager.password_manager_viewer import (
    FILTER_ADD_DATE,
    FILTER_LAST_USE_DATE,
    FILTER_USE_COUNT,
    PasswordManagerViewer,
)

# 统计“使用次数不少于 100”时使用的上限，覆盖实际可能出现的使用次数
MAX_USE_COUNT = 10000


class PasswordManagerPresenter(QObject):
    """密码管理器模块的桥梁组件"""

    SignalDeleted = Signal(name="删除密码")

    def __init__(self, viewer: PasswordManagerViewer, model: PasswordManagerModel):
        super().__init__()
        self.viewer = viewer
        self.model = model
        self._bind_signal()

    # region 对外接口
    def update_count(self):
        """更新各区间的使用次数统计"""
        count_rules = [
            (self.viewer.set_count_100, 100, MAX_USE_COUNT),
            (self.viewer.set_count_10, 10, 99),
            (self.viewer.set_count_1, 1, 9),
            (self.viewer.set_count_0, 0, 0),
        ]
        for set_count, min_count, max_count in count_rules:
            count = len(self.model.filter_use_count(min_count, max_count))
            set_count(count)

    def show_password_detail(self):
        """显示密码详情窗口"""
        dialog = dialog_password_detail.get_presenter()
        dialog.add_records(self.model.get_password_infos())
        dialog.exec()

    def set_passwords_need_delete(self):
        """把待删除的密码交给 Viewer 显示"""
        self.viewer.set_passwords_need_delete(self.get_passwords_need_delete())

    def get_passwords_need_delete(self) -> list:
        """获取同时符合所有已启用条件的密码，未启用任何条件时返回空列表。"""
        filters = self.viewer.get_delete_filters()
        if not self._has_enabled_filter(filters):
            return []

        # 从全部密码开始，逐个条件取交集，保持密码本原有的排列顺序
        passwords = self.model.get_passwords()
        for filter_name, is_enabled, value in filters:
            if not is_enabled:
                continue
            matched = self._get_matched_passwords(filter_name, value)
            passwords = self._keep_matched_passwords(passwords, matched)
        return passwords

    def delete_passwords(self, delete_passwords: list):
        """删除指定密码并通知外部刷新"""
        self.model.delete_passwords(delete_passwords)
        self.SignalDeleted.emit()

    def show_preview(self):
        """显示预览密码清单"""
        self.viewer.show_preview()

    def hidden_preview(self):
        """隐藏预览密码清单"""
        self.viewer.hidden_preview()

    # endregion

    # region 内部方法
    def _bind_signal(self):
        """绑定 Viewer 的信号"""
        connections = [
            (self.viewer.SignalShowDetail, self.show_password_detail),
            (self.viewer.SignalFilterUpdated, self.set_passwords_need_delete),
            (self.viewer.SignalDeleted, self.delete_passwords),
        ]
        for signal, slot in connections:
            signal.connect(slot)

    @staticmethod
    def _has_enabled_filter(filters) -> bool:
        """判断是否至少启用了一个删除条件"""
        for filter_item in filters:
            if filter_item[1]:
                return True
        return False

    def _get_matched_passwords(self, filter_name: str, value: int) -> list:
        """按单个删除条件获取匹配的密码"""
        if filter_name == FILTER_USE_COUNT:
            return self.model.filter_use_count(0, value)
        if filter_name == FILTER_ADD_DATE:
            return self.model.filter_add_time(value, is_inside=False)
        if filter_name == FILTER_LAST_USE_DATE:
            return self.model.filter_last_use_time(value, is_inside=False)
        raise ValueError('未知的删除条件：{0}'.format(filter_name))

    @staticmethod
    def _keep_matched_passwords(passwords: list, matched_passwords: list) -> list:
        """按原有顺序保留两组密码的交集"""
        result = []
        for password in passwords:
            if password in matched_passwords:
                result.append(password)
        return result
    # endregion
