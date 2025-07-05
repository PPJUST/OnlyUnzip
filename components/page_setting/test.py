from PySide6.QtWidgets import QApplication

from setting_model import SettingModel
from setting_presenter import SettingPresenter
from setting_viewer import SettingViewer

app_ = QApplication()
viewer = SettingViewer()
model = SettingModel()
presenter = SettingPresenter(viewer, model)
viewer.show()
app_.exec()
