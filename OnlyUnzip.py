import configparser
import os
import re
import shutil
import subprocess
import time

import filetype
import natsort
import qdarktheme
import send2trash  # win7不能使用winshell，用send2trash替代
from PySide2.QtCore import Signal, QThread, Qt
from PySide2.QtGui import QColor, QIcon
from PySide2.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMenu, QAction

from ui import Ui_MainWindow


class UnzipMainQthread(QThread):
    signal_ui_update = Signal(list)  # 自定义信号
    signal_send_unzip_result = Signal(list)  # 发送解压后文件的list

    def __init__(self, unzip_files_dict, parent=None):
        super().__init__(parent)

        is_unzip, is_delete, is_nested_folders, skip_rule = self.read_config()

        self.unzip_files_dict = unzip_files_dict
        self.is_unzip = is_unzip
        self.is_delete = is_delete
        self.is_nested_folders = is_nested_folders
        self.skip_rule = skip_rule

    @staticmethod
    def read_config():
        """读取配置文件，设置初始参数变量"""
        read_config = configparser.ConfigParser()
        read_config.read("config.ini", encoding='utf-8')

        is_unzip = read_config.get('DEFAULT', 'model') == 'unzip'
        is_delete = read_config.get('DEFAULT', 'delete_zip') == 'True'
        is_nested_folders = read_config.get('DEFAULT', 'nested_folders') == 'True'
        skip_suffix = read_config.get('DEFAULT', 'skip_suffix')
        # 设置7zip的文件后缀过滤规则
        if skip_suffix:
            skip_suffix_set = set(skip_suffix.split(' ')
                                  + [x.lower() for x in skip_suffix.split(' ')]
                                  + [x.upper() for x in skip_suffix.split(' ')])  # 原本+小写+大写
            skip_rule = ['-xr!*.' + x for x in skip_suffix_set]
        else:
            skip_rule = []

        return is_unzip, is_delete, is_nested_folders, skip_rule

    def run(self):
        total_files_number = len(self.unzip_files_dict)  # 需要解压的文件总数（分卷计数1）
        current_number = 0  # 当前文件编号
        wrong_password_file_number = 0  # 密码错误文件数
        damaged_file_number = 0  # 损坏的文件数
        pass_number = 0  # 跳过文件数
        success_number = 0
        the_pre_folder = ''  # 上一个文件所在文件夹，用于删除临时文件夹
        for first_file in self.unzip_files_dict:
            the_folder = os.path.split(first_file)[0]  # 文件所在文件夹
            current_number += 1  # 当前文件编号计数+1
            if current_number == 1:
                the_pre_folder = the_folder
            current_filename = OnlyUnzip.get_zip_name(first_file)  # 提取当前处理的文件名
            self.signal_ui_update.emit(['当前文件', current_filename])
            self.signal_ui_update.emit(['进度', f'{current_number}/{total_files_number} 测试密码中'])
            self.signal_ui_update.emit(['图标', None])
            file_list = self.unzip_files_dict[first_file]
            # 多传递两个参数current_number、total_files_number，用于保持传递信号的文本一致
            the_test_result, the_right_password = self.test_password(first_file, current_number, total_files_number)
            if the_test_result == '密码错误':
                wrong_password_file_number += 1
                self.signal_ui_update.emit(['历史记录-失败', f'{os.path.split(first_file)[1]} | 密码错误'])
            elif the_test_result == '不是压缩文件':
                pass_number += 1
                self.signal_ui_update.emit(
                    ['历史记录-跳过', f'{os.path.split(first_file)[1]} | 不是压缩文件（确定），已跳过'])
            elif the_test_result == '丢失分卷':
                damaged_file_number += 1
                self.signal_ui_update.emit(['历史记录-失败', f'{os.path.split(first_file)[1]} | 丢失分卷'])
            else:
                OnlyUnzip.right_password_number_add_one(the_right_password)  # 成功解压则密码使用次数+1
                OnlyUnzip.save_unzip_history(first_file, the_right_password)  # 保存解压历史
                self.signal_ui_update.emit(['进度', f'{current_number}/{total_files_number} | {the_right_password}'])
                self.signal_ui_update.emit(['历史记录-成功', f'{os.path.split(first_file)[1]} | {the_right_password}'])
                if self.is_unzip:  # 如果解压选项被选中，则执行解压操作
                    self.start_unzip(the_folder, first_file, file_list, the_right_password)
                    success_number += 1
                    # 由于添加了过滤解压功能，不再以解压后文件大小判断是否文件损坏
                    # if unzip_result == '文件损坏':
                    #     damaged_file_number += 1
                    #     self.signal_ui_update.emit(['历史记录-失败', f'{os.path.split(first_file)[1]} | 文件损坏(可能)'])
                    # if unzip_result == '解压成功':
                    #     success_number += 1
                if the_pre_folder != the_folder:  # 如果当前文件所在文件夹与上一个处理的文件所在文件夹不同，则删除上一个的临时文件夹
                    pre_temporary_folder = os.path.normpath(os.path.join(the_pre_folder, "UnzipTempFolder"))  # 临时文件夹
                    if os.path.exists(pre_temporary_folder):  # 处理遗留的临时文件夹
                        if OnlyUnzip.get_folder_size(pre_temporary_folder) == 0:
                            self.del_empty_folder(pre_temporary_folder)
                    the_pre_folder = the_folder
                if current_number == total_files_number:  # 完成全部文件处理后，删除临时文件夹
                    temporary_folder = os.path.normpath(os.path.join(the_folder, "UnzipTempFolder"))  # 临时文件夹
                    if os.path.exists(temporary_folder):  # 处理遗留的临时文件夹
                        if OnlyUnzip.get_folder_size(temporary_folder) == 0:
                            self.del_empty_folder(temporary_folder)
        # 全部完成后发送信号
        self.signal_ui_update.emit(['图标', './icon/全部完成.png'])
        self.signal_ui_update.emit(['当前文件', '————————————'])
        self.signal_ui_update.emit(
            ['进度',
             f'成功:{success_number}，密码错误:{wrong_password_file_number}，损坏:{damaged_file_number}，跳过:{pass_number}'])
        self.signal_ui_update.emit(['完成解压', None])

    def test_password(self, zipfile, current_number, total_files_number):
        """测试密码"""
        path_7zip = './7-Zip/7z.exe'  # 设置7zip路径
        passwords, _ = OnlyUnzip.read_password_return_list()  # 调用主程序的函数，提取密码
        the_right_password = ''
        the_test_result = '密码错误'
        test_password_number = 0
        total_test_password = len(passwords)
        for password in passwords:
            test_password_number += 1
            if test_password_number % 5 == 0:  # 每5次刷新一次ui
                self.signal_ui_update.emit(
                    ['进度',
                     f'{current_number}/{total_files_number} 测试密码中 {test_password_number}/{total_test_password}']
                )
            command_test = [path_7zip, "t", "-p" + password, "-y", zipfile]  # 组合完整7zip指令
            run_text_command = subprocess.run(command_test,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE,
                                              creationflags=subprocess.CREATE_NO_WINDOW)
            if run_text_command.returncode == 0:  # 返回码为0则测试成功
                the_right_password = password
                the_test_result = '测试成功'
                break
            elif run_text_command.returncode == 2:  # 返回码为2则说明文件有问题
                if "Cannot open the file as archive" in str(run_text_command.stderr):
                    the_test_result = '不是压缩文件'
                    break
                elif "Missing volume" in str(run_text_command.stderr) \
                        or 'Unexpected end of archive' in str(run_text_command.stderr):
                    the_test_result = '丢失分卷'
                    break
                # 密码错误的提示为：Cannot open encrypted archive. Wrong password?
        return the_test_result, the_right_password

    def start_unzip(self, the_folder, zipfile, zipfile_list, unzip_password):
        zip_name = OnlyUnzip.get_zip_name(zipfile)  # 解压文件名
        path_7zip = './7-Zip/7z.exe'  # 设置7zip路径
        temporary_folder = os.path.join(the_folder, "UnzipTempFolder")  # 临时文件夹
        unzip_folder = os.path.normpath(os.path.join(temporary_folder, zip_name).strip().strip('.'))  # 解压结果路径
        # 组合解压指令
        os.makedirs(unzip_folder)  # 创建解压路径的文件夹（如果一个文件名末尾是空格或者. ，则直接调用7zip解压时会创建一个无日期的文件夹，无法正常删除，所以会导致报错）
        command_unzip = [path_7zip,
                         "x",
                         "-p" + unzip_password, "-y",
                         zipfile,
                         "-o" + unzip_folder] + self.skip_rule  # 组合完整7zip指令
        subprocess.run(command_unzip,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       creationflags=subprocess.CREATE_NO_WINDOW)
        if self.is_delete:  # 根据选项选择是否删除原文件
            for i in zipfile_list:  # 删除原文件
                send2trash.send2trash(os.path.normpath(i))
        if self.is_nested_folders:
            self.nested_folders_true(temporary_folder)  # 检查解压结果，处理套娃
        else:
            self.nested_folders_false(temporary_folder)
        if os.path.exists(unzip_folder):  # 处理遗留的解压结果文件夹
            if OnlyUnzip.get_folder_size(unzip_folder) == 0:
                self.del_empty_folder(unzip_folder)

    @staticmethod
    def del_empty_folder(folder):
        """删除0kb文件夹"""
        print(f'准备删除 {folder}')
        try:
            os.rmdir(folder)
            print(f'已删除 {folder}')
        except OSError:
            all_dirpath = []
            for dirpath, dirnames, filenames in os.walk(folder):
                all_dirpath.append(dirpath)
            for i in all_dirpath[::-1]:
                os.rmdir(i)
                print(f'内部不为空 已删除内部文件夹 {i}')

    def nested_folders_true(self, folder):
        """处理套娃文件夹"""
        need_move_path = OnlyUnzip.check_folder_depth(folder)  # 需要移动的文件夹/文件路径
        need_move_filename = os.path.split(need_move_path)[1]  # 需要移动的文件夹/文件名称
        parent_folder = os.path.split(folder)[0]  # 临时文件夹的上级目录（原压缩包所在的目录）
        if need_move_filename not in os.listdir(parent_folder):  # 如果没有重名文件/文件夹
            shutil.move(need_move_path, parent_folder)
            new_path = os.path.join(parent_folder, os.path.split(need_move_path)[1])
            self.emit_unzip_result(new_path)
        else:
            rename_filename = OnlyUnzip.rename_recursion(need_move_path, folder)
            rename_full_path = os.path.join(os.path.split(need_move_path)[0], rename_filename)
            os.rename(need_move_path, rename_full_path)
            shutil.move(rename_full_path, parent_folder)
            new_path = os.path.join(parent_folder, os.path.split(rename_full_path)[1])
            self.emit_unzip_result(new_path)

    def nested_folders_false(self, folder):
        """不处理套娃文件夹"""
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
            new_path = os.path.join(parent_folder, os.path.split(need_move_path)[1])
            self.emit_unzip_result(new_path)
        else:
            rename_filename = OnlyUnzip.rename_recursion(need_move_path, folder)
            rename_full_path = os.path.join(os.path.split(need_move_path)[0], rename_filename)
            os.rename(need_move_path, rename_full_path)
            shutil.move(rename_full_path, parent_folder)
            new_path = os.path.join(parent_folder, os.path.split(rename_full_path)[1])
            self.emit_unzip_result(new_path)

    def emit_unzip_result(self, path):
        """发送list信号，包含解压后的所有文件，用于重复解压来处理嵌套压缩包"""
        nested_unzip_filepath = []
        if os.path.isfile(path):
            nested_unzip_filepath.append(path)
        elif os.path.isdir(path):
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    # 获取每个文件的完整路径，并添加到列表中
                    file_path = os.path.normpath(os.path.join(dirpath, filename))
                    nested_unzip_filepath.append(file_path)

        self.signal_send_unzip_result.emit(nested_unzip_filepath)


