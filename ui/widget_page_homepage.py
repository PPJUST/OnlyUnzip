# 主页

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox, QFrame

from constant import _ICON_STOP, _ICON_SKIP, _ICON_WARNING, _ICON_EXTRACT_GIF, _ICON_TEST_GIF, _ICON_FINISH, \
    _ICON_DISCONNECT, _ICON_MAIN_PATH, _ICON_MAIN_DEFAULT
from module import function_normal, function_archive
from module.function_7zip import Collect7zipResult
from module.function_config import GetSetting
from thread.thread_7zip import Thread7zip
from ui.label_drop import LabelDrop
from ui.src.ui_widget_page_homepage import Ui_Form


class WidgetPageHomepage(QFrame):
    signal_start_7zip = Signal()
    signal_finished_7zip = Signal()
    signal_7zip_result = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # ui设置
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.ui.toolButton_stop.setIcon(QIcon(_ICON_STOP))
        self.ui.toolButton_stop.clicked.connect(self._show_stop_dialog)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.toolButton_stop.setEnabled(False)

        # 添加控件
        self.label_drop = LabelDrop()
        self.ui.layout_label_drop.addWidget(self.label_drop)
        self.label_drop.signal_dropped.connect(self.drop_paths)
        self.set_default_drop_icon()

        # 实例化7zip线程
        self.thread_7zip = Thread7zip()
        # 绑定7zip线程运行信号
        self.thread_7zip.signal_stop.connect(self._state_stop_7zip)
        self.thread_7zip.signal_finish.connect(self._state_finished_7zip)
        self.thread_7zip.signal_finish_restart.connect(self._restart_7zip)
        # 绑定7zip线程进度信号
        self.thread_7zip.signal_current_file.connect(self._update_info_current_file)
        self.thread_7zip.signal_schedule_file.connect(self._update_info_schedule_file)
        self.thread_7zip.signal_schedule_test.connect(self._update_info_schedule_test)
        self.thread_7zip.signal_schedule_extract.connect(self._update_info_schedule_extract)
        # 中转7zip线程调用结果信号
        self.thread_7zip.signal_7zip_result.connect(self.signal_7zip_result.emit)

        # 实例收集类
        self.collect_result = Collect7zipResult()

    def set_default_drop_icon(self):
        output_path = GetSetting.output_folder()
        if output_path:
            self.label_drop.reset_icon(_ICON_MAIN_PATH)
        else:
            self.label_drop.reset_icon(_ICON_MAIN_DEFAULT)

    def drop_paths(self, paths):
        """拖入文件"""
        files = function_normal.get_files_in_paths(paths)
        self._handle_files(files)

    def _handle_files(self, files):
        """处理文件"""
        # 检查传入列表是否为空
        if not files:
            self._state_no_archive()
            return

        # 检查同级目录是否存在遗留的（非空）临时文件夹
        if function_normal.is_temp_folder_exists(files):
            self._state_temp_folder()
            return

        # 指定解压目录时，检查解压目录中是否存在遗留的（非空）临时文件夹
        output_path = GetSetting.output_folder()
        if function_normal.is_temp_folder_exists(output_path):
            self._state_temp_folder()
            return

        # 分类压缩包
        # dict结构：key为第一个分卷包路径/非分卷则为其本身，value为list，内部元素为其对应的所有分卷包
        file_dict = function_archive.split_archive(files)

        # 根据“是否仅处理压缩文件”选项再次筛选文件
        if GetSetting.check_filetype():
            file_dict = {key: value for key, value in file_dict.items() if function_archive.is_archive(key)}

        # 检查筛选后的文件是否为空
        if not file_dict:
            self._state_no_archive()
            return

        # 将最终需要处理的文件传递给7zip子线程，并启动子线程
        self._state_start_7zip()
        self.thread_7zip.set_file_dict(file_dict)
        self.thread_7zip.start()

    def _restart_7zip(self, paths):
        """将7zip线程传回的解压文件列表再次进行解压"""
        files = function_normal.get_files_in_paths(paths)
        if not files:
            self._state_finished_7zip()
            return

        # 检查同级目录是否存在遗留的（非空）临时文件夹
        if function_normal.is_temp_folder_exists(files):
            self._state_temp_folder()
            return

        # 指定解压目录时，检查解压目录中是否存在遗留的（非空）临时文件夹
        output_path = GetSetting.output_folder()
        if function_normal.is_temp_folder_exists(output_path):
            self._state_temp_folder()
            return

        # 分类压缩包
        # dict结构：key为第一个分卷包路径/非分卷则为其本身，value为list，内部元素为其对应的所有分卷包
        file_dict = function_archive.split_archive(files)

        # 根据“是否仅处理压缩文件”选项再次筛选文件
        if GetSetting.check_filetype():
            file_dict = {key: value for key, value in file_dict.items() if function_archive.is_archive(key)}

        # 检查筛选后的文件是否为空
        if not file_dict:
            self._state_finished_7zip()
            return

        # 将最终需要处理的文件传递给7zip子线程，并启动子线程
        self.signal_start_7zip.emit()
        self._state_start_7zip()
        self.thread_7zip.set_file_dict(file_dict)
        self.thread_7zip.start()

    def _show_stop_dialog(self):
        """显示停止对话框"""
        info = '是否停止当前的密码搜索任务\n（不会终止正在进行的解压操作）'
        reply = QMessageBox.question(self, '是否停止', info, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.thread_7zip.stop()
            self.ui.toolButton_stop.setEnabled(False)

    def _set_drop_label_state(self, enable: bool):
        """启用/禁用拖入控件"""
        self.label_drop.setEnabled(enable)

    def _state_no_archive(self):
        """状态-没有压缩文件"""
        self.label_drop.reset_icon(_ICON_SKIP)
        self.ui.label_schedule_file.setText('-/-')
        self.ui.label_current_file.setText('-')
        self.ui.label_state.setText('无压缩文件')
        self.ui.stackedWidget.setCurrentIndex(0)

    def _state_temp_folder(self):
        """状态-存在非空临时文件夹"""
        self.label_drop.reset_icon(_ICON_WARNING)
        self.ui.label_schedule_file.setText('-/-')
        self.ui.label_current_file.setText('-')
        self.ui.label_state.setText('存在遗留的临时文件夹，请检查')
        self.ui.stackedWidget.setCurrentIndex(0)

    def _state_start_7zip(self):
        """状态-启动7zip子线程"""
        self.signal_start_7zip.emit()
        self._set_drop_label_state(False)
        self.ui.toolButton_stop.setEnabled(True)
        if GetSetting.mode_extract():
            self.label_drop.reset_icon(_ICON_EXTRACT_GIF)
        else:
            self.label_drop.reset_icon(_ICON_TEST_GIF)

    def _state_stop_7zip(self):
        """状态-终止7zip子线程"""
        self.signal_finished_7zip.emit()
        self._set_drop_label_state(True)
        self.ui.toolButton_stop.setEnabled(False)
        self.label_drop.reset_icon(_ICON_DISCONNECT)
        self.ui.label_schedule_file.setText('-/-')
        self.ui.label_current_file.setText('-')
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.label_state.setText(self.collect_result.get_result_text())
        # 重置收集类的计数
        self.collect_result.reset_count()

    def _state_finished_7zip(self):
        """状态-7zip子线程运行结束"""
        self.signal_finished_7zip.emit()
        self._set_drop_label_state(True)
        self.ui.toolButton_stop.setEnabled(False)
        self.label_drop.reset_icon(_ICON_FINISH)
        self.ui.label_schedule_file.setText('-/-')
        self.ui.label_current_file.setText('-')
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.label_state.setText(self.collect_result.get_result_text())
        # 重置收集类的计数
        self.collect_result.reset_count()

    def _update_info_current_file(self, text):
        """更新当前文件"""
        self.ui.label_current_file.setText(text)

    def _update_info_schedule_file(self, text):
        """更新文件进度"""
        self.ui.label_schedule_file.setText(text)

    def _update_info_schedule_test(self, text):
        """更新密码测试进度"""
        self.ui.label_schedule_test.setText(text)
        if self.ui.stackedWidget.currentIndex() != 1:
            self.ui.stackedWidget.setCurrentIndex(1)

    def _update_info_schedule_extract(self, value):
        """更新解压进度"""
        self.ui.progressBar_schedule_extract.setValue(value)
        if self.ui.stackedWidget.currentIndex() != 2:
            self.ui.stackedWidget.setCurrentIndex(2)


if __name__ == "__main__":
    app_ = QApplication()
    app_.setStyle('Fusion')
    program_ui = WidgetPageHomepage()
    program_ui.show()
    app_.exec()
