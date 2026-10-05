import base64
from typing import Union

from PySide6.QtCore import QBuffer, QIODevice, QByteArray
from PySide6.QtGui import QMovie, QPixmap, Qt
from PySide6.QtWidgets import QLabel, QApplication, QSizePolicy


class LabelIcon(QLabel):
    """??????????label"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # ??????
        self.setScaledContents(True)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.setStyleSheet("background-color: lightgreen;")  # ???

        self.current_icon: Union[QPixmap, QMovie] = None  # ?????????
        self.pixmap_current: QPixmap = None  # ?????????
        self.movie_current: QMovie = None  # ???????

    def set_icon(self, icon: Union[QPixmap, bytes]):
        """??????
        :param icon: QPixmap???Base64???"""
        if isinstance(icon, bytes):
            self.pixmap_current = self._base64_to_pixmap(icon)
            self._stop_movie()
            self.setPixmap(self.pixmap_current)
            self.current_icon = self.pixmap_current

    def set_gif_icon(self, icon: Union[QMovie, bytes]):
        """??????
        :param icon: QMovie???Base64???"""
        if isinstance(icon, bytes):
            movie = self._base64_to_movie(icon)
            self._stop_movie()
            self.movie_current = movie
            self.setMovie(self.movie_current)
            self.movie_current.start()
            self.current_icon = self.movie_current

    @staticmethod
    def _base64_to_pixmap(image_base64: Union[bytes, str]) -> QPixmap:
        """base64????pixmap??
        :param image_base64: base64??????
        :return: QPixmap"""
        # ??base64??????
        byte_data = base64.b64decode(image_base64)

        # ????????QPixmap
        pixmap = QPixmap()
        buffer = QByteArray(byte_data)
        byte_array_device = QBuffer(buffer)
        byte_array_device.open(QBuffer.ReadOnly)
        pixmap.loadFromData(byte_array_device.data())

        return pixmap

    @staticmethod
    def _base64_to_movie(base64_str):
        """base64?????QMovie"""
        gif_data = base64.b64decode(base64_str)

        # ???? QBuffer ????????
        buffer = QBuffer()
        buffer.setData(gif_data)
        buffer.open(QIODevice.ReadOnly)

        # ?? QMovie ????? GIF ??
        movie = QMovie()
        movie.setDevice(buffer)
        movie.setCacheMode(QMovie.CacheAll)

        return movie

    def _stop_movie(self):
        """????"""
        if self.movie_current:
            self.movie_current.stop()

    """???????(????????,????)

    def set_pixmap_resized(self,pixmap:QPixmap):
        if not pixmap.isNull():
            super().setPixmap(pixmap.scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatio,  Qt.TransformationMode.SmoothTransformation  ))
    def set_movie_resized(self,movie:QMovie):
        if movie.isValid():
            movie.stop()
            movie.setScaledSize(self.size())
            self.setMovie(movie)
            movie.start()

    def resizeEvent(self, event):
        print(self.size())
        if isinstance(self.current_icon,QPixmap):
            self.set_pixmap_resized(self.current_icon)
        elif isinstance(self.current_icon,QMovie):
            self.set_movie_resized(self.current_icon)
        super().resizeEvent(event)
    """


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = LabelIcon()
    program_ui.show()
    app_.exec()
