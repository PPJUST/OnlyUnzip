from PySide6.QtWidgets import QApplication, QMainWindow

from window_model import WindowModel
from window_presenter import WindowPresenter
from window_viewer import WindowViewer




app_ = QApplication()
viewer = WindowViewer()
model = WindowModel()
presenter = WindowPresenter(viewer, model)
viewer.show()
app_.exec()
