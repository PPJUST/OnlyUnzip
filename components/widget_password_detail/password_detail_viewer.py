# 密码详情表的界面组件
from typing import Tuple

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem

from components.widget_password_detail.res.ui_table import Ui_Form


class PasswordDetailViewer(QWidget):
    """密码详情表的界面组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._setup_table()

    def add_record(self, password_info: Tuple[str, int, str, str]):
        """添加记录"""
        row_count = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row_count)
        for col, value in enumerate(password_info):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget.setItem(row_count, col, item)

    def _setup_table(self):
        """设置表格基本属性"""
        # 设置列数
        self.ui.tableWidget.setColumnCount(4)

        # 设置标题行
        headers = ['密码', '使用次数', '添加时间', '最后使用时间']
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)

        # 设置单元格不可编辑
        self.ui.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # 设置交替行颜色（便于阅读）
        self.ui.tableWidget.setAlternatingRowColors(True)

        # 启用排序（点击标题行自动排序）
        self.ui.tableWidget.setSortingEnabled(True)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = PasswordDetailViewer()
    program_ui.show()
    app_.exec()
