from PySide6.QtWidgets import QApplication

from home_model import HomeModel
from home_presenter import HomePresenter
from home_viewer import HomeViewer

app_ = QApplication()
viewer = HomeViewer()
model = HomeModel()
presenter = HomePresenter(viewer, model)
viewer.show()
app_.exec()
