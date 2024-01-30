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
