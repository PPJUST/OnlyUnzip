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
import os
import configparser
import re
import subprocess
import time
import natsort
import winshell
import shutil
import magic
import sys
from tqdm import tqdm
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
        self.ui.label_icon.dropSignal.connect(self.accept_path)  # 拖入文件
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


    def accept_path(self, paths):
        files = []
        folders = []
        for i in paths:
            if os.path.isfile(i):
                files.append(i)
            else:
                folders.append(i)

    def unzip_main_logic(self):
        """解压程序主逻辑"""

    def class_multi_volume(self, files):
        """区分普通压缩包与分卷压缩包（会自动获取文件夹下的所有相关分卷包）"""
        # 提取文件所在文件夹下的所有文件，用于补充分卷压缩包
        the_folder = os.path.split(files[0])[0]
        # 利用正则匹配分卷压缩包
        filenames = [os.path.split(x)[1] for x in files]
        ordinary_zip = [x for x in filenames]  # 复制
        re_rar = r"^(.+)\.part\d+\.rar$"  # 4种类压缩文件的命名规则
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip_top = r"^(.+)\.zip$"
        re_zip_other = r"^(.+)\.z\d+$"
        multi_volume_dict = {}  # 分卷文件字典（键值对为 第一个分卷：文件夹下的全部分卷（不管有没有在变量files中）
        for i in filenames:
            if re.match(re_7z, i):  # 匹配7z正则
                filename = re.match(re_7z, i).group(1)  # 提取文件名
                first_multi_volume = filename + r'.7z.001'  # 设置第一个分卷压缩包名，作为键名
                if first_multi_volume not in multi_volume_dict:  # 如果文件名不在字典内，则添加一个空键值对
                    multi_volume_dict[first_multi_volume] = set()  # 用集合添加（目的是为了后面的zip分卷，其实用列表更方便）
                multi_volume_dict[first_multi_volume].add(i)  # 添加键值对（示例.7z.001：示例.7z.001，示例.7z.002）
                ordinary_zip.remove(i)  # 将新列表中的分卷压缩包剔除
            elif re.match(re_rar, i):
                filename = re.match(re_rar, i).group(1)
                first_multi_volume = filename + r'.part1.rar'
                if first_multi_volume not in multi_volume_dict:
                    multi_volume_dict[first_multi_volume] = set()
                multi_volume_dict[first_multi_volume].add(i)
                ordinary_zip.remove(i)
            elif re.match(re_zip_other, i) or re.match(re_zip_top, i):  # 只要是zip后缀的，都视为分卷压缩包，因为解压的都是.zip后缀
                if re.match(re_zip_other, i):
                    filename = re.match(re_zip_other, i).group(1)
                else:
                    filename = re.match(re_zip_top, i).group(1)
                first_multi_volume = filename + r'.zip'
                if first_multi_volume not in multi_volume_dict:
                    multi_volume_dict[first_multi_volume] = set()
                multi_volume_dict[first_multi_volume].add(i)
                multi_volume_dict[first_multi_volume].add(first_multi_volume)  # zip分卷的特性，第一个分卷包名称是.zip后缀
                ordinary_zip.remove(i)
                if first_multi_volume in ordinary_zip:  # zip分卷特性，如果是分卷删除第一个.zip后缀的文件名，所以需要删除多出来的一个zip文件
                    ordinary_zip.remove(first_multi_volume)
        self.find_all_multi_volume_in_folder(the_folder, ordinary_zip, multi_volume_dict)
        # return the_folder, ordinary_zip, multi_volume_dict  # 返回普通压缩包、分卷压缩包

    def find_all_multi_volume_in_folder(self, the_folder, ordinary_zip, multi_volume_dict):
        """扩展文件夹下所有的在字典中的分卷压缩包，应对拖入文件少的问题"""
        all_filenames = os.listdir(the_folder)


    def is_zip_file(self, file):
        """检查文件是否是压缩包"""
        zip_type = ['application/x-rar', 'application/x-gzip', 'application/x-tar', 'application/zip',
                    'application/x-lzh-compressed', 'application/x-7z-compressed', 'application/x-xz',
                    'application/octet-stream', 'application/x-dosexec']
        file_type = magic.from_buffer(open(file, 'rb').read(2048), mime=True)
        if file_type in zip_type:
            return True
        else:
            return False

    def get_file_size(self, file):
        """获取文件大小"""
        size = os.path.getsize(file)
        return size

    def get_folder_size(self, folder):
        """获取文件夹大小"""
        size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for i in filenames:
                filepath = os.path.join(dirpath, i)
                size += os.path.getsize(filepath)
        return size


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
