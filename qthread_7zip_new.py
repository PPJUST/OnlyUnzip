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
import module.function_password
from constant import _PATH_7ZIP, _PASSWORD_NONE, _Unzip_Temp_Folder
from module import function_static, function_password, function_archive
from module.class_state import State7zResult, StateUpdateUI
from module.function_config import Config

os.environ["PYTHONIOENCODING"] = "UTF-8"
config_file = 'config.ini'
backup_dir = 'backup'


class Thread7z(QThread):
    signal_schedule = Signal()

    def __init__(self):
        super().__init__()
        self.file_dict = {}  # 需要处理的文件字典，{文件路径:(文件路径,...)..}

    def reset_file_dict(self, file_dict: dict):
        """重置参数"""
        self.file_dict = file_dict

    def reset_args(self):
        """重置参数"""
        pass

    def run(self):
        mode = Config().mode
        passwords = function_password.read_passwords()
        exclude_rules = Config().exclude_rules
        output_folder = Config().output_folder
        handling_nested_folder = Config().handling_nested_folder

        for index, file in enumerate(self.file_dict.keys(), start=1):
            # 不论哪个模式，都先使用7z的l命令进行测试
            # 先使用临时密码测试，如果返回成功则说明该文件无法使用l指令进行正常测试（无密码或者内部文件名未加密）
            # 如果返回其余情况，则按不同情况进行单独处理
            result_fake = self.test_fake_password(file)
            if result_fake is  True:  # 使用l命令寻找密码，找到正确密码后直接进行处理

                right_password= _PASSWORD_NONE
                for password in passwords:
                    result = function_archive.subprocess_run_7z('l', file, password)
                    if type(result) is State7zResult.Success:  # 找到正确密码
                        right_password = result.password
                        if mode == 'test':
                            self.signal_schedule.emit(result)
                        elif mode == 'extract':
                            result = self.extract_file(file, right_password,exclude_rules, output_folder)
                            self.signal_schedule.emit(result)
                        break
                if right_password == _PASSWORD_NONE:  # 没有找到正确密码
                    self.signal_schedule.emit(State7zResult.WrongPassword(file))
                    continue

            elif type(result_fake) in State7zResult.__dict__.values():  # 文件本身存在问题，跳过
                self.signal_schedule.emit(result_fake)
                continue

            else:  # 无法使用l命令，执行一般流程
                if mode == 'test':
                    for password in passwords:
                        result = function_archive.subprocess_7z_t(file, password)
                        if type(result) is State7zResult.WrongPassword:
                            continue
                        else:
                            self.signal_schedule.emit(result)
                            break
                elif mode == 'extract':
                    for password in passwords:
                        result = self.extract_file(file, password,exclude_rules, output_folder)
                        if type(result) is State7zResult.WrongPassword:
                            continue
                        else:
                            self.signal_schedule.emit(result)
                            break



    def test_fake_password(self, file):
        """使用临时密码测试文件，判断是否进行进一步操作
        :return: True: 可以使用l命令进行测试；
                 State7zResult类: 文件本身存在问题；
                 False: 不能使用l命令进行测试。
        """
        result_fake = function_archive.subprocess_run_7z('l', file, _PASSWORD_NONE)

        # 返回密码错误。则说明可以使用l命令进行测试
        if type(result_fake) is State7zResult.WrongPassword:
            return True
        # 返回文件占用/非压缩文件/空间不足/缺失分卷/未知错误，则说明文件本身存在问题
        elif type(result_fake) in [State7zResult.NotArchiveOrDamaged,
             State7zResult.FileOccupied,
             State7zResult.NotEnoughSpace,
             State7zResult.UnknownError,
             State7zResult.MissingVolume]:
            return result_fake
        # 返回成功，则不信赖l命令的结果
        elif type(result_fake) is State7zResult.Success:
            return False

    def extract_file(self, file, password,exclude_rules=(), output_folder=None, handling_nested_folder=False):
        """解压文件"""
        # 生成解压目标路径
        filetitle = function_static.get_filetitle(file)
        if output_folder:
            temp_folder = os.path.normpath(os.path.join(output_folder, _Unzip_Temp_Folder))
        else:  # 如果未指定输出文件夹，则输出路径为文件同级目录下的临时文件夹的文件名文件夹
            parent_folder = os.path.split(file)[0]
            temp_folder = os.path.normpath(os.path.join(parent_folder, _Unzip_Temp_Folder))
        extract_folder = os.path.normpath(os.path.join(temp_folder, filetitle))

        # 调用7z
        result =  self.process_7z_extract(file, password, exclude_rules,extract_folder)

        # 处理套娃文件夹
        if handling_nested_folder:




    def process_7z_extract(self, file, password, exclude_rules,output_folder):
        """使用popen方法调用7z进行解压操作，并实时发送进度信息"""
        # 同时读取stdout和stderr会导致管道堵塞，需要将这3个流重定向至1个管道中，使用switch 'bso1','bsp1',bse1'
        command = [_PATH_7ZIP,
                   'x',
                   'y',
                   file,
                   '-bsp1', '-bse1', '-bso1',
                   '-o' + output_folder,
                   '-p' + password]
        exclude_rules_str = ['-xr!*.' + i for i in exclude_rules if i]
        command += exclude_rules_str
        process = subprocess.Popen(command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   creationflags=subprocess.CREATE_NO_WINDOW,
                                   text=True,
                                   universal_newlines=True)

        # 读取信息流
        result_error = State7zResult.WrongPassword(file)  # 假设错误时的错误类
        pre_progress = 0  # 设置初始解压进度为0
        is_read_stderr = True  # 是否读取stderr流
        is_read_progress = True # 是否读取进度信息

        while True:
            try:
                output = process.stdout.readline()
            except UnicodeDecodeError:  # 编码错误 UnicodeDecodeError: 'gbk' codec can't decode byte 0xaa in position 32: illegal multibyte sequence
                output = ''
            if output == '' and process.poll() is not None:  # 终止事件
                break
            if output and is_read_stderr:  # 错误事件
                is_wrong_password = re.search('Wrong password', output)
                is_missing_volume = (re.search('Missing volume', output) or
                                     re.search('Unexpected end of archive',output))
                is_not_archive = re.search('Cannot open the file as', output)
                if is_wrong_password:
                    result_error = State7zResult.WrongPassword(file)
                    is_read_stderr = False
                    is_read_progress = False
                elif is_missing_volume:
                    result_error = State7zResult.MissingVolume(file)
                    is_read_stderr = False
                    is_read_progress = False
                elif is_not_archive:
                    result_error = State7zResult.NotArchiveOrDamaged(file)
                    is_read_stderr = False
                    is_read_progress = False

            if output and is_read_progress:  # 进度事件
                match_progress = re.search(r'(\d{1,3})% *\d* - ',
                                           output)  # 单文件输出信息：34% - 061-090；多文件输出信息：19% 10 - 031-060
                if match_progress:
                    is_read_stderr = False
                    current_progress = int(match_progress.group(1))  # 提取进度百分比（不含%）
                    if current_progress > pre_progress:
                        self.signal_schedule.emit(StateUpdateUI.ScheduleExtract(current_progress))  # 发送进度信号
                        pre_progress = current_progress

        # 检查7z返回码
        """7z.exe返回值代码
        Code码	含义
        0	没有错误
        1	警告（非致命错误，例如被占用）
        2	致命错误
        7	命令行错误
        8	内存不足，无法进行操作
        255	用户已停止进程
        """
        if process.poll() == 0:
            result = State7zResult.Success(file, password)
        elif process.poll() == 1:
            result = State7zResult.FileOccupied(file)
        elif process.poll() == 2:
            # 使用subprocess.Popen调用7z，返回码为2时的错误信息为"<_io.TextIOWrapper name=4 encoding='cp936'>"
            # 无法正确判断错误情况，所以需要在实时输出的错误信息流中进行判断操作
            result = result_error
        elif process.poll() == 8:
            result = State7zResult.NotEnoughSpace(file)
        else:
            result = State7zResult.UnknownError(file)

        return result
