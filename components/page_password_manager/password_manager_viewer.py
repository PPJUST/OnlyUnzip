# 密码管理器模块的界面组件
# 只负责显示统计信息和预览清单，并发出用户操作信号，不直接读写密码本
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QMessageBox, QWidget

from components.page_password_manager.res.ui_manager import Ui_Form

# 删除条件的名称，供 Presenter 区分不同的筛选方式
FILTER_USE_COUNT = 'use_count'
FILTER_ADD_DATE = 'add_date'
FILTER_LAST_USE_DATE = 'last_use_date'


class PasswordManagerViewer(QWidget):
    """密码管理器模块的界面组件"""

    SignalFilterUpdated = Signal(object, name="预删除密码的过滤器选项更新")
    SignalDeleted = Signal(object, name="删除密码的清单")
    SignalShowDetail = Signal(name="显示密码详情")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.passwords_need_delete = []

        self.hidden_preview()
        self._bind_signal()

    # region 对外接口
    def get_delete_filters(self):
        """读取删除条件，返回 (条件名称, 是否启用, 数值) 组成的列表。

        数值的含义由条件名称决定：使用次数上限，或距今天数。
        """
        filter_widgets = [
            (FILTER_USE_COUNT, self.ui.checkBox_delete_use_count, self.ui.spinBox_use_count),
            (FILTER_ADD_DATE, self.ui.checkBox_delete_add_date, self.ui.spinBox_add_date),
            (FILTER_LAST_USE_DATE, self.ui.checkBox_delete_use_date, self.ui.spinBox_use_date),
        ]

        filters = []
        for filter_name, check_box, spin_box in filter_widgets:
            filters.append((filter_name, check_box.isChecked(), spin_box.value()))
        return filters

    def set_count_100(self, count: int):
        """显示使用次数不少于 100 的密码数量"""
        self.ui.label_pw_count_100.setText(str(count))

    def set_count_10(self, count: int):
        """显示使用次数为 10~99 的密码数量"""
        self.ui.label_pw_count_10.setText(str(count))

    def set_count_1(self, count: int):
        """显示使用次数为 1~9 的密码数量"""
        self.ui.label_pw_count_1.setText(str(count))

    def set_count_0(self, count: int):
        """显示从未使用过的密码数量"""
        self.ui.label_pw_count_0.setText(str(count))

    def set_passwords_need_delete(self, passwords: list):
        """设置待删除的密码并更新数量、预览内容"""
        self.passwords_need_delete = passwords
        self.ui.label_count_delete.setText(str(len(passwords)))
        self.set_preview_passwords()

    def show_preview(self):
        """显示预览密码清单"""
        self.set_preview_passwords()
        self.ui.textBrowser_preview.setVisible(True)
        self.ui.label_spacer.setVisible(False)

    def hidden_preview(self):
        """隐藏预览密码清单"""
        self.ui.textBrowser_preview.setVisible(False)
        self.ui.label_spacer.setVisible(True)

    def show_confirm_dialog(self):
        """弹出删除确认弹窗，确认后发出删除信号"""
        reply = QMessageBox.question(
            self,
            "确认操作",
            "是否确认删除对应密码？\n删除后无法撤销！",
            QMessageBox.Yes | QMessageBox.No,  # 显示 Yes 和 No 按钮
            QMessageBox.No  # 默认选中 No 按钮
        )

        if reply == QMessageBox.Yes:
            self.SignalDeleted.emit(self.passwords_need_delete)

    # endregion

    # region 内部方法
    def change_preview(self):
        """在显示和隐藏预览清单之间切换"""
        if self.ui.textBrowser_preview.isVisible():
            self.hidden_preview()
        else:
            self.show_preview()

    def set_preview_passwords(self):
        """刷新预览密码清单的文本"""
        self.ui.textBrowser_preview.setText('\n'.join(self.passwords_need_delete))

    def _bind_signal(self):
        """绑定界面控件的信号"""
        connections = [
            # 删除条件变化后刷新待删除清单
            (self.ui.checkBox_delete_use_count.stateChanged, self.SignalFilterUpdated.emit),
            (self.ui.spinBox_use_count.valueChanged, self.SignalFilterUpdated.emit),
            (self.ui.checkBox_delete_add_date.stateChanged, self.SignalFilterUpdated.emit),
            (self.ui.spinBox_add_date.valueChanged, self.SignalFilterUpdated.emit),
            (self.ui.checkBox_delete_use_date.stateChanged, self.SignalFilterUpdated.emit),
            (self.ui.spinBox_use_date.valueChanged, self.SignalFilterUpdated.emit),
            # 操作按钮
            (self.ui.pushButton_show_detail.clicked, self.SignalShowDetail.emit),
            (self.ui.pushButton_preview.clicked, self.change_preview),
            (self.ui.pushButton_delete.clicked, self.show_confirm_dialog),
        ]
        for signal, slot in connections:
            signal.connect(slot)
    # endregion


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = PasswordManagerViewer()
    program_ui.show()
    app_.exec()
