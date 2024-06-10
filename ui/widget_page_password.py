# 密码页
from PySide6.QtWidgets import QWidget, QApplication

from module import function_password
from ui.src.ui_widget_page_password import Ui_Form


class WidgetPagePassword(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # ui设置
        self.ui.pushButton_open_export.setEnabled(False)
        self._show_password()

        # 绑定槽函数
        self.ui.pushButton_read_clipboard.clicked.connect(self._read_clipboard)
        self.ui.pushButton_export_password.clicked.connect(self._export_password)
        self.ui.pushButton_open_export.clicked.connect(self._open_export)
        self.ui.pushButton_update_password.clicked.connect(self._update_password)
        self.ui.plainTextEdit_password.textChanged.connect(self._show_password)

    def set_button_state(self, enable: bool):
        """启用/禁用解压相关的按钮"""
        self.ui.pushButton_update_password.setEnabled(enable)

    def _read_clipboard(self):
        """读取剪切板"""
        clipboard = QApplication.clipboard()
        self.ui.plainTextEdit_password.setPlainText(clipboard.text())

    def _export_password(self):
        """导出密码"""
        function_password.export_password()
        self.ui.pushButton_open_export.setEnabled(True)

    def _open_export(self):
        """打开导出的密码文件"""
        function_password.open_export()

    def _update_password(self):
        """更新密码"""
        text = self.ui.plainTextEdit_password.toPlainText()
        passwords = [i for i in text.split('\n') if i.strip()]
        passwords_strip = [i.strip() for i in passwords]  # 考虑到密码两端的空格，同时添加两种形式的密码
        passwords_join = list(set(passwords + passwords_strip))
        function_password.update_password(passwords_join)

        self.ui.plainTextEdit_password.clear()

    def _show_password(self):
        """在文本框中显示密码（淡色）"""
        text_info = '添加密码时，一个密码占一行，点击“更新密码”即可更新。\n\n'
        if not self.ui.plainTextEdit_password.toPlainText():
            passwords = function_password.read_password()
            text_password = '当前密码（按次数排列）\n' + '\n'.join(passwords)
            self.ui.plainTextEdit_password.setPlaceholderText(text_info + text_password)


if __name__ == "__main__":
    app_ = QApplication()
    app_.setStyle('Fusion')
    program_ui = WidgetPagePassword()
    program_ui.show()
    app_.exec()
