import os
import re
import subprocess

import send2trash  # win7不能使用winshell，用send2trash替代
from PySide6.QtCore import Signal, QThread

from constant import _PATH_7ZIP, _PASSWORD_NONE, _Unzip_Temp_Folder
from module import function_file, function_normal
from module import function_password, function_archive
from module.class_state import State7zResult, StateUpdateUI, StateSchedule
from module.function_config import Config

os.environ["PYTHONIOENCODING"] = "UTF-8"


class Thread7z(QThread):
    signal_schedule = Signal(object)

    def __init__(self):
        super().__init__()
        self.file_dict = {}  # 需要处理的文件字典，{文件路径:(文件路径,...)..}

    def reset_file_dict(self, file_dict: dict):
        """重置参数"""
        function_normal.print_function_info()
        self.file_dict = file_dict

    def run(self):
        function_normal.print_function_info()
        # 读取参数
        mode = Config().mode
        passwords = [_PASSWORD_NONE] + function_password.read_passwords()  # 插入一个假密码，用于判断无密码压缩文件
        exclude_rules = Config().exclude_rules
        output_folder = Config().output_folder if os.path.exists(Config().output_folder) else None
        handling_nested_folder = Config().handling_nested_folder
        delete_original_file = Config().delete_original_file
        # 发送开始信号
        if mode == 'test':
            self.signal_schedule.emit(StateSchedule.RunningTest())
        elif mode == 'extract':
            self.signal_schedule.emit(StateSchedule.RunningExtract())

        pre_temp_folder = None  # 上一个处理的文件生成的temp文件夹目录，用于删除

        for index_file, file in enumerate(self.file_dict.keys(), start=1):
            self.signal_schedule.emit(StateUpdateUI.CurrentFile(file))
            self.signal_schedule.emit(StateUpdateUI.ScheduleTotal(f'{index_file} / {len(self.file_dict)}'))
            # 不论哪个模式，都先使用7z的l命令进行测试
            # 先使用临时密码测试，如果返回成功则说明该文件无法使用l指令进行正常测试（无密码或者内部文件名未加密）
            # 如果返回其余情况，则按不同情况进行单独处理
            result_fake = self.test_fake_password(file)
            if result_fake is True:  # 使用l命令寻找密码，找到正确密码后直接进行处理
                right_password = _PASSWORD_NONE
                for index_pw, password in enumerate(passwords):
                    self.signal_schedule.emit(StateUpdateUI.ScheduleTest(f'{index_pw} / {len(passwords)}'))
                    is_continue = self.test_file(file, password, command_type='l')
                    if not is_continue:
                        right_password = password
                        if mode == 'extract':
                            self.extract_file(file, right_password, None, exclude_rules, output_folder,
                                              handling_nested_folder, delete_original_file)
                        break
                if right_password == _PASSWORD_NONE:  # 没有找到正确密码
                    continue

            elif type(result_fake) in State7zResult.__dict__.values():  # 文件本身存在问题，跳过
                self.signal_schedule.emit(result_fake)
                continue

            else:  # 无法使用l命令，执行一般流程
                if mode == 'test':
                    for index_pw, password in enumerate(passwords):
                        self.signal_schedule.emit(StateUpdateUI.ScheduleTest(f'{index_pw} / {len(passwords)}'))
                        is_continue = self.test_file(file, password)
                        if not is_continue:
                            break
                elif mode == 'extract':
                    files_list = self.file_dict[file]
                    for index_pw, password in enumerate(passwords):
                        self.signal_schedule.emit(StateUpdateUI.ScheduleTest(f'{index_pw} / {len(passwords)}'))
                        is_continue = self.extract_file(file, password, files_list, exclude_rules, output_folder,
                                                        handling_nested_folder, delete_original_file)
                        if not is_continue:
                            break

            # 处理temp文件夹
            if mode == 'extract':
                if output_folder and index_file == len(self.file_dict):
                    current_temp_folder = os.path.normpath(os.path.join(os.path.split(file)[0], _Unzip_Temp_Folder))
                    function_file.delete_empty_folder(current_temp_folder)
                elif not output_folder:
                    if not pre_temp_folder:
                        pre_temp_folder = os.path.normpath(os.path.join(os.path.split(file)[0], _Unzip_Temp_Folder))
                    current_temp_folder = os.path.normpath(os.path.join(os.path.split(file)[0], _Unzip_Temp_Folder))
                    if current_temp_folder != pre_temp_folder:
                        function_file.delete_empty_folder(pre_temp_folder)
                        pre_temp_folder = current_temp_folder
                    if index_file == len(self.file_dict):
                        function_file.delete_empty_folder(current_temp_folder)

        # 发送结束信号
        self.signal_schedule.emit(StateSchedule.Finish())

    @staticmethod
    def test_fake_password(file):
        """使用临时密码测试文件，判断是否进行进一步操作
        :return: True: 可以使用l命令进行测试；
                 State7zResult类: 文件本身存在问题；
                 False: 不能使用l命令进行测试。
        """
        function_normal.print_function_info()
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

    def test_file(self, file, password, command_type='t'):
        """测试文件
        :return: bool值，是否继续"""
        function_normal.print_function_info()
        if command_type == 't':
            result = function_archive.subprocess_7z_t(file, password)
        else:
            result = function_archive.subprocess_7z_l(file, password)
        self.signal_schedule.emit(result)

        if type(result) is State7zResult.WrongPassword:
            return True
        else:
            return False

    def extract_file(self, file, password, files_list=None, exclude_rules=(), output_folder=None,
                     handling_nested_folder=False, delete_original_file=False):
        """解压文件，并进行后续相关操作
        :return: bool值，是否继续"""
        function_normal.print_function_info()
        if not files_list:
            files_list = [file]

        # 生成解压目标路径
        filetitle = function_file.get_filetitle(file)
        if output_folder:
            temp_folder = os.path.normpath(os.path.join(output_folder, _Unzip_Temp_Folder))
        else:  # 如果未指定输出文件夹，则输出路径为文件同级目录下的临时文件夹的文件名文件夹
            parent_folder = os.path.split(file)[0]
            temp_folder = os.path.normpath(os.path.join(parent_folder, _Unzip_Temp_Folder))
        extract_folder = os.path.normpath(os.path.join(temp_folder, filetitle))

        # 调用7z
        result = self.process_7z_extract(file, password, exclude_rules, extract_folder)
        self.signal_schedule.emit(result)

        # 检查结果
        if type(result) is State7zResult.Success:
            # 是否删除原文件
            if delete_original_file:
                for i in files_list:
                    send2trash.send2trash(i)
            # 是否处理套娃文件夹
            top_folder = os.path.split(temp_folder)[0]
            if handling_nested_folder:
                # 移动内部首个多重文件夹/唯一文件
                move_path = function_file.get_first_multi_folder(extract_folder)
                function_file.move_file(move_path, top_folder)
                # 删除多余文件夹（temp文件夹不在此清理）
                function_file.delete_empty_folder(extract_folder)
            else:  # 类似于bandizip自动解压的文件夹逻辑
                listdir = os.listdir(extract_folder)
                if len(listdir) == 1:
                    # 移动下级路径
                    move_path = os.path.join(extract_folder, listdir[0])
                    function_file.move_file(move_path, top_folder)
                    # 删除多余文件夹（temp文件夹不在此清理）
                    function_file.delete_empty_folder(extract_folder)
                else:
                    function_file.move_file(extract_folder, top_folder)
            return False
        elif type(result) is State7zResult.WrongPassword:
            return True
        else:
            return False

    def process_7z_extract(self, file, password, exclude_rules, output_folder):
        """使用popen方法调用7z进行解压操作，并实时发送进度信息"""
        function_normal.print_function_info()
        # 同时读取stdout和stderr会导致管道堵塞，需要将这3个流重定向至1个管道中，使用switch 'bso1','bsp1',bse1'
        command = [_PATH_7ZIP,
                   'x',
                   '-y',
                   file,
                   '-bsp1', '-bse1', '-bso1',
                   '-o' + output_folder,
                   '-p' + password]
        print(command)
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
        is_read_progress = True  # 是否读取进度信息

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
                                     re.search('Unexpected end of archive', output))
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
