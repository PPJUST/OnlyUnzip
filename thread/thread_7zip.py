# 7zip子线程
import os
import re
import subprocess

from PySide6.QtCore import QThread, Signal

from constant import _PASSWORD_FAKE, _TEMP_FOLDER, _PATH_7ZIP
from module import function_password, function_7zip, function_normal
from module.function_7zip import Result7zip
from module.function_config import GetSetting


class Thread7zip(QThread):
    # 运行信号
    signal_start = Signal()
    signal_stop = Signal()
    signal_finish = Signal()
    signal_finish_restart = Signal(list)
    # 进度信号
    signal_current_file = Signal(str)
    signal_schedule_file = Signal(str)
    signal_schedule_test = Signal(str)
    signal_schedule_extract = Signal(int)
    # 7zip调用结果信号
    signal_7zip_result = Signal(object)

    def __init__(self):
        super().__init__()
        self._is_stop_thread = False  # 是否终止线程
        self._file_dict = dict()  # dict结构：key为第一个分卷包路径/非分卷则为其本身，value为list，内部元素为其对应的所有分卷包
        # 读取密码
        self._passwords = None
        # 读取配置
        self._mode_extract = None
        self._extract_to_folder = None  # 解压到同名文件夹
        self._delete_file = None  # 解压后删除源文件
        self._handle_multi_folder = None  # 处理多层嵌套文件夹
        self._handle_multi_archive = None  # 处理多层嵌套压缩包
        self._output_folder = None  # 解压至指定目录
        self._filter_suffix = None  # 解压时排除的文件后缀

        # 最终解压结果列表，用于处理嵌套压缩文件（再次调用解压）
        self._extract_file_result = []

    def set_file_dict(self, file_dict: dict):
        """设置需要处理的文件字典"""
        self._file_dict = file_dict

    def stop(self):
        """停止线程"""
        self._is_stop_thread = True

    def _update_setting(self):
        """更新设置"""
        # 读取密码
        # 虚拟密码放首位，用于测试无密码文件，文件名中提取的密码放第二位，密码表的密码放最后
        passwords_filename = function_password.read_password_from_files(list(self._file_dict.keys()))
        self._passwords = [_PASSWORD_FAKE] + passwords_filename + function_password.read_password()
        # 读取配置
        self._mode_extract = GetSetting.mode_extract()
        self._extract_to_folder = GetSetting.extract_to_folder()  # 解压到同名文件夹
        self._delete_file = GetSetting.delete_file()  # 解压后删除源文件
        self._handle_multi_folder = GetSetting.handle_multi_folder()  # 处理多层嵌套文件夹
        self._handle_multi_archive = GetSetting.handle_multi_archive()  # 处理多层嵌套压缩包
        self._output_folder = GetSetting.output_folder()  # 解压至指定目录
        self._filter_suffix = ['-xr!*.' + i for i in GetSetting.filter_suffix().split(' ') if i]  # 解压时排除的文件后缀

    def run(self):
        pass
        self._is_stop_thread = False
        self._extract_file_result.clear()
        self._update_setting()

        # 发送开始信号，更新主程序ui
        self.signal_start.emit()

        # 逐个处理文件
        count_file = len(self._file_dict)
        for index, file_first in enumerate(self._file_dict, start=1):
            if not os.path.exists(file_first):
                continue
            if self._is_stop_thread:
                break
            # 发送当前文件以及进度文本信号
            self.signal_current_file.emit(os.path.basename(file_first))
            self.signal_schedule_file.emit(f'{index}/{count_file}')
            # 不论是测试模式还是解压模式，都先使用7zip的l命令进行一次测试（l命令在l/t/x中最快）
            # 在使用l命令前，先使用虚拟密码进行一次测试，判断该文件是否可以使用l命令进行正常测试
            fake_test_result, archive_info_dict = function_7zip.test_fake_password(file_first)
            if fake_test_result is True:  # 可以使用l命令进行后续测试
                self._test_file_command_l(file_first, self._passwords)
            elif fake_test_result is False:  # 无法使用l命令进行测试，执行对应模式操作
                if self._mode_extract:  # 使用x命令进行解压
                    self._extract_file(file_first, self._passwords)
                else:  # 使用t命令进行测试
                    paths_inside = archive_info_dict['paths']
                    if paths_inside:
                        check_path_inside = paths_inside[0]  # 仅测试一个文件即可
                    else:
                        check_path_inside = None
                    self._test_file(file_first, self._passwords, check_path_inside=check_path_inside)
            else:  # 文件本身存在问题，不进行后续操作
                self.signal_7zip_result.emit(fake_test_result)

            # 处理当前文件同目录的temp文件夹
            if self._mode_extract:
                self._delete_temp_folder(file_first)

        # 发送结束信号
        if self._is_stop_thread:
            self.signal_stop.emit()
        else:
            if self._mode_extract and self._handle_multi_archive:
                self.signal_finish_restart.emit(self._extract_file_result)
            else:
                self.signal_finish.emit()

    def _test_file(self, file, passwords, check_path_inside=None):
        """调用7zip的t命令测试文件"""
        count_password = len(passwords)
        result = Result7zip.WrongPassword  # 兜底
        for index_password, password in enumerate(passwords, start=1):
            if self._is_stop_thread:
                break
            self.signal_schedule_test.emit(f'{index_password}/{count_password}')
            result, _ = function_7zip.call_7zip('t', file, password, check_path_inside=check_path_inside)
            if not isinstance(result, Result7zip.WrongPassword):  # 测试结果不为“错误密码”时，确定正确密码
                break

        # 发送结果信号
        self.signal_7zip_result.emit(result)

    def _test_file_command_l(self, file, passwords):
        """调用7zip的l命令测试文件"""
        # 参照t测试的代码
        count_password = len(passwords)
        result = Result7zip.WrongPassword  # 兜底
        right_password = _PASSWORD_FAKE  # 兜底
        for index_password, password in enumerate(passwords, start=1):
            if self._is_stop_thread:
                break
            self.signal_schedule_test.emit(f'{index_password}/{count_password}')
            result, _ = function_7zip.call_7zip('l', file, password)
            if not isinstance(result, Result7zip.WrongPassword):  # 测试结果不为“错误密码”时，确定正确密码
                right_password = password
                break

        # 发送结果信号
        if isinstance(result, Result7zip.Success) and self._mode_extract:  # 如果是解压模式，则进行解压操作
            self._extract_file(file, right_password)
        else:
            self.signal_7zip_result.emit(result)

    def _extract_file(self, file, passwords):
        """解压文件"""
        if isinstance(passwords, str):
            passwords = [passwords]

        # 确认解压目录
        if self._output_folder:
            temp_folder = os.path.normpath(os.path.join(self._output_folder, _TEMP_FOLDER))
        else:  # 在该文件同级目录下创建临时文件夹
            temp_folder = os.path.normpath(os.path.join(os.path.dirname(file), _TEMP_FOLDER))
        filetitle = function_normal.get_filetitle(file)
        extract_folder = os.path.normpath(os.path.join(temp_folder, filetitle))

        # 调用7zip的x命令解压文件
        count_password = len(passwords)
        result = Result7zip.WrongPassword  # 兜底

        for index_password, password in enumerate(passwords, start=1):
            if self._is_stop_thread:
                break
            self.signal_schedule_test.emit(f'{index_password}/{count_password}')
            result = self._run_7zip_x(file, extract_folder, password)
            if not isinstance(result, Result7zip.WrongPassword):  # 结果不为“错误密码”时，确定正确密码
                break

        # 发送结果信号
        self.signal_7zip_result.emit(result)

        # 处理解压结果（如果成功解压）
        if isinstance(result, Result7zip.Success):
            # 删除源文件
            if self._delete_file:
                files_list = self._file_dict[file]
                function_normal.delete_files(files_list)

            # 智能解压/解压到同名文件夹和处理嵌套多层文件夹
            # 先确定需要移动的文件/文件夹路径
            need_move_path = extract_folder  # 兜底
            # 第1次判断（智能解压）
            # 智能解压，参照bandizip的逻辑
            listdir = os.listdir(extract_folder)
            if len(listdir) == 1:
                need_move_path = os.path.normpath(os.path.join(extract_folder, listdir[0]))
            # 第2次判断（处理嵌套多层文件夹）
            if self._handle_multi_folder:  # 处理嵌套多层文件夹，提取内部第一个多层文件夹路径
                need_move_path = function_normal.get_first_multi_path(extract_folder)
            # 再确定目标移动目录（临时文件夹同级+解压到同名文件夹）
            parent_folder = os.path.dirname(temp_folder)
            if self._extract_to_folder:
                # 生成不存在的无同名文件夹路径，防止移动至已存在的同名文件夹中
                target_folder = os.path.normpath(os.path.join(parent_folder, filetitle))
                target_folder = os.path.normpath(os.path.join(
                    parent_folder, function_normal.create_nodup_filename(target_folder, parent_folder)))
                # 如果解压目录下级只有一个文件夹，且该文件夹名称与目标文件夹名相同，则直接移动到目标文件夹父目录
                if len(listdir) == 1:
                    _path = os.path.normpath(os.path.join(extract_folder, listdir[0]))
                    if os.path.isdir(_path) and os.path.basename(_path) == os.path.basename(target_folder):
                        target_folder = parent_folder
            else:
                target_folder = parent_folder

            # 移动
            final_path = function_normal.move_file(need_move_path, target_folder)
            # 收集解压结果（用于处理嵌套压缩文件）
            self._extract_file_result.append(final_path)

        # 删除临时文件夹下的多余文件/文件夹
        function_normal.delete_empty_folder(extract_folder)

    def _run_7zip_x(self, file, extract_folder, password):
        """调用7zip的x命令解压文件，并读取输出流"""
        # 同时读取stdout和stderr会导致管道堵塞，需要将这流重定向至1个管道中，使用switch 'bso1','bsp1',bse1'
        _7zip_command = [_PATH_7ZIP, 'x', '-y', file,
                         '-bsp1', '-bse1', '-bso1',
                         '-o' + extract_folder,
                         '-p' + password] + self._filter_suffix

        # 调用
        print('测试 7zip命令', _7zip_command)
        process = subprocess.Popen(_7zip_command,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   creationflags=subprocess.CREATE_NO_WINDOW,
                                   text=True,
                                   universal_newlines=True)

        # 读取实时输出流
        # 使用subprocess.Popen调用7zip时，返回码为2时的错误信息为"<_io.TextIOWrapper name=4 encoding='cp936'>"
        # 无法正确判断错误情况，所以需要在实时输出的错误信息输出流中进行读取判断操作
        result_error = Result7zip.WrongPassword(file)  # 兜底，默认为“密码错误”
        pre_progress = 0  # 解压进度，初始化0
        is_read_stderr = True  # 是否读取stderr流，出现报错事件后/读取到进度信息后不需要再读取，节省性能
        is_read_progress = True  # 是否读取进度信息，出现报错事件后不需要再读取，节省性能

        while True:
            try:
                output = process.stdout.readline()
                print('【7zip解压信息：', output, '】')  # 测试用
            except UnicodeDecodeError:
                # 有时会报错编码错误
                # UnicodeDecodeError: 'gbk' codec can't decode byte 0xaa in position 32: illegal multibyte sequence
                output = ''
            if output == '' and process.poll() is not None:  # 读取到空文本或返回码时，结束读取操作
                break
            if output and is_read_stderr:  # 读取错误事件
                is_wrong_password = re.search('Wrong password', output)
                is_missing_volume = re.search('Missing volume', output)
                is_not_archive = re.search('Cannot open the file as', output)
                if is_wrong_password:
                    result_error = Result7zip.WrongPassword(file)
                    is_read_stderr = False
                    is_read_progress = False
                elif is_missing_volume:
                    result_error = Result7zip.MissingVolume(file)
                    is_read_stderr = False
                    is_read_progress = False
                elif is_not_archive:  # 后缀指定格式不正确时zip会自动尝试正确格式解压，所以不需要停止读取输出流
                    result_error = Result7zip.NotArchiveOrDamaged(file)

            if output and is_read_progress:  # 读取进度事件
                # 单文件输出信息：34% - 061-090；多文件输出信息：19% 10 - 031-060。适用正则表达式 '(\d{1,3})% *\d* - '
                # 某些压缩包的输出信息：80% 13。适用正则表达式 '(\d{1,3})% *\d*'
                match_progress = re.search(r'(\d{1,3})% *\d*', output)
                if match_progress:
                    is_read_stderr = False
                    current_progress = int(match_progress.group(1))  # 提取进度百分比（不含%）
                    if current_progress > pre_progress:
                        self.signal_schedule_extract.emit(current_progress)
                        pre_progress = current_progress  # 重置进度

        # 读取返回码
        if process.poll() == 0:  # 没有错误
            # 实测有个特例，某个压缩包为rar格式，后缀为zip格式，解压时不会处理任何内部文件，没有生成解压结果，最终报错
            if os.path.exists(extract_folder):
                result = Result7zip.Success(file, password)
            else:
                result = Result7zip.UnknownError(file)
        elif process.poll() == 1:  # 警告（非致命错误，例如被占用）
            result = Result7zip.FileOccupied(file)
        elif process.poll() == 2:  # 致命错误
            result = result_error
        elif process.poll() == 8:  # 内存不足，无法进行操作
            result = Result7zip.NotEnoughSpace(file)
        else:  # 兜底
            result = Result7zip.UnknownError(file)

        return result

    def _delete_temp_folder(self, file):
        """删除文件同级目录中的空临时文件夹"""
        if self._output_folder:
            temp_folder = os.path.normpath(os.path.join(self._output_folder, _TEMP_FOLDER))
        else:  # 在该文件同级目录下创建临时文件夹
            temp_folder = os.path.normpath(os.path.join(os.path.dirname(file), _TEMP_FOLDER))

        if os.path.exists(temp_folder):
            function_normal.delete_empty_folder(temp_folder)
