import configparser
import os
import re
import shutil
import subprocess
import time

import magic
import natsort
import qdarktheme
# import winshell
import send2trash  # win7不能使用winshell，用send2trash替代
from PySide2.QtCore import Signal, QThread
from PySide2.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PySide2.QtGui import QColor

from ui import Ui_MainWindow


class unzip_main(QThread):
    signal_ui_update = Signal(list)  # 自定义信号

    def __init__(self, unzip_files_dict, parent=None):
        super(unzip_main, self).__init__(parent)
        self.unzip_files_dict = unzip_files_dict
        self.Main_OnlyUnzip = OnlyUnzip()

    def run(self):
        print(f'调用子线程 输入为 {self.unzip_files_dict}')
        total_files_number = len(self.unzip_files_dict)  # 需要解压的文件总数（分卷计数1）
        current_number = 0
        wrong_password_file_number = 0
        damaged_file_number = 0
        success_number = 0

        for first_file in self.unzip_files_dict:
            print(f'子线程处理的第一个文件 {first_file}')
            the_folder = os.path.split(first_file)[0]
            current_number += 1
            current_filename = self.Main_OnlyUnzip.get_zip_name(first_file)  # 提取当前处理的文件名
            print(f'子线程处理的第一个文件-提取文件名 {current_filename}')
            self.signal_ui_update.emit(['当前文件', current_filename])
            self.signal_ui_update.emit(['进度', f'{current_number}/{total_files_number} 测试密码中'])
            self.signal_ui_update.emit(['图标', None])
            file_list = self.unzip_files_dict[first_file]
            the_right_password = self.test_password(first_file)
            if the_right_password == '':
                wrong_password_file_number += 1
                self.signal_ui_update.emit(['历史记录-失败', f'{os.path.split(first_file)[1]} | 解压失败'])
            else:
                self.Main_OnlyUnzip.right_password_number_add_one(the_right_password)  # 成功解压则密码使用次数+1
                self.Main_OnlyUnzip.save_unzip_history(first_file, the_right_password)  # 保存解压历史
                self.signal_ui_update.emit(['进度', f'{current_number}/{total_files_number} | {the_right_password}'])
                self.signal_ui_update.emit(['历史记录-成功', f'{os.path.split(first_file)[1]} | {the_right_password}'])
                if self.Main_OnlyUnzip.ui.checkBox_model_unzip.isChecked():  # 如果解压选项被选中，则执行解压操作
                    unzip_result = self.start_unzip(the_folder, first_file, file_list, the_right_password)
                    if unzip_result == '文件损坏':
                        damaged_file_number += 1
                    if unzip_result == '解压成功':
                        success_number += 1
                if current_number == total_files_number:  # 完成全部文件处理后，删除临时文件夹
                    temporary_folder = os.path.join(the_folder, "UnzipTempFolder")  # 临时文件夹
                    if os.path.exists(temporary_folder):  # 处理遗留的临时文件夹
                        if self.Main_OnlyUnzip.get_folder_size(temporary_folder) == 0:
                            # winshell.delete_file(temporary_folder, no_confirm=True)
                            temporary_folder = temporary_folder.replace('/', '\\')
                            send2trash.send2trash(temporary_folder)
        # 全部完成后发送信号
        self.signal_ui_update.emit(['图标', './icon/全部完成.png'])
        self.signal_ui_update.emit(['当前文件', '————————————'])
        self.signal_ui_update.emit(['进度', f'成功：{success_number}，失败{wrong_password_file_number}，损坏：{damaged_file_number}'])

    def test_password(self, zipfile):
        print(f'子线程处理的第一个文件-测试密码 {zipfile}')
        print(f'子线程处理的第一个文件-测试密码 {os.path.exists(zipfile)}')
        path_7zip = './7-Zip/7z.exe'  # 设置7zip路径
        passwords, _ = self.Main_OnlyUnzip.read_password_return_list()  # 调用主程序的函数，提取密码
        password_try_number = 0  # 密码尝试次数
        the_right_password = ''
        for password in passwords:
            command_test = [path_7zip, "t", "-p" + password, "-y", zipfile]  # 组合完整7zip指令
            run_text_command = subprocess.run(command_test, creationflags=subprocess.CREATE_NO_WINDOW)
            if run_text_command.returncode != 0:
                password_try_number += 1  # 返回码不为0则解压失败，密码失败次数+1
            elif run_text_command.returncode == 0:
                the_right_password = password
                break
        print(f'正确密码 {the_right_password}')
        return the_right_password

    def start_unzip(self, the_folder, zipfile, zipfile_list, unzip_password):
        print(f'子线程中解压的文件 {zipfile}')
        zip_name = self.Main_OnlyUnzip.get_zip_name(zipfile)  # 解压文件名
        path_7zip = './7-Zip/7z.exe'  # 设置7zip路径
        temporary_folder = os.path.join(the_folder, "UnzipTempFolder")  # 临时文件夹
        unzip_folder = os.path.join(temporary_folder, zip_name)  # 解压结果路径
        # 组合解压指令
        command_unzip = [path_7zip, "x", "-p" + unzip_password, "-y", zipfile, "-o" + unzip_folder]  # 组合完整7zip指令
        subprocess.run(command_unzip, creationflags=subprocess.CREATE_NO_WINDOW)
        # 通过比较文件大小检查解压结果
        original_size = self.Main_OnlyUnzip.get_file_list_size(zipfile_list)  # 原文件大小
        unzip_size = self.Main_OnlyUnzip.get_folder_size(unzip_folder)  # 压缩结果大小
        if unzip_size < original_size * 0.95:  # 解压后文件大小如果小于原文件95%，则视为解压失败
            # winshell.delete_file(unzip_folder, no_confirm=True)  # 删除解压结果
            unzip_folder = unzip_folder.replace('/', '\\')
            send2trash.send2trash(unzip_folder)
            return '文件损坏'
        else:
            if self.Main_OnlyUnzip.ui.checkBox_delect_zip.isChecked():  # 根据选项选择是否删除原文件
                for i in zipfile_list:  # 删除原文件
                    # winshell.delete_file(i)
                    i = i.replace('/', '\\')
                    send2trash.send2trash(i)
            self.Main_OnlyUnzip.check_unzip_result(temporary_folder)  # 检查解压结果，处理套娃
            if os.path.exists(unzip_folder):  # 处理遗留的解压结果文件夹
                if self.Main_OnlyUnzip.get_folder_size(unzip_folder) == 0:
                    # winshell.delete_file(unzip_folder, no_confirm=True)
                    unzip_folder = unzip_folder.replace('/', '\\')
                    send2trash.send2trash(unzip_folder)
            return '解压成功'