class OnlyUnzip(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化
        self.create_new_ini()  # 创建初始设置文件
        self.check_config_version()  # 检查配置文件版本--后期删除该函数
        self.start_with_load_setting()  # 加载设置文件
        self.ui.label_icon.setPixmap('./icon/初始状态.png')
        self.ui.listWidget_history.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置历史记录控件的右键菜单属性
        self.nested_unzip_filepath = []  # 存放解压结果
        self.ui.stackedWidget.setCurrentIndex(0)

        # 设置槽函数
        self.ui.label_icon.dropSignal.connect(self.drop_files)  # 拖入文件
        self.ui.button_page_main.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))  # 切换页面
        self.ui.button_page_password.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))  # 切换页面
        self.ui.button_page_setting.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))  # 切换页面
        self.ui.button_page_history.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))  # 切换页面
        self.ui.buttonGroup.buttonClicked[int].connect(self.change_button_color)

        self.ui.button_update_password.clicked.connect(self.update_password)
        self.ui.button_read_clipboard.clicked.connect(self.read_clipboard)
        self.ui.button_export_password.clicked.connect(self.export_password)
        self.ui.button_export_password_with_number.clicked.connect(self.export_password_with_number)
        self.ui.button_open_password.clicked.connect(lambda: os.startfile('password export.txt'))
        self.ui.button_export_password.clicked.connect(lambda: self.ui.button_open_password.setEnabled(True))
        self.ui.button_export_password_with_number.clicked.connect(
            lambda: self.ui.button_open_password.setEnabled(True))

        self.ui.checkBox_model_unzip.stateChanged.connect(self.change_setting)
        self.ui.checkBox_model_test.stateChanged.connect(self.change_setting)
        self.ui.checkBox_nested_folders.stateChanged.connect(self.change_setting)
        self.ui.checkBox_nested_zip.stateChanged.connect(self.change_setting)
        self.ui.checkBox_delect_zip.stateChanged.connect(self.change_setting)
        self.ui.checkBox_check_zip.stateChanged.connect(self.change_setting)
        self.ui.lineedit_unzip_skip_suffix.textChanged.connect(self.change_setting)
        self.ui.listWidget_history.customContextMenuRequested.connect(self.show_menu_copy)  # 绑定历史记录控件的右键菜单

    def drop_files(self, filepaths):
        """检查拖入的文件"""
        all_files = []
        for i in filepaths:
            if os.path.exists(i):
                if os.path.isfile(i):
                    all_files.append(i)
                else:
                    files_in_folder = self.get_all_files_in_folder(i)
                    all_files += files_in_folder
        all_files = list(set(all_files))  # 转为集合再转为列表，用于去重
        self.run_unzip_qthread(all_files)

    @staticmethod
    def get_all_files_in_folder(folder):
        """获取文件夹下的所有文件，返回一个列表"""
        all_files = []
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                # 获取每个文件的完整路径，并添加到列表中
                file_path = os.path.normpath(os.path.join(dirpath, filename))
                all_files.append(file_path)
        return all_files

    @staticmethod
    def is_old_temporary_folder_exist(files):
        """检查之前解压的临时文件夹是否存在"""
        all_temporary_folder = set()  # 所有可能存在的临时文件夹
        for file in files:
            temporary_folder = os.path.join(os.path.split(file)[0], "UnzipTempFolder")
            all_temporary_folder.add(temporary_folder)
        for folder in all_temporary_folder:
            if os.path.exists(folder) and os.listdir(folder):
                return True
        return False

    def run_unzip_qthread(self, files):
        """解压的子线程"""
        if self.is_old_temporary_folder_exist(files):  # 如果存在临时文件夹，则不进行后续操作
            self.ui.label_icon.setPixmap('./icon/错误.png')
            self.ui.label_current_file.setText('————————————')
            self.ui.label_schedule.setText('存在遗留临时文件夹')
            self.ui.label_icon.setEnabled(True)
        else:
            if files:  # 列表或者字典都不为空则执行子线程
                need_unzip_files = self.check_zip(files)  # 检查是否是有压缩包
                if need_unzip_files:
                    self.ui.label_icon.setEnabled(False)  # 拖入文件执行解压前关闭Label控件，防止再次拖入文件导致报错
                    unzip_files_dict = self.class_multi_volume(need_unzip_files)  # 将压缩包分类 一般与分卷
                    # 运行子线程，进行测试与解压
                    self.unzip_qthread = UnzipMainQthread(unzip_files_dict)
                    self.unzip_qthread.signal_ui_update.connect(self.update_ui)
                    self.unzip_qthread.signal_send_unzip_result.connect(self.accept_nested_unzip_filepath)
                    self.unzip_qthread.start()
                else:  # 有一个为空则说明没有需要解压的文件
                    self.ui.label_icon.setPixmap('./icon/错误.png')
                    self.ui.label_current_file.setText('————————————')
                    self.ui.label_schedule.setText('没有压缩包')
                    self.ui.label_icon.setEnabled(True)
            else:  # 有一个为空则说明没有需要解压的文件
                self.ui.label_icon.setPixmap('./icon/错误.png')
                self.ui.label_current_file.setText('————————————')
                self.ui.label_schedule.setText('没有压缩包')
                self.ui.label_icon.setEnabled(True)

    def show_menu_copy(self, pos):
        """历史记录框中设置右键复制密码"""
        selected_item = self.ui.listWidget_history.currentItem()
        if selected_item and selected_item.data(Qt.UserRole) == '成功':  # 设置只有正确解压的项目文本才可以右键复制
            menu = QMenu()
            menu.adjustSize()
            copy_action = QAction('复制密码', menu)
            copy_action.triggered.connect(self.menu_copy_pw)
            menu.addAction(copy_action)
            menu.exec_(self.ui.listWidget_history.mapToGlobal(pos))

    def menu_copy_pw(self):
        selected_item = self.ui.listWidget_history.currentItem()
        text = selected_item.text().split(' | ')[1]  # 根据文本筛选出解压密码
        QApplication.clipboard().setText(text)

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
            item = QListWidgetItem(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + the_list[1])
            item.setTextColor(QColor(92, 167, 186))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)  # 启用UserRole
            item.setData(Qt.UserRole, '成功')  # 设置 UserRole 的值
            self.ui.listWidget_history.addItem(item)
        elif the_list[0] == '历史记录-失败':
            item = QListWidgetItem(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + the_list[1])
            item.setTextColor(QColor(254, 67, 101))
            self.ui.listWidget_history.addItem(item)
        elif the_list[0] == '历史记录-跳过':
            item = QListWidgetItem(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()) + the_list[1])
            item.setTextColor(QColor(255, 182, 193))
            self.ui.listWidget_history.addItem(item)
        elif the_list[0] == '完成解压':  # 完成解压后如果选择了嵌套压缩包，则在将解压结果重新运行子线程
            self.ui.label_icon.setEnabled(True)
            if self.ui.checkBox_nested_zip.isChecked():
                unzip_path = self.nested_unzip_filepath.copy()
                self.nested_unzip_filepath = []  # 重置结果
                self.drop_files(unzip_path)

    @staticmethod
    def save_unzip_history(zipfile, password):
        """保存解压历史"""
        with open('unzip_history.txt', 'a', encoding='utf-8') as hs:
            history = f'日期：{time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())} ' \
                      f'| 文件：{os.path.split(zipfile)[1]} | 密码：{password}\n\n'
            hs.write(history)

    @staticmethod
    def right_password_number_add_one(password):
        """正确密码次数+1"""
        read_config = configparser.ConfigParser()  # 注意大小写
        read_config.read("config.ini", encoding='utf-8')  # 配置文件的路径
        old_number = int(read_config.get(password, 'number'))
        read_config.set(password, 'number', str(old_number + 1))  # 次数加1
        read_config.write(open('config.ini', 'w', encoding='utf-8'))

    def accept_nested_unzip_filepath(self, filepath_list):
        """接受子线程发送的解压结果list信号"""
        self.nested_unzip_filepath += filepath_list

    @staticmethod
    def check_folder_depth(path):
        """检查文件夹深度，找出最后一级多文件的文件夹"""
        if len(os.listdir(path)) == 1:
            if os.path.isfile(os.path.join(path, os.listdir(path)[0])):  # 如果文件夹下只有一个文件，并且是文件
                last_path = os.path.join(path, os.listdir(path)[0])
                return last_path
            else:
                return OnlyUnzip.check_folder_depth(os.path.join(path, os.listdir(path)[0]))  # 临时文件夹下只有一个文件，但是文件夹，则递归
        else:
            last_path = path
            return last_path

    @staticmethod
    def rename_recursion(filepath, unzip_folder):
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
                # 修改判断逻辑：1.如果符合压缩包的正则并且第一个分卷包存在，则用第一个分卷包测试 2.否则按正常流程测试
                # 调用的class_multi_volume函数的输入值是一个列表，返回的是分卷的第一个包（符合分卷规则）或者原始文件（不符合分卷规则）
                check_file = list(self.class_multi_volume([i]).keys())[0]
                if os.path.exists(check_file):
                    if self.is_zip_file(check_file):
                        final_files.append(i)
                else:
                    if self.is_zip_file(i):
                        final_files.append(i)
        else:
            final_files = files
        return final_files

    @staticmethod
    def get_zip_name(file):
        """提取文件名"""
        filename = os.path.split(file)[1]
        re_rar = r"^(.+)\.part\d+\.rar$"  # 分卷压缩文件的命名规则
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip_top = r"^(.+)\.zip$"
        re_zip_type2 = r"^(.+)\.zip.\d+$"
        if re.match(re_7z, filename):
            zip_name = re.match(re_7z, filename).group(1)
        elif re.match(re_zip_top, filename):
            zip_name = re.match(re_zip_top, filename).group(1)
        elif re.match(re_rar, filename):
            zip_name = re.match(re_rar, filename).group(1)
        elif re.match(re_zip_type2, filename):
            zip_name = re.match(re_zip_type2, filename).group(1)
        else:
            zip_name = os.path.split(os.path.splitext(file)[0])[1]
        return zip_name

    @staticmethod
    def class_multi_volume(unzip_files):
        """区分普通压缩包与分卷压缩包（会自动获取文件夹下的所有相关分卷包）"""
        all_zip_dict = {}  # 存放最终结果
        # 按文件所在文件夹建立对应字典：文件夹-文件
        file_dict = {}
        for item in unzip_files:
            if os.path.split(item)[0] not in file_dict:
                file_dict[os.path.split(item)[0]] = set()
            file_dict[os.path.split(item)[0]].add(item)
        # 按文件夹逐个处理其中的文件
        for the_folder in file_dict:
            files = file_dict[the_folder]
            # 利用正则匹配分卷压缩包
            filenames = [os.path.split(x)[1] for x in files]
            ordinary_zip = [x for x in filenames]  # 复制
            re_rar = r"^(.+)\.part\d+\.rar$"  # 分卷压缩文件的命名规则
            re_7z = r"^(.+)\.7z\.\d+$"
            re_zip_top = r"^(.+)\.zip$"
            re_zip_other = r"^(.+)\.z\d+$"
            re_zip_type2 = r"^(.+)\.zip\.\d+$"
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
                elif re.match(re_zip_type2, i):  # 匹配zip格式2正则
                    filename = re.match(re_zip_type2, i).group(1)  # 提取文件名
                    first_multi_volume = os.path.join(the_folder, filename + r'.zip.001')  # 设置第一个分卷压缩包名，作为键名
                    if first_multi_volume not in multi_volume_dict:  # 如果文件名不在字典内，则添加一个空键值对
                        multi_volume_dict[first_multi_volume] = set()  # 用集合添加（目的是为了后面的zip分卷，其实用列表更方便）
                    multi_volume_dict[first_multi_volume].add(full_filepath)  # 添加键值对（示例.zip.001：示例.zip.001，示例.zip.002）
                    ordinary_zip.remove(i)  # 将新列表中的分卷压缩包剔除
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
            all_zip_dict.update(OnlyUnzip.find_all_multi_volume_in_folder(the_folder, ordinary_zip, multi_volume_dict))
        return all_zip_dict

    @staticmethod
    def find_all_multi_volume_in_folder(the_folder, ordinary_zip, multi_volume_dict):
        """扩展文件夹下所有的在字典中的分卷压缩包，应对拖入文件少的问题"""
        all_filenames = os.listdir(the_folder)
        re_rar = r"^(.+)\.part\d+\.rar$"  # 分卷压缩文件的命名规则
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip_top = r"^(.+)\.zip$"
        re_zip_other = r"^(.+)\.z\d+$"
        re_zip_type2 = r"^(.+)\.zip\.\d+$"

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
            elif re.match(re_zip_type2, i):  # 匹配zip格式2正则
                filename = re.match(re_zip_type2, i).group(1)
                guess_first_multi_volume = os.path.join(the_folder, filename + r'.zip.001')
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

    @staticmethod
    def is_zip_file(file):
        """检查文件是否是压缩包"""
        file_suffix = os.path.splitext(file)[1]  # 提取文件后缀名

        zip_type = ['zip', 'tar', 'rar', 'gz', '7z', 'xz']
        suffix_type = ['.zip', '.tar', '.rar', '.gz', '.7z', '.xz', '.iso']
        kind = filetype.guess(file)
        if kind is None:
            type_kind = None
        else:
            type_kind = kind.extension

        if type_kind in zip_type or file_suffix.lower() in suffix_type:  # filetype库识别符合或者后缀名符合
            return True
        else:
            return False

    @staticmethod
    def get_file_list_size(file_list):
        """获取文件大小"""
        total_size = 0
        for i in file_list:
            total_size += os.path.getsize(i)
        return total_size

    @staticmethod
    def get_folder_size(folder):
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
        """修改密码更新逻辑，不再显示原有密码
        # 更新密码框
        all_password = read_config.sections()  # 获取section
        self.ui.text_password.setPlainText('\n'.join(all_password))
        """
        # 更新选项
        code_model = read_config.get('DEFAULT', 'model')
        code_nested_folders = read_config.get('DEFAULT', 'nested_folders') == 'True'
        code_nested_zip = read_config.get('DEFAULT', 'nested_zip') == 'True'
        code_delete_zip = read_config.get('DEFAULT', 'delete_zip') == 'True'
        code_check_zip = read_config.get('DEFAULT', 'check_zip') == 'True'
        code_skip_suffix = read_config.get('DEFAULT', 'skip_suffix')
        if code_model == 'unzip':
            self.ui.checkBox_model_unzip.setChecked(True)
        elif code_model == 'test':
            self.ui.checkBox_model_test.setChecked(True)
        self.ui.checkBox_nested_folders.setChecked(code_nested_folders)
        self.ui.checkBox_nested_zip.setChecked(code_nested_zip)
        self.ui.checkBox_delect_zip.setChecked(code_delete_zip)
        self.ui.checkBox_check_zip.setChecked(code_check_zip)
        self.ui.lineedit_unzip_skip_suffix.setText(code_skip_suffix)

    @staticmethod
    def create_new_ini():
        """如果本地没有config文件则新建"""
        if not os.path.exists(os.path.join(os.getcwd(), 'config.ini')):
            with open('config.ini', 'w', encoding='utf-8') as cw:
                the_initialize = """[DEFAULT]
information = 
number = 0
model = unzip
nested_folders = True
nested_zip = False
delete_zip = True
check_zip = True
multithreading = 
skip_suffix = 

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

        # 重置密码框
        self.ui.text_password.setPlainText('')

    def read_clipboard(self):
        """读取剪切板"""
        clipboard = QApplication.clipboard()  # 创建一个剪贴板对象
        clipboard_text = clipboard.text()  # 读取剪贴板的文本
        self.ui.text_password.setPlainText(clipboard_text)

    @staticmethod
    def export_password():
        """导出密码"""
        sort_passwords, passwords_with_number = OnlyUnzip.read_password_return_list()
        with open("password export.txt", "w", encoding="utf-8") as pw:
            pw.write("\n".join(sort_passwords))

    @staticmethod
    def export_password_with_number():
        """导出带次数的密码"""
        sort_passwords, passwords_with_number = OnlyUnzip.read_password_return_list()
        with open("password export.txt", "w", encoding="utf-8") as pw:
            pw.write("\n".join(passwords_with_number))

    @staticmethod
    def read_password_return_list():
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

        suffix_text = self.ui.lineedit_unzip_skip_suffix.text()
        support_delimiters = ",|，| |;|；"
        the_skip_suffix = set([x for x in re.split(support_delimiters, suffix_text) if x])  # 提取分隔后的列表，去重去空
        read_config.set('DEFAULT', 'skip_suffix', ' '.join(the_skip_suffix))

        read_config.write(open('config.ini', 'w', encoding='utf-8'))  # 写入

    def change_button_color(self, button_id):
        """高亮点击的按钮"""
        original_style = self.ui.button_update_password.styleSheet()  # 按钮的原始样式
        clicked_style = f"{original_style} background-color: rgb(232, 221, 203);"  # 被点击后的样式
        for button in self.ui.buttonGroup.buttons():  # 重置按钮组中所有按钮的样式
            button.setStyleSheet(original_style)
        clicked_button = self.ui.buttonGroup.button(button_id)
        clicked_button.setStyleSheet(clicked_style)

    @staticmethod
    def check_config_version():
        """检查配置文件版本"""
        read_config = configparser.ConfigParser()  # 注意大小写
        read_config.read("config.ini", encoding='utf-8')  # 配置文件的路径
        if 'skip_suffix' not in read_config['DEFAULT']:
            read_config.set('DEFAULT', 'skip_suffix', '')
            read_config.write(open('config.ini', 'w', encoding='utf-8'))


app = QApplication()
qdarktheme.setup_theme("light")
# app.setStyle('Fusion')
show_ui = OnlyUnzip()
show_ui.setWindowIcon(QIcon('./icon/程序图标.ico'))
show_ui.setFixedSize(262, 232)
show_ui.show()
app.exec_()
