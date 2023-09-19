import configparser
import os
import re
import subprocess
import time
from typing import Tuple

import send2trash  # win7不能使用winshell，用send2trash替代
from PySide2.QtCore import Signal, QThread

import general_method

os.environ["PYTHONIOENCODING"] = "UTF-8"


class UnzipQthread(QThread):
    signal_update_ui = Signal(list)  # 发送更新主程序ui的信号，发送的list格式：['更新类型', '相关数据']
    signal_nested_zip = Signal(list)  # 发送处理嵌套压缩包的信号，发送的list格式：所有解压后文件路径list
    signal_stop = Signal()  # 中止操作的信号

    def __init__(self, unzip_files_dict, parent=None):
        super().__init__(parent)

        code_unzip, code_delete, code_nested_folders, code_nested_zip, skip_rule_7zip, unzip_to_folder = self.load_setting()

        self.unzip_files_dict = unzip_files_dict
        self.code_unzip = code_unzip  # bool，解压模式，True为解压，False为测试
        self.code_delete = code_delete  # bool，是否删除原文件
        self.code_nested_folders = code_nested_folders  # bool，是否处理嵌套文件夹
        self.code_nested_zip = code_nested_zip  # bool，是否处理嵌套压缩包
        self.skip_rule_7zip = skip_rule_7zip  # list，解压时跳过的后缀
        self.unzip_to_folder = unzip_to_folder  # str，解压到指定文件夹，可为空（则为解压文件的上级目录）

        self.nested_zip_filelist = []  # 存放解压结果，用于重复解压以处理嵌套压缩包
        self.code_stop = False
        self.signal_stop.connect(self.update_code_stop)

    @staticmethod
    def load_setting() -> Tuple[bool, bool, bool, bool, list, str]:
        """读取配置文件，用于设置初始参数
        返回值为：
        解压模式 bool
        删除原文件 bool
        处理套娃文件夹 bool
        处理套娃压缩包 bool
        解压时跳过的后缀名（已转换为7zip指令格式） list"""
        general_method.print_current_function()
        config = configparser.ConfigParser()
        config.read("config.ini", encoding='utf-8')

        code_unzip = config.get('DEFAULT', 'model') == 'unzip'
        code_delete = config.get('DEFAULT', 'delete_zip') == 'True'
        code_nested_folders = config.get('DEFAULT', 'nested_folders') == 'True'
        code_nested_zip = config.get('DEFAULT', 'nested_zip') == 'True'

        skip_suffix = config.get('DEFAULT', 'skip_suffix')
        # 设置7zip的文件后缀过滤规则
        if skip_suffix:
            skip_suffix_set = set(skip_suffix.split(' ')
                                  + [x.lower() for x in skip_suffix.split(' ')]
                                  + [x.upper() for x in skip_suffix.split(' ')])  # 原本+小写+大写
            skip_rule_7zip = ['-xr!*.' + x for x in skip_suffix_set]
        else:
            skip_rule_7zip = []

        # 设置解压路径
        unzip_to_folder = config.get('DEFAULT', 'unzip_to_folder')
        if not os.path.exists(unzip_to_folder) or os.path.isfile(unzip_to_folder):
            unzip_to_folder = ''

        return code_unzip, code_delete, code_nested_folders, code_nested_zip, skip_rule_7zip, unzip_to_folder

    def run(self):
        general_method.print_current_function()
        number_total = len(self.unzip_files_dict)  # 文件总个数（分卷计数1）
        number_current = 0  # 当前文件编号
        number_wrong_pw = 0  # 密码错误的文件数
        number_damaged = 0  # 损坏的文件数
        number_skip = 0  # 跳过的文件数（经检测不是压缩包的会跳过）
        number_success = 0  # 成功解压的文件数
        pre_folder = ''  # 上一个解压文件所在文件夹的路径，用于删除遗留的临时文件夹
        unzip_history_dict = {}  # 保存解压历史
        self.signal_update_ui.emit(['子线程-开始'])

        for file_key in self.unzip_files_dict:  # 只解压dict中的key
            if self.code_stop:  # 如果是停止状态，则中止循环
                break
            else:
                if self.unzip_to_folder:  # 如果指定了目标文件夹
                    target_folder = self.unzip_to_folder
                else:  # 否则为每个文件的上级文件夹
                    target_folder = os.path.split(file_key)[0]  # 文件所在文件夹
                file_value = self.unzip_files_dict[file_key]  # 提取当前key对应的value，用于删除文件
                number_current += 1  # 计数+1
                if number_current == 1:  # 单独处理解压第1个文件时的上一个文件夹
                    pre_folder = target_folder
                current_filename = os.path.split(file_key)[1]  # 提取当前文件的文件名
                self.signal_update_ui.emit(['子线程-当前文件', current_filename])
                self.signal_update_ui.emit(['子线程-总进度', f'{number_current}/{number_total}'])

                test_result, correct_password = self.test_password(file_key)
                if test_result == '密码错误':
                    number_wrong_pw += 1
                    self.signal_update_ui.emit(['子线程-记录-密码错误', os.path.split(file_key)[1]])
                elif test_result == '不是压缩文件':
                    number_skip += 1
                    self.signal_update_ui.emit(['子线程-记录-不是压缩文件', os.path.split(file_key)[1]])
                elif test_result == '文件被占用':
                    number_skip += 1
                    self.signal_update_ui.emit(['子线程-记录-文件被占用', os.path.split(file_key)[1]])
                elif test_result == '磁盘空间不足':
                    number_skip += 1
                    self.signal_update_ui.emit(['子线程-记录-磁盘空间不足', os.path.split(file_key)[1]])
                elif test_result == '丢失分卷':
                    number_damaged += 1
                    self.signal_update_ui.emit(['子线程-记录-丢失分卷', os.path.split(file_key)[1]])
                elif test_result == '未知错误':
                    number_damaged += 1
                    self.signal_update_ui.emit(['子线程-记录-未知错误', os.path.split(file_key)[1]])
                elif test_result == '测试成功':  # 成功的密码测试
                    number_success += 1
                    if correct_password != ' ':
                        self.add_password_number(correct_password)  # 正确密码次数+1

                    unzip_history_dict[file_key] = correct_password  # 添加记录
                    self.signal_update_ui.emit(['子线程-记录-成功', os.path.split(file_key)[1], correct_password])

                    if self.code_unzip:  # 如果当前为解压模式，则执行解压操作
                        self.start_unzip(target_folder, file_key, file_value, correct_password)

                    if pre_folder != target_folder:  # 如果当前文件所在文件夹与上一个处理的文件所在文件夹不同，则删除上一个的临时文件夹
                        pre_temp_folder = os.path.normpath(os.path.join(pre_folder, "UnzipTempFolder"))  # 上一个临时文件夹
                        if os.path.exists(pre_temp_folder):  # 处理遗留的临时文件夹
                            general_method.delete_folder_if_empty(pre_temp_folder)
                        pre_folder = target_folder

                    if number_current == number_total:  # 完成全部文件处理后，删除最后的临时文件夹
                        temp_folder = os.path.normpath(os.path.join(target_folder, "UnzipTempFolder"))
                        if os.path.exists(temp_folder):
                            general_method.delete_folder_if_empty(temp_folder)

        # 全部完成后
        self.save_unzip_history(None, None, fp_dict=unzip_history_dict)  # 保存解压历史
        self.signal_update_ui.emit(['子线程-结束',
                                    f'成功:{number_success},失败:{number_wrong_pw},损坏:{number_damaged},跳过:{number_skip}'])
        if self.code_nested_zip and not self.code_stop:
            self.signal_nested_zip.emit(self.nested_zip_filelist)

    def test_password(self, file: str) -> Tuple[str, str]:
        """传入单个文件路径，执行密码测试，并返回解压结果和正确密码"""
        general_method.print_current_function()
        from main import OnlyUnzip

        path_7zip = './7-Zip/7z.exe'  # 设置7zip路径
        passwords, _ = OnlyUnzip.get_sorted_pwlist()  # 调用主程序的函数，提取密码列表list
        passwords.insert(0, ' ')
        correct_password = ' '
        test_result = '密码错误'  # 默认为密码错误，在循环过程中更新result
        current_test_pw_number = 0  # 当前测试密码的编号
        total_pw_number = len(passwords)  # 总密码个数

        # 逻辑：循环执行命令行，直到全部循环完或者中途碰到特定返回码或错误码后break循环，并返回指定结果，否则使用默认的result
        for password in passwords:
            if self.code_stop:  # 如果停止进程
                test_result = '未知错误'
                break
            else:
                current_test_pw_number += 1
                self.signal_update_ui.emit(['子线程-测试密码进度', f'{current_test_pw_number}/{total_pw_number}'])
                command_test = [path_7zip,
                                "t",
                                "-p" + password,
                                "-y",
                                file, ]  # 组合完整7zip指令

                process = subprocess.run(command_test,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         creationflags=subprocess.CREATE_NO_WINDOW,
                                         text=True)

                # print(f'process.stdout {process.stdout}')
                print(f'7zip错误信息流： {process.stderr}')
                # print(f'process.returncode {process.returncode}')

                if process.returncode == 0:  # 返回码为0则测试成功
                    correct_password = password
                    test_result = '测试成功'
                    break
                elif process.returncode == 1:  # 返回码为1则说明文件被占用
                    test_result = '文件被占用'
                    break
                elif process.returncode == 2:  # 返回码为2则说明无法解压
                    # 密码错误的返回提示为"Cannot open encrypted archive. Wrong password?"
                    if "Wrong password" not in str(process.stderr):
                        if "Cannot open the file as archive" in str(process.stderr):
                            test_result = '不是压缩文件'
                            break
                        elif "Missing volume" in str(process.stderr) or 'Unexpected end of archive' in str(
                                process.stderr):
                            test_result = '丢失分卷'
                            break
                        else:
                            test_result = '未知错误'
                            break
                        # 备忘录 需要扩大错误码判断范围
                elif process.returncode == 8:  # 返回码为8则说明当前磁盘空间不足
                    test_result = '磁盘空间不足'
                    break
                else:  # 处理其他的报错
                    test_result = '未知错误'
                    break

        return test_result, correct_password

    def start_unzip(self, target_folder, zipfile, zipfile_list, unzip_password):
        """执行解压
        传入参数：
        target_folder 解压到该目录
        zipfile 需解压的文件
        zipfile_list 解压文件所在的文件组，用于删除
        unzip_password 解压密码
        """
        general_method.print_current_function()
        # 解压逻辑：指定目录 >> 临时文件夹UnzipTempFolder >> filename名的文件夹 >> 解压结果
        filetitle = general_method.get_filetitle(zipfile)  # 提取不含后缀的文件名
        path_7zip = './7-Zip/7z.exe'  # 设置7zip路径
        temp_folder = os.path.normpath(os.path.join(target_folder, "UnzipTempFolder"))  # 生成临时文件夹的路径
        unzip_folder = os.path.normpath(os.path.join(temp_folder, filetitle).strip().strip('.'))  # 生成解压的路径
        # 创建解压路径的文件夹（如果一个文件名末尾是空格或者. ，直接调用7zip解压时会创建一个无日期的文件夹，无法正常删除，导致报错）
        os.makedirs(unzip_folder)

        # 组合指令，先组合无密码指令，如果有密码则添加指令
        process = [path_7zip, "x", "-y", zipfile, "-bsp1",
                   "-o" + unzip_folder] + self.skip_rule_7zip  # -bsp1指令作用是实时输出信息
        if unzip_password != '':  # 添加密码指令
            process += ["-p" + unzip_password]

        self.signal_update_ui.emit(['子线程-解压进度', 0])  # 解压前发送信号更新ui
        process = subprocess.Popen(process,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   creationflags=subprocess.CREATE_NO_WINDOW,
                                   text=True)

        pre_percent = 0
        while True:
            try:
                line = process.stdout.readline()
            except UnicodeDecodeError:  # 编码报错 UnicodeDecodeError: 'gbk' codec can't decode byte 0xae in position 205: illegal multibyte sequence
                line = ''
            if line == '' and process.poll() is not None:
                break
            # 在实时输出中查找进度信息并解析
            match = re.search(r'(\d{1,3})%', line)
            if match:
                progress_percent = int(match.group(1))  # 提取进度百分比（不含%）
                if progress_percent > pre_percent:
                    self.signal_update_ui.emit(['子线程-解压进度', progress_percent])
                    pre_percent = progress_percent

        # 解压完成后执行相关操作
        if self.code_delete:  # 是否删除原文件
            for i in zipfile_list:
                send2trash.send2trash(i)  # 删除文件到回收站

        self.check_nested_folders(temp_folder, self.code_nested_folders)  # 是否处理套娃文件夹

    def check_nested_folders(self, temp_folder: str, code_nested_folders: bool):
        """传入文件夹路径folder参数，将最深一级非空文件夹移动到target_folder中（处理套娃文件夹）
        可选参数 code_nested_folders:True 处理套娃文件夹；False 不处理套娃文件夹，仅做1次基础移动操作"""
        general_method.print_current_function()
        unzip_foldername = os.listdir(temp_folder)[0]  # 获取临时文件夹下自动创建的文件夹名
        unzip_dirpath = os.path.normpath(os.path.join(temp_folder, unzip_foldername))  # 获取完整路径
        final_folder = os.path.split(temp_folder)[0]

        if code_nested_folders:
            new_path = general_method.process_nested_folders(unzip_dirpath, target_folder=final_folder)
        else:
            new_path = general_method.process_nested_folders(unzip_dirpath, target_folder=final_folder, mode=False)

        self.collect_unzip_result(new_path)

    def collect_unzip_result(self, path: str):
        """传入文件/文件夹路径，保存解压结果（解压后的所有文件路径）的列表list，用于重复解压以处理嵌套压缩包"""
        general_method.print_current_function()
        unzip_filepath = []
        if os.path.isfile(path):
            unzip_filepath.append(path)
        else:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    # 获取每个文件的完整路径，并添加到列表中
                    file_path = os.path.normpath(os.path.join(dirpath, filename))
                    unzip_filepath.append(file_path)

        self.nested_zip_filelist += unzip_filepath

    @staticmethod
    def save_unzip_history(filepath: str, password: str, fp_dict: dict = None):
        """保存解压记录到本地"""
        general_method.print_current_function()
        with open('unzip_history.txt', 'a', encoding='utf-8') as ha:
            add_text = ''
            if fp_dict:
                for key in fp_dict:
                    add_text += f'■日期：{time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())} ' \
                                f'■文件路径：{key} ' \
                                f'■解压密码：{fp_dict[key]}\n' \
                                f'--------------------------------------------\n'
            else:
                add_text = f'■日期：{time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())} ' \
                           f'■文件路径：{filepath} ' \
                           f'■解压密码：{password}\n' \
                           f'--------------------------------------------\n'
            ha.write(add_text)

    @staticmethod
    def add_password_number(password: str):
        """将解压密码使用次数+1"""
        general_method.print_current_function()
        config = configparser.ConfigParser()
        config.read("config.ini", encoding='utf-8')
        old_number = int(config.get(password, 'number'))
        config.set(password, 'number', str(old_number + 1))  # 次数+1
        config.write(open('config.ini', 'w', encoding='utf-8'))

    def update_code_stop(self):
        self.code_stop = True
