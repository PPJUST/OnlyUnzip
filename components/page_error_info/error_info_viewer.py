# 报错信息模块的界面组件
from PySide6.QtWidgets import QApplication, QWidget

from components.page_error_info.res.ui_error_info import Ui_Form


class ErrorInfoViewer(QWidget):
    """报错信息模块的界面组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._set_info()

    def append_info(self, info: str):
        self.ui.textBrowser.append(info)

    def _set_info(self):
        self.ui.textBrowser.setPlaceholderText('报错信息')


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = ErrorInfoViewer()
    program_ui.show()
    app_.exec()
