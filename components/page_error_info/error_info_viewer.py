# 报错信息模块的界面组件
from PySide6.QtWidgets import QApplication, QWidget

from components.page_error_info.res.ui_error_info import Ui_Form


class ErrorInfoViewer(QWidget):
    """报错信息模块的界面组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 没有信息时显示提示文本
        self.ui.textBrowser.setPlaceholderText('报错信息')

    def append_info(self, info: str):
        """在信息区域追加一行文本

        :param info: 已格式化好的信息文本
        """
        self.ui.textBrowser.append(info)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = ErrorInfoViewer()
    program_ui.show()
    app_.exec()
