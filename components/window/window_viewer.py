# ????????
import lzytools_Qt
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow

from components.window.res.icon_base64 import ICON_HOMEPAGE, ICON_PASSWORD, ICON_SETTING, ICON_HISTORY, \
    ICON_PIXEL_128X128, ICON_ABOUT, ICON_WARNING
from components.window.res.ui_mainWindow import Ui_MainWindow

_ID = 'id'  # ?????id??,?????
_DEFAULT_BUTTON_STYLE = ''  # ???????
_HIGHLIGHT_BUTTON_STYLE = r'background-color: rgb(255, 228, 181);'  # ???????


class WindowViewer(QMainWindow):
    """????????"""
    PageChanged = Signal(object, name='?????')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ???
        self.resize(330, 330)
        self.ui.pushButton_error.setVisible(False)
        self.ui.pushButton_about.setVisible(False)
        # ???????
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        # ??????
        self.ui.pushButton_home.setProperty(_ID, 0)
        self.ui.pushButton_password.setProperty(_ID, 1)
        self.ui.pushButton_setting.setProperty(_ID, 2)
        self.ui.pushButton_history.setProperty(_ID, 3)
        self.ui.pushButton_error.setProperty(_ID, 4)
        self.ui.pushButton_about.setProperty(_ID, 5)
        self.change_page(0)
        # ??????
        self._set_button_size()
        # ????
        self.setWindowIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_PIXEL_128X128))
        self.ui.pushButton_home.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_HOMEPAGE))
        self.ui.pushButton_password.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_PASSWORD))
        self.ui.pushButton_setting.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_SETTING))
        self.ui.pushButton_history.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_HISTORY))
        self.ui.pushButton_error.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_WARNING))
        self.ui.pushButton_about.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_ABOUT))
        # ????
        self.ui.buttonGroup.buttonClicked.connect(self.change_page)
        self.ui.stackedWidget.currentChanged.connect(self.PageChanged.emit)

    def add_page_home(self, widget: QWidget):
        """??????"""
        self.ui.page_home.layout().addWidget(widget)

    def add_page_password(self, widget: QWidget):
        """??????"""
        self.ui.page_password.layout().addWidget(widget)

    def add_page_setting(self, widget: QWidget):
        """??????"""
        self.ui.page_setting.layout().addWidget(widget)

    def add_page_history(self, widget: QWidget):
        """??????"""
        self.ui.page_history.layout().addWidget(widget)

    def add_page_error_info(self, widget: QWidget):
        """????????"""
        self.ui.page_error_info.layout().addWidget(widget)

    def add_page_about(self, widget: QWidget):
        """??????"""
        self.ui.page_about.layout().addWidget(widget)

    def add_page_password_manager(self, widget: QWidget):
        """?????????"""
        self.ui.page_password_manager.layout().addWidget(widget)

    def open_page_error_info(self):
        self.change_page(4)

    def show_button_error_info(self):
        self.ui.pushButton_error.setVisible(True)

    def hide_button_error_info(self):
        self.ui.pushButton_error.setVisible(False)

    def open_page_about(self):
        self.change_page(6)

    def open_page_password_manager(self):
        self.change_page(5)

    def change_page(self, id_button):
        """??"""
        # ????
        index = id_button if isinstance(id_button, int) else id_button.property(_ID)
        # ??
        self.ui.stackedWidget.setCurrentIndex(index)
        # ??
        for button in self.ui.buttonGroup.buttons():
            id_ = button.property(_ID)
            if id_ == index:
                button.setStyleSheet(_HIGHLIGHT_BUTTON_STYLE)
            else:
                button.setStyleSheet(_DEFAULT_BUTTON_STYLE)

    def top_window(self):
        """??????"""
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.show()  # ?? setWindowFlags() ??????? show() ?????????

    def disable_top_window(self):
        """??????"""
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.show()  # ?? setWindowFlags() ??????? show() ?????????

    def lock_size(self):
        """??????"""
        self.setFixedSize(self.size())

    def disable_lock_size(self):
        """????????"""
        # setFixedSize()????????????????????,?????????????????
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)

    def _set_button_size(self):
        """??????"""
        self.ui.pushButton_home.setFixedHeight(round(self.ui.pushButton_home.width() * 0.618, 0))
        self.ui.pushButton_password.setFixedHeight(round(self.ui.pushButton_password.width() * 0.618, 0))
        self.ui.pushButton_setting.setFixedHeight(round(self.ui.pushButton_setting.width() * 0.618, 0))
        self.ui.pushButton_history.setFixedHeight(round(self.ui.pushButton_history.width() * 0.618, 0))
        self.ui.pushButton_error.setFixedHeight(round(self.ui.pushButton_history.width() * 0.618, 0))
        self.ui.pushButton_about.setFixedHeight(round(self.ui.pushButton_history.width() * 0.618, 0))

        font = QFont()
        font.setPointSize(12)
        self.ui.pushButton_home.setFont(font)
        self.ui.pushButton_password.setFont(font)
        self.ui.pushButton_setting.setFont(font)
        self.ui.pushButton_history.setFont(font)
        self.ui.pushButton_error.setFont(font)
        self.ui.pushButton_about.setFont(font)

    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        max_ = max(width, height)
        self.resize(max_, max_)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = WindowViewer()
    program_ui.show()
    app_.exec()
