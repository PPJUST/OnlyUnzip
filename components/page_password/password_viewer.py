# 密码模块的界面组件
# 仅用于显示，不执行具体方法
import lzytools_Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget

from components.page_password.res.icon_base64 import ICON_ERASER
from components.page_password.res.ui_page_password import Ui_Form


class PasswordViewer(QWidget):
    """密码模块的界面组件"""
    ReadClipboard = Signal(name="读取剪贴板")
    OutputPassword = Signal(name="导出密码")
    OpenPassword = Signal(name="打开密码文件")
    UpdatePassword = Signal(str, name="更新密码本")
    DropFiles = Signal(list, name="拖入文件")
    OpenPasswordManager = Signal(name="打开密码管理器")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 初始化
        self.ui.pushButton_open.setEnabled(False)
        # self.ui.pushButton_update.setEnabled(False)
        self._bind_signal()
        self._load_icon()
        self.ui.plainTextEdit_password.dropEvent = self.drop_event

    def append_pw(self, text: str):
        """向密码框中添加密码"""
        self.ui.plainTextEdit_password.appendPlainText(text)

    def set_open_button_enable(self, is_enable: bool):
        """设置打开导出密码文件按钮是否启用"""
        self.ui.pushButton_open.setEnabled(is_enable)

    def show_pw_count_info(self, text: str):
        """显示密码本统计信息"""
        self.ui.plainTextEdit_password.setPlaceholderText(text)

    def clear_pw(self):
        """清空密码框"""
        self.ui.plainTextEdit_password.clear()

    def _bind_signal(self):
        """绑定信号"""
        self.ui.pushButton_password_details.clicked.connect(self.OpenPasswordManager.emit)
        self.ui.pushButton_clipboard.clicked.connect(self.ReadClipboard.emit)
        self.ui.pushButton_output.clicked.connect(self.OutputPassword.emit)
        self.ui.pushButton_open.clicked.connect(self.OpenPassword.emit)
        self.ui.pushButton_update.clicked.connect(
            lambda: self.UpdatePassword.emit(self.ui.plainTextEdit_password.toPlainText()))
        # self.ui.plainTextEdit_password.textChanged.connect(self._pw_text_changed)
        self.ui.toolButton_clear.clicked.connect(self.clear_pw)

    def _load_icon(self):
        """加载图标"""
        self.ui.toolButton_clear.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_ERASER))

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
    program_ui = PasswordViewer()
    program_ui.show()
    app_.exec()
