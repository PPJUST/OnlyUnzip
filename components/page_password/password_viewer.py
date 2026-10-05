# ?????????
# ?????,???????
import lzytools_Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget

from components.page_password.res.icon_base64 import ICON_ERASER
from components.page_password.res.ui_page_password import Ui_Form


class PasswordViewer(QWidget):
    """?????????"""
    ReadClipboard = Signal(name="?????")
    OutputPassword = Signal(name="????")
    OpenPassword = Signal(name="??????")
    UpdatePassword = Signal(str, name="?????")
    DropFiles = Signal(list, name="????")
    OpenPasswordManager = Signal(name="???????")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # ???
        self.ui.pushButton_open.setEnabled(False)
        # self.ui.pushButton_update.setEnabled(False)
        self._bind_signal()
        self._load_icon()
        self.ui.plainTextEdit_password.dropEvent = self.drop_event

    def append_pw(self, text: str):
        """?????????"""
        self.ui.plainTextEdit_password.appendPlainText(text)

    def set_open_button_enable(self, is_enable: bool):
        """????????????????"""
        self.ui.pushButton_open.setEnabled(is_enable)

    def show_pw_count_info(self, text: str):
        """?????????"""
        self.ui.plainTextEdit_password.setPlaceholderText(text)

    def clear_pw(self):
        """?????"""
        self.ui.plainTextEdit_password.clear()

    def _bind_signal(self):
        """????"""
        self.ui.pushButton_password_details.clicked.connect(self.OpenPasswordManager.emit)
        self.ui.pushButton_clipboard.clicked.connect(self.ReadClipboard.emit)
        self.ui.pushButton_output.clicked.connect(self.OutputPassword.emit)
        self.ui.pushButton_open.clicked.connect(self.OpenPassword.emit)
        self.ui.pushButton_update.clicked.connect(
            lambda: self.UpdatePassword.emit(self.ui.plainTextEdit_password.toPlainText()))
        # self.ui.plainTextEdit_password.textChanged.connect(self._pw_text_changed)
        self.ui.toolButton_clear.clicked.connect(self.clear_pw)

    def _load_icon(self):
        """????"""
        self.ui.toolButton_clear.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_ERASER))

    def drop_event(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

            # ???????????
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
