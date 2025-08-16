import base64
from typing import Union

from PySide6.QtCore import QBuffer, QIODevice, QByteArray
from PySide6.QtGui import QMovie, QPixmap, Qt
from PySide6.QtWidgets import QLabel, QApplication, QSizePolicy


class LabelIcon(QLabel):
    """用于显示图标的自定义label"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 设置居中对齐
        self.setScaledContents(True)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.setStyleSheet("background-color: lightgreen;")  # 测试用

        self.current_icon: Union[QPixmap, QMovie] = None  # 当前显示的图片对象
        self.pixmap_current: QPixmap = None  # 当前设置的静态图片
        self.movie_current: QMovie = None  # 当前设置的动画

    def set_icon(self, icon: Union[QPixmap, bytes]):
        """设置静态图标
        :param icon: QPixmap对象或Base64字符串"""
        if isinstance(icon, bytes):
            self.pixmap_current = self._base64_to_pixmap(icon)
            self._stop_movie()
            self.setPixmap(self.pixmap_current)
            self.current_icon = self.pixmap_current

    def set_gif_icon(self, icon: Union[QMovie, bytes]):
        """设置动态图标
        :param icon: QMovie对象或Base64字符串"""
        if isinstance(icon, bytes):
            movie = self._base64_to_movie(icon)
            self._stop_movie()
            self.movie_current = movie
            self.setMovie(self.movie_current)
            self.movie_current.start()
            self.current_icon = self.movie_current

    @staticmethod
    def _base64_to_pixmap(image_base64: Union[bytes, str]) -> QPixmap:
        """base64图片转为pixmap对象
        :param image_base64: base64字节或字符串
        :return: QPixmap"""
        # 解码base64字节或字符串
        byte_data = base64.b64decode(image_base64)

        # 将字节数据转换为QPixmap
        pixmap = QPixmap()
        buffer = QByteArray(byte_data)
        byte_array_device = QBuffer(buffer)
        byte_array_device.open(QBuffer.ReadOnly)
        pixmap.loadFromData(byte_array_device.data())

        return pixmap

    @staticmethod
    def _base64_to_movie(base64_str):
        """base64字符串转为QMovie"""
        gif_data = base64.b64decode(base64_str)

        # 创建一个 QBuffer 来存储二进制数据
        buffer = QBuffer()
        buffer.setData(gif_data)
        buffer.open(QIODevice.ReadOnly)

        # 创建 QMovie 对象并加载 GIF 数据
        movie = QMovie()
        movie.setDevice(buffer)
        movie.setCacheMode(QMovie.CacheAll)

        return movie

    def _stop_movie(self):
        """停止动画"""
        if self.movie_current:
            self.movie_current.stop()

    """自适应显示图片（以下方法未能实现，不再使用）

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
