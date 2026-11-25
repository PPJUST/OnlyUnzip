# 主窗口的界面组件

import lzytools_Qt
from PySide6.QtCore import Signal
from PySide6.QtGui import Qt, QFont
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow
from PyTaskbar import TaskbarProgress, ProgressType

from components.window.res.icon_base64 import ICON_HOMEPAGE, ICON_PASSWORD, ICON_SETTING, ICON_HISTORY, \
    ICON_PIXEL_128X128, ICON_ABOUT, ICON_WARNING
from components.window.res.ui_mainWindow import Ui_MainWindow

_ID = 'id'  # 绑定按钮的 id 名称，仅用于索引
_DEFAULT_BUTTON_STYLE = ''  # 默认的按钮样式
_HIGHLIGHT_BUTTON_STYLE = r'background-color: rgb(255, 228, 181);'  # 高亮的按钮样式

# 页面名称与 stackedWidget 索引的对应关系，集中管理避免各处硬编码数字
_PAGE_INDEX = {
    'home': 0,
    'password': 1,
    'setting': 2,
    'history': 3,
    'error': 4,
    'password_manager': 5,
    'about': 6,
}


class WindowViewer(QMainWindow):
    """主窗口的界面组件"""

    PageChanged = Signal(object, name='已切换页面')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Windows 任务栏进度条状态
        self._progress = None
        self._last_progress_state = None
        self._count_progress = 0
        self._index_progress = 0

        # 页面控件与页面名称的对应关系
        self._page_widgets = {
            'home': self.ui.page_home,
            'password': self.ui.page_password,
            'setting': self.ui.page_setting,
            'history': self.ui.page_history,
            'error': self.ui.page_error_info,
            'password_manager': self.ui.page_password_manager,
            'about': self.ui.page_about,
        }

        self._init_buttons()
        self._init_window()
        self.change_page(_PAGE_INDEX['home'])

        # 绑定信号
        self.ui.buttonGroup.buttonClicked.connect(self.change_page)
        self.ui.stackedWidget.currentChanged.connect(self.PageChanged.emit)

    def _init_buttons(self):
        """统一设置导航按钮的 id、图标、尺寸和字体"""
        font = QFont()
        font.setPointSize(12)

        buttons = [
            (self.ui.pushButton_home, ICON_HOMEPAGE, _PAGE_INDEX['home']),
            (self.ui.pushButton_password, ICON_PASSWORD, _PAGE_INDEX['password']),
            (self.ui.pushButton_setting, ICON_SETTING, _PAGE_INDEX['setting']),
            (self.ui.pushButton_history, ICON_HISTORY, _PAGE_INDEX['history']),
            (self.ui.pushButton_error, ICON_WARNING, _PAGE_INDEX['error']),
            (self.ui.pushButton_about, ICON_ABOUT, _PAGE_INDEX['about']),
        ]
        for button, icon, index in buttons:
            button.setProperty(_ID, index)
            button.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(icon))
            button.setFixedHeight(round(button.width() * 0.618, 0))
            button.setFont(font)

    def _init_window(self):
        """设置窗口初始属性和图标"""
        self.resize(330, 330)
        self.ui.pushButton_error.setVisible(False)
        self.ui.pushButton_about.setVisible(False)
        # 屏蔽最大化功能
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_PIXEL_128X128))

    def add_page(self, page_name: str, widget: QWidget):
        """把子页面控件添加到指定的页面中"""
        self._page_widgets[page_name].layout().addWidget(widget)

    def open_page(self, page_name: str):
        """打开指定的页面"""
        self.change_page(_PAGE_INDEX[page_name])

    def show_button_error_info(self):
        self.ui.pushButton_error.setVisible(True)

    def hide_button_error_info(self):
        self.ui.pushButton_error.setVisible(False)

    def change_page(self, page):
        """切换页面，参数可以是页面索引或导航按钮对象"""
        if isinstance(page, int):
            index = page
        else:
            index = page.property(_ID)

        self.ui.stackedWidget.setCurrentIndex(index)
        for button in self.ui.buttonGroup.buttons():
            if button.property(_ID) == index:
                button.setStyleSheet(_HIGHLIGHT_BUTTON_STYLE)
            else:
                button.setStyleSheet(_DEFAULT_BUTTON_STYLE)

    def top_window(self):
        """设置窗口置顶"""
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.show()  # 修改窗口标志后需要重新调用 show() 才能生效

    def disable_top_window(self):
        """取消窗口置顶"""
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.show()

    def lock_size(self):
        """锁定窗口大小"""
        self.setFixedSize(self.size())

    def disable_lock_size(self):
        """取消锁定窗口大小"""
        # setFixedSize() 同时设置了最小和最大尺寸，取消时重新设置即可
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)

    def set_progress_count(self, count: int):
        self._count_progress = count

    def set_progress_index(self, index: int):
        self._index_progress = index
        if self._count_progress <= 0:
            return
        percent = int(self._index_progress / self._count_progress * 100)
        self.show_normal_progress(percent)

    def _set_progress_type(self, progress_type):
        """切换任务栏进度状态，仅在状态变化时更新"""
        if self._progress is None:
            return
        if self._last_progress_state != progress_type:
            self._last_progress_state = progress_type
            self._progress.set_progress_type(progress_type)

    def show_indeterminate_progress(self):
        """任务栏显示不确定进度状态"""
        self._set_progress_type(ProgressType.INDETERMINATE)

    def show_normal_progress(self, value: int):
        """任务栏显示正常进度状态
        :param value:int，0~100"""
        if self._progress is None:
            return
        self._set_progress_type(ProgressType.NORMAL)
        self._progress.set_progress(value)

    def show_error_progress(self):
        """任务栏显示错误进度状态"""
        self._set_progress_type(ProgressType.ERROR)

    def show_finish_progress(self):
        """任务栏显示结束进度状态"""
        if self._progress is None:
            return
        if self._last_progress_state != ProgressType.NOPROGRESS:
            self._last_progress_state = ProgressType.NOPROGRESS
            self._progress.set_progress_type(ProgressType.NOPROGRESS)
            self._progress.flash_done()

    def resizeEvent(self, event):
        # 保持窗口为正方形
        side = max(event.size().width(), event.size().height())
        self.resize(side, side)

    def showEvent(self, event):
        super().showEvent(event)
        if self._progress is None:
            self._progress = TaskbarProgress(int(self.winId()))


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = WindowViewer()
    program_ui.show()
    app_.exec()
