from PySide6.QtWidgets import QApplication

from password_model import PasswordModel
from password_presenter import PasswordPresenter
from password_viewer import PasswordViewer

app_ = QApplication()
viewer = PasswordViewer()
model = PasswordModel()
presenter = PasswordPresenter(viewer, model)
viewer.show()
app_.exec()
