# 设置模块的界面组件
# 仅用于显示，不执行具体方法
import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QFileDialog
from lzytools._qt_pyside6._function import base64_to_pixmap

from components.page_setting.res.icon_base64 import ICON_CHOOSE, ICON_OPEN
from components.page_setting.res.ui_page_setting import Ui_Form


class SettingViewer(QWidget):
    """设置模块的界面组件"""
    ChangeArchiveModelText = Signal(bool, name="修改为测试模式")
    ChangeArchiveModelExtract = Signal(bool, name="修改为解压模式")
    ChangeTryUnknownFiletype = Signal(bool, name="修改处理未知格式的文件")
    ChangeReadPasswordFromFilename = Signal(bool, name="修改从文件名中读取密码")
    ChangeWriteFilename = Signal(bool, name="修改写入文件名")
    ChangeWriteFilenameLeftPart = Signal(str, name="修改密码格式左边部分")
    ChangeWriteFilenameRightPart = Signal(str, name="修改密码格式右边部分")
    ChangeWriteFilenamePosition = Signal(str, name="修改密码格式位置")
    ChangeExtractModelSmart = Signal(bool, name="修改智能解压模式")
    ChangeExtractModelDirect = Signal(bool, name="修改直接解压模式")
    ChangeExtractModelSameFolder = Signal(bool, name="修改同名目录解压模式")
    ChangeDeleteFile = Signal(bool, name="修改解压后删除原文件")
    ChangeRecursiveExtract = Signal(bool, name="修改递归解压")
    ChangeCoverModel = Signal(str, name="修改覆盖模式")
    ChangeBreakFolder = Signal(bool, name="修改解散文件夹")
    ChangeBreakFolderModel = Signal(str, name="修改解散文件夹模式")
    ChangeExtractOutputFolder = Signal(bool, name="修改是否解压至指定目录")
    ChangeExtractOutputFolderPath = Signal(str, name="修改解压输出目录")
    ChangeExtractFilter = Signal(bool, name="修改解压文件过滤器")
    ChangeExtractFilterRule = Signal(str, name="修改解压文件过滤器规则")
    ChangeTopWindow = Signal(bool, name="修改窗口置顶")
    ChangeLockSize = Signal(bool, name="修改锁定窗口大小")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 初始化
        self._bind_signal()
        self._set_icon()

    def lock(self):
        """锁定全部设置项，禁止修改"""
        self._set_enable(False)

    def unlock(self):
        """解锁全部设置项，允许修改"""
        self._set_enable(True)

    def _choose_dirpath(self):
        """打开对话框，选择指定解压目录"""
        dirpath = QFileDialog.getExistingDirectory(self, "指定解压输出目录")
        if dirpath:
            self.ui.lineEdit_extract_output_folder.setText(dirpath)

    def _open_dirpath(self):
        """打开指定的解压目录"""
        dirpath = self.ui.lineEdit_extract_output_folder.text()
        if dirpath:
            os.startfile(dirpath)

    def _set_icon(self):
        self.ui.toolButton_choose.setIcon(base64_to_pixmap(ICON_CHOOSE))
        self.ui.toolButton_open.setIcon(base64_to_pixmap(ICON_OPEN))

    def _set_enable(self, is_enable: bool):
        self.ui.radioButton_mode1_test.setEnabled(is_enable)
        self.ui.radioButton_mode1_extract.setEnabled(is_enable)
        self.ui.checkBox_read_password_from_filename.setEnabled(is_enable)
        self.ui.checkBox_try_unknown_filetype.setEnabled(is_enable)
        self.ui.widget_test.setEnabled(is_enable)
        self.ui.widget_extract.setEnabled(is_enable)

    """以下为设置选项的方法"""

    def set_setting_model_extract(self):
        """设置压缩包处理模式：解压模式"""
        self.ui.radioButton_mode1_extract.setChecked(True)
        self.ui.radioButton_mode1_test.setChecked(False)
        # 隐藏/显示相应的设置项
        self._show_settings_extract()

    def set_setting_model_test(self):
        """设置压缩包处理模式：测试模式"""
        self.ui.radioButton_mode1_extract.setChecked(False)
        self.ui.radioButton_mode1_test.setChecked(True)
        # 隐藏/显示相应的设置项
        self._show_settings_test()

    def _show_settings_extract(self):
        """显示解压模式的设置项，隐藏测试模式的设置项"""
        self.ui.widget_extract.setVisible(True)
        self.ui.widget_test.setVisible(False)

    def _show_settings_test(self):
        """显示测试模式的设置项，隐藏解压模式的设置项"""
        self.ui.widget_extract.setVisible(False)
        self.ui.widget_test.setVisible(True)

    def set_setting_is_try_unknown_filetype(self, is_enable: bool):
        """通用选项
        设置是否尝试处理未知格式的文件"""
        self.ui.checkBox_try_unknown_filetype.setChecked(is_enable)

    def set_setting_is_read_password_from_filename(self, is_enable: bool):
        """通用选项
        设置是否尝试从文件名中读取密码"""
        self.ui.checkBox_read_password_from_filename.setChecked(is_enable)

    def set_setting_write_filename(self, is_enable: bool):
        """测试模式选项
        设置检索到正确密码后是否将其写入文件名"""
        self.ui.checkBox_write_filename.setChecked(is_enable)

    def set_setting_write_filename_left_part(self, text: str):
        """测试模式选项
        将密码写入文件名时的左侧字符"""
        self.ui.lineEdit_left_word.setText(text)

    def set_setting_write_filename_right_part(self, text: str):
        """测试模式选项
        将密码写入文件名时的右侧字符"""
        self.ui.lineEdit_right_word.setText(text)

    def set_setting_write_filename_position(self, option: str):
        """测试模式选项
        将密码写入文件名时的位置
        :param option: 对应的comboBox选项文本"""
        self.ui.comboBox_pw_position.setCurrentText(option)

    def set_setting_write_filename_preview(self, preview: str):
        """测试模式选项
        将密码写入文件名时的文件名示例"""
        self.ui.label_preview_filename.setText(preview)

    def set_setting_extract_model_smart(self):
        """解压模式选项
        设置解压模式为智能解压（逻辑类似于BandiZip）"""
        self.ui.radioButton_mode2_smart_extract.setChecked(True)
        self.ui.radioButton_mode2_direct_extract.setChecked(False)
        self.ui.radioButton_mode2_extract_same_folder.setChecked(False)

    def set_setting_extract_model_direct(self):
        """解压模式选项
        设置解压模式为直接解压（不对结果进行处理）"""
        self.ui.radioButton_mode2_smart_extract.setChecked(False)
        self.ui.radioButton_mode2_direct_extract.setChecked(True)
        self.ui.radioButton_mode2_extract_same_folder.setChecked(False)

    def set_setting_extract_model_same_folder(self):
        """解压模式选项
        设置解压模式为解压到同名目录（结果放置于新建的同名目录中）"""
        self.ui.radioButton_mode2_smart_extract.setChecked(False)
        self.ui.radioButton_mode2_direct_extract.setChecked(False)
        self.ui.radioButton_mode2_extract_same_folder.setChecked(True)

    def set_setting_delete_file(self, is_enable: bool):
        """解压模式选项
        设置解压后删除原文件"""
        self.ui.checkBox_delete_origin.setChecked(is_enable)

    def set_setting_recursive_extract(self, is_enable: bool):
        """解压模式选项
        设置完成解压任务后是否进行递归解压（再次执行直到没有能解压的文件）"""
        self.ui.checkBox_recursive_extract.setChecked(is_enable)

    def set_setting_cover_model(self, option: str):
        """解压模式选项
        设置重名文件覆盖模式
        :param option: 对应的comboBox选项文本"""
        self.ui.comboBox_cover_file.setCurrentText(option)

    def set_setting_break_folder(self, is_enable: bool):
        """解压模式选项
        设置完成单个解压任务后是否解散文件夹"""
        self.ui.checkBox_break_folder.setChecked(is_enable)

    def set_setting_break_folder_model(self, option: str):
        """解压模式选项
        设置解散文件夹的模式
        :param option: 对应的comboBox选项文本"""
        self.ui.comboBox_break_folder.setCurrentText(option)

    def set_setting_extract_to_folder(self, is_enable: bool):
        """解压模式选项
        设置是否解压至指定目录"""
        self.ui.checkBox_extract_output_folder.setChecked(is_enable)

    def set_setting_extract_output_folder(self, dirpath: str):
        """测试模式选项
        设置解压输出目录"""
        self.ui.lineEdit_extract_output_folder.setText(dirpath)
        self.ui.lineEdit_extract_output_folder.setToolTip(dirpath)

    def set_setting_filter(self, is_enable: bool):
        """解压模式选项
        设置解压时是否过滤文件"""
        self.ui.checkBox_extract_filter.setChecked(is_enable)

    def set_setting_filter_rule(self, rule: str):
        """测试模式选项
        设置过滤文件规则"""
        self.ui.plainTextEdit_extract_filter_rule.setPlainText(rule)

    def set_top_window(self, is_enable: bool):
        """设置是否置顶窗口"""
        self.ui.checkBox_top_window.setChecked(is_enable)

    def set_lock_size(self, is_enable: bool):
        """设置是否锁定窗口大小"""
        self.ui.checkBox_lock_size.setChecked(is_enable)

    """以下为信号绑定的方法"""

    def _bind_signal(self):
        """绑定信号"""
        # 弹窗
        self.ui.toolButton_choose.clicked.connect(self._choose_dirpath)
        self.ui.toolButton_open.clicked.connect(self._open_dirpath)
        # 模式
        self.ui.radioButton_mode1_extract.clicked.connect(self._change_archive_model)
        self.ui.radioButton_mode1_test.clicked.connect(self._change_archive_model)

        # 处理未知文件
        self.ui.checkBox_try_unknown_filetype.stateChanged.connect(self.ChangeTryUnknownFiletype.emit)
        # 从文件名中读取密码
        self.ui.checkBox_read_password_from_filename.stateChanged.connect(self.ChangeReadPasswordFromFilename.emit)
        # 密码写入文件名
        self.ui.checkBox_write_filename.stateChanged.connect(self.ChangeWriteFilename.emit)
        self.ui.lineEdit_left_word.textChanged.connect(self.ChangeWriteFilenameLeftPart.emit)
        self.ui.lineEdit_right_word.textChanged.connect(self.ChangeWriteFilenameRightPart.emit)
        self.ui.comboBox_pw_position.currentTextChanged.connect(self.ChangeWriteFilenamePosition.emit)
        # 解压模式
        self.ui.radioButton_mode2_smart_extract.clicked.connect(self._change_extract_model)
        self.ui.radioButton_mode2_direct_extract.clicked.connect(self._change_extract_model)
        self.ui.radioButton_mode2_extract_same_folder.clicked.connect(self._change_extract_model)
        # 删除原文件
        self.ui.checkBox_delete_origin.stateChanged.connect(self.ChangeDeleteFile.emit)
        # 递归解压
        self.ui.checkBox_recursive_extract.stateChanged.connect(self.ChangeRecursiveExtract.emit)
        # 覆盖模式
        self.ui.comboBox_cover_file.currentTextChanged.connect(self.ChangeCoverModel.emit)
        # 解散文件夹
        self.ui.checkBox_break_folder.stateChanged.connect(self.ChangeBreakFolder.emit)
        self.ui.comboBox_break_folder.currentTextChanged.connect(
            lambda: self.ChangeBreakFolderModel.emit(self.ui.comboBox_break_folder.currentText()))
        # 解压到指定目录
        self.ui.checkBox_extract_output_folder.stateChanged.connect(self.ChangeExtractOutputFolder.emit)
        self.ui.lineEdit_extract_output_folder.textChanged.connect(self.ChangeExtractOutputFolderPath.emit)
        # 过滤文件
        self.ui.checkBox_extract_filter.stateChanged.connect(self.ChangeExtractFilter.emit)
        self.ui.plainTextEdit_extract_filter_rule.textChanged.connect(
            lambda: self.ChangeExtractFilterRule.emit(self.ui.plainTextEdit_extract_filter_rule.toPlainText()))
        # 置顶窗口
        self.ui.checkBox_top_window.stateChanged.connect(self.ChangeTopWindow.emit)
        # 锁定窗口大小
        self.ui.checkBox_lock_size.stateChanged.connect(self.ChangeLockSize.emit)

    def _change_archive_model(self):
        if self.ui.radioButton_mode1_extract.isChecked():
            self.ChangeArchiveModelExtract.emit(True)
            self._show_settings_extract()
        elif self.ui.radioButton_mode1_test.isChecked():
            self.ChangeArchiveModelText.emit(True)
            self._show_settings_test()

    def _change_extract_model(self):
        if self.ui.radioButton_mode2_smart_extract.isChecked():
            self.ChangeExtractModelSmart.emit(True)
        elif self.ui.radioButton_mode2_direct_extract.isChecked():
            self.ChangeExtractModelDirect.emit(True)
        elif self.ui.radioButton_mode2_extract_same_folder.isChecked():
            self.ChangeExtractModelSameFolder.emit(True)


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = SettingViewer()
    program_ui.show()
    app_.exec()
