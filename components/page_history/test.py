from PySide6.QtWidgets import QApplication

from history_model import HistoryModel
from history_presenter import HistoryPresenter
from history_viewer import HistoryViewer

app_ = QApplication()
viewer = HistoryViewer()
model = HistoryModel()
presenter = HistoryPresenter(viewer, model)
viewer.show()
app_.exec()
