from PySide2.QtWidgets import QApplication, QLabel, QMainWindow
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Signal, QCoreApplication
from PySide2.QtUiTools import QUiLoader
import subprocess
import configparser
import os
import re
import random
import natsort
import shutil
# import winshell
import sys
from ui_v1 import Ui_MainWindow


class OnlyUnzip(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化
        self.start_with_load_setting()
        self.ui.label_icon.setPixmap('./icon/初始状态.png')

        # 设置槽函数
        self.ui.label_icon.dropSignal.connect(self.accept_drop_path)  # 拖入文件
        self.ui.button_page_main.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(0))  # 切换页面
        self.ui.button_page_password.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(1))  # 切换页面
        self.ui.button_page_setting.clicked.connect(lambda :self.ui.stackedWidget.setCurrentIndex(2))  # 切换页面
        self.ui.button_update_password.clicked.connect(self.update_password)
        self.ui.button_export_password.clicked.connect(self.export_password)
        self.ui.button_export_password_with_number.clicked.connect(self.export_password_with_number)

        self.ui.checkBox_model_unzip.stateChanged.connect(self.change_setting)
        self.ui.checkBox_model_test.stateChanged.connect(self.change_setting)
        self.ui.checkBox_nested_folders.stateChanged.connect(self.change_setting)
        self.ui.checkBox_nested_zip.stateChanged.connect(self.change_setting)
        self.ui.checkBox_delect_zip.stateChanged.connect(self.change_setting)
        self.ui.checkBox_check_zip.stateChanged.connect(self.change_setting)


    def accept_drop_path(self, paths):
        print(paths)


    def start_with_load_setting(self):
        """启动时更新界面"""
        read_config = configparser.ConfigParser()  # 注意大小写
        read_config.read("config.ini", encoding='utf-8')  # 配置文件的路径
        # 更新密码框
        all_password = read_config.sections()  # 获取section
        self.ui.text_password.setPlainText('\n'.join(all_password))
        # 更新选项
        code_model = read_config.get('DEFAULT', 'model')
        code_nested_folders = read_config.get('DEFAULT', 'nested_folders') == 'True'
        code_nested_zip = read_config.get('DEFAULT', 'nested_zip') == 'True'
        code_delete_zip = read_config.get('DEFAULT', 'delete_zip') == 'True'
        code_check_zip = read_config.get('DEFAULT', 'check_zip') == 'True'
        if code_model == 'unzip':
            self.ui.checkBox_model_unzip.setChecked(True)
        elif code_model == 'test':
            self.ui.checkBox_model_test.setChecked(True)
        self.ui.checkBox_nested_folders.setChecked(code_nested_folders)
        self.ui.checkBox_nested_zip.setChecked(code_nested_zip)
        self.ui.checkBox_delect_zip.setChecked(code_delete_zip)
        self.ui.checkBox_check_zip.setChecked(code_check_zip)


    def update_password(self):
        """更新密码"""
        new_all_password = [x for x in self.ui.text_password.toPlainText().split('\n') if x.strip()]
        read_config = configparser.ConfigParser()  # 注意大小写
        read_config.read("config.ini", encoding='utf-8')  # 配置文件的路径
        old_all_password = read_config.sections()  # 获取section
        for i in new_all_password:
            if i not in old_all_password:
                read_config.add_section(i)
                read_config.set(i, 'number', '0')
                old_all_password.append(i)
        read_config.write(open('config.ini', 'w', encoding='utf-8'))  # 写入

    def export_password(self):
        """导出密码"""
        sort_passwords, passwords_with_number = self.read_password_return_list()
        with open("password export.txt", "w", encoding="utf-8") as pw:
            pw.write("\n".join(sort_passwords))

    def export_password_with_number(self):
        """导出带次数的密码"""
        sort_passwords, passwords_with_number = self.read_password_return_list()
        with open("password export.txt", "w", encoding="utf-8") as pw:
            pw.write("\n".join(passwords_with_number))

    def read_password_return_list(self):
        """读取配置文件，返回两种密码列表"""
        read_config = configparser.ConfigParser()  # 注意大小写
        read_config.read("config.ini", encoding='utf-8')  # 配置文件的路径
        # 按密码的使用次数排序
        all_password = read_config.sections()  # 获取section
        passwords_with_number = []  # 设置空列表，方便后续排序操作
        sort_passwords = []  # 最终排序结果
        for password in all_password:  # 遍历全部密码
            passwords_with_number.append(
                read_config.get(password, 'number') + ' - ' + password)  # value - section，使用次数 - 密码
        passwords_with_number = natsort.natsorted(passwords_with_number)[::-1]  # 按数字大小降序排序
        for i in passwords_with_number:
            print(f'测试 {i}')
            sort_passwords.append(re.search(r' - (.+)', i).group(1))  # 正则提取 - 后的section

        return sort_passwords, passwords_with_number

    def change_setting(self):
        """修改设置项（选项不多，选择全部重写ini文件"""
        read_config = configparser.ConfigParser()  # 注意大小写
        read_config.read("config.ini", encoding='utf-8')  # 配置文件的路径
        if self.ui.checkBox_model_unzip.isChecked():
            read_config.set('DEFAULT', 'model', 'unzip')
        else:
            read_config.set('DEFAULT', 'model', 'test')
        read_config.set('DEFAULT', 'nested_folders', str(self.ui.checkBox_nested_folders.isChecked()))
        read_config.set('DEFAULT', 'nested_zip', str(self.ui.checkBox_nested_zip.isChecked()))
        read_config.set('DEFAULT', 'delete_zip', str(self.ui.checkBox_delect_zip.isChecked()))
        read_config.set('DEFAULT', 'check_zip', str(self.ui.checkBox_check_zip.isChecked()))
        read_config.write(open('config.ini', 'w', encoding='utf-8'))  # 写入








app = QApplication([])
show_ui = OnlyUnzip()
show_ui.show()
app.exec_()
