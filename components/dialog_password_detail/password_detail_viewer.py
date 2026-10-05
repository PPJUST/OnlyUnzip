# ??????????
from typing import Tuple

import lzytools.time
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QDialog

from components.dialog_password_detail.res.ui_table import Ui_Dialog


class PasswordDetailViewer(QDialog):
    """??????????"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self._setup_table()

        self.ui.pushButton_quit.clicked.connect(self.close)

    def add_record(self, password_info: Tuple[str, int, str, str]):
        """????
        :param password_info: ??,????,????,??????"""
        row_count = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row_count)

        _name = str(password_info[0])
        use_count = str(password_info[1])
        add_time = lzytools.time.convert_duration_to_date(password_info[2])
        last_use_time = lzytools.time.convert_duration_to_date(password_info[3])
        info = [_name, use_count, add_time, last_use_time]

        for col, value in enumerate(info):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget.setItem(row_count, col, item)

    def _setup_table(self):
        """????????"""
        # ????
        self.ui.tableWidget.setColumnCount(4)

        # ?????
        headers = ['??', '????', '????', '??????']
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)

        # ?????????
        self.ui.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # ???????(????)
        self.ui.tableWidget.setAlternatingRowColors(True)

        # ????(?????????)
        self.ui.tableWidget.setSortingEnabled(True)

    def clear(self):
        self.ui.tableWidget.clear()


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = PasswordDetailViewer()
    program_ui.show()
    app_.exec()
