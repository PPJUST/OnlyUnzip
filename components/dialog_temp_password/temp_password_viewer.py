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

        # 初始化
        self.setFixedSize(300, 300)
        self.ui.pushButton_write_to_db.setEnabled(False)
        self._bind_signal()
        self.ui.plainTextEdit_password.dropEvent = self.drop_event
        self.ui.plainTextEdit_password.textChanged.connect(self.check_pw)
        self._set_tip()

    def append_pw(self, text: str):
        """向密码框中添加密码"""
        self.ui.plainTextEdit_password.appendPlainText(text)

    def get_passwords(self):
        """获取当前密码"""
        splits = self.ui.plainTextEdit_password.toPlainText().split('\n')
        pws = [i for i in splits if i]
        return pws

    def set_db_button_enable(self, is_enable: bool):
        """设置写入密码本按钮是否启用"""
        self.ui.pushButton_write_to_db.setEnabled(is_enable)

    def clear_pw(self):
        """清空密码框"""
        self.ui.plainTextEdit_password.clear()

    def check_pw(self):
        """检查密码框"""
        if self.ui.plainTextEdit_password.toPlainText():
            self.set_db_button_enable(True)
        else:
            self.set_db_button_enable(False)

    def _bind_signal(self):
        """绑定信号"""
        self.ui.pushButton_read_clipboard.clicked.connect(self.ReadClipboard.emit)
        self.ui.pushButton_write_to_db.clicked.connect(self._emit_signal_write_to_db)
        self.ui.pushButton_clear_password.clicked.connect(self.clear_pw)

    def _set_tip(self):
        self.ui.plainTextEdit_password.setPlaceholderText(
            '仅在本次运行期间生效\n\n程序退出后将自动删除\n\n临时密码即使被使用也不会写入密码本（除非主动写入）')

    def _emit_signal_write_to_db(self):
        self.WriteToDB.emit(self.get_passwords())
        self.clear_pw()

    def drop_event(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

            # 获取所有拖入文件的路径
            urls = event.mimeData().urls()
            file_paths = [url.toLocalFile() for url in urls]
            self.DropFiles.emit(file_paths)

        else:
            event.ignore()


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = TempPasswordViewer()
    program_ui.show()
    app_.exec()
