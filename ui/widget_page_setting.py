# 设置页
import os

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QApplication, QFileDialog

from constant import _ICON_ASK_PATH, _ICON_CLEAR, _ICON_OPEN_FOLDER
from module.function_config import GetSetting, ResetSetting
from ui.src.ui_widget_page_setting import Ui_Form


class WidgetPageSetting(QWidget):
    signal_output_path = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 设置ui
        self.ui.lineEdit_output_path.setReadOnly(True)
        self.ui.toolButton_ask_path.setIcon(QIcon(_ICON_ASK_PATH))
        self.ui.toolButton_clear_path.setIcon(QIcon(_ICON_CLEAR))
        self.ui.toolButton_open_path.setIcon(QIcon(_ICON_OPEN_FOLDER))

        # 初始化
        self._load_setting()
        self._set_extract_checkbox_state()  # 刷新一次，防止测试模式时没有禁用设置

        # 绑定槽函数
        self.ui.checkBox_mode_extract.stateChanged.connect(self._change_setting_mode)
        self.ui.checkBox_mode_extract.stateChanged.connect(self._set_extract_checkbox_state)
        self.ui.checkBox_extract_smart.stateChanged.connect(self._change_setting_smart_extract)
        self.ui.checkBox_delete_file.stateChanged.connect(self._change_setting_delete_file)
        self.ui.checkBox_handle_multi_folder.stateChanged.connect(self._change_setting_handle_multi_folder)
        self.ui.checkBox_check_filetype.stateChanged.connect(self._change_setting_check_filetype)
        self.ui.checkBox_handle_multi_archive.stateChanged.connect(self._change_setting_handle_multi_archive)
        self.ui.checkBox_handle_multi_archive.stateChanged.connect(self._sync_button_state)
        self.ui.lineEdit_output_path.textChanged.connect(self._change_setting_output_path)
        self.ui.lineEdit_output_path.textChanged.connect(self._send_output_path)
        self.ui.lineEdit_filter_suffix.textChanged.connect(self._change_setting_filter_suffix)
        self.ui.toolButton_ask_path.clicked.connect(self._ask_dirpath)
        self.ui.toolButton_clear_path.clicked.connect(self._clear_dirpath)
        self.ui.toolButton_open_path.clicked.connect(self._open_dirpath)

    def set_widgets_state(self, enable: bool):
        """启用/禁用控件"""
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            widget.setEnabled(enable)

    def _load_setting(self):
        """加载设置"""
        self.ui.checkBox_mode_extract.setChecked(GetSetting.mode_extract())
        self.ui.checkBox_mode_test.setChecked(not GetSetting.mode_extract())
        self.ui.checkBox_extract_smart.setChecked(GetSetting.smart_extract())
        self.ui.checkBox_extract_folder.setChecked(not GetSetting.smart_extract())
        self.ui.checkBox_delete_file.setChecked(GetSetting.delete_file())
        self.ui.checkBox_handle_multi_folder.setChecked(GetSetting.handle_multi_folder())
        self.ui.checkBox_check_filetype.setChecked(GetSetting.check_filetype())
        self.ui.checkBox_handle_multi_archive.setChecked(GetSetting.handle_multi_archive())
        self.ui.lineEdit_output_path.setText(GetSetting.output_folder())
        self.ui.lineEdit_filter_suffix.setText(GetSetting.filter_suffix())

    def _send_output_path(self):
        """发送解压路径信号"""
        self.signal_output_path.emit()

    def _ask_dirpath(self):
        """选择解压目录"""
        dirpath = QFileDialog.getExistingDirectory(self, "指定解压目录")
        if dirpath:
            self.ui.lineEdit_output_path.setText(os.path.normpath(dirpath))

    def _clear_dirpath(self):
        """清除解压目录"""
        self.ui.lineEdit_output_path.clear()

    def _open_dirpath(self):
        path = self.ui.lineEdit_output_path.text()
        if path and os.path.exists(path):
            os.startfile(self.ui.lineEdit_output_path.text())

    def _sync_button_state(self):
        """同步按钮状态（递归解压&仅处理压缩包）"""
        if self.ui.checkBox_handle_multi_archive.isChecked():
            self.ui.checkBox_check_filetype.setChecked(True)

    def _change_setting_mode(self):
        """修改设置项"""
        ResetSetting.mode_extract(self.ui.checkBox_mode_extract.isChecked())
        ResetSetting.mode_test(not self.ui.checkBox_mode_extract.isChecked())

    def _set_extract_checkbox_state(self):
        """启用/禁用解压相关的勾选框"""
        state = self.ui.checkBox_mode_extract.isChecked()
        self.ui.checkBox_extract_smart.setEnabled(state)
        self.ui.checkBox_extract_folder.setEnabled(state)
        self.ui.checkBox_delete_file.setEnabled(state)
        self.ui.checkBox_handle_multi_folder.setEnabled(state)
        self.ui.checkBox_handle_multi_archive.setEnabled(state)
        self.ui.lineEdit_output_path.setEnabled(state)
        self.ui.toolButton_ask_path.setEnabled(state)
        self.ui.toolButton_clear_path.setEnabled(state)
        self.ui.toolButton_open_path.setEnabled(state)
        self.ui.lineEdit_filter_suffix.setEnabled(state)

    def _change_setting_smart_extract(self):
        """修改设置项"""
        ResetSetting.smart_extract(self.ui.checkBox_extract_smart.isChecked())
        ResetSetting.extract_to_folder(not self.ui.checkBox_extract_smart.isChecked())

    def _change_setting_delete_file(self):
        """修改设置项"""
        ResetSetting.delete_file(self.ui.checkBox_delete_file.isChecked())

    def _change_setting_handle_multi_folder(self):
        """修改设置项"""
        ResetSetting.handle_multi_folder(self.ui.checkBox_handle_multi_folder.isChecked())

    def _change_setting_check_filetype(self):
        """修改设置项"""
        ResetSetting.check_filetype(self.ui.checkBox_check_filetype.isChecked())

    def _change_setting_handle_multi_archive(self):
        """修改设置项"""
        ResetSetting.handle_multi_archive(self.ui.checkBox_handle_multi_archive.isChecked())

    def _change_setting_output_path(self):
        """修改设置项"""
        ResetSetting.output_folder(self.ui.lineEdit_output_path.text())

    def _change_setting_filter_suffix(self):
        """修改设置项"""
        ResetSetting.filter_suffix(self.ui.lineEdit_filter_suffix.text())


if __name__ == "__main__":
    app_ = QApplication()
    app_.setStyle('Fusion')
    program_ui = WidgetPageSetting()
    program_ui.show()
    app_.exec()
