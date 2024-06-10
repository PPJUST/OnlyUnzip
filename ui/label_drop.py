# 支持拖入文件/文件夹的label

from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import QLabel

from constant import _ICON_MAIN_DEFAULT, _ICON_DROP


class LabelDrop(QLabel):
    """支持拖入文件/文件夹的label"""

    signal_dropped = Signal(list)  # 发送拖入的所有路径list

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setScaledContents(True)

        self.setPixmap(QPixmap(_ICON_MAIN_DEFAULT))
        self.last_icon_pixmap = None  # 上一个图标的pixmap对象
        self.icon_movie = QMovie()  # 动图对象，用于显示GIF

    def reset_icon(self, icon: str):
        if icon.endswith('.gif'):
            self.icon_movie = QMovie(icon)
            self.setMovie(self.icon_movie)
            self.icon_movie.start()
        else:
            self.icon_movie.stop()
            self.setPixmap(QPixmap(icon))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.last_icon_pixmap = self.pixmap()
            self.setPixmap(QPixmap(_ICON_DROP))
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setPixmap(self.last_icon_pixmap)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            drop_paths = [url.toLocalFile() for url in urls]
            self.signal_dropped.emit(drop_paths)
