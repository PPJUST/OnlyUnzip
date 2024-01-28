import os
import re
import time

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QMovie, QPalette
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMenu, QFileDialog, QMessageBox

import module.function_archive
import module.function_file
import module.function_filetype
import module.function_password
from constant import _ICON_TEST_GIF, _ICON_EXTRACT_GIF, _ICON_MAIN, _ICON_DEFAULT, _ICON_DEFAULT_WITH_OUTPUT, _ICON_ERROR, \
    _ICON_FINISH
from module import function_config
from module import function_static
from module.function_config import Config
from qthread_7zip import ExtractQthread
from ui import Ui_MainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        # 初始化
        function_static.init_settings()  # 检查初始文件
        self.load_config()  # 加载设置文件
        self.check_output_dir()
        self.movie_label_icon = None  # 设置动图对象

        # 设置ui属性
        self.ui.listWidget_history.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置历史记录控件的右键菜单属性
        self.ui.stackedWidget_main.setCurrentIndex(0)  # 将主页面设为第1页
        self.ui.stackedWidget_schedule.setCurrentIndex(0)  # 将信息页设为第1页
        self.change_page(self.ui.buttonGroup.id(self.ui.buttonGroup.buttons()[0]))  # 设置第一个按钮的颜色

        # 实例化子线程
        self.qthread = ExtractQthread()
        self.qthread.signal_update_ui.connect(self.update_ui)
        self.qthread.signal_extracted_files.connect(lambda x: self.accept_files(x))

        """
        连接信号与槽函数
        """
        # 设置标签页的切换
        self.ui.buttonGroup.buttonClicked[int].connect(self.change_page)

        # 主页面
        self.ui.label_drop_file.signal_dropped.connect(self.accept_files)
        self.ui.button_stop.clicked.connect(self.stop_qthread)

        # 密码页的按钮
        self.ui.button_update_password.clicked.connect(self.update_password)  # 更新密码
        self.ui.button_read_clipboard.clicked.connect(self.read_clipboard)  # 读取剪切板
        self.ui.button_export_password.clicked.connect(lambda: module.function_password.export_password(
            with_count=False))  # 导出密码
        self.ui.button_export_password_with_number.clicked.connect(
            lambda: module.function_password.export_password(with_count=True))  # 导出含次数的密码
        self.ui.button_export_password.clicked.connect(lambda: self.ui.button_open_password.setEnabled(True))
        self.ui.button_export_password_with_number.clicked.connect(
            lambda: self.ui.button_open_password.setEnabled(True))
        self.ui.button_open_password.clicked.connect(lambda: os.startfile('密码导出.txt'))  # 打开导出的密码文件

        # 设置页的按钮
        self.ui.checkBox_mode_extract.stateChanged.connect(self.update_setting)
        self.ui.checkBox_mode_extract.stateChanged.connect(lambda: self.set_checkbox_enable(mode=True))
        self.ui.checkBox_mode_test.stateChanged.connect(self.update_setting)
        self.ui.checkBox_mode_test.stateChanged.connect(lambda: self.set_checkbox_enable(mode=False))

        self.ui.checkBox_un_nest_dir.stateChanged.connect(self.update_setting)
        self.ui.checkBox_un_nest_archive.stateChanged.connect(self.update_setting)
        self.ui.checkBox_delete_archive.stateChanged.connect(self.update_setting)
        self.ui.checkBox_check_filetype.stateChanged.connect(self.update_setting)
        self.ui.lineedit_exclude_rule.textChanged.connect(self.update_setting)
        self.ui.lineedit_output_dir.textChanged.connect(self.update_setting)
        self.ui.lineedit_output_dir.textChanged.connect(self.check_output_dir)
        self.ui.button_ask_folder.clicked.connect(self.choose_output_dir)

        # 历史记录页的操作
        self.ui.listWidget_history.customContextMenuRequested.connect(self.history_page_menu)  # 右键菜单

    def accept_files(self, path_list: list):
        """接收路径列表，提取出其中所有文件"""
        function_static.print_function_info()
        file_list = set()
        for path in path_list:
            path = os.path.normpath(path)  # 格式化路径，防止后续出错
            if os.path.exists(path):
                if os.path.isfile(path):
                    file_list.add(path)
                else:
                    walk_files = module.function_file.get_files_list(path)
                    file_list.update(walk_files)
        file_list = list(file_list)  # 转为列表，方便后续使用
        self.start_thread(file_list)

    def start_thread(self, file_list: list):
        """调用子线程进行后续操作"""
        function_static.print_function_info()
        output_dir = self.ui.lineedit_output_dir.text()
        # 先检查是否存在遗留的临时文件夹
        if function_static.is_temp_folder_exists(file_list) and function_static.is_temp_folder_exists(output_dir):
            # 再检查文件列表是否为空
            if file_list:
                # 对传入的文件列表进行处理，利用正则检查文件名是否符合分卷命名规则，将符合项转换为{第一个包:(全部分卷)..}的格式
                volume_archive_dict = module.function_archive.find_volume_archives(file_list)
                # 提取上述方法识别出的所有分卷文件
                all_volume_archive_files = set()
                for value in volume_archive_dict.values():
                    all_volume_archive_files.update(value)
                # 提取文件列表中不符合上述要求的其他项（不论是否为压缩包）
                other_file_dict = {}  # 保持字典格式的统一，{第一个包:(全部分卷)..}的格式
                for file in file_list:
                    if file not in all_volume_archive_files:
                        other_file_dict[file] = set()
                        other_file_dict[file].add(file)
                # 合并两个dict
                all_file_dict = {}  # 全部文件的dict
                all_file_dict.update(volume_archive_dict)
                all_file_dict.update(other_file_dict)
                # 根据是否需要识别压缩包，分两种情况获取最终需要执行操作的文件dict
                extract_file_dict = {}  # 最终执行操作的文件
                if self.ui.checkBox_check_filetype.isChecked():  # 仅压缩包
                    for file in all_file_dict:
                        if module.function_archive.is_archive(file):
                            extract_file_dict[file] = all_file_dict[file]
                else:
                    extract_file_dict.update(all_file_dict)
                # 将需要执行操作的文件dict传递给子线程
                if extract_file_dict:
                    self.set_widget_enable(mode=False)  # 禁用部分ui
                    # 设置子线程
                    self.qthread.reset_setting()  # 更新设置
                    self.qthread.set_extract_files_dict(extract_file_dict)  # 传递解压文件dict
                    self.qthread.start()
                else:  # 没有需解压的文件，则提示
                    self.update_ui('2-1')
            else:  # 没有需解压的文件，则提示
                self.update_ui('2-1')
        else:  # 如果有遗留的临时文件夹
            self.update_ui('2-2')

    def set_widget_enable(self, mode=True):
        """在解压开始前，设置相关控件的enable属性，防止解压过程中修改选项导致报错"""
        function_static.print_function_info()
        # 主页面
        self.ui.label_drop_file.setEnabled(mode)
        # 密码页
        self.ui.button_update_password.setEnabled(mode)
        # 设置页
        self.ui.scrollAreaWidgetContents.setEnabled(mode)

    def set_checkbox_enable(self, mode=True):
        """切换模式后启用/禁用相关设置项"""
        self.ui.checkBox_delete_archive.setEnabled(mode)
        self.ui.checkBox_check_filetype.setEnabled(mode)
        self.ui.checkBox_un_nest_dir.setEnabled(mode)
        self.ui.checkBox_un_nest_archive.setEnabled(mode)
        self.ui.lineedit_output_dir.setEnabled(mode)
        self.ui.lineedit_exclude_rule.setEnabled(mode)

    def history_page_menu(self, pos):
        """历史记录页中的右键菜单，用于复制密码"""
        function_static.print_function_info()

        def menu_copy_pw():
            item = self.ui.listWidget_history.currentItem()
            text = item.text().split(' | ', maxsplit=1)[1]  # 根据文本筛选出解压密码
            QApplication.clipboard().setText(text)

        selected_item = self.ui.listWidget_history.currentItem()
        if selected_item and selected_item.data(Qt.UserRole) == '4-7':  # 只有成功的行项目才可以右键
            menu = QMenu()
            menu.adjustSize()
            copy_action = QAction('复制解压密码', menu)
            copy_action.triggered.connect(menu_copy_pw)
            menu.addAction(copy_action)
            menu.exec_(self.ui.listWidget_history.mapToGlobal(pos))

    def update_ui(self, code: str, data: list = None):
        """根据传入的list，分不同情况更新ui
        type_list格式：['更新类型', '相关数据']"""
        function_static.print_function_info()
        if code == '1-1':  # 初始状态
            self.ui.label_drop_file.setPixmap(_ICON_DEFAULT)
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮
        elif code == '2-1':  # 没有需要解压的文件
            self.ui.label_drop_file.setPixmap(_ICON_FINISH)
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('没有需要解压的文件')
        elif code == '2-2':  # 存在遗留临时文件夹
            self.ui.label_drop_file.setPixmap(_ICON_ERROR)
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('存在遗留临时文件夹')
        elif code == '1-2':  # 启动子线程
            self.ui.button_stop.setVisible(True)  # 显示停止按钮
            self.movie_label_icon = None
            if self.ui.checkBox_mode_test.isChecked():  # 按选项设置不同图标
                # self.ui.label_drop_file.setPixmap(icon_test)
                self.movie_label_icon = QMovie(_ICON_TEST_GIF)
            else:
                # self.ui.label_drop_file.setPixmap(icon_extract)
                self.movie_label_icon = QMovie(_ICON_EXTRACT_GIF)
            self.ui.label_drop_file.setMovie(self.movie_label_icon)
            self.movie_label_icon.start()  # 开始动图
        elif code == '3-1':  # 更新当前文件
            self.ui.label_current_file.setText(data[0])
        elif code == '3-2':  # 更新总进度
            self.ui.label_schedule_file.setText(data[0])
        elif code == '3-3':  # 更新密码测试进度
            self.ui.label_schedule_test.setText(data[0])
            self.ui.stackedWidget_schedule.setCurrentIndex(1)
        elif code == '4-1':  # 历史记录-密码错误
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + data[0] + " ■密码错误"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(254, 67, 101))
            self.ui.listWidget_history.addItem(item)
        elif code == '4-2':  # 历史记录-丢失分卷
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + data[0] + " ■缺少分卷"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(254, 67, 101))
            self.ui.listWidget_history.addItem(item)
        elif code == '4-5':  # 历史记录-未知错误
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + data[0] + " ■未知错误"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(254, 67, 101))
            self.ui.listWidget_history.addItem(item)
        elif code == '4-3':  # 历史记录-不是压缩文件或损坏
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + data[0] + " ■不是压缩文件或已损坏，已跳过"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(255, 182, 193))
            self.ui.listWidget_history.addItem(item)
        elif code == '4-4':  # 历史记录-文件被占用
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + data[0] + " ■文件被占用，已跳过"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(255, 182, 193))
            self.ui.listWidget_history.addItem(item)
        elif code == '4-6':  # 历史记录-磁盘空间不足
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + data[0] + " ■磁盘空间不足，已跳过"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(255, 182, 193))
            self.ui.listWidget_history.addItem(item)
        elif code == '4-7':  # 历史记录-成功
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + data[0] + " | " + data[1]
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(92, 167, 186))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # 启用UserRole
            item.setData(Qt.UserRole, '4-7')  # 设置 UserRole 的值
            self.ui.listWidget_history.addItem(item)
        elif code == '3-4':  # 更新解压进度
            self.ui.progressBar_extract.setValue(data[0])
            self.ui.stackedWidget_schedule.setCurrentIndex(2)
        elif code == '1-3':  # 完成全部任务
            self.ui.label_drop_file.setPixmap(_ICON_FINISH)
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('全部完成')
            self.ui.label_schedule_finish.setText(data[0])
            self.set_widget_enable(mode=True)
            self.ui.stackedWidget_schedule.setCurrentIndex(0)
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮
            self.movie_label_icon.stop()  # 停止动图
        elif code == '1-4':  # 中止任务
            self.ui.label_schedule_file.setText('等待当前文件完成执行')
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮
            self.set_widget_enable(mode=True)  # 启用被禁用的ui
            self.movie_label_icon.stop()  # 停止动图

    def load_config(self):
        """读取配置文件，更新选项"""
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
        self.ui.checkBox_un_nest_dir.setChecked(setting_handling_nested_folder)
        self.ui.checkBox_un_nest_archive.setChecked(setting_handling_nested_archive)
        self.ui.checkBox_delete_archive.setChecked(setting_delete_original_file)
        self.ui.checkBox_check_filetype.setChecked(setting_check_filetype)
        self.ui.lineedit_exclude_rule.setText(' '.join(setting_exclude_rules))
        self.ui.lineedit_output_dir.setText(setting_output_folder)

    def update_password(self):
        """更新密码"""
        function_static.print_function_info()
        function_config.backup_config()  # 更新前备份配置文件

        add_pw = [n for n in self.ui.text_password.toPlainText().split('\n') if n.strip()]
        add_pw_strip = [n.strip() for n in add_pw]
        pw_list = list(set(add_pw + add_pw_strip))  # 转为集合去重
        module.function_password.update_password(pw_list)

        self.ui.text_password.clear()  # 重置密码框

    def read_clipboard(self):
        """读取剪切板"""
        function_static.print_function_info()
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        self.ui.text_password.setPlainText(clipboard_text)

    def update_setting(self):
        """更新设置"""
        function_static.print_function_info()
        mode = 'extract' if self.ui.checkBox_mode_extract.isChecked() else 'test'
        un_nest_dir = str(self.ui.checkBox_un_nest_dir.isChecked())
        un_nest_archive = str(self.ui.checkBox_un_nest_archive.isChecked())
        delete_archive = str(self.ui.checkBox_delete_archive.isChecked())
        check_filetype = str(self.ui.checkBox_check_filetype.isChecked())
        output_dir = str(self.ui.lineedit_output_dir.text())

        exclude_text = self.ui.lineedit_exclude_rule.text()
        support_delimiters = ",|，| |;|；"
        exclude_list = set([i for i in re.split(support_delimiters, exclude_text) if i])  # 提取分隔后的数据，去重去空值
        exclude_rule = ' '.join(exclude_list)  # 转为字符串



        Config.update_config_mode(mode)
        Config.update_config_handling_nested_folder(un_nest_dir)
        Config.update_config_handling_nested_archive(un_nest_archive)
        Config.update_config_delete_original_file(delete_archive)
        Config.update_config_check_filetype(check_filetype)
        Config.update_exclude_rules(exclude_rule)
        Config.update_config_output_folder(output_dir)


    def change_page(self, button_id):
        """切换标签页，并高亮被点击的标签页按钮"""
        function_static.print_function_info()
        original_style = self.ui.button_update_password.styleSheet()  # 按钮的原始样式
        clicked_style = f'background-color: rgb(255, 228, 181);'  # 被点击后的样式
        # 重置按钮组中所有按钮的样式
        for button in self.ui.buttonGroup.buttons():
            button.setStyleSheet(original_style)
        # 高亮被点击的按钮
        clicked_button = self.ui.buttonGroup.button(button_id)
        clicked_button.setStyleSheet(clicked_style)
        # 切换标签页
        new_page_number = self.ui.buttonGroup.buttons().index(self.ui.buttonGroup.button(button_id))
        self.ui.stackedWidget_main.setCurrentIndex(new_page_number)

    def choose_output_dir(self):
        """弹出对话框选择输出文件夹"""
        function_static.print_function_info()
        dirpath = QFileDialog.getExistingDirectory(self, "选择指定解压路径文件夹")
        if dirpath:
            self.ui.lineedit_output_dir.setText(os.path.normpath(dirpath))

    def check_output_dir(self):
        """检查是否指定了解压输出路径，并修改相关ui显示"""
        function_static.print_function_info()
        output_dir = self.ui.lineedit_output_dir.text()
        if output_dir:
            if not os.path.exists(output_dir) or os.path.isfile(output_dir):
                self.ui.lineedit_output_dir.setStyleSheet('border: 1px solid red;')
                self.ui.label_drop_file.setPixmap(_ICON_DEFAULT)
            else:
                self.ui.lineedit_output_dir.setStyleSheet('')
                self.ui.label_drop_file.setPixmap(_ICON_DEFAULT_WITH_OUTPUT)
        else:
            self.ui.lineedit_output_dir.setStyleSheet('')
            self.ui.label_drop_file.setPixmap(_ICON_DEFAULT)

    def stop_qthread(self):
        """中止解压子线程"""
        function_static.print_function_info()
        reply = QMessageBox.question(self, '确认对话框',
                                     f'是否中止当前任务\n（不终止当前正在执行的文件，\n仅中止之后的任务）',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.update_ui('1-4')
            self.qthread.signal_stop.emit()


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
    app.exec_()


if __name__ == "__main__":
    main()
