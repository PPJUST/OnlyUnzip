from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from components import window

if __name__ == "__main__":
    app_ = QApplication()
    app_.setStyle('Fusion')
    # 设置白色背景色
    # palette = QPalette()
    # palette.setColor(QPalette.Window, QColor(255, 255, 255))
    # app_.setPalette(palette)

    # 设置全局字体
    font = QFont("Microsoft YaHei", 10)  # 字体名称和大小
    app_.setFont(font)

    presenter = window.get_presenter()
    viewer = presenter.viewer
    model = presenter.model
    viewer.setWindowTitle('OnlyUnzip v2.0.0')
    viewer.resize(300, 300)
    viewer.show()
    app_.exec()
