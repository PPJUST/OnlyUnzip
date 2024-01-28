import os
import re
import shutil
import subprocess
import time
from typing import Tuple

import send2trash  # win7不能使用winshell，用send2trash替代
from PySide6.QtCore import Signal, QThread

import module.function_archive
import module.function_file
import module.function_filetype
import module.function_password
from constant import _PATH_7ZIP
from module import function_static
from module.function_config import Config

os.environ["PYTHONIOENCODING"] = "UTF-8"
config_file = 'config.ini'
backup_dir = 'backup'


class ExtractQthread(QThread):
    signal_update_ui = Signal(str, list)  # 发送更新主程序ui的信号，发送的list格式：代码, 数据
    signal_extracted_files = Signal(list)  # 发送所有解压出的文件路径list
    signal_stop = Signal()  # 中止操作的信号

    def __init__(self):
        super().__init__()
        # 初始化设置项
        self.code_mode = 'extract'  # str，执行方法，extract解压或test测试
        self.code_un_nest_dir = True  # bool，是否处理嵌套文件夹
        self.code_un_nest_archive = False  # bool，是否处理嵌套压缩包
        self.code_delete_archive = True  # bool，解压完成后是否删除原文件
        self.output_dir = ''  # str，解压到指定文件夹，如果为空则解压到文件所在目录
        self.exclude_rule = []  # list，解压时排除解压文件的规则（暂时仅支持排除后缀名）
        # check_filetype 在外部判断，不在子线程中处理

        # 设置初始变量
        self.extract_files_dict = {}  # 需要解压的文件dict，格式为{第一个包:(全部分卷包),...)
        self.extracted_filelist = []  # 解压出的所有文件路径list
        self.pw_list = []  # 用于测试的密码list
        self.code_stop = True  # 停止代码，用于终止操作，True为停止

        # 连接信号
        self.signal_stop.connect(self.update_code_stop)

    def reset_setting(self):
        """重置设置项与变量"""
        function_static.print_function_info()
        # 重置设置项
        config = Config()
        self.code_mode = config.mode
        self.code_un_nest_dir = config.handling_nested_folder
        self.code_un_nest_archive = config.handling_nested_archive
        self.code_delete_archive = config.delete_original_file
        self.output_dir = config.output_folder

        rule_set = config.exclude_rules
        if rule_set:
            self.exclude_rule = ['-xr!*.' + x for x in rule_set]  # 排除后缀名的语法

        # 重置变量
        self.code_stop = True
        self.extracted_filelist.clear()
        self.pw_list, _ = module.function_password.read_passwords()

    def set_extract_files_dict(self, file_dict: dict):
        """设置需要解压的文件dict变量"""
        function_static.print_function_info()
        self.extract_files_dict = file_dict
        self.code_stop = False

    def run(self):
        """启动子线程"""
        function_static.print_function_info()
        # 发送更新ui信号
        self.signal_update_ui.emit('1-2', [])  # 启动子线程

        # 设置初始变量
        count_total = len(self.extract_files_dict)  # 文件总个数（分卷计数1）
        number_current = 0  # 当前文件编号
        final_file = None  # 当前处理的文件
        count_wrong_pw = 0  # 密码错误的文件数
        count_damaged = 0  # 损坏的文件数
        count_skip = 0  # 跳过的文件数（经检测不是压缩包的会跳过）
        count_success = 0  # 成功解压的文件数
        pre_dirpath = ''  # 上一个解压文件所在文件夹的路径，用于删除遗留的临时文件夹
        history_dict = {}  # 保存解压历史

        # 循环需要解压的文件dict
        for file_key, file_value in self.extract_files_dict.items():  # 只需要解压dict中的key（第一个卷）
            if self.code_stop:  # 如果是停止状态，则中止循环
                break
            else:
                # 文件进度计数+1
                number_current += 1
                final_file = file_key
                # 获取解压目标目录
                if self.output_dir:  # 如果指定了目标文件夹
                    output_dir = self.output_dir
                else:  # 否则为每个文件的所在目录
                    output_dir = os.path.split(file_key)[0]
                # 单独处理第1个文件的上一个文件夹
                if number_current == 1:
                    pre_dirpath = output_dir
                # 提取当前文件的文件名，用于更新ui
                current_filename = os.path.split(file_key)[1]
                self.signal_update_ui.emit('3-1', [current_filename])
                self.signal_update_ui.emit('3-2', [f'{number_current}/{count_total}'])
                # 调用密码测试函数
                if self.code_mode == 'test':
                    code_result, right_pw, test_pw_number, list_files = self.test_pw_command_l(file_key)  # 先使用l命令测试
                    if code_result == '4-7' and test_pw_number == 1:  # 如果首个密码就成功，则不信赖该次结果
                        code_result, right_pw = self.test_pw(file_key)
                else:
                    code_result, right_pw, test_pw_number, list_files = self.test_pw_command_l(file_key)  # 先使用l命令测试
                    if code_result == '4-7' and test_pw_number == 1:  # 如果首个密码就成功，则不信赖该次结果
                        # 如果当前文件是zip，7zip会测试其内部所有文件，如果内部文件数太多，会导致使用x指令测试时很慢
                        if module.function_archive.is_zip_archive(file_key) and len(list_files) > 200:  # 如果符合上述情况，则先调用t测试在用x解压
                            code_result, right_pw = self.test_pw(file_key)
                            if code_result == '4-7':  # 如果测试成功，则添加密码参数调用x指令
                                code_result, right_pw = self.extract_archive(output_dir, file_key, right_pw)
                            else:  # 否则，不需要继续执行x指令，直接出结果
                                pass
                        else:  # 正常执行x指令进行解压
                            code_result, right_pw = self.extract_archive(output_dir, file_key)
                    else:  # 已获取真实的密码，可以直接解压
                        code_result, right_pw = self.extract_archive(output_dir, file_key, right_pw)
                # 检查状态码
                if code_result == '4-1':
                    count_wrong_pw += 1
                    self.signal_update_ui.emit(code_result, [current_filename])
                elif code_result in ['4-3', '4-4', '4-6']:
                    count_skip += 1
                    self.signal_update_ui.emit(code_result, [current_filename])
                elif code_result in ['4-2', '4-5']:
                    count_damaged += 1
                    self.signal_update_ui.emit(code_result, [current_filename])
                elif code_result == '4-7':  # 成功的密码测试
                    count_success += 1
                    # 正确密码次数+1
                    if right_pw != '':
                        module.function_password.add_pw_count(right_pw)
                    # 更新ui
                    self.signal_update_ui.emit(code_result, [current_filename, right_pw])
                    # 保存历史记录至字典
                    history_dict[file_key] = right_pw
                    # 如果执行的是解压函数，则进行后续检查
                    if self.code_mode == 'extract':
                        # 是否删除源文件
                        if self.code_delete_archive:
                            for i in file_value:
                                send2trash.send2trash(i)  # 删除文件到回收站
                        # 生成临时文件夹的路径
                        temp_folder = os.path.normpath(os.path.join(output_dir, "UnzipTempFolder"))
                        # 是否处理套娃文件夹
                        self.check_nested_folders(temp_folder, self.code_un_nest_dir)
                # 处理生成的临时文件夹（x指令下即使没有成功解压也会生成临时文件）
                # 如果当前文件所在文件夹与上一个处理的文件所在文件夹不同，则删除上一个的临时文件夹
                if pre_dirpath != output_dir:
                    pre_temp_folder = os.path.normpath(os.path.join(pre_dirpath, "UnzipTempFolder"))
                    if os.path.exists(pre_temp_folder):
                        function_static.delete_empty_folder(pre_temp_folder)
                    pre_dirpath = output_dir
        # 完成全部任务处理后，删除最后的临时文件夹
        # 提取临时文件夹路径
        if self.output_dir:  # 如果指定了目标文件夹
            output_dir = self.output_dir
        else:  # 否则为每个文件的所在目录
            output_dir = os.path.split(final_file)[0]
        temp_folder = os.path.normpath(os.path.join(output_dir, "UnzipTempFolder"))
        if os.path.exists(temp_folder):
            function_static.delete_empty_folder(temp_folder)

        # 全部完成后，保存解压历史
        self.save_pw_history(history_dict=history_dict)
        # 更新ui
        self.signal_update_ui.emit('1-3', [
            f'成功:{count_success},失败:{count_wrong_pw},损坏:{count_damaged},跳过:{count_skip}'])
        # 是否处理套娃压缩包
        if self.code_un_nest_archive and not self.code_stop:
            self.signal_extracted_files.emit(self.extracted_filelist)

    def test_pw_command_l(self, file: str) -> Tuple[str, any, int, list]:
        """使用7zip的l命令测试密码，比另外两个调用多了个返回值（最快的方法）"""
        function_static.print_function_info()

        """
        以下代码参照了测试时的代码
        """
        passwords, _ = module.function_password.read_passwords()
        passwords.insert(0, ' ')  # 插入一个空格密码，用于测试无密码压缩包
        right_pw = ' '  # 默认为空格密码，即无密码，实际传递时用空字符串''
        test_result = '4-1'  # 默认为4-1，即密码错误，在循环过程中更新
        test_pw_number = 0  # 当前测试密码的编号
        total_pw_count = len(passwords)  # 总密码个数
        list_files = []

        # 逻辑：循环执行命令行，直到全部循环完或者中途碰到特定返回码或错误码后break循环，并返回指定结果，否则使用默认的结果
        for pw in passwords:
            if self.code_stop:
                test_result = '4-5'
                break
            else:
                # 密码计数+1
                test_pw_number += 1
                # 发送信号更新ui
                self.signal_update_ui.emit('3-3', [f'{test_pw_number}/{total_pw_count}'])
                # 组合7zip指令t
                command_test = [_PATH_7ZIP, "l", file, "-p" + pw, '-bse2']
                # 调用7zip函数，获取返回码
                return_code, list_files = self.subprocess_7zip_run(command_test)
                test_result = return_code
                if return_code == '4-7':
                    if pw == ' ':
                        pw = ''  # 如果无密码，实际传递时用空字符串''
                    right_pw = pw
                    break
                elif return_code in ['4-2', '4-3', '4-4', '4-5', '4-6']:
                    break
                # 对返回码4-1不作处理（即密码错误继续循环）

        return test_result, right_pw, test_pw_number, list_files

    def test_pw(self, file: str) -> Tuple[str, any]:
        """传入压缩文件执行密码测试，并返回解压结果和正确密码"""
        function_static.print_function_info()
        # 设置初始变量
        passwords, _ = module.function_password.read_passwords()
        passwords.insert(0, ' ')  # 插入一个空格密码，用于测试无密码压缩包
        right_pw = ' '  # 默认为空格密码，即无密码，实际传递时用空字符串''
        test_result = '4-1'  # 默认为4-1，即密码错误，在循环过程中更新
        test_pw_number = 0  # 当前测试密码的编号
        total_pw_count = len(passwords)  # 总密码个数

        # 逻辑：循环执行命令行，直到全部循环完或者中途碰到特定返回码或错误码后break循环，并返回指定结果，否则使用默认的结果
        for pw in passwords:
            if self.code_stop:
                test_result = '4-5'
                break
            else:
                # 密码计数+1
                test_pw_number += 1
                # 发送信号更新ui
                self.signal_update_ui.emit('3-3', [f'{test_pw_number}/{total_pw_count}'])
                # 组合7zip指令t
                command_test = [_PATH_7ZIP, "t", file, "-p" + pw, '-bse2']
                # 调用7zip函数，获取返回码
                return_code, _ = self.subprocess_7zip_run(command_test)
                test_result = return_code
                if return_code == '4-7':
                    if pw == ' ':
                        pw = ''  # 如果无密码，实际传递时用空字符串''
                    right_pw = pw
                    break
                elif return_code in ['4-2', '4-3', '4-4', '4-5', '4-6']:
                    break
                # 对返回码4-1不作处理（即密码错误继续循环）

        return test_result, right_pw

    def extract_archive(self, output_dir, archive_file, right_password: str = None) -> Tuple[str, any]:
        """执行解压操作
        传入参数：
        output_dir 解压到该目录
        archive_file 需解压的文件
        password 正确的密码（可选参数）"""
        function_static.print_function_info()
        # 解压逻辑：指定目录 >> 临时文件夹UnzipTempFolder >> filename名的文件夹 >> 解压结果
        filetitle = function_static.get_filetitle(archive_file)  # 提取不含后缀的文件名
        filetitle = function_static.check_filetitle(filetitle)  # 剔除文件名首尾的空格和.
        temp_folder = os.path.normpath(os.path.join(output_dir, "UnzipTempFolder"))  # 生成临时文件夹的路径
        extract_folder = os.path.normpath(os.path.join(temp_folder, filetitle))  # 生成解压文件夹的路径
        # 手动创建解压路径的文件夹（使用7zip自动创建时，如果文件名末尾是空格或者. ，7zip会创建一个无日期的文件夹，无法正常删除，导致报错）
        os.makedirs(extract_folder)

        # 更新ui
        # self.signal_update_ui.emit('3-4', [0])
        """
        以下代码参照了测试时的代码，有一点变动
        """
        # 设置初始变量
        if right_password:
            passwords = [right_password]
        else:
            passwords, _ = module.function_password.read_passwords()
            passwords.insert(0, ' ')  # 插入一个空格密码，用于测试无密码压缩包
        right_pw = ' '  # 默认为空格密码，即无密码，实际传递时用空字符串''
        extract_result = '4-1'  # 默认为4-1，即密码错误，在循环过程中更新
        test_pw_number = 0  # 当前测试密码的编号
        total_pw_count = len(passwords)  # 总密码个数

        # 逻辑：循环执行命令行，直到全部循环完或者中途碰到特定返回码或错误码后break循环，并返回指定结果，否则使用默认的结果
        for pw in passwords:
            if self.code_stop:
                extract_result = '4-5'
                break
            else:
                # 密码计数+1
                test_pw_number += 1
                # 发送信号更新ui
                self.signal_update_ui.emit('3-3', [f'{test_pw_number}/{total_pw_count}'])
                # 组合7zip指令，先组合无密码指令，如果有密码则添加指令
                command_extract = [_PATH_7ZIP, "x", "-y", archive_file, '-bsp1', '-bse1', '-bso1',
                                   "-o" + extract_folder, "-p" + pw] + self.exclude_rule
                # 调用7zip函数，获取返回码
                return_code = self.subprocess_7zip_popen(command_extract)
                extract_result = return_code
                if return_code == '4-7':
                    if pw == ' ':
                        pw = ''  # 如果无密码，实际传递时用空字符串''
                    right_pw = pw
                    break
                elif return_code in ['4-2', '4-3', '4-4', '4-5', '4-6']:
                    break
                # 对返回码4-1不作处理（即密码错误继续循环）
        return extract_result, right_pw

    def subprocess_7zip_popen(self, command: list) -> str:
        """使用popen方法调用7zip，并返回对应信息，专用于x命令"""
        function_static.print_function_info()
        """
        同时读取stdout和stderr会导致堵塞
        所以需要在7zip命令行中将3种输出都重定向至一个流中，即 'bso1','bsp1',bse1'"""
        # print(f'执行指令 {" ".join(command)}')
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   creationflags=subprocess.CREATE_NO_WINDOW,
                                   text=True,
                                   universal_newlines=True)
        # 读取信息流
        stderr_error_code = '4-1'  # 通过信息流判断返回码为2时的错误码
        pre_progress = 0  # 设置初始解压进度为0
        code_find_error = False  # 判断是否已经在stdout中找到错误信息，如果已找到则不再读取进度信息

        while True:
            try:
                output = process.stdout.readline()
            except UnicodeDecodeError:  # UnicodeDecodeError: 'gbk' codec can't decode byte 0xaa in position 32: illegal multibyte sequence
                output = ''
            if output == '' and process.poll() is not None:
                break
            if output:
                # print('【7zip输出流：】', output.strip())
                # 查询错误信息
                match_wrong_pw = re.search('Wrong password', output)
                match_lost_volume = re.search('Missing volume', output) or re.search('Unexpected end of archive',
                                                                                     output)
                match_not_archive = re.search('Cannot open the file as', output)
                if match_wrong_pw:
                    stderr_error_code = '4-1'
                    code_find_error = True
                elif match_lost_volume:
                    stderr_error_code = '4-2'
                    code_find_error = True
                elif match_not_archive:
                    stderr_error_code = '4-3'
                    code_find_error = True
                # 查询进度信息
                if not code_find_error:
                    match_progress = re.search(r'(\d{1,3})% *\d* - ', output)  # 单文件时 34% - 061-090；多文件时 19% 10 - 031-060
                    if match_progress:
                        current_progress = int(match_progress.group(1))  # 提取进度百分比（不含%）
                        if current_progress > pre_progress:
                            # 更新进度ui
                            self.signal_update_ui.emit('3-4', [current_progress])
                            pre_progress = current_progress

        # 检查7zip的返回码
        """
        Code码	含义
        0	没有错误
        1	警告（非致命错误，例如被占用）
        2	致命错误
        7	命令行错误
        8	内存不足，无法进行操作
        255	用户已停止进程"""
        if process.poll() == 0:
            test_result = '4-7'
        elif process.poll() == 1:
            test_result = '4-4'
        elif process.poll() == 2:
            # 由于使用subprocess.Popen调用程序，返回码为2时的错误信息为"<_io.TextIOWrapper name=4 encoding='cp936'>"
            # 无法正确判断错误情况，所以需要在实时输出的错误信息流中进行判断操作
            test_result = stderr_error_code
        elif process.poll() == 8:
            test_result = '4-6'
        else:
            test_result = '4-5'
        return test_result

    @staticmethod
    def subprocess_7zip_run(command: list) -> Tuple[str, list]:
        """使用run方法调用7zip，并返回对应信息（专用于l和t指令）"""
        function_static.print_function_info()
        list_files = []
        process = subprocess.run(command,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 creationflags=subprocess.CREATE_NO_WINDOW,
                                 text=True,
                                 universal_newlines=True)

        if process.returncode == 0:
            test_result = '4-7'
            list_files = str(process.stdout).strip().split('\n')
        elif process.returncode == 1:
            test_result = '4-4'
        elif process.returncode == 2:
            text_stderr = str(process.stderr)
            if not text_stderr:  # 解压自解压程序时返回的err流可能为空
                test_result = '4-1'
            elif 'Wrong password' in text_stderr:
                test_result = '4-1'
            elif 'Missing volume' in text_stderr or 'Unexpected end of archive' in text_stderr:
                test_result = '4-2'
            elif 'Cannot open the file as' in str(process.stderr):
                test_result = '4-3'
            else:
                test_result = '4-5'
        elif process.returncode == 8:
            test_result = '4-6'
        else:
            test_result = '4-5'

        return test_result, list_files

    def check_nested_folders(self, target_folder: str, code_un_nest_dir: bool):
        """传入文件夹路径folder参数，将最深一级非空文件夹移动到target_folder的同级目录（处理套娃文件夹）
        可选参数 code_un_nest_dir:True 处理套娃文件夹；False 不处理套娃文件夹，仅做1次基础移动操作"""
        function_static.print_function_info()
        extract_dirname = os.listdir(target_folder)[0]  # 获取临时文件夹下自动创建的文件夹名
        extract_dirpath = os.path.normpath(os.path.join(target_folder, extract_dirname))  # 获取完整路径
        final_folder = os.path.split(target_folder)[0]

        if code_un_nest_dir:
            new_path = function_static.un_nest_folders(extract_dirpath, target_folder=final_folder)
        else:
            new_path = function_static.un_nest_folders(extract_dirpath, target_folder=final_folder, mode_nested=False)

        self.collect_extract_result(new_path)  # 收集解压结果

    def collect_extract_result(self, path: str):
        """传入文件/文件夹路径，保存解压结果（解压后的所有文件路径）的列表list，用于重复解压以处理嵌套压缩包"""
        function_static.print_function_info()
        extract_result = []
        if os.path.isfile(path):
            extract_result.append(path)
        else:
            extract_result = module.function_file.get_files_list(path)

        self.extracted_filelist += extract_result

    @staticmethod
    def save_pw_history(history_dict: dict = None):
        """保存记录到本地"""
        function_static.print_function_info()
        history_filetitle = '历史记录'
        history_suffix = '.txt'
        history_filename = history_filetitle + history_suffix

        if os.path.exists(history_filename) and os.path.getsize(history_filename) > 100 * 1024:  # 历史记录超过100kb则重置
            new_history_file = f'{backup_dir}/{history_filetitle} {time.strftime("%Y_%m_%d %H_%M_%S ", time.localtime())}{history_suffix}'
            shutil.move(history_filename, new_history_file)

        with open(history_filename, 'a', encoding='utf-8') as ha:
            add_text = ''
            for key in history_dict:
                add_text += f'■日期：{time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())} ' \
                            f'■文件路径：{key} ' \
                            f'■解压密码：{history_dict[key]}\n' \
                            f'--------------------------------------------\n'
            ha.write(add_text)

    def update_code_stop(self):
        function_static.print_function_info()
        self.code_stop = True


class ReadStd(QThread):
    def __init__(self, process_std):
        super().__init__()
        self.timeout = 10  # 超时时间，以毫秒为单位
        self.process_std = process_std
        self.std_readline = ''

    def run(self):
        self.std_readline = self.process_std.readline()

    def execute_with_timeout(self):
        self.start()
        self.wait(self.timeout)  # 等待超时时间（以毫秒为单位）

        if self.isRunning():
            # 如果线程仍在运行，表示超时
            self.std_readline = ''
            # self.quit()  # 不在这里退出，单独一个函数手动退出
        return self.std_readline
