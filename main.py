import os
import re

from PySide6.QtGui import QColor, QIcon, QPalette
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from constant import _ICON_MAIN, _ICON_DEFAULT, _ICON_DEFAULT_WITH_OUTPUT, \
    _PASSWORD_EXPORT, _ICON_PAGE_HISTORY, _ICON_PAGE_PASSWORD, _ICON_PAGE_SETTING, _ICON_PAGE_HOME, \
    _ICON_STOP
from module import function_archive
from module import function_file
from module import function_normal
from module import function_password
from module.class_count_7z_result import Count7zResult
from module.class_state import StateError, StateUpdateUI, StateSchedule, State7zResult
from module.function_config import Config
from qthread_7zip import Thread7z
from ui.drop_label import DropLabel
from ui.history_listWidget import HistoryListWidget
from ui.ui_main import Ui_MainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 添加自定义控件
        self.dropped_label = DropLabel()
        self.ui.verticalLayout_dropped_label.addWidget(self.dropped_label)

        self.history_listWidget = HistoryListWidget()
        self.ui.verticalLayout_history.addWidget(self.history_listWidget)

        # 初始化
        function_normal.init_settings()  # 检查初始文件
        self.load_config()
        self.check_output_folder()
        self.count_7z_result = Count7zResult()  # 用于收集结果

        # 设置ui
        self.ui.stackedWidget_main.setCurrentIndex(0)  # 将主页面设为第1页
        self.ui.stackedWidget_schedule.setCurrentIndex(0)  # 将信息页设为第1页
        self.change_page(self.ui.buttonGroup.id(self.ui.buttonGroup.buttons()[0]))  # 设置第一个按钮的颜色
        self.ui.button_page_home.setIcon(QIcon(_ICON_PAGE_HOME))
        self.ui.button_page_history.setIcon(QIcon(_ICON_PAGE_HISTORY))
        self.ui.button_page_password.setIcon(QIcon(_ICON_PAGE_PASSWORD))
        self.ui.button_page_setting.setIcon(QIcon(_ICON_PAGE_SETTING))
        self.ui.button_stop.setIcon(QIcon(_ICON_STOP))
        self.ui.button_stop.setEnabled(False)
        self.ui.text_password.setPlaceholderText(
            '添加密码，一个密码占一行，点击“更新密码”即可更新\n支持拖入密码数据库文件直接更新')

        # 实例化子线程
        self.thread_7z = Thread7z()
        self.thread_7z.signal_schedule.connect(self.update_info_on_ui)

        # 设置槽函数
        # 标签页
        self.ui.buttonGroup.buttonClicked.connect(self.change_page)
        # 主页
        self.dropped_label.signal_dropped.connect(self.dropped_files)
        self.ui.button_stop.clicked.connect(self.stop_thread_7z)
        # 密码
        self.ui.button_update_password.clicked.connect(self.update_password)
        self.ui.button_read_clipboard.clicked.connect(self.read_clipboard)
        self.ui.button_export_password.clicked.connect(function_password.export_passwords)
        self.ui.button_export_password.clicked.connect(lambda: self.ui.button_open_password.setEnabled(True))
        self.ui.button_open_password.clicked.connect(lambda: os.startfile(_PASSWORD_EXPORT))
        self.ui.text_password.textChanged.connect(self.drop_password_pickle)
        # 设置页
        self.ui.checkBox_mode_extract.stateChanged.connect(lambda: self.set_checkbox_enable(mode=True))
        self.ui.checkBox_mode_test.stateChanged.connect(lambda: self.set_checkbox_enable(mode=False))
        self.ui.button_ask_folder.clicked.connect(self.choose_output_folder)
        self.ui.lineEdit_output_folder.textChanged.connect(self.check_output_folder)
        self.ui.checkBox_mode_extract.stateChanged.connect(lambda: self.update_config('mode'))
        self.ui.checkBox_mode_test.stateChanged.connect(lambda: self.update_config('mode'))
        self.ui.checkBox_handling_nested_folder.stateChanged.connect(lambda: self.update_config('nested_folder'))
        self.ui.checkBox_handling_nested_archive.stateChanged.connect(lambda: self.update_config('nested_archive'))
        self.ui.checkBox_delete_original_file.stateChanged.connect(lambda: self.update_config('delete_original_file'))
        self.ui.checkBox_check_filetype.stateChanged.connect(lambda: self.update_config('check_filetype'))
        self.ui.lineEdit_exclude_rules.textChanged.connect(lambda: self.update_config('exclude_rules'))
        self.ui.lineEdit_output_folder.textChanged.connect(lambda: self.update_config('output_folder'))
        self.ui.checkBox_handling_nested_archive.stateChanged.connect(self.set_nested_checkbox)

    def load_config(self):
        """读取配置文件，更新选项"""
        function_normal.print_function_info()
        # 读取
        config = Config()
        setting_mode = config.mode
        setting_handling_nested_folder = config.handling_nested_folder
        setting_handling_nested_archive = config.handling_nested_archive
        setting_delete_original_file = config.delete_original_file
        setting_check_filetype = config.check_filetype
        setting_exclude_rules = config.exclude_rules
        setting_output_folder = config.output_folder

        # 更新选项
        if setting_mode == 'extract':
            self.ui.checkBox_mode_extract.setChecked(True)
            self.set_checkbox_enable(mode=True)
        elif setting_mode == 'test':
            self.ui.checkBox_mode_test.setChecked(True)
            self.set_checkbox_enable(mode=False)
        self.ui.checkBox_handling_nested_folder.setChecked(setting_handling_nested_folder)
        self.ui.checkBox_handling_nested_archive.setChecked(setting_handling_nested_archive)
        self.ui.checkBox_delete_original_file.setChecked(setting_delete_original_file)
        self.ui.checkBox_check_filetype.setChecked(setting_check_filetype)
        self.ui.lineEdit_exclude_rules.setText(' '.join(setting_exclude_rules))
        self.ui.lineEdit_output_folder.setText(setting_output_folder)

    def set_checkbox_enable(self, mode=True):
        """切换模式后启用/禁用相关设置项"""
        function_normal.print_function_info()
        self.ui.checkBox_delete_original_file.setEnabled(mode)
        self.ui.checkBox_handling_nested_folder.setEnabled(mode)
        self.ui.checkBox_handling_nested_archive.setEnabled(mode)
        self.ui.lineEdit_output_folder.setEnabled(mode)
        self.ui.lineEdit_exclude_rules.setEnabled(mode)

    def set_widget_enable(self, mode=True):
        """启动7zip子线程前启用/禁用相关控件"""
        function_normal.print_function_info()
        # 主页
        self.dropped_label.setEnabled(mode)
        # 密码页
        self.ui.button_update_password.setEnabled(mode)
        # 设置页
        self.ui.scrollAreaWidgetContents.setEnabled(mode)

    def check_output_folder(self):
        """检查是否指定了解压输出路径，并修改相关ui显示"""
        function_normal.print_function_info()
        output_dir = self.ui.lineEdit_output_folder.text()
        if output_dir:
            if not os.path.exists(output_dir) or os.path.isfile(output_dir):
                self.ui.lineEdit_output_folder.setStyleSheet('border: 1px solid red;')
                self.dropped_label.reset_icon(_ICON_DEFAULT)
            else:
                self.ui.lineEdit_output_folder.setStyleSheet('')
                self.dropped_label.reset_icon(_ICON_DEFAULT_WITH_OUTPUT)
        else:
            self.ui.lineEdit_output_folder.setStyleSheet('')
            self.dropped_label.reset_icon(_ICON_DEFAULT)

    def change_page(self, button_id):
        """切换标签页，并高亮被点击的标签页按钮"""
        function_normal.print_function_info()
        # 统一为int索引
        if type(button_id) is int:
            buttons_index = button_id
        else:
            buttons_index = self.ui.buttonGroup.id(button_id)

        # 切换标签页
        new_page_number = self.ui.buttonGroup.buttons().index(self.ui.buttonGroup.button(buttons_index))
        self.ui.stackedWidget_main.setCurrentIndex(new_page_number)

        # 高亮被点击的按钮
        original_style = self.ui.button_update_password.styleSheet()
        for button in self.ui.buttonGroup.buttons():
            button.setStyleSheet(original_style)

        clicked_style = r'background-color: rgb(255, 228, 181);'
        clicked_button = self.ui.buttonGroup.button(buttons_index)
        clicked_button.setStyleSheet(clicked_style)

    def dropped_files(self, paths: list):
        """拖入文件后进行测试或解压"""
        function_normal.print_function_info()
        file_list = []
        for path in paths:
            path = os.path.normpath(path)
            if os.path.exists(path):
                if os.path.isfile(path):
                    file_list.append(path)
                else:
                    walk_files = function_file.get_files_list(path)
                    file_list += walk_files
        file_list = list(set(file_list))

        self.start_7zip_thread(file_list)

    def choose_output_folder(self):
        """弹出对话框，选择文件夹"""
        function_normal.print_function_info()
        dirpath = QFileDialog.getExistingDirectory(self, "选择指定解压路径文件夹")
        if dirpath:
            self.ui.lineEdit_output_folder.setText(os.path.normpath(dirpath))

    def update_config(self, setting_item: str):
        """更新配置文件"""
        function_normal.print_function_info()
        if setting_item == 'mode':
            mode = 'extract' if self.ui.checkBox_mode_extract.isChecked() else 'test'
            Config.update_config_mode(mode)
        elif setting_item == 'nested_folder':
            handling_nested_folder = self.ui.checkBox_handling_nested_folder.isChecked()
            Config.update_config_handling_nested_folder(handling_nested_folder)
        elif setting_item == 'nested_archive':
            handling_nested_archive = self.ui.checkBox_handling_nested_archive.isChecked()
            Config.update_config_handling_nested_archive(handling_nested_archive)
        elif setting_item == 'delete_original_file':
            delete_original_file = self.ui.checkBox_delete_original_file.isChecked()
            Config.update_config_delete_original_file(delete_original_file)
        elif setting_item == 'check_filetype':
            check_filetype = self.ui.checkBox_check_filetype.isChecked()
            Config.update_config_check_filetype(check_filetype)
        elif setting_item == 'exclude_rules':
            exclude_text = self.ui.lineEdit_exclude_rules.text()
            support_delimiters = ',|，| |;|；'
            exclude_list = set([i for i in re.split(support_delimiters, exclude_text) if i])
            exclude_rule = ' '.join(exclude_list)
            Config.update_exclude_rules(exclude_rule)
        elif setting_item == 'output_folder':
            output_dir = str(self.ui.lineEdit_output_folder.text())
            Config.update_config_output_folder(output_dir)

    def update_password(self):
        """更新密码"""
        function_normal.print_function_info()
        function_password.backup_passwords()
        add_pw = [n for n in self.ui.text_password.toPlainText().split('\n') if n.strip()]
        add_pw_strip = [n.strip() for n in add_pw]
        pw_list = list(set(add_pw + add_pw_strip))  # 考虑到密码两端的空格，需要添加两种形式的密码
        function_password.update_passwords(pw_list)
        self.ui.text_password.clear()

    def read_clipboard(self):
        """读取剪切板"""
        function_normal.print_function_info()
        clipboard = QApplication.clipboard()
        self.ui.text_password.setPlainText(clipboard.text())

    def start_7zip_thread(self, files: list):
        """调用子线程"""
        function_normal.print_function_info()
        output_dir = self.ui.lineEdit_output_folder.text()
        # 检查是否存在遗留的临时文件夹
        if function_normal.is_temp_folder_exists(files) and function_normal.is_temp_folder_exists(output_dir):
            self.update_info_on_ui(StateError.TempFolder())
            return

        # 检查传入文件列表是否为空
        if not files:
            self.update_info_on_ui(StateError.NoArchive())
            return

        # 检查传入文件列表，提取出符合分卷压缩文件规则的文件，转换为{第一个分卷压缩包:(全部分卷)..}格式
        volume_archive_dict = function_archive.find_volume_archives(files)

        # 提取其余非分卷的文件
        other_file_dict = {}  # 保持字典格式的统一，{文件路径:(文件路径)..}
        volume_archives = set()
        for value in volume_archive_dict.values():
            volume_archives.update(value)
        for file in files:
            if file not in volume_archives:
                other_file_dict[file] = set()
                other_file_dict[file].add(file)

        # 合并两个dict
        file_dict = {}
        file_dict.update(volume_archive_dict)
        file_dict.update(other_file_dict)

        # 根据是否仅需要识别压缩文件，分两种情况获取最终需要执行操作的文件dict
        final_file_dict = {}
        if self.ui.checkBox_check_filetype.isChecked():
            for file in file_dict:
                if function_archive.is_archive(file):
                    final_file_dict[file] = file_dict[file]
        else:
            final_file_dict.update(file_dict)

        # 检查
        if not final_file_dict:
            self.update_info_on_ui(StateError.NoArchive())
            return

        # 将dict传递给子线程
        if final_file_dict:
            self.ui.button_stop.setEnabled(True)
            self.dropped_label.setEnabled(False)
            self.thread_7z.reset_file_dict(final_file_dict)
            self.thread_7z.start()

    def stop_thread_7z(self):
        """停止7z子线程"""
        function_normal.print_function_info()
        info = '是否中止当前任务\n（不终止当前正在解压的文件，\n仅中止之后的任务）'
        reply = QMessageBox.question(self, '确认对话框', info, QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.thread_7z.stop()

    def update_info_on_ui(self, state_class):
        """
        更新ui
        :param state_class: 自定义State类
        """
        function_normal.print_function_info()
        # StateError类，错误信息
        if type(state_class) in StateError.__dict__.values():
            self.dropped_label.reset_icon(state_class.icon)
            self.ui.label_current_file.setText(state_class.current_file)
            self.ui.label_schedule_state.setText(state_class.schedule_state)
            self.ui.button_stop.setEnabled(False)
            if type(state_class) is StateError.NoArchive:  # 因为没有可解压文件而返回错误码
                self.ui.stackedWidget_schedule.setCurrentIndex(0)
                result_text = self.count_7z_result.get_result_text()
                self.ui.label_schedule_state.setText(result_text)
                self.ui.label_current_file.setText('')
                self.ui.button_stop.setEnabled(False)
                self.dropped_label.setEnabled(True)
                self.ui.page_setting.setEnabled(True)

        # StateUpdateUI类，更新进度ui
        elif type(state_class) in StateUpdateUI.__dict__.values():
            text = state_class.text
            if type(state_class) is StateUpdateUI.CurrentFile:  # 当前文件
                self.ui.label_current_file.setText(text)
            elif type(state_class) is StateUpdateUI.ScheduleTotal:  # 总文件进度
                self.ui.label_schedule_total.setText(text)
            elif type(state_class) is StateUpdateUI.SchedulePassword:  # 测试密码进度
                self.ui.label_schedule_test.setText(text)
                if self.ui.stackedWidget_schedule.currentIndex() != 1:
                    self.ui.stackedWidget_schedule.setCurrentIndex(1)
            elif type(state_class) is StateUpdateUI.ScheduleExtract:  # 解压进度
                self.ui.progressBar_extract.setValue(text)
                if self.ui.stackedWidget_schedule.currentIndex() != 2:
                    self.ui.stackedWidget_schedule.setCurrentIndex(2)
        # StateSchedule类，测试/解压情况
        elif type(state_class) in StateSchedule.__dict__.values():
            # 修改图标
            icon = state_class.icon
            self.dropped_label.reset_icon(icon)
            # 锁定设置页（防止修改选项后出错）
            self.ui.page_setting.setEnabled(False)
            # 切页及修改结果文本
            is_handling_nested_archive = self.ui.checkBox_handling_nested_archive.isChecked()
            if type(state_class) in [StateSchedule.Finish, StateSchedule.Stop]:
                self.ui.stackedWidget_schedule.setCurrentIndex(0)
                result_text = self.count_7z_result.get_result_text(is_reset=not is_handling_nested_archive)
                self.ui.label_schedule_state.setText(result_text)
                self.ui.label_current_file.setText('')
                self.ui.button_stop.setEnabled(False)
                self.dropped_label.setEnabled(True)
                self.ui.page_setting.setEnabled(True)
            # 选中解套压缩包，且有解压结果，则在结束后再次解压
            if (type(state_class) is StateSchedule.Finish and
                    is_handling_nested_archive and
                    self.thread_7z.extract_result_paths):
                self.dropped_files(self.thread_7z.extract_result_paths)

        # State7zResult类，7z调用结果
        elif type(state_class) in State7zResult.__dict__.values():
            self.count_7z_result.collect_result(state_class)  # 收集结果
            self.history_listWidget.insert_item(state_class)  # 添加历史记录
            if type(state_class) is State7zResult.Success:
                password = state_class.password
                function_password.add_pw_count(password)

    def drop_password_pickle(self):
        """向密码框拖入了密码数据库"""
        function_password.backup_passwords()
        text = self.ui.text_password.toPlainText()
        if text.startswith('file:///') and text.endswith('.pickle'):
            pickle_file = text[8:]
            passwords = function_password.read_passwords(pickle_file)
            function_password.update_passwords(passwords)
            self.ui.text_password.clear()

    def set_nested_checkbox(self):
        """联动checkbox选项"""
        if self.ui.checkBox_handling_nested_archive.isChecked():
            self.ui.checkBox_check_filetype.setChecked(True)


def main():
    app = QApplication()
    app.setStyle('Fusion')
    # 设置白色背景色
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    app.setPalette(palette)

    show_ui = Main()
    show_ui.setWindowIcon(QIcon(_ICON_MAIN))
    show_ui.setFixedSize(262, 232)
    show_ui.show()
    app.exec()


if __name__ == "__main__":
    main()
