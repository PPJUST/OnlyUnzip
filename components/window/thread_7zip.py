import os
import time

import lzytools.archive
import lzytools.file
from PySide6.QtCore import QThread, Signal

from common import function_7zip, function_move, function_file, function_filename
from common.class_7zip import Result7zip, ModelCoverFile, ModelExtract, ModelBreakFolder, Position, \
    TYPES_MODEL_EXTRACT, TYPES_MODEL_BREAK_FOLDER
from common.class_file_info import FileInfo, FileInfoList
from common.function_7zip import _7ZIP_PATH, FAKE_PASSWORD


class TemplateThread(QThread):
    """子线程模板"""
    StepInfo = Signal(str, name='步骤信息')
    SignalCurrentFile = Signal(str, name='当前处理的文件名')
    SignalTaskCount = Signal(int, name='需要处理的文件总数')
    SignalTaskIndex = Signal(int, name='当前处理的文件索引')
    SignalCurrentPw = Signal(str, name='当前使用的密码')
    SignalPwCount = Signal(int, name='待测试密码总数')
    SignalPwIndex = Signal(int, name='当前使用的密码索引')
    SignalResult = Signal(FileInfo, name='自定义文件信息类')
    SignalStart = Signal(name='开始')
    SignalFinish = Signal(FileInfoList, name='结束，传递最终的文件信息类清单')

    def __init__(self):
        super().__init__()
        self.fileinfo_task: FileInfoList = None  # 待处理的文件信息类清单
        self.passwords = list()  # 密码清单
        self.is_read_pw_from_filename = False  # 是否从文件名中读取密码
        self.is_stop_task = False  # 是否终止任务

    def set_task(self, task: FileInfoList):
        """设置任务清单"""
        print('设置任务清单')
        self.fileinfo_task = task

    def set_passwords(self, passwords: list):
        """设置密码清单"""
        print('设置密码清单')
        self.passwords = passwords.copy()

        if FAKE_PASSWORD not in self.passwords:
            self.passwords.insert(0, FAKE_PASSWORD)

    def set_is_read_pw_from_filename(self, is_enable: bool):
        """设置是否从文件名中读取密码"""
        self.is_read_pw_from_filename = is_enable

    def stop_task(self):
        """终止任务"""
        self.is_stop_task = True

    def _run_command_l_with_fake_password(self, file: str):
        """使用虚拟密码进行l指令测试，根据返回结果决定后续指令的使用
        :return:True，可以使用l指令进行测试
               False，不能使用l指令进行测试
               Result7zip类，测试出错，返回错误结果"""
        self.StepInfo.emit('压缩文件完整性测试...')
        print('虚拟密码测试')
        test_result = function_7zip.process_7zip_l(_7ZIP_PATH, file, FAKE_PASSWORD)
        # 如果是Success，则不信任测试结果，后续不再使用l命令测试
        if isinstance(test_result, Result7zip.Success):
            return False
        # 如果是Result7zip.WrongPassword，则继续使用l命令测试密码
        elif isinstance(test_result, Result7zip.WrongPassword):
            return True
        # 如果是Result7zip.WrongFiletype，则继续测试（暂定，有些后缀不对的压缩文件7zip会自动尝试正确的解压格式，不需要直接返回报错）
        # elif isinstance(test_result, Result7zip.WrongFiletype):
        #     return True
        # 如果是其他致命错误，则终止后续操作，直接返回该错误
        elif test_result in (Result7zip.WrongFiletype, Result7zip.Skip, Result7zip.Warning, Result7zip.MissingVolume,
                             Result7zip.UnknownError, Result7zip.ErrorCommand, Result7zip.NotEnoughMemory,
                             Result7zip.UserStopped):
            return test_result
        else:
            return False


