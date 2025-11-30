# 主窗口的界面组件
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow
from lzytools._qt_pyside6 import base64_to_pixmap

from components.window.res.icon_base64 import ICON_HOMEPAGE, ICON_PASSWORD, ICON_SETTING, ICON_HISTORY, \
    ICON_PIXEL_128X128, ICON_ABOUT
from components.window.res.ui_mainWindow import Ui_MainWindow

_ID = 'id'  # 绑定按钮的id名称，仅用于索引
_DEFAULT_BUTTON_STYLE = ''  # 默认的按钮样式
_HIGHLIGHT_BUTTON_STYLE = r'background-color: rgb(255, 228, 181);'  # 高亮的按钮样式


# 　todo 首页左上角添加一个按钮，点击后拉伸出常用按钮选项，用于快速修改设置（暂定为解压/测试模式，处理未知格式文件，窗口置顶）

class WindowViewer(QMainWindow):
    """主窗口的界面组件"""
    PageChanged = Signal(object, name='已切换页面')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化
        self.resize(330, 330)
        self.ui.pushButton_about.setVisible(False)
        # 屏蔽最大化功能
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        # 设置按钮索引
        self.ui.pushButton_home.setProperty(_ID, 0)
        self.ui.pushButton_password.setProperty(_ID, 1)
        self.ui.pushButton_setting.setProperty(_ID, 2)
        self.ui.pushButton_history.setProperty(_ID, 3)
        self.ui.pushButton_about.setProperty(_ID, 4)
        self.change_page(0)
        # 设置按钮尺寸
        self._set_button_size()
        # 设置图标
        self.setWindowIcon(base64_to_pixmap(ICON_PIXEL_128X128))
        self.ui.pushButton_home.setIcon(base64_to_pixmap(ICON_HOMEPAGE))
        self.ui.pushButton_password.setIcon(base64_to_pixmap(ICON_PASSWORD))
        self.ui.pushButton_setting.setIcon(base64_to_pixmap(ICON_SETTING))
        self.ui.pushButton_history.setIcon(base64_to_pixmap(ICON_HISTORY))
        self.ui.pushButton_about.setIcon(base64_to_pixmap(ICON_ABOUT))
        # 绑定信号
        self.ui.buttonGroup.buttonClicked.connect(self.change_page)
        self.ui.stackedWidget.currentChanged.connect(self.PageChanged.emit)

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

    def add_page_about(self, widget: QWidget):
        """添加关于控件"""
        self.ui.page_about.layout().addWidget(widget)

    def add_page_password_manager(self, widget: QWidget):
        """添加密码管理器控件"""
        self.ui.page_password_manager.layout().addWidget(widget)

    def open_page_about(self):
        self.change_page(5)

    def open_page_password_manager(self):
        self.change_page(4)

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
        self.ui.pushButton_about.setFixedHeight(round(self.ui.pushButton_history.width() * 0.618, 0))

        font = QFont()
        font.setPointSize(12)
        self.ui.pushButton_home.setFont(font)
        self.ui.pushButton_password.setFont(font)
        self.ui.pushButton_setting.setFont(font)
        self.ui.pushButton_history.setFont(font)
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
