# 临时密码模块的界面组件

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QDialog

from components.dialog_temp_password.res.ui_dialog import Ui_Dialog


class TempPasswordViewer(QDialog):
    """临时密码模块的界面组件"""
    ReadClipboard = Signal(name="读取剪贴板")
    WriteToDB = Signal(list, name="写入密码本")
    DropFiles = Signal(list, name="拖入文件")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 初始化界面
        self.setFixedSize(300, 300)
        self._set_tip()
        self._bind_signal()
        self._setup_password_edit()

    def append_pw(self, text: str):
        """向密码框中添加密码"""
        if text.strip():
            self.ui.plainTextEdit_password.appendPlainText(text)

    def get_passwords(self) -> list:
        """获取密码框中的所有密码

        :return: 去掉空白行后的密码列表
        """
        text = self.ui.plainTextEdit_password.toPlainText()
        passwords = []
        for line in text.splitlines():
            password = line
            if password.strip():
                passwords.append(password)
        return passwords

    def clear_pw(self):
        """清空密码框"""
        self.ui.plainTextEdit_password.clear()

    def _set_db_button_enable(self, is_enable: bool):
        """设置写入密码本按钮是否启用"""
        self.ui.pushButton_write_to_db.setEnabled(is_enable)

    def _check_pw(self):
        """根据密码框内容更新写入按钮状态"""
        has_password = bool(self.ui.plainTextEdit_password.toPlainText().strip())
        self._set_db_button_enable(has_password)

    def _bind_signal(self):
        """绑定按钮信号"""
        self.ui.pushButton_read_clipboard.clicked.connect(self.ReadClipboard.emit)
        self.ui.pushButton_write_to_db.clicked.connect(self._write_to_db_clicked)
        self.ui.pushButton_clear_password.clicked.connect(self.clear_pw)

    def _setup_password_edit(self):
        """设置密码框的拖入与内容变化处理"""
        self.ui.plainTextEdit_password.dropEvent = self.drop_event
        self.ui.plainTextEdit_password.textChanged.connect(self._check_pw)
        self._check_pw()

    def _set_tip(self):
        """设置密码框提示文字"""
        tip_lines = [
            '仅在本次运行期间生效',
            '',
            '程序退出后将自动删除',
            '',
            '临时密码即使被使用也不会写入密码本（除非主动写入）',
        ]
        self.ui.plainTextEdit_password.setPlaceholderText('\n'.join(tip_lines))

    def _write_to_db_clicked(self):
        """点击写入按钮时发出信号并清空密码框"""
        self.WriteToDB.emit(self.get_passwords())
        self.clear_pw()

    def drop_event(self, event):
        """处理拖入文件的事件"""
        if not event.mimeData().hasUrls():
            event.ignore()
            return

        event.acceptProposedAction()
        file_paths = []
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path:
                file_paths.append(path)
        if file_paths:
            self.DropFiles.emit(file_paths)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = TempPasswordViewer()
    program_ui.show()
    app_.exec()