class ThreadTest(TemplateThread):
    """测试子线程"""

    def __init__(self):
        super().__init__()
        self.is_write_filename = False
        self.write_left_part = ''
        self.write_right_part = ''
        self.write_position = Position.Left()

    def run(self):
        print('执行测试子线程')
        self.is_stop_task = False
        self.SignalStart.emit()
        self.SignalPwCount.emit(len(self.passwords))
        self.SignalTaskCount.emit(self.fileinfo_task.count())

        for index, file_info in enumerate(self.fileinfo_task.get_file_infos(), start=1):
            if self.is_stop_task:
                break
            else:
                pass

            self.SignalTaskIndex.emit(index)
            file_info: FileInfo
            file_first = file_info.filepath
            self.SignalCurrentFile.emit(file_first)
            print('当前处理的文件：', file_first)
            test_result = self.test_file(file_first, self.passwords)

            # 如果结果是成功，则进行进一步操作
            if isinstance(test_result, Result7zip.Success):
                # 是否将密码写入文件名
                if self.is_write_filename:
                    right_password = test_result.password
                    self._write_to_filename(file_info, right_password)

            # 将结果写入文件信息类，并发送信号
            file_info.set_7zip_result(test_result)
            if isinstance(test_result, Result7zip.Success):
                file_info.set_password(test_result.password)
            self.SignalResult.emit(file_info)

        # 结束后发送结束信号
        self.SignalFinish.emit(self.fileinfo_task)

    def test_file(self, filepath: str, passwords: list):
        """测试指定文件"""
        # 仅处理存在的文件
        if not os.path.exists(filepath):
            return Result7zip.Skip()

        # 根据选项是否提取文件名中可能存在的密码
        if self.is_read_pw_from_filename:
            _filetitle = lzytools.archive.get_filetitle(os.path.basename(filepath))
            pws_filename = function_filename.read_password_from_filename(_filetitle)
            for _pw in pws_filename:
                if _pw and _pw not in passwords:
                    passwords.append(_pw)

        # 先测试一次虚拟密码，根据测试结果选择使用l或t指令（l指令比t指令要快，优先使用l指令）
        print('测试模式 执行一次虚拟密码测试')
        fake_result = self._run_command_l_with_fake_password(filepath)
        # 提取内部最小的文件路径，l或t可以仅测试其中一个文件，以加快速度
        smallest_file_path_inside = function_7zip.get_smallest_file_in_archive(filepath)
        print(f"最小文件 {smallest_file_path_inside}")
        if fake_result is True:  # 可以使用l指令进行后续测试
            print('使用l指令进行密码测试')
            for index_pw, pw in enumerate(passwords, start=1):
                if self.is_stop_task:
                    break
                else:
                    pass
                self.SignalPwIndex.emit(index_pw)
                self.SignalCurrentPw.emit(pw)
                final_result = function_7zip.process_7zip_l(_7ZIP_PATH, filepath, pw, smallest_file_path_inside)
                # 如果测试结果是密码错误，则继续进行测试，否则直接中断
                if isinstance(final_result, Result7zip.WrongPassword):
                    continue
                else:
                    break
        elif fake_result is False:  # 不可以使用l指令，可以使用t指令
            print('使用t指令进行密码测试')
            for index_pw, pw in enumerate(passwords, start=1):
                if self.is_stop_task:
                    break
                else:
                    pass
                self.SignalPwIndex.emit(index_pw)
                self.SignalCurrentPw.emit(pw)
                final_result = function_7zip.process_7zip_t(_7ZIP_PATH, filepath, pw, smallest_file_path_inside)
                # 如果测试结果是密码错误，则继续进行测试，否则直接中断
                if isinstance(final_result, Result7zip.WrongPassword):
                    continue
                else:
                    break
        else:  # 是具体的结果类时，说明文件有问题，不进行后续测试
            print('虚拟密码测试检测出文件存在问题，不进行后续测试')
            final_result = fake_result

        # 返回最终结果
        return final_result

    def _write_to_filename(self, file_info: FileInfo, password: str):
        """将密码写入文件名"""
        # 如果密码为虚拟密码，则不进行写入
        if password == FAKE_PASSWORD:
            return
        # 组合密码部分
        position = self.write_position
        left_part = self.write_left_part
        right_part = self.write_right_part
        if isinstance(position, Position.Left) and not right_part:  # 防止密码与文件名之间没有间隔符号
            right_part = ' '
        elif isinstance(position, Position.Right) and not left_part:
            left_part = ' '
        pw_part = f'{left_part}{password}{right_part}'

        # 需要重命名的文件列表（写入文件名时，如果是分卷压缩文件组，则写入组中所有的文件）
        if file_info.related_files:
            files_need_to_change = list(file_info.related_files)
        else:
            files_need_to_change = [file_info.filepath]

        # 执行重命名
        for file in files_need_to_change:
            filename = os.path.basename(file)
            filetitle = lzytools.archive.get_filetitle(filename)
            extension = filename.replace(filetitle, '', 1)
            # 组合新的文件名
            if isinstance(position, Position.Left):
                new_filename = f'{pw_part}{filetitle}{extension}'
            elif isinstance(position, Position.Right):
                new_filename = f'{filetitle}{pw_part}{extension}'
            else:
                raise Exception('位置参数错误')
            # 重命名
            new_filepath = os.path.join(os.path.dirname(file), new_filename)
            os.rename(file, new_filepath)


