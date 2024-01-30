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

        for index, file in enumerate(self.file_dict.keys(), start=1):
            # 不论哪个模式，都先使用7z的l命令进行测试
            # 先使用临时密码测试，如果返回成功则说明该文件无法使用l指令进行正常测试（无密码或者内部文件名未加密）
            # 如果返回其余情况，则按不同情况进行单独处理
            right_password_by_l = _PASSWORD_NONE  # 尝试使用l指令寻找的正确密码
            result_fake = function_archive.subprocess_run_7z('l', file, _PASSWORD_NONE)
            if type(result_fake) is  State7zResult.WrongPassword:  # 返回密码错误。则继续使用密码字典寻找正确密码
                test_passwords = function_password.read_passwords()
                for password in test_passwords:
                    result = function_archive.subprocess_run_7z('l', file, password)
                    if type(result) is State7zResult.Success:  # 找到正确密码
                        right_password_by_l = result.password
                        break
            elif type(result_fake) is  State7zResult.FileOccupied:  # 返回文件占用，则不再处理该文件
                pass  # 备忘录
            elif type(result_fake) is State7zResult.NotArchiveOrDamaged:
                pass
            elif type(result_fake) is State7zResult.UnknownError:
                pass

            if right_password_by_l != _PASSWORD_NONE:  # 如果找到了正确密码，则直接按正确密码执行
                if mode == 'test':
                    self.signal_schedule.emit(State7zResult.Success(file, right_password_by_l))
                elif mode == 'extract':
                    pass # 备忘录
            else:  # 未找到则按正常流程执行
                pass

    def extract_archive(self):
        """解压文件"""



    def process_7z_extract(self, file, password, exclude_rules,output_folder=None):
        """使用popen方法调用7z进行解压操作，并实时发送进度信息"""
        # 同时读取stdout和stderr会导致管道堵塞，需要将这3个流重定向至1个管道中，使用switch 'bso1','bsp1',bse1'
        if output_folder:
            output_folder = os.path.normpath(os.path.join(output_folder,_Unzip_Temp_Folder))  # 输出的临时文件夹
            extract_folder = os.path.normpath(os.path.join(output_folder, filetitle))  # 生成解压文件夹的路径


        command = [_PATH_7ZIP,
                   'x',
                   'y',
                   file,
                   '-bsp1', '-bse1', '-bso1',
                   '-o' + output_folder,
                   '-p' + password]
        command += exclude_rules
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
