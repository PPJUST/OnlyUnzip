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
        fenjuan_full_dict, no_fenjuan_files = self.check_fenjuan_zip(drop_files)  # 调用检查分卷函数，分离分卷文件和普通文件

        files_number = len(no_fenjuan_files) + len(fenjuan_full_dict)  # 总文件数
        rate_file_number = 0  # 到第几个文件了
        error_number = 0  # 解压失败的文件数
        damage_number = 0  # 损坏的压缩文件数
        zip_path = './7-Zip/7z.exe'  # 设置7zip指令

        for file in no_fenjuan_files:  # 开始逐个处理压缩文件（先处理不是分卷的文件）
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
                    # 检查解压结果和原文件大小比较
                    original_size = os.path.getsize(file)  # 原文件大小
                    unzip_size = self.get_folder_size(unzip_path)  # 压缩结果大小
                    if unzip_size < original_size * 0.9:  # 解压后文件大小如果小于原文件90%则说明压缩包损坏
                        winshell.delete_file(unzip_path, no_confirm=True)  # 删除解压结果
                        damage_number += 1  # 计数+1
                        break  # 退出当前文件循环
                    else:
                        # send2trash.send2trash(file)
                        winshell.delete_file(file, no_confirm=True)  # 删除原文件到回收站
                        self.right_password_number_add_one(password)  # 成功解压则密码使用次数+1
                        self.check_unzip_result(unzip_path, file_directory, temporary_folder)  # 执行检查函数，并传递需要的变量
                        break  # 检查完结果后退出循环
            if password_try_number == len(passwords):
                error_number += 1
        for first_fenjuan_file in fenjuan_full_dict.keys():  # 然后处理分卷压缩包，解压键，成功的话再删除值
            '''
            下面的处理代码基本与上面的非分卷处理代码相同，大部分只在删除文件的地方有改动
            改动的地方用★标注
            '''
            rate_file_number += 1
            self.info_text_change(rate_file_number, files_number)
            # 设置7z的指令
            file_directory = os.path.split(first_fenjuan_file)[0]  # 文件的父目录
            file_name_without_suffix = self.draw_fenjuan_prefix(first_fenjuan_file)  # 单独的没有后缀的文件名★
            temporary_folder = os.path.join(file_directory, "unzipTempFolder")  # 临时存放解压结果的文件夹
            unzip_path = os.path.join(temporary_folder, file_name_without_suffix)  # 解压到临时文件下与文件同名的文件夹中
            password_try_number = 0  # 密码尝试次数
            for password in passwords:
                zip_command = [zip_path, "x", "-p" + password, "-y", first_fenjuan_file, "-o" + unzip_path]  # 组合完整7z指令
                # self.unzip_start(zip_command)
                self.unzip_start(zip_command)
                if self.result.returncode != 0:
                    password_try_number += 1  # 返回码不为0则解压失败，密码失败次数+1
                elif self.result.returncode == 0:
                    # 检查解压结果和原文件大小比较
                    original_size = 0
                    for x in fenjuan_full_dict[first_fenjuan_file]:
                        original_size += os.path.getsize(x)  # 原文件大小(各个分卷合并）★
                    unzip_size = self.get_folder_size(unzip_path)  # 压缩结果大小
                    if unzip_size < original_size * 0.9:  # 解压后文件大小如果小于原文件90%则说明压缩包损坏
                        winshell.delete_file(unzip_path, no_confirm=True)  # 删除解压结果
                        damage_number += 1  # 计数+1
                        break  # 退出当前文件循环
                    else:
                        # send2trash.send2trash(file)
                        for x in fenjuan_full_dict[first_fenjuan_file]:
                            winshell.delete_file(x, no_confirm=True)  # 删除各个压缩文件到回收站★
                        self.right_password_number_add_one(password)  # 成功解压则密码使用次数+1
                        self.check_unzip_result(unzip_path, file_directory, temporary_folder)  # 执行检查函数，并传递需要的变量
                        break  # 检查完结果后退出循环
            if password_try_number == len(passwords):
                error_number += 1
        try:
            if len(os.listdir(temporary_folder)) == 0:  # 解压完成后如果临时文件夹为空，则删除
                # send2trash.send2trash(temporary_folder)
                winshell.delete_file(temporary_folder, no_confirm=True)
        except FileNotFoundError:
            pass
        self.icon_change('unzip_finish')
        self.ui.label_info.setText(f'成功:{files_number - error_number} 失败:{error_number} 损坏:{damage_number}')

    def get_folder_size(self, folder):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def check_fenjuan_zip(self, files):
        """检查分卷压缩包"""
        new_files = [x for x in files]  # 复制列表，最后会输出不包含分卷的列表
        re_rar = "^(.+)\.part\d+\.rar$"
        re_7z = "^(.+)\.7z\.\d+$"
        re_zip_top = "^(.+)\.zip$"
        re_zip_other = "^(.+)\.z\d+$"
        fenjuan_full_dict = {}  # 分卷文件字典（键值对为 第一个分卷：全部分卷）
        for i in files:
            if re.match(re_7z, i):  # 匹配7z正则
                prefix = re.match(re_7z, i).group(1) + r'.7z.001'  # 设置字典的键（提取的正则前缀+手工添加后缀）
                if prefix not in fenjuan_full_dict:  # 如果文件名不在字典内，则添加一个空键值对
                    fenjuan_full_dict[prefix] = set()  # 用集合添加（目的是为了后面的zip分卷，其实用列表更方便）
                fenjuan_full_dict[prefix].add(i)  # 添加键值对（示例.7z.001：示例.7z.001，示例.7z.002）
                new_files.remove(i)  # 将新列表中的分卷压缩包剔除
            elif re.match(re_zip_other, i) or re.match(re_zip_top, i):  # 只要是zip后缀的，都视为分卷压缩包
                if re.match(re_zip_other, i):
                    prefix = re.match(re_zip_other, i).group(1) + r'.zip'
                else:
                    prefix = re.match(re_zip_top, i).group(1) + r'.zip'
                if prefix not in fenjuan_full_dict:
                    fenjuan_full_dict[prefix] = set()
                fenjuan_full_dict[prefix].add(i)
                fenjuan_full_dict[prefix].add(prefix)  # zip分卷的特性，第一个分卷包名称是.zip后缀
                new_files.remove(i)
                if prefix in new_files:  # zip分卷特性，如果是分卷删除第一个.zip后缀的文件名
                    new_files.remove(prefix)
                else:
                    pass
            elif re.match(re_rar, i):
                prefix = re.match(re_rar, i).group(1) + r'.part1.rar'
                if prefix not in fenjuan_full_dict:
                    fenjuan_full_dict[prefix] = set()
                fenjuan_full_dict[prefix].add(i)
                new_files.remove(i)
        # 检查没有导入的压缩包分卷（例如files只包括其中某几个分卷）
        one_of_files = files[0]
        all_files = os.listdir(os.path.split(one_of_files)[0])
        dir_file_list = []
        for i in all_files:
            dir_file_list.append(os.path.join(os.path.split(one_of_files)[0] + '/' + i))
        # 假设使用的是完整文件名（文件路径+文件名+后缀）
        for i in dir_file_list:
            if re.match(re_7z, i):  # 匹配7z正则
                prefix = re.match(re_7z, i).group(1) + r'.7z.001'
                if prefix in fenjuan_full_dict:
                    fenjuan_full_dict[prefix].add(i)
            elif re.match(re_zip_other, i):
                prefix = re.match(re_zip_other, i).group(1) + r'.zip'
                if prefix in fenjuan_full_dict:
                    fenjuan_full_dict[prefix].add(i)
            elif re.match(re_rar, i):
                prefix = re.match(re_rar, i).group(1) + r'.part1.rar'
                if prefix in fenjuan_full_dict:
                    fenjuan_full_dict[prefix].add(i)
        return fenjuan_full_dict, new_files  # fenjuan_full_dict：分卷文件，new_files：不包含分卷的文件

    def draw_fenjuan_prefix(self, file_name):
        """提取分卷文件的文件名（不包含后缀）"""
        re_rar = "^(.+)\.part\d+\.rar$"
        re_7z = "^(.+)\.7z\.\d+$"
        re_zip_top = "^(.+)\.zip$"
        re_zip_other = "^(.+)\.z\d+$"
        if re.match(re_7z, file_name):  # 匹配7z正则
            prefix = re.match(re_7z, file_name).group(1)
        elif re.match(re_zip_top, file_name):
            prefix = re.match(re_zip_top, file_name).group(1)
        elif re.match(re_rar, file_name):
            prefix = re.match(re_rar, file_name).group(1)
        prefix_filename = os.path.split(prefix)[1]
        return prefix_filename

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
    main()
