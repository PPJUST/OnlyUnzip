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

import general_method
import update_config
from qthread_unzip import UnzipQthread
from ui import Ui_MainWindow


class OnlyUnzip(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """
        初始化设置
        """
        self.check_config()  # 检查配置文件
        update_config.update_config_version()  # 更新配置文件
        self.load_setting()  # 加载设置文件
        self.update_ui(['初始状态'])  # 设置初始图标
        self.check_unzip_folder()
        self.ui.listWidget_history.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置历史记录控件的右键菜单属性

        self.ui.stackedWidget_main.setCurrentIndex(0)  # 将主页面设为第1页
        self.ui.stackedWidget_schedule.setCurrentIndex(0)  # 将信息页设为第1页
        self.change_page(self.ui.buttonGroup.id(self.ui.buttonGroup.buttons()[0]))  # 设置第一个按钮的颜色

        """
        连接信号与槽函数
        """
        # 设置标签页的切换
        self.ui.buttonGroup.buttonClicked[int].connect(self.change_page)

        # 主页面
        self.ui.label_icon.dropSignal.connect(self.drop_files)
        self.ui.button_stop.clicked.connect(self.stop_qthread)

        # 密码页的按钮
        self.ui.button_update_password.clicked.connect(self.update_password)  # 更新密码
        self.ui.button_read_clipboard.clicked.connect(self.read_clipboard)  # 读取剪切板
        self.ui.button_export_password.clicked.connect(lambda: self.export_password(with_number=False))  # 导出密码
        self.ui.button_export_password_with_number.clicked.connect(
            lambda: self.export_password(with_number=True))  # 导出含次数的密码
        self.ui.button_export_password.clicked.connect(lambda: self.ui.button_open_password.setEnabled(True))
        self.ui.button_export_password_with_number.clicked.connect(
            lambda: self.ui.button_open_password.setEnabled(True))
        self.ui.button_open_password.clicked.connect(lambda: os.startfile('password export.txt'))  # 打开导出的密码文件

        # 设置页的按钮
        self.ui.checkBox_model_unzip.stateChanged.connect(self.update_setting)
        self.ui.checkBox_model_test.stateChanged.connect(self.update_setting)
        self.ui.checkBox_nested_folders.stateChanged.connect(self.update_setting)
        self.ui.checkBox_nested_zip.stateChanged.connect(self.update_setting)
        self.ui.checkBox_delect_zip.stateChanged.connect(self.update_setting)
        self.ui.checkBox_check_zip.stateChanged.connect(self.update_setting)
        self.ui.lineedit_unzip_skip_suffix.textChanged.connect(self.update_setting)
        self.ui.lineedit_unzip_to_folder.textChanged.connect(self.update_setting)
        self.ui.button_ask_folder.clicked.connect(self.ask_unzip_folder)

        # 历史记录页的操作
        self.ui.listWidget_history.customContextMenuRequested.connect(self.show_menu_copy)  # 右键菜单

    def drop_files(self, path_list: list):
        """接收自定义label控件的drop信号，取得所有拖入路径的列表list，如果是文件夹则提取其中所有文件路径
        获取所有文件路径列表list后，调用解压函数"""
        general_method.print_current_function()
        filepath_list = set()  # 使用集合存储，方便去重
        for path in path_list:
            path = os.path.normpath(path)  # 格式化路径，防止后续出错
            if os.path.exists(path):
                if os.path.isfile(path):
                    filepath_list.add(path)
                else:
                    files_in_folder = general_method.get_filelist(path)
                    filepath_list.update(files_in_folder)
        filepath_list = list(filepath_list)  # 转为列表，方便后续使用
        self.start_unzip(filepath_list)

    def start_unzip(self, filepath_list: list):
        """传入文件路径list后，调用子线程进行解压或测试操作"""
        general_method.print_current_function()
        if self.check_temp_folder(filepath_list):  # 如果不存在临时文件夹
            if filepath_list:  # 拖入文件列表不为空
                # 将传入的文件列表list按正则区分为分卷压缩包与非分卷压缩包，格式为dict
                split_archive_dict = general_method.get_split_archive_dict(filepath_list)  # 提取文件列表中符合分卷压缩包规则的dict
                all_split_archive_files = set()  # 存放识别出的分卷字典中的所有文件
                for value in split_archive_dict.values():
                    all_split_archive_files.update(value)

                other_files_dict = {}  # 存放分卷压缩包以外的文件（不论是否为压缩包）
                for file in filepath_list:
                    if file not in all_split_archive_files:
                        other_files_dict[file] = set()  # 键值对的值设置为集合，与分卷dict保持一致
                        other_files_dict[file].add(file)

                # 根据是否勾选“仅解压压缩包”，分两种方法处理两个dict
                unzip_files_dict = {}
                if self.ui.checkBox_check_zip.isChecked():
                    for file in split_archive_dict:
                        if general_method.is_archive(file):
                            unzip_files_dict[file] = split_archive_dict[file]
                    for file in other_files_dict:
                        if general_method.is_archive(file):
                            unzip_files_dict[file] = other_files_dict[file]
                else:
                    unzip_files_dict.update(split_archive_dict)
                    unzip_files_dict.update(other_files_dict)

                # 将最终得到的需解压文件dict传递给子线程
                if unzip_files_dict:
                    self.set_widget_enable(mode=False)
                    # 设置子线程
                    self.qthread_unzip = UnzipQthread(unzip_files_dict)
                    self.qthread_unzip.signal_update_ui.connect(self.update_ui)
                    self.qthread_unzip.signal_nested_zip.connect(lambda x: self.drop_files(x))
                    self.qthread_unzip.start()
                else:  # 没有需解压的文件，则提示
                    self.update_ui(['没有需要解压的文件'])
                    self.set_widget_enable()
            else:  # 没有需解压的文件，则提示
                self.update_ui(['没有需要解压的文件'])
                self.set_widget_enable()
        else:  # 如果有遗留的临时文件夹
            self.update_ui(['存在遗留临时文件夹'])
            self.set_widget_enable()

    def check_temp_folder(self, filepath_list: list) -> bool:
        """传入文件路径列表list，检查对应路径的同级文件夹是否有临时文件夹（前一次解压未正常删除的）
        如果存在临时文件夹并且其中有相应文件/文件夹，则返回False，终止下一步操作"""
        general_method.print_current_function()

        all_temporary_folder = set()  # 所有可能存在的临时文件夹路径（添加后缀自动生成，非真实路径）

        # 如果指定了解压路径文件夹
        unzip_to_folder = self.ui.lineedit_unzip_to_folder.text()
        if unzip_to_folder and os.path.exists(unzip_to_folder) and os.path.isdir(unzip_to_folder):  # 如果解压文件夹符合规则
            all_temporary_folder.add(os.path.normpath(os.path.join(unzip_to_folder, 'UnzipTempFolder')))
        else:
            for path in filepath_list:
                temporary_folder = os.path.normpath(os.path.join(os.path.split(path)[0], 'UnzipTempFolder'))
                all_temporary_folder.add(temporary_folder)

        for folder in all_temporary_folder:
            if os.path.exists(folder) and os.listdir(folder):
                return False
        return True

    def set_widget_enable(self, mode=True):
        """在解压开始前，设置相关控件的enable属性，防止解压过程中修改选项导致报错"""
        general_method.print_current_function()
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

    def show_menu_copy(self, pos):
        """历史记录页中的右键菜单，用于复制密码"""
        general_method.print_current_function()

        def menu_copy_pw():
            item = self.ui.listWidget_history.currentItem()
            text = item.text().split(' | ', maxsplit=1)[1]  # 根据文本筛选出解压密码
            QApplication.clipboard().setText(text)

        selected_item = self.ui.listWidget_history.currentItem()
        if selected_item and selected_item.data(Qt.UserRole) == '测试成功':  # 只有正常解压的项目文本才可以右键
            menu = QMenu()
            menu.adjustSize()
            copy_action = QAction('复制解压密码', menu)
            copy_action.triggered.connect(menu_copy_pw)
            menu.addAction(copy_action)
            menu.exec_(self.ui.listWidget_history.mapToGlobal(pos))

    def update_ui(self, type_list: list):
        """根据传入的list，分不同情况更新ui
        type_list格式：['更新类型', '相关数据']"""
        if type_list[0] == '初始状态':
            self.ui.label_icon.setPixmap('./icon/初始状态.png')
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮
        elif type_list[0] == '没有需要解压的文件':
            self.ui.label_icon.setPixmap('./icon/全部完成.png')
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('没有需要解压的文件')
        elif type_list[0] == '存在遗留临时文件夹':
            self.ui.label_icon.setPixmap('./icon/错误.png')
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('存在遗留临时文件夹')
        elif type_list[0] == '子线程-开始':
            self.ui.button_stop.setVisible(True)  # 显示停止按钮
            if self.ui.checkBox_model_test.isChecked():  # 按选项设置不同图标
                self.ui.label_icon.setPixmap('./icon/测试密码.png')
            else:
                self.ui.label_icon.setPixmap('./icon/正在解压.png')
        elif type_list[0] == '子线程-当前文件':
            self.ui.label_current_file.setText(type_list[1])
        elif type_list[0] == '子线程-总进度':
            self.ui.label_schedule_file.setText(type_list[1])
        elif type_list[0] == '子线程-测试密码进度':
            self.ui.label_schedule_test.setText(type_list[1])
            self.ui.stackedWidget_schedule.setCurrentIndex(1)
        elif type_list[0] == '子线程-记录-密码错误':
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + type_list[1] + " ■密码错误"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(254, 67, 101))
            self.ui.listWidget_history.addItem(item)
        elif type_list[0] == '子线程-记录-丢失分卷':
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + type_list[1] + " ■缺少分卷"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(254, 67, 101))
            self.ui.listWidget_history.addItem(item)
        elif type_list[0] == '子线程-记录-未知错误':
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + type_list[1] + " ■未知错误"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(254, 67, 101))
            self.ui.listWidget_history.addItem(item)
        elif type_list[0] == '子线程-记录-不是压缩文件':
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + type_list[1] + " ■不是压缩文件，已跳过"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(255, 182, 193))
            self.ui.listWidget_history.addItem(item)
        elif type_list[0] == '子线程-记录-文件被占用':
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + type_list[1] + " ■文件被占用，已跳过"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(255, 182, 193))
            self.ui.listWidget_history.addItem(item)
        elif type_list[0] == '子线程-记录-磁盘空间不足':
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + type_list[1] + " ■磁盘空间不足，已跳过"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(255, 182, 193))
            self.ui.listWidget_history.addItem(item)
        elif type_list[0] == '子线程-记录-成功':
            item_text = time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + type_list[1] + f" | {type_list[2]}"
            item = QListWidgetItem(item_text)
            item.setTextColor(QColor(92, 167, 186))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # 启用UserRole
            item.setData(Qt.UserRole, '测试成功')  # 设置 UserRole 的值
            self.ui.listWidget_history.addItem(item)
        elif type_list[0] == '子线程-解压进度':
            self.ui.progressBar_unzip.setValue(type_list[1])
            self.ui.stackedWidget_schedule.setCurrentIndex(2)
        elif type_list[0] == '子线程-结束':
            self.ui.label_icon.setPixmap('./icon/全部完成.png')
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule_file.setText('全部完成')
            self.ui.label_schedule_finish.setText(type_list[1])
            self.set_widget_enable(mode=True)
            self.ui.stackedWidget_schedule.setCurrentIndex(0)
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮
        elif type_list[0] == '子线程-中止':
            self.ui.label_schedule_file.setText('等待当前文件完成执行')
            self.ui.button_stop.setVisible(False)  # 隐藏停止按钮

    def load_setting(self):
        """加载配置文件，并更新UI"""
        general_method.print_current_function()
        config = configparser.ConfigParser()
        config.read("config.ini", encoding='utf-8')
        # 读取对应数据
        code_model = config.get('DEFAULT', 'model')
        code_nested_folders = config.get('DEFAULT', 'nested_folders') == 'True'
        code_nested_zip = config.get('DEFAULT', 'nested_zip') == 'True'
        code_delete_zip = config.get('DEFAULT', 'delete_zip') == 'True'
        code_check_zip = config.get('DEFAULT', 'check_zip') == 'True'
        code_skip_suffix = config.get('DEFAULT', 'skip_suffix')
        code_unzip_to_folder = config.get('DEFAULT', 'unzip_to_folder')
        # 更新UI
        if code_model == 'unzip':
            self.ui.checkBox_model_unzip.setChecked(True)
        elif code_model == 'test':
            self.ui.checkBox_model_test.setChecked(True)
        self.ui.checkBox_nested_folders.setChecked(code_nested_folders)
        self.ui.checkBox_nested_zip.setChecked(code_nested_zip)
        self.ui.checkBox_delect_zip.setChecked(code_delete_zip)
        self.ui.checkBox_check_zip.setChecked(code_check_zip)
        self.ui.lineedit_unzip_skip_suffix.setText(code_skip_suffix)
        self.ui.lineedit_unzip_to_folder.setText(code_unzip_to_folder)

    @staticmethod
    def check_config():
        """检查初始配置文件，若本地不存在则新建"""
        general_method.print_current_function()
        if not os.path.exists('config.ini'):
            with open('config.ini', 'w', encoding='utf-8') as cw:
                the_setting = """[DEFAULT]
information = 
number = 0
model = unzip
nested_folders = True
nested_zip = False
delete_zip = True
check_zip = True
multithreading = 
skip_suffix = 
unzip_to_folder = 
"""
                cw.write(the_setting)
        if not os.path.exists('backup_config'):
            os.mkdir('backup_config')

    def update_password(self):
        """更新密码"""
        general_method.print_current_function()
        self.backup_config()  # 备份一次配置文件
        add_pw = [n for n in self.ui.text_password.toPlainText().split('\n') if n.strip()]
        add_pw_strip = [n.strip() for n in self.ui.text_password.toPlainText().split('\n') if n.strip()]
        add_pw = set(add_pw)  # 转为集合去重
        add_pw_strip = set(add_pw_strip)

        config = configparser.ConfigParser()
        config.read("config.ini", encoding='utf-8')
        old_passwords = config.sections()  # 获取section
        for pw in add_pw:
            if pw not in old_passwords:
                config.add_section(pw)
                config.set(pw, 'number', '0')
                old_passwords.append(pw)
        for pw in add_pw_strip:
            if pw not in old_passwords:
                config.add_section(pw)
                config.set(pw, 'number', '0')
                old_passwords.append(pw)
        config.write(open('config.ini', 'w', encoding='utf-8'))

        # 重置密码框
        self.ui.text_password.setPlainText('')

    def read_clipboard(self):
        """读取剪切板"""
        general_method.print_current_function()
        clipboard = QApplication.clipboard()  # 创建一个剪贴板对象
        clipboard_text = clipboard.text()  # 读取剪贴板的文本
        self.ui.text_password.setPlainText(clipboard_text)

    @staticmethod
    def backup_config():
        """在更新密码前备份配置文件"""
        general_method.print_current_function()
        new_name = f'config_{time.strftime("%Y_%m_%d_%H_%M_%S ", time.localtime())}.ini'
        shutil.copyfile('config.ini', f'backup_config/{new_name}')

    @staticmethod
    def export_password(with_number: bool = False):
        """导出当前密码到本地，按传参判断是否添加使用次数"""
        general_method.print_current_function()
        sort_passwords, sort_passwords_with_number = OnlyUnzip.get_sorted_pwlist()
        # 导出密码
        with open("password export.txt", "w", encoding="utf-8") as pw:
            if with_number:
                pw.write("\n".join(sort_passwords_with_number))
            else:
                pw.write("\n".join(sort_passwords))

    @staticmethod
    def get_sorted_pwlist() -> Tuple[list, list]:
        """读取配置文件，返回2个密码列表list"""
        general_method.print_current_function()
        config = configparser.ConfigParser()
        config.read("config.ini", encoding='utf-8')
        # 按密码的使用次数排序
        all_password = config.sections()
        sort_passwords_with_number = []  # 设置空列表，方便后续排序操作
        sort_passwords = []  # 最终排序结果
        for password in all_password:  # 遍历全部密码
            sort_passwords_with_number.append(config.get(password, 'number') + ' - ' + password)  # 使用次数 - 密码
        sort_passwords_with_number = natsort.natsorted(sort_passwords_with_number)[::-1]  # 按数字大小降序排序
        for i in sort_passwords_with_number:
            sort_passwords.append(re.search(r' - (.+)', i).group(1))  # 正则提取 - 后的section

        return sort_passwords, sort_passwords_with_number

    def update_setting(self):
        """点击按钮后更新设置项（选项不多，重写整个配置文件）"""
        general_method.print_current_function()
        config = configparser.ConfigParser()
        config.read("config.ini", encoding='utf-8')

        if self.ui.checkBox_model_unzip.isChecked():
            config.set('DEFAULT', 'model', 'unzip')
        else:
            config.set('DEFAULT', 'model', 'test')
        config.set('DEFAULT', 'nested_folders', str(self.ui.checkBox_nested_folders.isChecked()))
        config.set('DEFAULT', 'nested_zip', str(self.ui.checkBox_nested_zip.isChecked()))
        config.set('DEFAULT', 'delete_zip', str(self.ui.checkBox_delect_zip.isChecked()))
        config.set('DEFAULT', 'check_zip', str(self.ui.checkBox_check_zip.isChecked()))

        suffix_text = self.ui.lineedit_unzip_skip_suffix.text()
        support_delimiters = ",|，| |;|；"
        skip_suffix = set([x for x in re.split(support_delimiters, suffix_text) if x])  # 提取分隔后的列表，去重去空值
        config.set('DEFAULT', 'skip_suffix', ' '.join(skip_suffix))

        config.set('DEFAULT', 'unzip_to_folder', str(self.ui.lineedit_unzip_to_folder.text()))

        config.write(open('config.ini', 'w', encoding='utf-8'))
        self.check_unzip_folder()  # 检查解压路径文件夹

    def change_page(self, button_id):
        """切换标签页，并高亮被点击的标签页按钮"""
        general_method.print_current_function()
        # 高亮按钮
        original_style = self.ui.button_update_password.styleSheet()  # 按钮的原始样式
        clicked_style = f"{original_style} background-color: rgb(255, 228, 181);"  # 被点击后的样式
        for button in self.ui.buttonGroup.buttons():  # 重置按钮组中所有按钮的样式
            button.setStyleSheet(original_style)
        clicked_button = self.ui.buttonGroup.button(button_id)
        clicked_button.setStyleSheet(clicked_style)
        # 切换标签页
        page = self.ui.buttonGroup.buttons().index(self.ui.buttonGroup.button(button_id))
        self.ui.stackedWidget_main.setCurrentIndex(page)

    def ask_unzip_folder(self):
        """弹出对话框选择文件夹，用于解压到该文件夹下"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择指定解压路径文件夹")
        if folder_path:
            self.ui.lineedit_unzip_to_folder.setText(os.path.normpath(folder_path))

    def check_unzip_folder(self):
        """检查指定的解压路径文件夹是否存在，如果不存在则提示，并返回bool值"""
        unzip_to_folder = self.ui.lineedit_unzip_to_folder.text()
        if unzip_to_folder:
            if not os.path.exists(unzip_to_folder) or os.path.isfile(unzip_to_folder):
                self.ui.lineedit_unzip_to_folder.setStyleSheet("border: 1px solid red;")
                self.ui.label_icon.setPixmap('./icon/初始状态.png')
            else:
                self.ui.lineedit_unzip_to_folder.setStyleSheet("")
                self.ui.label_icon.setPixmap('./icon/初始状态_指定文件夹.png')
        else:
            self.ui.lineedit_unzip_to_folder.setStyleSheet("")
            self.ui.label_icon.setPixmap('./icon/初始状态.png')

    def stop_qthread(self):
        """中止解压子线程"""
        reply = QMessageBox.question(self, '确认对话框',
                                     f'是否中止当前任务\n（不终止当前正在执行的文件，\n仅中止之后的任务）',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.update_ui(['子线程-中止'])
            self.qthread_unzip.signal_stop.emit()


def main():
    app = QApplication()
    app.setStyle('Fusion')
    show_ui = OnlyUnzip()
    show_ui.setWindowIcon(QIcon('./icon/程序图标.ico'))
    show_ui.setFixedSize(262, 232)
    show_ui.show()
    app.exec_()


if __name__ == "__main__":
    main()
