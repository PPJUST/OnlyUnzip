# 自定义拖入控件

from PySide6.QtCore import Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel
from constant import _ICON_DEFAULT, _ICON_DROP


class DropLabel(QLabel):
    signal_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.icon = _ICON_DEFAULT
        self.last_icon = None
        self.reset_icon(self.icon)

    def reset_icon(self, icon:str):
        self.icon = icon
        self.setPixmap(QPixmap(icon))


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.last_icon = self.pixmap()
            self.setPixmap(QPixmap(_ICON_DROP))
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setPixmap(QPixmap(self.last_icon))

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            drop_path = [url.toLocalFile() for url in urls]
            self.signal_dropped.emit(drop_path)
