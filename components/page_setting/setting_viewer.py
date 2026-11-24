# 设置模块的界面组件
# 只负责显示设置项并发出信号，不直接读写配置文件
import os
import sys

import lzytools
import lzytools_Qt
from PySide6.QtCore import QEvent, QTimer, Signal
from PySide6.QtWidgets import QApplication, QFileDialog, QWidget

from components.page_setting.res.icon_base64 import ICON_CHOOSE, ICON_OPEN, ICON_BLACK_LIST, ICON_WHITE_LIST
from components.page_setting.res.ui_page_setting import Ui_Form


class SettingViewer(QWidget):
    """设置模块的界面组件"""

    ChangeArchiveModelTest = Signal(bool, name="修改为测试模式")
    ChangeArchiveModelExtract = Signal(bool, name="修改为解压模式")
    ChangePreFilterModeDefault = Signal(bool, name="修改文件预筛选模式为默认模式")
    ChangePreFilterModeBlackList = Signal(bool, name="修改文件预筛选模式为黑名单模式")
    ChangePreFilterModeBlackListRule = Signal(list, name="修改文件预筛选模式的黑名单规则")
    ChangePreFilterModeWhiteList = Signal(bool, name="修改文件预筛选模式为白名单模式")
    ChangePreFilterModeWhiteListRule = Signal(list, name="修改文件预筛选模式的白名单规则")
    ChangeTryUnknownFiletype = Signal(bool, name="修改处理未知格式的文件")
    ChangeReadPasswordFromFilename = Signal(bool, name="修改从文件名中读取密码")
    ChangeWriteFilenameT = Signal(bool, name="修改测试模式的密码写入文件名")
    ChangeWriteFilenameLeftPart = Signal(str, name="修改密码格式左边部分")
    ChangeWriteFilenameRightPart = Signal(str, name="修改密码格式右边部分")
    ChangeWriteFilenamePosition = Signal(str, name="修改密码格式位置")
    ChangeExtractModelSmart = Signal(bool, name="修改智能解压模式")
    ChangeExtractModelDirect = Signal(bool, name="修改直接解压模式")
    ChangeExtractModelSameFolder = Signal(bool, name="修改同名目录解压模式")
    ChangeRecursiveExtract = Signal(bool, name="修改递归解压")
    ChangeProcessFileAfterExtractSuccess = Signal(bool, name="修改解压成功后的源文件操作")
    ChangeDeleteFile = Signal(bool, name="修改解压成功后的源文件操作-删除文件")
    ChangeMoveOriginFileAfterSuccess = Signal(bool, name="修改解压成功后的源文件操作-移动到指定路径")
    ChangePathMoveOriginFileAfterSuccess = Signal(str, name="修改解压成功后的源文件操作-移动到的指定路径")
    ChangeWriteFilenameE = Signal(bool, name="修改解压成功后的源文件操作-密码写入文件名")
    ChangeInsertCharToFilenameAfterSuccess = Signal(bool, name="修改解压成功后的源文件操作-向文件名中添加指定文本")
    ChangeInsertCharToFilenameAfterSuccessPosition = Signal(str,
                                                            name="修改解压成功后的源文件操作-向文件名中添加指定文本的位置")
    ChangeInsertCharToFilenameAfterSuccessChar = Signal(str, name="修改解压成功后的源文件操作-向文件名中添加的指定文本")
    ChangeProcessFileAfterExtractFailure = Signal(bool, name="修改解压失败后的源文件操作")
    ChangeMoveOriginFileAfterFailure = Signal(bool, name="修改解压失败后的源文件操作-移动到指定路径")
    ChangePathMoveOriginFileAfterFailure = Signal(str, name="修改解压失败后的源文件操作-移动到的指定路径")
    ChangeInsertCharToFilenameAfterFailure = Signal(bool, name="修改解压失败后的源文件操作-向文件名中添加指定文本")
    ChangeInsertCharToFilenameAfterFailurePosition = Signal(str,
                                                            name="修改解压失败后的源文件操作-向文件名中添加指定文本的位置")
    ChangeInsertCharToFilenameAfterFailureChar = Signal(str, name="修改解压失败后的源文件操作-向文件名中添加的指定文本")
    ChangeCoverModel = Signal(str, name="修改覆盖模式")
    ChangeBreakFolder = Signal(bool, name="修改解散文件夹")
    ChangeBreakFolderModel = Signal(str, name="修改解散文件夹模式")
    ChangeExtractOutputFolder = Signal(bool, name="修改是否解压至指定目录")
    ChangeExtractOutputFolderPath = Signal(str, name="修改解压输出目录")
    ChangeExtractFilter = Signal(bool, name="修改解压文件过滤器")
    ChangeExtractFilterRule = Signal(str, name="修改解压文件过滤器规则")
    Change7ZipPath = Signal(str, name="修改7zip路径")
    ChangeTopWindow = Signal(bool, name="修改窗口置顶")
    ChangeLockSize = Signal(bool, name="修改锁定窗口大小")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._bind_signal()
        self._set_icon()

        # 规则输入停止 1 秒后再发出信号，避免每输入一个字符都写配置文件
        self._timer_black_list_rule = self._create_rule_timer(self._emit_black_list_rule)
        self._timer_white_list_rule = self._create_rule_timer(self._emit_white_list_rule)

        # 屏蔽下拉框的滚轮事件，避免误改设置
        for combo in [self.ui.comboBox_break_folder, self.ui.comboBox_pw_position, self.ui.comboBox_cover_file]:
            combo.installEventFilter(self)

    # region 通用方法
    def lock(self):
        """锁定全部设置项，禁止修改"""
        self._set_enable(False)

    def unlock(self):
        """解锁全部设置项，允许修改"""
        self._set_enable(True)

    def _create_rule_timer(self, timeout_slot):
        """创建规则输入框使用的单次延时定时器"""
        timer = QTimer()
        timer.setInterval(1000)
        timer.setSingleShot(True)
        timer.timeout.connect(timeout_slot)
        return timer

    def _choose_dirpath(self):
        """打开对话框，选择指定解压目录"""
        dirpath = QFileDialog.getExistingDirectory(self, "指定解压输出目录")
        if dirpath:
            self.ui.lineEdit_extract_output_folder.setText(dirpath)

    def _choose_7zip_path(self):
        """打开对话框，选择指定的 7zip 路径"""
        path, _ = QFileDialog.getOpenFileName(self, "选择7Zip路径", filter="7z.exe (7z.exe)")
        if not path:
            return
        path = os.path.normpath(path)
        if os.path.basename(path) != '7z.exe':
            return

        # 如果 7zip 文件在程序目录下，则转换为相对路径
        app_parent = os.path.normpath(os.path.dirname(sys.argv[0]))
        if lzytools.file.is_subpath(app_parent, path):
            path = os.path.join('.\\', os.path.relpath(path, app_parent))
        self.ui.lineEdit_7zip_path.setText(path)

    def _open_dirpath(self):
        """打开指定的解压目录"""
        dirpath = self.ui.lineEdit_extract_output_folder.text()
        if dirpath:
            os.startfile(dirpath)

    def _set_icon(self):
        """设置各按钮的图标"""
        icon_buttons = [
            (self.ui.toolButton_open_black_list, ICON_BLACK_LIST),
            (self.ui.toolButton_open_white_list, ICON_WHITE_LIST),
            (self.ui.toolButton_choose, ICON_CHOOSE),
            (self.ui.toolButton_open, ICON_OPEN),
            (self.ui.toolButton_choose_7zip_path, ICON_CHOOSE),
        ]
        for button, icon in icon_buttons:
            button.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(icon))

    def _set_enable(self, is_enable: bool):
        """批量启用/禁用可操作的设置项"""
        widgets = [
            self.ui.radioButton_mode1_test,
            self.ui.radioButton_mode1_extract,
            self.ui.radioButton_pre_filter_mode_default,
            self.ui.radioButton_pre_filter_mode_black_list,
            self.ui.radioButton_pre_filter_mode_white_list,
            self.ui.toolButton_open_black_list,
            self.ui.toolButton_open_white_list,
            self.ui.checkBox_read_password_from_filename,
            self.ui.checkBox_try_unknown_filetype,
            self.ui.lineEdit_7zip_path,
            self.ui.widget_test,
            self.ui.widget_extract,
        ]
        for widget in widgets:
            widget.setEnabled(is_enable)

    def _check_radio(self, checked_widget, other_widgets):
        """选中指定单选按钮，并取消同组其他按钮的选中状态"""
        checked_widget.setChecked(True)
        for widget in other_widgets:
            widget.setChecked(False)

    def _show_settings(self, is_extract: bool):
        """显示解压模式或测试模式对应的设置区域"""
        self.ui.widget_extract.setVisible(is_extract)
        self.ui.widget_test.setVisible(not is_extract)

    def _fill_text_edit(self, text_edit, rules):
        """用规则列表刷新文本框内容"""
        text_edit.clear()
        for rule in rules:
            if rule:
                text_edit.append(rule)

    def _emit_rules(self, text_edit, signal):
        """把文本框中的非空行作为规则列表发出"""
        rules = []
        for line in text_edit.toPlainText().split('\n'):
            if line:
                rules.append(line)
        signal.emit(rules)

    # endregion

    # region 设置选项的显示方法
    def set_setting_model_extract(self):
        """设置压缩包处理模式：解压模式"""
        self._check_radio(self.ui.radioButton_mode1_extract, [self.ui.radioButton_mode1_test])
        self._show_settings(True)
        self.ChangeArchiveModelExtract.emit(True)

    def set_setting_model_test(self):
        """设置压缩包处理模式：测试模式"""
        self._check_radio(self.ui.radioButton_mode1_test, [self.ui.radioButton_mode1_extract])
        self._show_settings(False)
        self.ChangeArchiveModelTest.emit(True)

    def set_setting_pre_filter_mode_default(self):
        """设置文件预筛选模式：默认模式"""
        self._check_radio(self.ui.radioButton_pre_filter_mode_default, [
            self.ui.radioButton_pre_filter_mode_black_list,
            self.ui.radioButton_pre_filter_mode_white_list,
        ])

    def set_setting_pre_filter_mode_black_list(self):
        """设置文件预筛选模式：黑名单模式"""
        self._check_radio(self.ui.radioButton_pre_filter_mode_black_list, [
            self.ui.radioButton_pre_filter_mode_default,
            self.ui.radioButton_pre_filter_mode_white_list,
        ])

    def set_setting_pre_filter_mode_white_list(self):
        """设置文件预筛选模式：白名单模式"""
        self._check_radio(self.ui.radioButton_pre_filter_mode_white_list, [
            self.ui.radioButton_pre_filter_mode_default,
            self.ui.radioButton_pre_filter_mode_black_list,
        ])

    def set_setting_pre_filter_mode_black_list_rule(self, rules):
        """设置文件预筛选模式：黑名单模式规则"""
        self._fill_text_edit(self.ui.textEdit_black_list, rules)

    def set_setting_pre_filter_mode_white_list_rule(self, rules):
        """设置文件预筛选模式：白名单模式规则"""
        self._fill_text_edit(self.ui.textEdit_white_list, rules)

    def set_setting_is_try_unknown_filetype(self, is_enable: bool):
        """通用选项：设置是否尝试处理未知格式的文件"""
        self.ui.checkBox_try_unknown_filetype.setChecked(is_enable)

    def set_setting_is_read_password_from_filename(self, is_enable: bool):
        """通用选项：设置是否尝试从文件名中读取密码"""
        self.ui.checkBox_read_password_from_filename.setChecked(is_enable)

    def set_setting_write_filename_t(self, is_enable: bool):
        """测试模式选项：检索到正确密码后是否将其写入文件名"""
        self.ui.checkBox_write_filename_t.setChecked(is_enable)
        self._show_setting_write_filename(is_enable)

    def _show_setting_write_filename(self, is_show: bool):
        """显示/隐藏写入文件名选项的子选项"""
        self.ui.widget_write_filename.setVisible(is_show)

    def set_setting_write_filename_left_part(self, text: str):
        """测试模式选项：将密码写入文件名时的左侧字符"""
        self.ui.lineEdit_left_word.setText(text)

    def set_setting_write_filename_right_part(self, text: str):
        """测试模式选项：将密码写入文件名时的右侧字符"""
        self.ui.lineEdit_right_word.setText(text)

    def set_setting_write_filename_position(self, option: str):
        """测试模式选项：将密码写入文件名时的位置（option 为下拉框选项文本）"""
        self.ui.comboBox_pw_position.setCurrentText(option)

    def set_setting_write_filename_preview(self, preview: str):
        """测试模式选项：将密码写入文件名时的文件名示例"""
        self.ui.label_preview_filename.setText(preview)

    def set_setting_extract_model_smart(self):
        """解压模式选项：智能解压（逻辑类似于 BandiZip）"""
        self._check_radio(self.ui.radioButton_mode2_smart_extract, [
            self.ui.radioButton_mode2_direct_extract,
            self.ui.radioButton_mode2_extract_same_folder,
        ])

    def set_setting_extract_model_direct(self):
        """解压模式选项：直接解压（不对结果进行处理）"""
        self._check_radio(self.ui.radioButton_mode2_direct_extract, [
            self.ui.radioButton_mode2_smart_extract,
            self.ui.radioButton_mode2_extract_same_folder,
        ])

    def set_setting_extract_model_same_folder(self):
        """解压模式选项：解压到同名目录"""
        self._check_radio(self.ui.radioButton_mode2_extract_same_folder, [
            self.ui.radioButton_mode2_smart_extract,
            self.ui.radioButton_mode2_direct_extract,
        ])

    def set_setting_recursive_extract(self, is_enable: bool):
        """解压模式选项：完成解压任务后是否进行递归解压"""
        self.ui.checkBox_recursive_extract.setChecked(is_enable)

    def set_setting_process_file_after_extract_success(self, is_enable: bool):
        """解压模式选项：解压成功后是否进行源文件操作"""
        self.ui.checkBox_process_file_after_extract_success.setChecked(is_enable)
        self._show_setting_process_file_after_extract_success(is_enable)

    def _show_setting_process_file_after_extract_success(self, is_show: bool):
        """显示/隐藏解压成功后源文件操作选项"""
        self.ui.widget_process_file_after_extract_success.setVisible(is_show)

    def set_setting_delete_file(self, is_enable: bool):
        """解压模式选项：解压成功后删除源文件"""
        self.ui.checkBox_delete_origin.setChecked(is_enable)

    def set_setting_is_move_origin_file_after_success(self, is_enable: bool):
        """解压模式选项：解压成功后移动源文件"""
        self.ui.checkBox_move_origin_file_after_success.setChecked(is_enable)
        self._show_setting_move_origin_file_after_success(is_enable)

    def set_setting_path_move_origin_file_after_success(self, path: str):
        """解压模式选项：解压成功后移动源文件的指定路径"""
        self.ui.lineEdit_move_origin_file_after_success.setText(path)

    def _show_setting_move_origin_file_after_success(self, is_show: bool):
        """显示/隐藏解压成功后移动源文件的路径输入框"""
        self.ui.lineEdit_move_origin_file_after_success.setVisible(is_show)

    def set_setting_write_filename_e(self, is_enable: bool):
        """解压模式选项：解压成功后是否将密码写入源文件的文件名"""
        self.ui.checkBox_write_filename_e.setChecked(is_enable)

    def set_setting_is_insert_char_to_filename_after_success(self, is_enable: bool):
        """解压模式选项：解压成功后向文件名中添加指定文本"""
        self.ui.checkBox_insert_char_to_filename_after_success.setChecked(is_enable)
        self._show_setting_insert_char_to_filename_after_success(is_enable)

    def set_setting_position_insert_char_to_filename_after_success(self, option: str):
        """解压模式选项：解压成功后向文件名中添加指定文本的位置"""
        self.ui.comboBox_insert_char_to_filename_after_success_position.setCurrentText(option)

    def set_setting_char_insert_char_to_filename_after_success(self, char: str):
        """解压模式选项：解压成功后向文件名中添加的指定文本"""
        self.ui.lineEdit_insert_char_to_filename_after_success_char.setText(char)

    def _show_setting_insert_char_to_filename_after_success(self, is_show: bool):
        """显示/隐藏解压成功后向文件名中添加指定文本的区域"""
        self.ui.widget_insert_char_to_filename_after_success.setVisible(is_show)

    def set_setting_process_file_after_extract_failure(self, is_enable: bool):
        """解压模式选项：解压失败后是否进行源文件操作"""
        self.ui.checkBox_process_file_after_extract_failure.setChecked(is_enable)
        self._show_setting_process_file_after_extract_failure(is_enable)

    def _show_setting_process_file_after_extract_failure(self, is_show: bool):
        """显示/隐藏解压失败后源文件操作选项"""
        self.ui.widget_process_file_after_extract_failure.setVisible(is_show)

    def set_setting_is_move_origin_file_after_failure(self, is_enable: bool):
        """解压模式选项：解压失败后移动源文件"""
        self.ui.checkBox_move_origin_file_after_failure.setChecked(is_enable)
        self._show_setting_move_origin_file_after_failure(is_enable)

    def set_setting_path_move_origin_file_after_failure(self, path: str):
        """解压模式选项：解压失败后移动源文件的指定路径"""
        self.ui.lineEdit_move_origin_file_after_failure.setText(path)

    def _show_setting_move_origin_file_after_failure(self, is_show: bool):
        """显示/隐藏解压失败后移动源文件的路径输入框"""
        self.ui.lineEdit_move_origin_file_after_failure.setVisible(is_show)

    def set_setting_is_insert_char_to_filename_after_failure(self, is_enable: bool):
        """解压模式选项：解压失败后向文件名中添加指定文本"""
        self.ui.checkBox_insert_char_to_filename_after_failure.setChecked(is_enable)
        self._show_setting_insert_char_to_filename_after_failure(is_enable)

    def set_setting_position_insert_char_to_filename_after_failure(self, option: str):
        """解压模式选项：解压失败后向文件名中添加指定文本的位置"""
        self.ui.comboBox_insert_char_to_filename_after_failure_position.setCurrentText(option)

    def set_setting_char_insert_char_to_filename_after_failure(self, char: str):
        """解压模式选项：解压失败后向文件名中添加的指定文本"""
        self.ui.lineEdit_insert_char_to_filename_after_failure_char.setText(char)

    def _show_setting_insert_char_to_filename_after_failure(self, is_show: bool):
        """显示/隐藏解压失败后向文件名中添加指定文本的区域"""
        self.ui.widget_insert_char_to_filename_after_failure.setVisible(is_show)

    def set_setting_cover_model(self, option: str):
        """解压模式选项：设置重名文件覆盖模式（option 为下拉框选项文本）"""
        self.ui.comboBox_cover_file.setCurrentText(option)

    def set_setting_break_folder(self, is_enable: bool):
        """解压模式选项：完成单个解压任务后是否解散文件夹"""
        self.ui.checkBox_break_folder.setChecked(is_enable)

    def set_setting_break_folder_model(self, option: str):
        """解压模式选项：解散文件夹的模式（option 为下拉框选项文本）"""
        self.ui.comboBox_break_folder.setCurrentText(option)

    def set_setting_extract_to_folder(self, is_enable: bool):
        """解压模式选项：是否解压至指定目录"""
        self.ui.checkBox_extract_output_folder.setChecked(is_enable)
        self._show_setting_extract_to_folder(is_enable)

    def set_setting_extract_output_folder(self, dirpath: str):
        """解压模式选项：设置解压输出目录"""
        self.ui.lineEdit_extract_output_folder.setText(dirpath)
        self.ui.lineEdit_extract_output_folder.setToolTip(dirpath)

    def _show_setting_extract_to_folder(self, is_show: bool):
        """显示/隐藏解压至指定目录选项"""
        self.ui.lineEdit_extract_output_folder.setVisible(is_show)
        self.ui.toolButton_choose.setVisible(is_show)
        self.ui.toolButton_open.setVisible(is_show)

    def set_setting_filter(self, is_enable: bool):
        """解压模式选项：解压时是否过滤文件"""
        self.ui.checkBox_extract_filter.setChecked(is_enable)
        self._show_setting_filter(is_enable)

    def set_setting_filter_rule(self, rule: str):
        """解压模式选项：设置过滤文件规则"""
        self.ui.plainTextEdit_extract_filter_rule.setPlainText(rule)

    def _show_setting_filter(self, is_show: bool):
        """显示/隐藏过滤文件规则选项"""
        self.ui.plainTextEdit_extract_filter_rule.setVisible(is_show)

    def set_setting_7zip_path(self, filepath: str):
        """设置 7zip 路径"""
        self.ui.lineEdit_7zip_path.setText(filepath)

    def set_top_window(self, is_enable: bool):
        """设置是否置顶窗口"""
        self.ui.checkBox_top_window.setChecked(is_enable)

    def set_lock_size(self, is_enable: bool):
        """设置是否锁定窗口大小"""
        self.ui.checkBox_lock_size.setChecked(is_enable)

    # endregion

    # region 信号绑定与槽函数
    def _bind_signal(self):
        """把界面控件的信号连接到信号成员或内部槽函数"""
        connections = [
            # 目录与文件选择弹窗
            (self.ui.toolButton_choose.clicked, self._choose_dirpath),
            (self.ui.toolButton_choose_7zip_path.clicked, self._choose_7zip_path),
            (self.ui.toolButton_open.clicked, self._open_dirpath),
            # 压缩包处理模式
            (self.ui.radioButton_mode1_extract.clicked, self._change_archive_model),
            (self.ui.radioButton_mode1_test.clicked, self._change_archive_model),
            # 文件预筛选模式
            (self.ui.radioButton_pre_filter_mode_default.clicked, self._change_pre_filter_model),
            (self.ui.radioButton_pre_filter_mode_black_list.clicked, self._change_pre_filter_model),
            (self.ui.radioButton_pre_filter_mode_white_list.clicked, self._change_pre_filter_model),
            (self.ui.textEdit_black_list.textChanged, self._change_black_list_rule),
            (self.ui.textEdit_white_list.textChanged, self._change_white_list_rule),
            (self.ui.toolButton_open_black_list.clicked, self._open_black_list_page),
            (self.ui.toolButton_open_white_list.clicked, self._open_white_list_page),
            (self.ui.pushButton_return_1.clicked, self._return_to_main_page),
            (self.ui.pushButton_return_2.clicked, self._return_to_main_page),
            # 通用选项
            (self.ui.checkBox_try_unknown_filetype.stateChanged, self.ChangeTryUnknownFiletype.emit),
            (self.ui.checkBox_read_password_from_filename.stateChanged, self.ChangeReadPasswordFromFilename.emit),
            # 测试模式的密码写入文件名
            (self.ui.checkBox_write_filename_t.stateChanged, self.ChangeWriteFilenameT.emit),
            (self.ui.checkBox_write_filename_t.stateChanged, self._show_setting_write_filename),
            (self.ui.lineEdit_left_word.textChanged, self.ChangeWriteFilenameLeftPart.emit),
            (self.ui.lineEdit_right_word.textChanged, self.ChangeWriteFilenameRightPart.emit),
            (self.ui.comboBox_pw_position.currentTextChanged, self.ChangeWriteFilenamePosition.emit),
            # 解压模式
            (self.ui.radioButton_mode2_smart_extract.clicked, self._change_extract_model),
            (self.ui.radioButton_mode2_direct_extract.clicked, self._change_extract_model),
            (self.ui.radioButton_mode2_extract_same_folder.clicked, self._change_extract_model),
            (self.ui.checkBox_recursive_extract.stateChanged, self.ChangeRecursiveExtract.emit),
            # 解压成功后的源文件操作
            (self.ui.checkBox_process_file_after_extract_success.stateChanged,
             self.ChangeProcessFileAfterExtractSuccess.emit),
            (self.ui.checkBox_process_file_after_extract_success.stateChanged,
             self._show_setting_process_file_after_extract_success),
            (self.ui.checkBox_delete_origin.stateChanged, self.ChangeDeleteFile.emit),
            (self.ui.checkBox_move_origin_file_after_success.stateChanged, self.ChangeMoveOriginFileAfterSuccess.emit),
            (self.ui.checkBox_move_origin_file_after_success.stateChanged,
             self._show_setting_move_origin_file_after_success),
            (self.ui.checkBox_write_filename_e.stateChanged, self.ChangeWriteFilenameE.emit),
            (self.ui.checkBox_insert_char_to_filename_after_success.stateChanged,
             self.ChangeInsertCharToFilenameAfterSuccess.emit),
            (self.ui.checkBox_insert_char_to_filename_after_success.stateChanged,
             self._show_setting_insert_char_to_filename_after_success),
            (self.ui.comboBox_insert_char_to_filename_after_success_position.currentTextChanged,
             self.ChangeInsertCharToFilenameAfterSuccessPosition.emit),
            (self.ui.lineEdit_insert_char_to_filename_after_success_char.textChanged,
             self.ChangeInsertCharToFilenameAfterSuccessChar.emit),
            # 解压失败后的源文件操作
            (self.ui.checkBox_process_file_after_extract_failure.stateChanged,
             self.ChangeProcessFileAfterExtractFailure.emit),
            (self.ui.checkBox_process_file_after_extract_failure.stateChanged,
             self._show_setting_process_file_after_extract_failure),
            (self.ui.checkBox_move_origin_file_after_failure.stateChanged, self.ChangeMoveOriginFileAfterFailure.emit),
            (self.ui.checkBox_move_origin_file_after_failure.stateChanged,
             self._show_setting_move_origin_file_after_failure),
            (self.ui.checkBox_insert_char_to_filename_after_failure.stateChanged,
             self.ChangeInsertCharToFilenameAfterFailure.emit),
            (self.ui.checkBox_insert_char_to_filename_after_failure.stateChanged,
             self._show_setting_insert_char_to_filename_after_failure),
            (self.ui.comboBox_insert_char_to_filename_after_failure_position.currentTextChanged,
             self.ChangeInsertCharToFilenameAfterFailurePosition.emit),
            (self.ui.lineEdit_insert_char_to_filename_after_failure_char.textChanged,
             self.ChangeInsertCharToFilenameAfterFailureChar.emit),
            # 解压设置
            (self.ui.comboBox_cover_file.currentTextChanged, self.ChangeCoverModel.emit),
            (self.ui.checkBox_break_folder.stateChanged, self.ChangeBreakFolder.emit),
            (self.ui.comboBox_break_folder.currentTextChanged, self.ChangeBreakFolderModel.emit),
            (self.ui.checkBox_extract_output_folder.stateChanged, self.ChangeExtractOutputFolder.emit),
            (self.ui.checkBox_extract_output_folder.stateChanged, self._show_setting_extract_to_folder),
            (self.ui.lineEdit_extract_output_folder.textChanged, self.ChangeExtractOutputFolderPath.emit),
            (self.ui.checkBox_extract_filter.stateChanged, self.ChangeExtractFilter.emit),
            (self.ui.checkBox_extract_filter.stateChanged, self._show_setting_filter),
            (self.ui.plainTextEdit_extract_filter_rule.textChanged, self._emit_extract_filter_rule),
            # 窗口设置
            (self.ui.lineEdit_7zip_path.textChanged, self.Change7ZipPath.emit),
            (self.ui.checkBox_top_window.stateChanged, self.ChangeTopWindow.emit),
            (self.ui.checkBox_lock_size.stateChanged, self.ChangeLockSize.emit),
        ]
        for signal, slot in connections:
            signal.connect(slot)

    def _open_black_list_page(self):
        """切换到黑名单规则页"""
        self.ui.stackedWidget.setCurrentIndex(1)

    def _open_white_list_page(self):
        """切换到白名单规则页"""
        self.ui.stackedWidget.setCurrentIndex(2)

    def _return_to_main_page(self):
        """返回设置主页面"""
        self.ui.stackedWidget.setCurrentIndex(0)

    def _emit_extract_filter_rule(self):
        """发出解压过滤规则（文本框信号本身不携带文本）"""
        self.ChangeExtractFilterRule.emit(self.ui.plainTextEdit_extract_filter_rule.toPlainText())

    def _change_archive_model(self):
        if self.ui.radioButton_mode1_extract.isChecked():
            self.ChangeArchiveModelExtract.emit(True)
            self._show_settings(True)
        elif self.ui.radioButton_mode1_test.isChecked():
            self.ChangeArchiveModelTest.emit(True)
            self._show_settings(False)

    def _change_pre_filter_model(self):
        if self.ui.radioButton_pre_filter_mode_default.isChecked():
            self.ChangePreFilterModeDefault.emit(True)
        elif self.ui.radioButton_pre_filter_mode_black_list.isChecked():
            self.ChangePreFilterModeBlackList.emit(True)
        elif self.ui.radioButton_pre_filter_mode_white_list.isChecked():
            self.ChangePreFilterModeWhiteList.emit(True)

    def _change_extract_model(self):
        if self.ui.radioButton_mode2_smart_extract.isChecked():
            self.ChangeExtractModelSmart.emit(True)
        elif self.ui.radioButton_mode2_direct_extract.isChecked():
            self.ChangeExtractModelDirect.emit(True)
        elif self.ui.radioButton_mode2_extract_same_folder.isChecked():
            self.ChangeExtractModelSameFolder.emit(True)

    def _change_black_list_rule(self):
        self._timer_black_list_rule.start()

    def _change_white_list_rule(self):
        self._timer_white_list_rule.start()

    def _emit_black_list_rule(self):
        self._emit_rules(self.ui.textEdit_black_list, self.ChangePreFilterModeBlackListRule)

    def _emit_white_list_rule(self):
        self._emit_rules(self.ui.textEdit_white_list, self.ChangePreFilterModeWhiteListRule)

    def eventFilter(self, obj, event):
        # 屏蔽指定下拉框的滚轮事件，避免误操作
        wheel_filtered_combos = [
            self.ui.comboBox_break_folder,
            self.ui.comboBox_cover_file,
            self.ui.comboBox_pw_position,
        ]
        if event.type() == QEvent.Wheel and obj in wheel_filtered_combos:
            return True
        return super().eventFilter(obj, event)
    # endregion


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = SettingViewer()
    program_ui.show()
    app_.exec()