class ThreadExtract(TemplateThread):
    """解压子线程"""

    def __init__(self):
        super().__init__()
        # 解压时参数
        self.cover_model: str = ''
        self.is_extract_to_folder: bool = False
        self.extract_output_path: str = ''
        self.is_filter: bool = False
        self.filter_rules: str = ''
        self.is_delete_file: bool = False

        # 解压后参数
        self.extract_model: TYPES_MODEL_EXTRACT = None  # 解压模式
        self.is_break_folder: bool = False  # 是否解散文件夹
        self.break_folder_model: TYPES_MODEL_BREAK_FOLDER = None

    def run(self):
        print('执行解压子线程')
        self.is_stop_task = False
        self.SignalStart.emit()
        self.SignalPwCount.emit(len(self.passwords))
        self.SignalTaskCount.emit(self.fileinfo_task.count())

        for index, file_info in enumerate(self.fileinfo_task.get_file_infos(), start=1):
            if self.is_stop_task:
                break
            else:
                pass

            self.SignalTaskIndex.emit(index)
            file_info: FileInfo
            file_first = file_info.filepath
            self.SignalCurrentFile.emit(file_first)
            print('当前处理的文件：', file_first)
            extract_result, extract_path = self.extract_file(file_first, self.passwords)

            # 将结果写入文件信息类，并发送信号
            file_info.set_7zip_result(extract_result)
            if isinstance(extract_result, Result7zip.Success):
                file_info.set_password(extract_result.password)
                file_info.set_extract_path(extract_path)
            self.SignalResult.emit(file_info)

        # 结束后发送结束信号
        self.SignalFinish.emit(self.fileinfo_task)

    def extract_file(self, filepath: str, passwords: list):
        # 仅处理存在的文件
        if not os.path.exists(filepath):
            return Result7zip.Skip()

        # 根据选项是否提取文件名中可能存在的密码
        if self.is_read_pw_from_filename:
            _filetitle = lzytools.archive.get_filetitle(os.path.basename(filepath))
            pws_filename = function_filename.read_password_from_filename(_filetitle)
            for _pw in pws_filename:
                if _pw not in passwords:
                    passwords.append(_pw)

        # 先测试一次虚拟密码，根据测试结果选择使用的指令
        print('解压模式 执行一次虚拟密码测试')
        fake_result = self._run_command_l_with_fake_password(filepath)
        if fake_result is True:  # 可以使用l指令进行后续测试
            print('使用l指令进行密码测试，并在找到密码后进行解压')
            final_result, extract_path = self.extract_after_test_l(filepath, passwords)
        elif fake_result is False:  # 不使用lt指令，直接使用x指令尝试解压
            print('直接使用x指令尝试解压')
            final_result, extract_path = self.extract_with_test_x(filepath, passwords)
        else:  # 压缩文件存在致命错误，不进行后续操作
            print('虚拟密码测试检测出文件存在问题，不进行后续测试')
            final_result = fake_result
            extract_path = None

        return final_result, extract_path

    def extract_after_test_l(self, filepath: str, passwords: list):
        """使用l命令进行测试，并在搜索到正确密码后执行解压操作，返回最终结果类"""
        # 提取内部最小的文件路径，l或t可以仅测试其中一个文件，以加快速度
        self.StepInfo.emit('压缩文件完整性测试...')
        smallest_file_path_inside = function_7zip.get_smallest_file_in_archive(filepath)
        # 先测试，找到密码后再解压
        final_result = None  # 最终结果
        extract_path = None  # 如果成功处理，则为解压后最终的路径
        for index_pw, pw in enumerate(passwords, start=1):
            if self.is_stop_task:
                break
            else:
                pass

            self.SignalPwIndex.emit(index_pw)
            self.SignalCurrentPw.emit(pw)
            final_result = function_7zip.process_7zip_l(_7ZIP_PATH, filepath, pw, smallest_file_path_inside)
            # 如果搜索到了正确密码，则进行解压操作
            if isinstance(final_result, Result7zip.Success):
                true_password = pw
                final_result, extract_path = self.extract(filepath, true_password)
                break
            # 如果是测试结果是密码错误，则继续搜索
            elif isinstance(final_result, Result7zip.WrongPassword):
                pass
            # 如果测试结果是其他报错，则直接中断
            else:
                break

        return final_result, extract_path

    def extract_with_test_x(self, filepath: str, passwords: list):
        """使用x指令进行密码测试，并返回最终结果类"""
        # 进行一次特殊处理，有些内部文件名未加密的压缩文件，在使用x命令测试时会遍历所有文件，而不是仅检查其中的一部分文件，在这种情况下使用t命令的速度更快
        # 所以先用虚拟密码和t指令测试一次，计算其耗时，再和后续的x指令耗时相比较，如果t指令耗时较短则使用t指令进行后续测试
        start_time = time.time()
        self.StepInfo.emit('压缩文件完整性测试...')
        final_result = function_7zip.process_7zip_t(_7ZIP_PATH, filepath, FAKE_PASSWORD)
        runtime_t = time.time() - start_time  # t命令的耗时

        is_continue_with_t = False  # 如果t命令耗时更短则使用t指令进行后续操作
        extract_path = None  # 如果成功处理，则为解压后最终的路径
        # 使用x命令解压
        for index_pw, pw in enumerate(passwords, start=1):
            if self.is_stop_task:
                break
            else:
                pass

            if is_continue_with_t:
                break

            self.SignalPwIndex.emit(index_pw)
            self.SignalCurrentPw.emit(pw)
            start_time = time.time()
            final_result, extract_path = self.extract(filepath, pw)
            runtime_x = time.time() - start_time  # x命令的耗时
            # 如果解压返回结果为成功，则退出循环
            if isinstance(final_result, Result7zip.Success):
                break
            # 如果是解压返回结果是密码错误，则继续搜索
            elif isinstance(final_result, Result7zip.WrongPassword):
                pass
            # 如果是其他报错，则直接退出循环
            else:
                break

            # 对比耗时，使用耗时更短的指令
            if runtime_t < runtime_x:
                is_continue_with_t = True

        # 切换为t指令
        if is_continue_with_t:
            for index_pw, pw in enumerate(passwords, start=1):
                if self.is_stop_task:
                    break
                else:
                    pass

                self.SignalPwIndex.emit(index_pw)
                self.SignalCurrentPw.emit(pw)
                final_result = function_7zip.process_7zip_t(_7ZIP_PATH, filepath, pw)
                # 如果搜索到了正确密码，则进行解压操作
                if isinstance(final_result, Result7zip.Success):
                    final_result, extract_path = self.extract(filepath, pw)
                    break
                # 如果是测试结果是密码错误，则继续搜索
                elif isinstance(final_result, Result7zip.WrongPassword):
                    pass
                # 如果测试结果是其他报错，则直接中断
                else:
                    break

        return final_result, extract_path

    def extract(self, file, password):
        """解压操作"""
        # 提取命令行参数
        # 覆盖选项
        if isinstance(self.cover_model, str):
            part_cover = self.cover_model
        elif isinstance(self.cover_model, (ModelCoverFile.RenameOld,
                                           ModelCoverFile.RenameNew,
                                           ModelCoverFile.Skip,
                                           ModelCoverFile.Overwrite)):
            part_cover = self.cover_model.switch
        else:
            raise Exception('覆盖模式参数错误')

        # 解压路径
        if self.is_extract_to_folder and self.extract_output_path:
            part_extract_to = self.extract_output_path
        else:
            part_extract_to = os.path.dirname(file)
        print('part_extract_to', self.is_extract_to_folder, self.extract_output_path)

        # 过滤器规则
        if self.is_filter and self.filter_rules:
            filter_rule = self.filter_rules
        else:
            filter_rule = ''

        result_7zip = function_7zip.progress_7zip_x_with_temp_folder(_7ZIP_PATH, file, password,
                                                                     cover_model=part_cover,
                                                                     output_folder=part_extract_to,
                                                                     filter_rule=filter_rule)

        # 提取原文件的文件名（剔除压缩文件后缀格式）
        filename_origin = lzytools.archive.get_filetitle(os.path.basename(file))

        # 如果处理成功，则进行进一步处理
        if isinstance(result_7zip, Result7zip.Success):
            # 根据对应模式移动临时文件夹下的文件/文件夹
            self.StepInfo.emit('解压完成，移出临时文件夹中...')
            temp_folder = function_7zip.get_temp_dirpath(part_extract_to)  # 要移动的文件夹
            parent_folder = os.path.dirname(temp_folder)  # 移动至该文件夹下
            if isinstance(self.extract_model, ModelExtract.Smart):
                extract_path = function_move.move_to_smart(temp_folder, parent_folder, dirname_=filename_origin)
            elif isinstance(self.extract_model, ModelExtract.SameFolder):
                extract_path = function_move.move_to_same_dirname(temp_folder, parent_folder, dirname_=filename_origin)
            elif isinstance(self.extract_model, ModelExtract.Direct):
                extract_path = function_move.move_to_no_deal(temp_folder, parent_folder)
            else:
                extract_path = None
            # 是否解散文件夹（仅在解压结果为文件夹时才执行）
            if self.is_break_folder:
                self.StepInfo.emit('解压完成，解散文件夹中...')
                if os.path.isdir(extract_path):
                    if isinstance(self.break_folder_model, ModelBreakFolder.MoveToTop):
                        extract_path = function_file.break_folder_top(extract_path)
                    elif isinstance(self.break_folder_model, ModelBreakFolder.MoveBottom):
                        extract_path = function_file.break_folder_bottom(extract_path)
                    elif isinstance(self.break_folder_model, ModelBreakFolder.MoveFiles):
                        extract_path = function_file.break_folder_files(extract_path)
                    else:
                        pass
            # 是否删除原文件（删除同组中的全部文件）
            file_info = self.fileinfo_task.get_file_info(file)
            related_files = file_info.related_files
            if self.is_delete_file:
                for i in related_files:
                    lzytools.file.delete(i, send_to_trash=True)

            # 删除空的临时解压文件夹
            guess_temp_folder = function_7zip.get_temp_dirpath(part_extract_to)
            if os.path.exists(guess_temp_folder) and not lzytools.file.get_size(guess_temp_folder):
                lzytools.file.delete(guess_temp_folder)

            print("处理文件:", file, "处理结果", result_7zip, "解压路径", extract_path)
            return result_7zip, extract_path
        else:
            # 删除空的临时解压文件夹
            guess_temp_folder = function_7zip.get_temp_dirpath(part_extract_to)
            if self.is_stop_task:  # 如果是由于用户主动终止而导致任务终止的，则删除整个临时文件夹（不管临时文件夹是否为空）
                if os.path.exists(guess_temp_folder):
                    lzytools.file.delete(guess_temp_folder)
            else:  # 否则，仅在临时文件夹为空时删除该文件夹
                if os.path.exists(guess_temp_folder) and not lzytools.file.get_size(guess_temp_folder):
                    lzytools.file.delete(guess_temp_folder)

            return result_7zip, None
