from PySide6.QtWidgets import QApplication

from temp_password_model import TempPasswordModel
from temp_password_presenter import TempPasswordPresenter
from temp_password_viewer import TempPasswordViewer

app_ = QApplication()
viewer = TempPasswordViewer()
model = TempPasswordModel()
presenter = TempPasswordPresenter(viewer, model)
viewer.show()
app_.exec()
