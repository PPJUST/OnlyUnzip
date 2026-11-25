import base64
from typing import Union

from PySide6.QtCore import QBuffer, QIODevice
from PySide6.QtGui import QMovie, QPixmap, Qt
from PySide6.QtWidgets import QApplication, QLabel, QSizePolicy


class LabelIcon(QLabel):
    """用于显示图标的自定义label"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setScaledContents(True)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.current_icon = None  # 当前显示的图片对象
        self.pixmap_current = None  # 当前设置的静态图片
        self.movie_current = None  # 当前设置的动画

    def set_icon(self, icon: Union[QPixmap, bytes]):
        """设置静态图标
        :param icon: base64编码的bytes数据"""
        if not isinstance(icon, bytes):
            return

        self.pixmap_current = self._base64_to_pixmap(icon)
        self._stop_movie()
        self.setPixmap(self.pixmap_current)
        self.current_icon = self.pixmap_current

    def set_gif_icon(self, icon: Union[QMovie, bytes]):
        """设置动态图标
        :param icon: base64编码的bytes数据"""
        if not isinstance(icon, bytes):
            return

        movie = self._base64_to_movie(icon)
        self._stop_movie()
        self.movie_current = movie
        self.setMovie(self.movie_current)
        self.movie_current.start()
        self.current_icon = self.movie_current

    @staticmethod
    def _base64_to_pixmap(image_base64: bytes) -> QPixmap:
        """base64数据转为QPixmap"""
        byte_data = base64.b64decode(image_base64)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_data)
        return pixmap

    @staticmethod
    def _base64_to_movie(image_base64: bytes) -> QMovie:
        """base64数据转为QMovie"""
        gif_data = base64.b64decode(image_base64)

        buffer = QBuffer()
        buffer.setData(gif_data)
        buffer.open(QIODevice.ReadOnly)

        movie = QMovie()
        movie.setDevice(buffer)
        movie.setCacheMode(QMovie.CacheAll)
        return movie

    def _stop_movie(self):
        """停止动画"""
        if self.movie_current:
            self.movie_current.stop()


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = LabelIcon()
    program_ui.show()
    app_.exec()
