# 密码详情表的界面组件
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDialog, QTableWidget, QTableWidgetItem

from components.dialog_password_detail.res.ui_table import Ui_Dialog


class PasswordDetailViewer(QDialog):
    """密码详情表的界面组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self._setup_table()
        self.ui.pushButton_quit.clicked.connect(self.close)

    def add_record(self, values: list):
        """在表格末尾添加一行

        :param values: 各列要显示的文本，顺序与表头一致
        """
        self.add_records([values])

    def add_records(self, values_list: list):
        """批量添加表格行

        :param values_list: 每行文本组成的列表
        """
        table = self.ui.tableWidget
        # 插入数据期间先关闭排序，避免行顺序被提前打乱
        table.setSortingEnabled(False)

        for values in values_list:
            row = table.rowCount()
            table.insertRow(row)
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, column, item)

        table.setSortingEnabled(True)

    def clear(self):
        """清空表格中的记录，保留表头"""
        self.ui.tableWidget.setRowCount(0)

    def _setup_table(self):
        """设置表格基本属性"""
        table = self.ui.tableWidget

        # 设置列数与标题行
        table.setColumnCount(4)
        headers = ['密码', '使用次数', '添加时间', '最后使用时间']
        table.setHorizontalHeaderLabels(headers)

        # 设置单元格不可编辑
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # 设置交替行颜色（便于阅读）
        table.setAlternatingRowColors(True)

        # 启用排序（点击标题行自动排序）
        table.setSortingEnabled(True)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = PasswordDetailViewer()
    program_ui.show()
    app_.exec()
