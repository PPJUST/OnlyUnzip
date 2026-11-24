# 历史模块的界面组件
import os.path
from typing import Tuple

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QAction
from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QMenu

from common.class_7zip import RESULT_STATES
from common.class_file_info import FileInfo
from components.page_history.res.ui_page_history import Ui_Form

PASSWORD_ROLE = Qt.UserRole
FILE_INFO_ROLE = Qt.UserRole + 1


class HistoryViewer(QWidget):
    """历史模块的界面组件"""
    HistoryFilter = Signal(str, str, name='历史记录筛选器')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 初始化
        self.ui.listWidget_records.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.ui.listWidget_records.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget_records.setWordWrap(True)
        self.ui.listWidget_records.customContextMenuRequested.connect(self._context_menu)  # 右键菜单
        self.ui.listWidget_records.setSpacing(3)
        self.ui.comboBox_result_state.addItems(RESULT_STATES)
        self.ui.lineEdit_search.setPlaceholderText('搜索文本')

        # 绑定信号
        self.ui.toolButton_filter.clicked.connect(self.emit_signal)

    def add_record(self, record_text: str, color: Tuple[int, int, int], password: str = None,
                   file_info: FileInfo = None):
        """添加记录"""
        item = QListWidgetItem()
        item.setText(record_text + '\n' + '-' * 20)
        if color:
            item.setForeground(QColor(color[0], color[1], color[2]))

        if password or file_info:
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        if password:  # 密码用于右键复制
            item.setData(PASSWORD_ROLE, password)
        if file_info:  # 文件信息用于右键打开路径、按结果类型筛选
            item.setData(FILE_INFO_ROLE, file_info)

        self.ui.listWidget_records.addItem(item)
        self.ui.listWidget_records.scrollToBottom()  # 滚动到底部

    def filter_history(self, result_class: list, search_text: str):
        """筛选历史记录
        :param result_class: 需要筛选的结果类
        :param search_text: 需要搜索的文本"""
        for i in range(self.ui.listWidget_records.count()):
            item = self.ui.listWidget_records.item(i)
            self._update_item_visible(item, result_class, search_text)

    def _update_item_visible(self, item: QListWidgetItem, result_class: list, search_text: str):
        """更新单个行项目的显示状态"""
        file_info: FileInfo = item.data(FILE_INFO_ROLE)
        if file_info and result_class:
            result_7zip = file_info.get_7zip_result()
            if result_7zip:
                item.setHidden(not self._is_match_result_class(result_7zip, result_class))

        if search_text and not item.isHidden() and search_text not in item.text():
            item.setHidden(True)

    @staticmethod
    def _is_match_result_class(result_7zip, result_class: list) -> bool:
        """判断结果是否属于指定的结果类"""
        for class_ in result_class:
            if isinstance(result_7zip, class_):
                return True
        return False

    def show_all_history(self):
        """显示所有历史记录"""
        for i in range(self.ui.listWidget_records.count()):
            item = self.ui.listWidget_records.item(i)
            item.setHidden(False)

    def emit_signal(self):
        """发生筛选信号"""
        filter_result_state = self.ui.comboBox_result_state.currentText()
        filter_search_text = self.ui.lineEdit_search.text()
        self.HistoryFilter.emit(filter_result_state, filter_search_text)

    def _context_menu(self, pos):
        """右键菜单"""
        selected_item = self.ui.listWidget_records.currentItem()
        if not selected_item or not selected_item.data(PASSWORD_ROLE):
            return

        file_info: FileInfo = selected_item.data(FILE_INFO_ROLE)
        is_show_password = bool(file_info and file_info.password)
        is_show_origin = bool(file_info and file_info.filepath and os.path.exists(file_info.filepath))
        is_show_extract = bool(file_info and file_info.extract_path and os.path.exists(file_info.extract_path))

        menu = QMenu()
        menu.adjustSize()
        if is_show_password:
            self._add_menu_action(menu, '复制密码', self._copy_password)
        if is_show_origin:
            self._add_menu_action(menu, '打开源文件路径', self._open_origin_path)
        if is_show_extract:
            self._add_menu_action(menu, '打开文件解压结果路径', self._open_extract_result_path)
        menu.exec(self.mapToGlobal(pos))

    @staticmethod
    def _add_menu_action(menu: QMenu, text: str, slot):
        """向菜单添加动作并绑定处理方法"""
        action = QAction(text, menu)
        action.triggered.connect(slot)
        menu.addAction(action)

    def _copy_password(self):
        """复制行项目中的密码到剪切板"""
        selected_item = self.ui.listWidget_records.currentItem()
        if selected_item:
            QApplication.clipboard().setText(selected_item.data(PASSWORD_ROLE))

    def _open_origin_path(self):
        """打开行项目中的源文件路径"""
        file_info = self._get_selected_file_info()
        if file_info and file_info.filepath:
            os.startfile(file_info.filepath)

    def _open_extract_result_path(self):
        """打开行项目中的解压结果路径"""
        file_info = self._get_selected_file_info()
        if file_info and file_info.extract_path:
            os.startfile(file_info.extract_path)

    def _get_selected_file_info(self) -> FileInfo:
        """获取当前行项目中的文件信息"""
        selected_item = self.ui.listWidget_records.currentItem()
        if not selected_item:
            return None
        return selected_item.data(FILE_INFO_ROLE)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = HistoryViewer()
    program_ui.show()
    app_.exec()
