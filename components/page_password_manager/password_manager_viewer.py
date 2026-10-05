# ????????????
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox

from components.page_password_manager.res.ui_manager import Ui_Form


class PasswordManagerViewer(QWidget):
    """????????????"""
    SignalFilterUpdated = Signal(object, name="?????????????")
    SignalDeleted = Signal(object, name="???????")
    SignalShowDetail = Signal(name="??????")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.passwords_need_delete = []

        self.hidden_preview()
        self._bind_signal()

    def set_count_100(self, count: int):
        """??????>100?????"""
        self.ui.label_pw_count_100.setText(str(count))

    def set_count_10(self, count: int):
        """??10<????<100?????"""
        self.ui.label_pw_count_10.setText(str(count))

    def set_count_1(self, count: int):
        """??1<????<10?????"""
        self.ui.label_pw_count_1.setText(str(count))

    def set_count_0(self, count: int):
        """???????????"""
        self.ui.label_pw_count_0.setText(str(count))

    def set_passwords_need_delete(self, passwords: list):
        """?????????"""
        self.passwords_need_delete = passwords
        self.ui.label_count_delete.setText(str(len(passwords)))
        self.set_preview_passwords()

    def change_preview(self):
        if self.ui.textBrowser_preview.isVisible():
            self.hidden_preview()
        else:
            self.show_preview()

    def set_preview_passwords(self):
        """???????????"""
        self.ui.textBrowser_preview.setText('\n'.join(self.passwords_need_delete))

    def show_preview(self):
        """????????"""
        self.set_preview_passwords()
        self.ui.textBrowser_preview.setVisible(True)
        self.ui.label_spacer.setVisible(False)

    def hidden_preview(self):
        """????????"""
        self.ui.textBrowser_preview.setVisible(False)
        self.ui.label_spacer.setVisible(True)

    def show_confirm_dialog(self):
        """??????"""
        reply = QMessageBox.question(
            self,
            "????",
            "???????????\n???????!",
            QMessageBox.Yes | QMessageBox.No,  # ??Yes?No??
            QMessageBox.No  # ????No??
        )

        # ????????????
        if reply == QMessageBox.Yes:
            self.SignalDeleted.emit(self.passwords_need_delete)

    def _bind_signal(self):
        self.ui.checkBox_delete_use_count.stateChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.spinBox_use_count.valueChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.checkBox_delete_add_date.stateChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.spinBox_add_date.valueChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.checkBox_delete_use_date.stateChanged.connect(self.SignalFilterUpdated.emit)
        self.ui.spinBox_use_date.valueChanged.connect(self.SignalFilterUpdated.emit)

        self.ui.pushButton_show_detail.clicked.connect(self.SignalShowDetail.emit)
        self.ui.pushButton_preview.clicked.connect(self.change_preview)
        self.ui.pushButton_delete.clicked.connect(self.show_confirm_dialog)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = PasswordManagerViewer()
    program_ui.show()
    app_.exec()
