# 主窗口的界面组件
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow
from lzytools._qt_pyside6 import base64_to_pixmap

from components.window.res.icon_base64 import ICON_APP, ICON_HOMEPAGE, ICON_PASSWORD, ICON_SETTING, ICON_HISTORY
from components.window.res.ui_mainWindow import Ui_MainWindow

_ID = 'id'  # 绑定按钮的id名称，仅用于索引
_DEFAULT_BUTTON_STYLE = ''  # 默认的按钮样式
_HIGHLIGHT_BUTTON_STYLE = r'background-color: rgb(255, 228, 181);'  # 高亮的按钮样式


class WindowViewer(QMainWindow):
    """主窗口的界面组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化
        # 设置按钮索引
        self.ui.pushButton_home.setProperty(_ID, 0)
        self.ui.pushButton_password.setProperty(_ID, 1)
        self.ui.pushButton_setting.setProperty(_ID, 2)
        self.ui.pushButton_history.setProperty(_ID, 3)
        self.change_page(0)
        # 设置按钮尺寸
        self._set_button_size()
        # 设置图标
        self.setWindowIcon(base64_to_pixmap(ICON_APP))
        self.ui.pushButton_home.setIcon(base64_to_pixmap(ICON_HOMEPAGE))
        self.ui.pushButton_password.setIcon(base64_to_pixmap(ICON_PASSWORD))
        self.ui.pushButton_setting.setIcon(base64_to_pixmap(ICON_SETTING))
        self.ui.pushButton_history.setIcon(base64_to_pixmap(ICON_HISTORY))
        # 绑定信号
        self.ui.buttonGroup.buttonClicked.connect(self.change_page)

    def add_page_home(self, widget: QWidget):
        """添加主页控件"""
        self.ui.page_home.layout().addWidget(widget)

    def add_page_password(self, widget: QWidget):
        """添加密码控件"""
        self.ui.page_password.layout().addWidget(widget)

    def add_page_setting(self, widget: QWidget):
        """添加设置控件"""
        self.ui.page_setting.layout().addWidget(widget)

    def add_page_history(self, widget: QWidget):
        """添加历史控件"""
        self.ui.page_history.layout().addWidget(widget)

    def change_page(self, id_button):
        """切页"""
        # 获取索引
        index = id_button if isinstance(id_button, int) else id_button.property(_ID)
        # 切页
        self.ui.stackedWidget.setCurrentIndex(index)
        # 高亮
        for button in self.ui.buttonGroup.buttons():
            id_ = button.property(_ID)
            if id_ == index:
                button.setStyleSheet(_HIGHLIGHT_BUTTON_STYLE)
            else:
                button.setStyleSheet(_DEFAULT_BUTTON_STYLE)

    def top_window(self):
        """设置窗口置顶"""
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.show()  # 使用 setWindowFlags() 后需要重新调用 show() 方法才能使更改生效

    def disable_top_window(self):
        """取消窗口置顶"""
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.show()  # 使用 setWindowFlags() 后需要重新调用 show() 方法才能使更改生效

    def lock_size(self):
        """锁定窗口大小"""
        self.setFixedSize(self.size())

    def disable_lock_size(self):
        """取消锁定窗口大小"""
        # setFixedSize()实际上是同时设置了最小和最大尺寸为相同值，取消锁定直接重新设置最大最小值即可
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)

    def _set_button_size(self):
        """设置按钮尺寸"""
        self.ui.pushButton_home.setFixedHeight(round(self.ui.pushButton_home.width() * 0.618, 0))
        self.ui.pushButton_password.setFixedHeight(round(self.ui.pushButton_password.width() * 0.618, 0))
        self.ui.pushButton_setting.setFixedHeight(round(self.ui.pushButton_setting.width() * 0.618, 0))
        self.ui.pushButton_history.setFixedHeight(round(self.ui.pushButton_history.width() * 0.618, 0))


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = WindowViewer()
    program_ui.show()
    app_.exec()
