import base64
from typing import Union

from PySide6.QtCore import QBuffer, QIODevice, QByteArray
from PySide6.QtGui import QMovie, QPixmap
from PySide6.QtWidgets import QLabel, QApplication


class LabelIcon(QLabel):
    """用于显示图标的自定义label"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)  # 居中显示
        self.movie_current: QMovie = None  # 当前设置的GIF动作

    def set_icon(self, icon: Union[QPixmap, bytes]):
        """设置静态图标
        :param icon: QPixmap对象或Base64字符串"""
        if isinstance(icon, bytes):
            icon = self._base64_to_pixmap(icon)
        self._stop_movie()
        self.setPixmap(icon)

    def set_gif_icon(self, icon:   Union[QMovie, bytes]):
        """设置动态图标
        :param icon: QMovie对象或Base64字符串"""
        if isinstance(icon, bytes):
            icon = self._base64_to_movie(icon)
        self._stop_movie()
        self.movie_current = icon
        self.setMovie(self.movie_current)
        self.movie_current.start()

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


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = LabelIcon()
    program_ui.show()
    app_.exec()
