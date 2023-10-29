import configparser
import os
import re
import shutil
import time
from typing import Tuple

import natsort
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor, QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMenu, QAction, QFileDialog, QMessageBox

from qthread_7zip import ExtractQthread
from ui import Ui_MainWindow
from model import function_config
from model import function_static


icon_test = './icon/测试密码.png'
icon_main = './icon/程序图标.png'
icon_origin = './icon/初始状态.png'
icon_origin_with_output = './icon/初始状态_指定文件夹.png'
icon_error = './icon/错误.png'
icon_finish = './icon/全部完成.png'
icon_extract = './icon/正在解压.png'
icon_stop = './icon/中止.png'





class OnlyUnzip(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """
        初始化设置
        """
        # 初始设置
        function_config.check_config()  # 检查配置文件是否存在
        self.load_config()  # 加载设置文件
        self.update_ui('1-1')  # 设置初始图标
        self.check_output_dir()

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
        self.ui.label_icon.dropSignal.connect(self.accept_files)
        self.ui.button_stop.clicked.connect(self.stop_qthread)

        # 密码页的按钮
        self.ui.button_update_password.clicked.connect(self.update_password)  # 更新密码
        self.ui.button_read_clipboard.clicked.connect(self.read_clipboard)  # 读取剪切板
        self.ui.button_export_password.clicked.connect(lambda: function_config.export_pw(with_number=False))  # 导出密码
        self.ui.button_export_password_with_number.clicked.connect(
            lambda: function_config.export_pw(with_number=True))  # 导出含次数的密码
        self.ui.button_export_password.clicked.connect(lambda: self.ui.button_open_password.setEnabled(True))
        self.ui.button_export_password_with_number.clicked.connect(
            lambda: self.ui.button_open_password.setEnabled(True))
        self.ui.button_open_password.clicked.connect(lambda: os.startfile('密码导出.txt'))  # 打开导出的密码文件

        # 设置页的按钮
        self.ui.checkBox_mode_extract.stateChanged.connect(self.update_setting)
        self.ui.checkBox_mode_test.stateChanged.connect(self.update_setting)
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
                    walk_files = function_static.get_files_list(path)
                    file_list.update(walk_files)
        file_list = list(file_list)  # 转为列表，方便后续使用
        self.start_thread(file_list)

    def start_thread(self, file_list: list):
        """调用子线程进行后续操作"""
        function_static.print_function_info()
        output_dir = self.ui.lineedit_output_dir.text()
        # 先检查是否存在遗留的临时文件夹
        if function_static.check_temp_folder(file_list) and function_static.check_temp_folder(output_dir):
            # 再检查文件列表是否为空
            if file_list:
                # 对传入的文件列表进行处理，利用正则检查文件名是否符合分卷命名规则，将符合项转换为{第一个包:(全部分卷)..}的格式
                volume_archive_dict = function_static.get_volume_archive_dict(file_list)
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
                        if function_static.check_filetype(file):
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

        self.set_widget_enable()  # 启用被禁用的ui


    def set_widget_enable(self, mode=True):
        """在解压开始前，设置相关控件的enable属性，防止解压过程中修改选项导致报错"""
        function_static.print_function_info()
        if mode:
            # 主页面
            self.ui.label_icon.setEnabled(True)
            # 密码页
            self.ui.button_update_password.setEnabled(True)
            # 设置页
            self.ui.scrollAreaWidgetContents.setEnabled(True)
        else:
            # 主页面
            self.ui.label_icon.setEnabled(False)
            # 密码页
            self.ui.button_update_password.setEnabled(False)
            # 设置页
            self.ui.scrollAreaWidgetContents.setEnabled(False)

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

    def update_ui(self, code:str, data:list=None):
        """根据传入的list，分不同情况更新ui
        type_list格式：['更新类型', '相关数据']"""
        function_static.print_function_info()
        function_static.print_function_info()
        if code == '1-1':  # 初始状态
            self.ui.label_icon.setPixmap(icon_origin)
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮
        elif code == '2-1':  # 没有需要解压的文件
            self.ui.label_icon.setPixmap(icon_finish)
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('没有需要解压的文件')
        elif code == '2-2':  # 存在遗留临时文件夹
            self.ui.label_icon.setPixmap(icon_error)
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('存在遗留临时文件夹')
        elif code == '1-2':  # 启动子线程
            self.ui.button_stop.setVisible(True)  # 显示停止按钮
            if self.ui.checkBox_mode_test.isChecked():  # 按选项设置不同图标
                self.ui.label_icon.setPixmap(icon_test)
            else:
                self.ui.label_icon.setPixmap(icon_extract)
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
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) +data[0] + " ■未知错误"
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
            self.ui.label_icon.setPixmap(icon_finish)
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('全部完成')
            self.ui.label_schedule_finish.setText(data[0])
            self.set_widget_enable(mode=True)
            self.ui.stackedWidget_schedule.setCurrentIndex(0)
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮
        elif code == '1-4':  # 中止任务
            self.ui.label_schedule_file.setText('等待当前文件完成执行')
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮

    def load_config(self):
        """加载配置文件，并更新UI"""
        function_static.print_function_info()
        # 读取数据
        config_dict = function_config.read_setting()
        code_mode = config_dict['mode']
        code_un_nest_dir = config_dict['un_nest_dir']
        code_un_nest_archive = config_dict['un_nest_archive']
        code_delete_archive = config_dict['delete_archive']
        code_check_filetype = config_dict['check_filetype']
        code_exclude_rule = config_dict['exclude_rule']
        code_output_dir = config_dict['output_dir']
        # 更新UI
        if code_mode == 'extract':
            self.ui.checkBox_mode_extract.setChecked(True)
        elif code_mode == 'test':
            self.ui.checkBox_mode_test.setChecked(True)
        self.ui.checkBox_un_nest_dir.setChecked(code_un_nest_dir)
        self.ui.checkBox_un_nest_archive.setChecked(code_un_nest_archive)
        self.ui.checkBox_delete_archive.setChecked(code_delete_archive)
        self.ui.checkBox_check_filetype.setChecked(code_check_filetype)
        self.ui.lineedit_exclude_rule.setText(code_exclude_rule)
        self.ui.lineedit_output_dir.setText(code_output_dir)


    def update_password(self):
        """更新密码"""
        function_static.print_function_info()
        function_config.backup_config()  # 更新前备份配置文件

        add_pw = [n for n in self.ui.text_password.toPlainText().split('\n') if n.strip()]
        add_pw_strip = [n.strip() for n in add_pw]
        pw_list = list(set(add_pw+add_pw_strip))  # 转为集合去重
        function_config.update_pw(pw_list)

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

        config_dict = {'mode': mode,
                        'un_nest_dir': un_nest_dir,
                        'un_nest_archive': un_nest_archive,
                        'delete_archive': delete_archive,
                        'check_filetype': check_filetype,
                        'exclude_rule': exclude_rule,
                        'output_dir': output_dir}

        function_config.update_setting(config_dict)  # 调用


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
                self.ui.label_icon.setPixmap(icon_origin)
            else:
                self.ui.lineedit_output_dir.setStyleSheet('')
                self.ui.label_icon.setPixmap(icon_origin_with_output)
        else:
            self.ui.lineedit_output_dir.setStyleSheet('')
            self.ui.label_icon.setPixmap(icon_origin)

    def stop_qthread(self):
        """中止解压子线程"""
        function_static.print_function_info()
        reply = QMessageBox.question(self, '确认对话框',
                                     f'是否中止当前任务\n（不终止当前正在执行的文件，\n仅中止之后的任务）',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.update_ui(['子线程-中止'])
            self.qthread.signal_stop.emit()


def main():
    app = QApplication()
    app.setStyle('Fusion')
    show_ui = OnlyUnzip()
    show_ui.setWindowIcon(QIcon(icon_main))
    show_ui.setFixedSize(262, 232)
    show_ui.show()
    app.exec_()


if __name__ == "__main__":
    main()
