# ???????????

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QDialog

from components.dialog_temp_password.res.ui_dialog import Ui_Dialog


class TempPasswordViewer(QDialog):
    """???????????"""
    ReadClipboard = Signal(name="?????")
    WriteToDB = Signal(list, name="?????")
    DropFiles = Signal(list, name="????")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # ???
        self.setFixedSize(300, 300)
        self.ui.pushButton_write_to_db.setEnabled(False)
        self._bind_signal()
        self.ui.plainTextEdit_password.dropEvent = self.drop_event
        self.ui.plainTextEdit_password.textChanged.connect(self.check_pw)
        self._set_tip()

    def append_pw(self, text: str):
        """?????????"""
        self.ui.plainTextEdit_password.appendPlainText(text)

    def get_passwords(self):
        """??????"""
        splits = self.ui.plainTextEdit_password.toPlainText().split('\n')
        pws = [i for i in splits if i]
        return pws

    def set_db_button_enable(self, is_enable: bool):
        """?????????????"""
        self.ui.pushButton_write_to_db.setEnabled(is_enable)

    def clear_pw(self):
        """?????"""
        self.ui.plainTextEdit_password.clear()

    def check_pw(self):
        """?????"""
        if self.ui.plainTextEdit_password.toPlainText():
            self.set_db_button_enable(True)
        else:
            self.set_db_button_enable(False)

    def _bind_signal(self):
        """????"""
        self.ui.pushButton_read_clipboard.clicked.connect(self.ReadClipboard.emit)
        self.ui.pushButton_write_to_db.clicked.connect(self._emit_signal_write_to_db)
        self.ui.pushButton_clear_password.clicked.connect(self.clear_pw)

    def _set_tip(self):
        self.ui.plainTextEdit_password.setPlaceholderText(
            '??????????\n\n??????????\n\n?????????????????(??????)')

    def _emit_signal_write_to_db(self):
        self.WriteToDB.emit(self.get_passwords())
        self.clear_pw()

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
    program_ui = TempPasswordViewer()
    program_ui.show()
    app_.exec()
