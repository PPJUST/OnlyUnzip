import lzytools._qt_pyside6
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QToolButton

from components.page_home.res.icon_base64 import ICON_TEMP_PASSWORD
from components.page_home.res.label_icon import LabelIcon


class LabelIconWithFloatButton(LabelIcon):
    """用于显示图标的自定义label，附带一个左下角悬浮的button"""
    ButtonClicked = Signal(name="点击按钮")

    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建悬浮按钮
        self.float_button = QToolButton()
        self.float_button.setFixedSize(25, 25)
        self.float_button.setIcon(lzytools._qt_pyside6.base64_to_pixmap(ICON_TEMP_PASSWORD))

        # 将按钮添加到窗口，但不使用布局管理器控制其位置
        self.float_button.setParent(self)
        self.float_button.clicked.connect(self.ButtonClicked.emit)
        self.float_button.show()

        # 调整按钮初始位置
        self.adjust_button_position()

    def adjust_button_position(self):
        """调整按钮位置，固定在widget的左下角"""
        # 获取窗口大小
        widget_height = self.height()

        # 获取按钮大小
        button_height = self.float_button.height()

        # 设置按钮位置
        margin_left = 10
        margin_bottom = 20
        x = margin_left
        y = widget_height - button_height - margin_bottom

        self.float_button.move(x, y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_button_position()


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = LabelIconWithFloatButton()
    program_ui.show()
    app_.exec()
