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
import multiprocessing
import winshell


class only_unzip(QMainWindow):
    def __init__(self):
        self.ui = QUiLoader().load('ui_main.ui')

        # 初始化
        self.ui.setFixedSize(200, 200)  # 设置窗口大小，用于固定大小
        self.add_label_main()  # 添加main控件
        self.read_password()

        # 设置对齐方式为居中
        self.ui.label_main.setAlignment(Qt.AlignCenter)
        self.ui.label_info.setAlignment(Qt.AlignCenter)

        # 设置槽函数
        self.ui.button_quit.clicked.connect(lambda: quit())  # 退出按钮
        self.ui.button_password.clicked.connect(self.form_size_change)  # 显示密码按钮
        self.ui.button_update.clicked.connect(self.update_password)
        self.ui.label_main.drop_signal.connect(lambda drop_path: self.drop_in_file(drop_path))

    def form_size_change(self):
        """扩大窗口，显示密码框"""
        if self.ui.button_password.text() == '显示密码框':
            self.ui.setFixedSize(400, 200)  # 设置窗口大小，用于固定大小
            self.ui.button_password.setText('隐藏密码框')
        elif self.ui.button_password.text() == '隐藏密码框':
            self.ui.setFixedSize(200, 200)  # 设置窗口大小，用于固定大小
            self.ui.button_password.setText('显示密码框')

    def icon_change(self, icon_number):
        if icon_number == 'unzip_star':
            self.ui.label_main.setPixmap(QPixmap("./icon/解压中.png").scaled(120, 120, aspectRatioMode=Qt.KeepAspectRatio))
        elif icon_number == 'unzip_finish':
            self.ui.label_main.setPixmap(QPixmap("./icon/完成.png").scaled(120, 120, aspectRatioMode=Qt.KeepAspectRatio))
        QCoreApplication.processEvents()

    def info_text_change(self, rate_file_number, files_number):
        self.ui.label_info.setText(f'解压中：{rate_file_number}/{files_number}')
        QCoreApplication.processEvents()  # 手动刷新

    def unzip_start(self, zip_command):
        self.result = subprocess.run(zip_command)

    def drop_in_file(self, drop_path):
        """拖入文件后处理获得的列表信号"""
        drop_dirs = []
        drop_files = []
        for i in drop_path:  # 检查拖入的是文件还是文件夹
            if os.path.isdir(i):
                drop_dirs.append(i)
            elif os.path.isfile(i):
                drop_files.append(i)

        self.icon_change('unzip_star')
        files_number = len(drop_files)  # 总文件数
        rate_file_number = 0  # 到第几个文件了
        error_number = 0  # 解压失败的文件数
        zip_path = './7-Zip/7z.exe'  # 设置7z指令

        for file in drop_files:  # 开始逐个处理压缩文件
            rate_file_number += 1
            self.info_text_change(rate_file_number, files_number)
            # 设置7z的指令
            file_directory = os.path.split(file)[0]  # 文件的父目录
            file_name_without_suffix = os.path.split(os.path.splitext(file)[0])[1]  # 单独的没有后缀的文件名
            temporary_folder = os.path.join(file_directory, "unzipTempFolder")  # 临时存放解压结果的文件夹
            unzip_path = os.path.join(temporary_folder, file_name_without_suffix)  # 解压到临时文件下与文件同名的文件夹中
            password_try_number = 0  # 密码尝试次数
            for password in passwords:
                zip_command = [zip_path, "x", "-p" + password, "-y", file, "-o" + unzip_path]  # 组合完整7z指令
                # self.unzip_start(zip_command)
                self.unzip_start(zip_command)
                if self.result.returncode != 0:
                    password_try_number += 1  # 返回码不为0则解压失败，密码失败次数+1
                elif self.result.returncode == 0:
                    # send2trash.send2trash(file)
                    winshell.delete_file(file, no_confirm=True)  # 删除原文件到回收站
                    self.right_password_number_add_one(password)  # 成功解压则密码使用次数+1
                    self.check_unzip_result(unzip_path, file_directory, temporary_folder)  # 执行检查函数，并传递需要的变量

                    break  # 检查完结果后退出循环
            if password_try_number == len(passwords):
                error_number += 1
        if len(os.listdir(temporary_folder)) == 0:  # 解压完成后如果临时文件夹为空，则删除
            # send2trash.send2trash(temporary_folder)
            winshell.delete_file(temporary_folder, no_confirm=True)
        self.icon_change('unzip_finish')
        self.ui.label_info.setText(f'成功：{files_number - error_number}，失败：{error_number}')

    def check_unzip_result(self, unzip_path, file_directory, temporary_folder):
        """检查解压结果"""
        '''
        检查解压结果：
        1. 如果解压后文件夹内有多个文件，则移动该文件夹到父目录，结束操作
        2. 如果解压后文件夹内只有一个文件/文件夹，则移动该文件/文件夹到解压文件夹，再次检查
        3. 注意同名文件/文件夹
        '''
        if len(os.listdir(unzip_path)) > 1:  # 如果解压后的不是单个文件
            if os.path.split(unzip_path)[1] in os.listdir(file_directory):  # 如果有重复文件
                new_unzip_path_name = unzip_path + ' -new' + str(random.randint(1, 99))
                os.rename(unzip_path, new_unzip_path_name)
                shutil.move(new_unzip_path_name, file_directory)
            else:
                shutil.move(unzip_path, file_directory)
        elif len(os.listdir(unzip_path)) == 1:
            self.single_file_move(unzip_path)
            if len(os.listdir(temporary_folder)) == 1 and os.path.isdir(temporary_folder + '/' + os.listdir(temporary_folder)[0]) and len(os.listdir(temporary_folder + '/' + os.listdir(temporary_folder)[0])) > 1:  # 文件夹全都移动到父目录后，最终移动到根目录
                if os.listdir(temporary_folder)[0] in os.listdir(file_directory):  # 如果有重复文件
                    new_name = temporary_folder + '/' + os.listdir(temporary_folder)[0] + ' -new' + str(random.randint(1, 99))
                    os.rename(temporary_folder + '/' + os.listdir(temporary_folder)[0], new_name)
                    shutil.move(new_name, file_directory)
                else:
                    shutil.move(temporary_folder + '/' + os.listdir(temporary_folder)[0], file_directory)

    def single_file_move(self, check_path):
        """单文件转移到父目录"""
        if len(os.listdir(check_path)) == 1:  # 必须要加的判断，不然递归的时候如果有多文件会直接移动其中的第一个文件到父目录
            single_path = check_path + '/' + os.listdir(check_path)[0]
            if os.path.isfile(single_path):  # 如果唯一路径是文件，则直接移动
                if os.path.split(single_path)[1] in os.listdir(os.path.split(os.path.split(check_path)[0])[0]):  # 如果有重复文件
                    new_single_path_name = os.path.splitext(single_path)[0] + ' -new' + str(random.randint(1, 99)) + os.path.splitext(single_path)[1]
                    os.rename(single_path, new_single_path_name)
                    shutil.move(new_single_path_name, os.path.split(os.path.split(check_path)[0])[0])
                else:
                    shutil.move(single_path, os.path.split(os.path.split(check_path)[0])[0])
                if len(os.listdir(check_path)) == 0:
                    winshell.delete_file(check_path, no_confirm=True)
            else:  # 如果唯一路径是文件夹
                if os.path.split(single_path)[1] in os.listdir(os.path.split(check_path)[0]):  # 如果有重复文件
                    new_single_path_name = single_path + ' -new' + str(random.randint(1, 99))
                    os.rename(single_path, new_single_path_name)
                    shutil.move(new_single_path_name, os.path.split(check_path)[0])
                else:
                    shutil.move(single_path, os.path.split(check_path)[0])
                if len(os.listdir(check_path)) == 0:
                    winshell.delete_file(check_path, no_confirm=True)
                if len(os.listdir(os.path.split(check_path)[0])) == 1:
                    new_check_path = os.path.split(check_path)[0] + '/' + os.listdir(os.path.split(check_path)[0])[0]
                    self.single_file_move(new_check_path)

    def right_password_number_add_one(self, right_password):
        """正确的密码次数加1"""
        self.password = configparser.ConfigParser()  # 注意大小写
        self.password.read("password.ini", encoding='utf-8')  # 配置文件的路径
        old_number = int(self.password.get(right_password, 'number'))
        self.password.set(right_password, 'number', str(old_number + 1))  # 次数加1
        self.password.write(open('password.ini', 'w', encoding='utf-8'))
        self.read_password()

    def add_label_main(self):
        """添加main控件"""
        self.ui.label_main = MyLabel()
        self.ui.layout_label.addWidget(self.ui.label_main)
        self.ui.label_main.setPixmap(QPixmap("./icon/初始.png").scaled(120, 120, aspectRatioMode=Qt.KeepAspectRatio))

    def read_password(self):
        """读取密码"""
        self.password = configparser.ConfigParser()  # 注意大小写
        self.password.read("password.ini", encoding='utf-8')  # 配置文件的路径

        # 实现使用次数多的密码优先显示
        global passwords
        passwords = self.password.sections()  # 获取section
        sort_passwords = []  # 设置空列表，方便后续操作
        resort_passwords = []
        for password in passwords:  # 遍历全部密码
            sort_passwords.append(self.password.get(password, 'number') + ' - ' + password)  # value - section 组合
        sort_passwords = reversed(natsort.natsorted(sort_passwords))  # 按数字大小降序排序
        for i in sort_passwords:
            resort_passwords.append(re.search(r' - (.+)', i).group(1))  # 正则提取 - 后的section
        passwords = resort_passwords  # 重新赋值回去

        self.ui.text_edit_password.setText('\n'.join(passwords))  # 更新密码框

    def update_password(self):
        """更新密码"""
        new_section_temp = self.ui.text_edit_password.toPlainText().split('\n')
        new_section = [x for x in new_section_temp if x != '']
        for i in new_section:
            if i not in self.password.sections():
                self.password.add_section(i)
                self.password.set(i, 'number', '0')
                self.password.write(open('password.ini', 'w', encoding='utf-8'))  # 写入
        self.read_password()
        self.ui.setFixedSize(200, 200)  # 更新密码后重设大小
        self.ui.button_password.setText('显示密码框')


# 重写label类
class MyLabel(QLabel):
    drop_signal = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)  # 设置可拖入

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            drop_path = [url.toLocalFile() for url in urls]  # 获取多个文件的路径的列表
            self.drop_signal.emit(drop_path)  # 发送信号


def main():
    app = QApplication([])
    app.setStyle('Fusion')    # 设置风格
    show_ui = only_unzip()
    show_ui.ui.show()
    app.exec_()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