class OnlyUnzip(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化
        self.setFixedSize(262, 232)
        self.create_new_ini()  # 创建初始设置文件
        self.start_with_load_setting()  # 加载设置文件
        self.ui.label_icon.setPixmap('./icon/初始状态.png')

        # 设置槽函数
        self.ui.label_icon.dropSignal.connect(self.drop_files)  # 拖入文件
        self.ui.button_page_main.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))  # 切换页面
        self.ui.button_page_password.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))  # 切换页面
        self.ui.button_page_setting.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))  # 切换页面
        self.ui.button_page_history.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))  # 切换页面
        self.ui.buttonGroup.buttonClicked[int].connect(self.change_button_color)

        self.ui.button_update_password.clicked.connect(self.update_password)
        self.ui.button_export_password.clicked.connect(self.export_password)
        self.ui.button_export_password_with_number.clicked.connect(self.export_password_with_number)

        self.ui.checkBox_model_unzip.stateChanged.connect(self.change_setting)
        self.ui.checkBox_model_test.stateChanged.connect(self.change_setting)
        self.ui.checkBox_nested_folders.stateChanged.connect(self.change_setting)
        self.ui.checkBox_nested_zip.stateChanged.connect(self.change_setting)
        self.ui.checkBox_delect_zip.stateChanged.connect(self.change_setting)
        self.ui.checkBox_check_zip.stateChanged.connect(self.change_setting)

    def drop_files(self, filepaths):
        """检查拖入的文件"""
        all_files = []
        for i in filepaths:
            if os.path.isfile(i):
                all_files.append(i)
            else:
                files_in_folder = self.get_all_files_in_folder(i)
                all_files += files_in_folder
        all_files = list(set(all_files))  # 转为集合再转为列表，用于去重
        self.run_unzip_qthread(all_files)

    def get_all_files_in_folder(self, folder):
        """获取文件夹下的所有文件，返回一个列表"""
        all_files = []
        for root, directories, files in os.walk(folder):
            for filename in files:
                # 获取每个文件的完整路径，并添加到列表中
                file_path = os.path.join(root, filename)
                file_path = file_path.replace('/', '\\')
                all_files.append(file_path)
                print(f'---------file_path {file_path}')
        return all_files

    def run_unzip_qthread(self, files):
        print(f'输入的文件 {files}')
        if files:  # 列表或者字典都不为空则执行子线程
            unzip_files = self.check_zip(files)  # 检查是否是压缩包
            print(f'检查是压缩包的文件 {unzip_files}')
            if unzip_files:
                unzip_files_dict = self.class_multi_volume(unzip_files)  # 将压缩包分类 一般与分卷
                print(f'--------unzip_files_dict {unzip_files_dict}')
                # 运行子线程，进行测试与解压
                self.unzip_qthread = unzip_main(unzip_files_dict)
                self.unzip_qthread.signal_ui_update.connect(self.update_ui)
                self.unzip_qthread.start()
            else:  # 有一个为空则说明没有需要解压的文件
                self.ui.label_icon.setPixmap('./icon/初始状态.png')
                self.ui.label_current_file.setText('————————————')
                self.ui.label_schedule.setText('没有压缩包')
        else:  # 有一个为空则说明没有需要解压的文件
            self.ui.label_icon.setPixmap('./icon/初始状态.png')
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule.setText('没有压缩包')

    def update_ui(self, the_list):
        if the_list[0] == '当前文件':
            self.ui.label_current_file.setText(the_list[1])
        elif the_list[0] == '进度':
            self.ui.label_schedule.setText(the_list[1])
        elif the_list[0] == '图标':
            if the_list[1] is None:
                if self.ui.checkBox_model_test.isChecked():  # 按选项设置不同图标
                    self.ui.label_icon.setPixmap('./icon/测试密码.png')
                else:
                    self.ui.label_icon.setPixmap('./icon/正在解压.png')
            else:
                self.ui.label_icon.setPixmap(the_list[1])
        elif the_list[0] == '历史记录-成功':
            item = QListWidgetItem(the_list[1])
            item.setTextColor(QColor(92, 167, 186))
            self.ui.listWidget_history.addItem(item)
        elif the_list[0] == '历史记录-失败':
            item = QListWidgetItem(the_list[1])
            item.setTextColor(QColor(254, 67, 101))
            self.ui.listWidget_history.addItem(item)

    def save_unzip_history(self, zipfile, password):
        """保存解压历史"""
        with open('unzip_history.txt', 'a', encoding='utf-8') as hs:
            history = f'日期：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} 文件：{os.path.split(zipfile)[1]} 密码：{password}\n'
            hs.write(history)

    def right_password_number_add_one(self, password):
        """正确密码次数+1"""
        read_config = configparser.ConfigParser()  # 注意大小写
        read_config.read("config.ini", encoding='utf-8')  # 配置文件的路径
        old_number = int(read_config.get(password, 'number'))
        read_config.set(password, 'number', str(old_number + 1))  # 次数加1
        read_config.write(open('config.ini', 'w', encoding='utf-8'))

    def check_unzip_result(self, folder):
        """检查解压结果，处理套娃文件夹和压缩包"""
        # if self.ui.checkBox_nested_zip.isChecked():  # 如果套娃压缩包选项选中
        #     maybe_nested_zip_files = self.get_all_files_in_folder(folder)
        #     self.drop_files(maybe_nested_zip_files)
        if self.ui.checkBox_nested_folders.isChecked():  # 如果套娃文件夹选项选中
            need_move_path = self.check_folder_depth(folder)  # 需要移动的文件夹/文件路径
            need_move_filename = os.path.split(need_move_path)[1]  # 需要移动的文件夹/文件名称
            parent_folder = os.path.split(folder)[0]  # 临时文件夹的上级目录（原压缩包所在的目录）
            if need_move_filename not in os.listdir(parent_folder):  # 如果没有重名文件/文件夹
                shutil.move(need_move_path, parent_folder)
            else:
                rename_filename = self.rename_recursion(need_move_path, folder)
                rename_full_path = os.path.join(os.path.split(need_move_path)[0], rename_filename)
                os.rename(need_move_path, rename_full_path)
                shutil.move(rename_full_path, parent_folder)
        else:
            unzip_folder = os.listdir(folder)[0]
            full_folder_path = os.path.join(folder, unzip_folder)
            on_folder_files = [os.path.join(full_folder_path, x) for x in os.listdir(full_folder_path)]
            parent_folder = os.path.split(folder)[0]
            if len(on_folder_files) == 1:  # 如果文件夹下就一个文件/文件夹，则直接移动
                need_move_path = on_folder_files[0]
                need_move_filename = os.path.split(need_move_path)[1]
            else:  # 如果有多个文件/文件夹，则保留文件夹
                need_move_path = full_folder_path
                need_move_filename = os.path.split(need_move_path)[1]
            if need_move_filename not in os.listdir(parent_folder):  # 如果没有重名文件/文件夹
                shutil.move(need_move_path, parent_folder)
            else:
                rename_filename = self.rename_recursion(need_move_path, folder)
                rename_full_path = os.path.join(os.path.split(need_move_path)[0], rename_filename)
                os.rename(need_move_path, rename_full_path)
                shutil.move(rename_full_path, parent_folder)

    def check_folder_depth(self, path):
        """检查文件夹深度，找出最后一级多文件的文件夹"""
        if len(os.listdir(path)) == 1:
            if os.path.isfile(os.path.join(path, os.listdir(path)[0])):  # 如果文件夹下只有一个文件，并且是文件
                last_path = os.path.join(path, os.listdir(path)[0])
                return last_path
            else:
                return self.check_folder_depth(os.path.join(path, os.listdir(path)[0]))  # 临时文件夹下只有一个文件，但是文件夹，则递归
        else:
            last_path = path
            return last_path

    def rename_recursion(self, filepath, unzip_folder):
        """递归改名，确保无同名文件"""
        parent_directory = os.path.split(unzip_folder)[0]
        filename_without_suffix = os.path.split(os.path.splitext(filepath)[0])[1]
        suffix = os.path.splitext(filepath)[1]
        count = 1
        while True:
            new_filename = f"{filename_without_suffix} - new{count}{suffix}"
            if new_filename not in os.listdir(parent_directory):
                return new_filename
            else:
                count += 1

    def check_zip(self, files):
        """是否检查压缩包，返回检查后的结果"""
        final_files = []
        if self.ui.checkBox_check_zip.isChecked():
            for i in files:
                if self.is_zip_file(i):
                    final_files.append(i)
        else:
            final_files = files
        return final_files

    def get_zip_name(self, file):
        """提取文件名"""
        filename = os.path.split(file)[1]
        re_rar = r"^(.+)\.part\d+\.rar$"  # 4种压缩文件的命名规则
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip_top = r"^(.+)\.zip$"
        if re.match(re_7z, filename):
            zip_name = re.match(re_7z, filename).group(1)
        elif re.match(re_zip_top, filename):
            zip_name = re.match(re_zip_top, filename).group(1)
        elif re.match(re_rar, filename):
            zip_name = re.match(re_rar, filename).group(1)
        else:
            zip_name = os.path.split(os.path.splitext(file)[0])[1]
        return zip_name

    def class_multi_volume(self, files):
        """区分普通压缩包与分卷压缩包（会自动获取文件夹下的所有相关分卷包）"""
        # 文件所在的文件夹
        the_folder = os.path.split(files[0])[0]
        # 利用正则匹配分卷压缩包
        filenames = [os.path.split(x)[1] for x in files]
        ordinary_zip = [x for x in filenames]  # 复制
        re_rar = r"^(.+)\.part\d+\.rar$"  # 4种压缩文件的命名规则
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip_top = r"^(.+)\.zip$"
        re_zip_other = r"^(.+)\.z\d+$"
        multi_volume_dict = {}  # 分卷文件字典（键值对为 第一个分卷：文件夹下的全部分卷（不管有没有在变量files中）
        for i in filenames:
            full_filepath = os.path.join(the_folder, i)
            if re.match(re_7z, i):  # 匹配7z正则
                filename = re.match(re_7z, i).group(1)  # 提取文件名
                first_multi_volume = os.path.join(the_folder, filename + r'.7z.001')  # 设置第一个分卷压缩包名，作为键名
                if first_multi_volume not in multi_volume_dict:  # 如果文件名不在字典内，则添加一个空键值对
                    multi_volume_dict[first_multi_volume] = set()  # 用集合添加（目的是为了后面的zip分卷，其实用列表更方便）
                multi_volume_dict[first_multi_volume].add(full_filepath)  # 添加键值对（示例.7z.001：示例.7z.001，示例.7z.002）
                ordinary_zip.remove(i)  # 将新列表中的分卷压缩包剔除
            elif re.match(re_rar, i):
                filename = re.match(re_rar, i).group(1)
                first_multi_volume = os.path.join(the_folder, filename + r'.part1.rar')
                if first_multi_volume not in multi_volume_dict:
                    multi_volume_dict[first_multi_volume] = set()
                multi_volume_dict[first_multi_volume].add(full_filepath)
                ordinary_zip.remove(i)
            elif re.match(re_zip_other, i) or re.match(re_zip_top, i):  # 只要是zip后缀的，都视为分卷压缩包，因为解压的都是.zip后缀
                if re.match(re_zip_other, i):
                    filename = re.match(re_zip_other, i).group(1)
                else:
                    filename = re.match(re_zip_top, i).group(1)
                first_multi_volume = os.path.join(the_folder, filename + r'.zip')
                if first_multi_volume not in multi_volume_dict:
                    multi_volume_dict[first_multi_volume] = set()
                multi_volume_dict[first_multi_volume].add(full_filepath)
                multi_volume_dict[first_multi_volume].add(first_multi_volume)  # zip分卷的特性，第一个分卷包名称是.zip后缀
                ordinary_zip.remove(i)
                if first_multi_volume in ordinary_zip:  # zip分卷特性，如果是分卷删除第一个.zip后缀的文件名，所以需要删除多出来的一个zip文件
                    ordinary_zip.remove(first_multi_volume)
        return self.find_all_multi_volume_in_folder(the_folder, ordinary_zip, multi_volume_dict)
        # return the_folder, ordinary_zip, multi_volume_dict  # 返回普通压缩包、分卷压缩包

    def find_all_multi_volume_in_folder(self, the_folder, ordinary_zip, multi_volume_dict):
        """扩展文件夹下所有的在字典中的分卷压缩包，应对拖入文件少的问题"""
        all_filenames = os.listdir(the_folder)
        re_rar = r"^(.+)\.part\d+\.rar$"  # 4种压缩文件的命名规则
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip_top = r"^(.+)\.zip$"
        re_zip_other = r"^(.+)\.z\d+$"

        for i in all_filenames:
            full_filepath = os.path.join(the_folder, i)
            if re.match(re_7z, i):  # 匹配7z正则
                filename = re.match(re_7z, i).group(1)
                guess_first_multi_volume = os.path.join(the_folder, filename + r'.7z.001')
                if guess_first_multi_volume in multi_volume_dict:
                    if full_filepath not in multi_volume_dict[guess_first_multi_volume]:
                        multi_volume_dict[guess_first_multi_volume].add(full_filepath)
            elif re.match(re_rar, i):
                filename = re.match(re_rar, i).group(1)
                guess_first_multi_volume = os.path.join(the_folder, filename + r'.part1.rar')
                if guess_first_multi_volume in multi_volume_dict:
                    if full_filepath not in multi_volume_dict[guess_first_multi_volume]:
                        multi_volume_dict[guess_first_multi_volume].add(full_filepath)
            elif re.match(re_zip_other, i) or re.match(re_zip_top, i):  # 只要是zip后缀的，都视为分卷压缩包，因为解压的都是.zip后缀
                if re.match(re_zip_other, i):
                    filename = re.match(re_zip_other, i).group(1)
                else:
                    filename = re.match(re_zip_top, i).group(1)
                guess_first_multi_volume = os.path.join(the_folder, filename + r'.zip')
                if guess_first_multi_volume in multi_volume_dict:
                    if full_filepath not in multi_volume_dict[guess_first_multi_volume]:
                        multi_volume_dict[guess_first_multi_volume].add(full_filepath)
        # 将普通压缩包的列表转为字典，与分卷压缩包的字典合并
        ordinary_zip_dict = {}
        for i in ordinary_zip:
            full_filepath = os.path.join(the_folder, i)
            ordinary_zip_dict[full_filepath] = set()
            ordinary_zip_dict[full_filepath].add(full_filepath)

        all_zip_dict = {}
        all_zip_dict.update(ordinary_zip_dict)
        all_zip_dict.update(multi_volume_dict)
        # return ordinary_zip, multi_volume_dict  # 返回普通压缩包的列表、分卷压缩包的字典
        return all_zip_dict

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

    def get_file_list_size(self, file_list):
        """获取文件大小"""
        total_size = 0
        for i in file_list:
            total_size += os.path.getsize(i)
        return total_size

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

    def create_new_ini(self):
        """如果本地没有condig文件则新建"""
        if not os.path.exists(os.path.join(os.getcwd(), 'config.ini')):
            with open('config.ini', 'w', encoding='utf-8') as cw:
                the_initialize = """[DEFAULT]
information = 
number = 0
model = unzip
nested_folders = True
nested_zip = True
delete_zip = True
check_zip = True
multithreading = 

[无密码]
number = 9999"""
                cw.write(the_initialize)

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

    def change_button_color(self, button_id):
        """高亮点击的按钮"""
        original_style = self.ui.button_update_password.styleSheet()  # 按钮的原始样式
        clicked_style = f"{original_style} background-color: rgb(232, 221, 203);"  # 被点击后的样式
        for button in self.ui.buttonGroup.buttons():  # 重置按钮组中所有按钮的样式
            button.setStyleSheet(original_style)
        clicked_button = self.ui.buttonGroup.button(button_id)
        clicked_button.setStyleSheet(clicked_style)


app = QApplication()
qdarktheme.setup_theme("light")
show_ui = OnlyUnzip()
show_ui.show()
app.exec_()
