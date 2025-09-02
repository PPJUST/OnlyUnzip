# 密码管理器模块的界面组件
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget

from components.page_password_manager.res.ui_manager import Ui_Form


class PasswordManagerViewer(QWidget):
    """密码管理器模块的界面组件"""
    SignalFilterUpdated = Signal(object, name="预删除密码的过滤器选项更新")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.passwords_need_delete = []

        self._bind_signal()

    def set_count_100(self, count: int):
        """显示使用次数>100的密码数量"""
        self.ui.label_pw_count_100.setText(str(count))

    def set_count_10(self, count: int):
        """显示10<使用次数<100的密码数量"""
        self.ui.label_pw_count_10.setText(str(count))

    def set_count_1(self, count: int):
        """显示1<使用次数<10的密码数量"""
        self.ui.label_pw_count_1.setText(str(count))

    def set_count_0(self, count: int):
        """显示未使用过的密码数量"""
        self.ui.label_pw_count_0.setText(str(count))

    def set_passwords_need_delete(self, passwords: list):
        """设置需要删除的密码"""
        self.passwords_need_delete = passwords
        self.ui.label_count_delete.setText(str(len(passwords)))

    def _bind_signal(self):
        self.ui.checkBox_delete_use_count.stateChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.spinBox_use_count.valueChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.checkBox_delete_add_date.stateChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.spinBox_add_date.valueChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.checkBox_delete_use_date.stateChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.spinBox_use_date.valueChanged.connect(self.SignalFilterUpdated.emit)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = PasswordManagerViewer()
    program_ui.show()
    app_.exec()
