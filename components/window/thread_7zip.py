import os
import time
from typing import Union

import lzytools.file
from PySide6.QtCore import QThread, Signal

from common import function_7zip, function_move, function_file
from common.class_7zip import Result7zip, ModelCoverFile, ModelExtract, ModelBreakFolder
from common.class_file_info import FileInfo, FileInfoList

_FAKE_PASSWORD = 'FAKEPASSWORD'
_7ZIP_PATH = r'./7-Zip/7z.exe'


class TemplateThread(QThread):
    """子线程模板"""
    SignalCurrentFile = Signal(str, name='当前处理的文件名')
    SignalTaskCount = Signal(int, name='需要处理的文件总数')
    SignalTaskIndex = Signal(int, name='当前处理的文件索引')
    SignalPwCount = Signal(int, name='待测试密码总数')
    SignalPwIndex = Signal(int, name='当前使用的密码索引')
    SignalResult = Signal(FileInfo, name='自定义文件信息类')
    SignalStart = Signal(name='开始')
    SignalFinish = Signal(FileInfoList, name='结束，传递最终的文件信息类清单')

    def __init__(self):
        super().__init__()
        self.fileinfo_task: FileInfoList = None  # 待处理的文件信息类清单
        self.passwords = list()  # 密码清单

    def set_task(self, task: FileInfoList):
        """设置任务清单"""
        print('设置任务清单')
        self.fileinfo_task = task

    def set_passwords(self, passwords: list):
        """设置密码清单"""
        print('设置密码清单')
        self.passwords = passwords.copy()

        if _FAKE_PASSWORD not in self.passwords:
            self.passwords.insert(0,_FAKE_PASSWORD)



    def _run_command_l_with_fake_password(self, file: str):
        """使用虚拟密码进行l指令测试，根据返回结果决定后续指令的使用
        :return:True，可以使用l指令进行测试
               False，不能使用l指令进行测试
               Result7zip类，测试出错，返回错误结果"""
        print('虚拟密码测试')
        test_result = function_7zip.process_7zip_l(_7ZIP_PATH, file, _FAKE_PASSWORD)
        # 如果是Success，则不信任测试结果，后续不再使用l命令测试
        if isinstance(test_result, Result7zip.Success):
            return False
        # 如果是Result7zip.WrongPassword，则继续使用l命令测试密码
        elif isinstance(test_result, Result7zip.WrongPassword):
            return True
        # 如果是Result7zip.WrongFiletype，则继续测试（暂定，有些后缀不对的压缩文件7zip会自动尝试正确的解压格式，不需要直接返回报错）
        elif isinstance(test_result, Result7zip.WrongFiletype):
            return True
        # 如果是其他致命错误，则终止后续操作，直接返回该错误
        elif test_result in (Result7zip.Skip, Result7zip.Warning, Result7zip.MissingVolume, Result7zip.UnknownError,
                             Result7zip.ErrorCommand, Result7zip.NotEnoughMemory, Result7zip.UserStopped):
            return test_result
        else:
            return False


class ThreadTest(TemplateThread):
    """测试子线程"""

    def run(self):
        print('执行测试子线程')
        self.SignalStart.emit()
        self.SignalPwCount.emit(len(self.passwords))
        self.SignalTaskCount.emit(self.fileinfo_task.count())

        for index, file_info in enumerate(self.fileinfo_task.get_file_infos(), start=1):
            self.SignalTaskIndex.emit(index)
            file_info: FileInfo
            file_first = file_info.filepath
            self.SignalCurrentFile.emit(file_first)
            print('当前处理的文件：', file_first)
            test_result = self.test_file(file_first, self.passwords)

            # 将结果写入文件信息类，并发送信号
            file_info.set_7zip_result(test_result)
            self.SignalResult.emit(file_info)

        # 结束后发送结束信号
        self.SignalFinish.emit(self.fileinfo_task)

    def test_file(self, filepath: str, passwords: list):
        """测试指定文件"""
        # 仅处理存在的文件
        if not os.path.exists(filepath):
            return Result7zip.Skip()

        # 先测试一次虚拟密码，根据测试结果选择使用l或t指令（l指令比t指令要快，优先使用l指令）
        print('执行一次虚拟密码测试')
        fake_result = self._run_command_l_with_fake_password(filepath)
        # 备忘录 提取内部路径，l或t可以仅测试其中一个文件
        if fake_result is True:  # 可以使用l指令进行后续测试
            print('使用l指令进行密码测试')
            for index_pw, pw in enumerate(passwords, start=1):
                self.SignalPwIndex.emit(index_pw)
                final_result = function_7zip.process_7zip_l(_7ZIP_PATH, filepath, pw)
                # 如果结果是成功，则寻找到正确密码，否则继续进行测试
                if isinstance(final_result, Result7zip.Success):
                    break
        elif fake_result is False:  # 不可以使用l指令，可以使用t指令
            print('使用t指令进行密码测试')
            for index_pw, pw in enumerate(passwords, start=1):
                self.SignalPwIndex.emit(index_pw)
                final_result = function_7zip.process_7zip_t(_7ZIP_PATH, filepath, pw)
                # 如果结果是成功，则寻找到正确密码，否则继续进行测试
                if isinstance(final_result, Result7zip.Success):
                    break
        else:  # 是具体的结果类时，说明文件有问题，不进行后续测试
            print('虚拟密码测试检测出文件存在问题，不进行后续测试')
            final_result = fake_result

        # 返回最终结果
        return final_result


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
        self.extract_model :Union[ModelExtract.Smart, ModelExtract.SameFolder, ModelExtract.Direct]= None  # 解压模式
        self.is_break_folder: bool = False # 是否解散文件夹
        self.break_folder_model :Union[ModelBreakFolder.MoveToTop, ModelBreakFolder.MoveBottom,ModelBreakFolder.MoveFiles]= None

    def run(self):
        print('执行解压子线程')
        self.SignalStart.emit()
        self.SignalPwCount.emit(len(self.passwords))
        self.SignalTaskCount.emit(self.fileinfo_task.count())

        for index, file_info in enumerate(self.fileinfo_task.get_file_infos(), start=1):
            self.SignalTaskIndex.emit(index)
            file_info: FileInfo
            file_first = file_info.filepath
            self.SignalCurrentFile.emit(file_first)
            print('当前处理的文件：', file_first)
            extract_result, extract_path = self.extract_file(file_first, self.passwords)


            # 将结果写入文件信息类，并发送信号
            file_info.set_7zip_result(extract_result)
            if isinstance(extract_result, Result7zip.Success):
                file_info.set_extract_path(extract_path)
            self.SignalResult.emit(file_info)

        # 结束后发送结束信号
        self.SignalFinish.emit(self.fileinfo_task)

    def extract_file(self, filepath: str, passwords: list):
        # 仅处理存在的文件
        if not os.path.exists(filepath):
            return Result7zip.Skip()

        # 先测试一次虚拟密码，根据测试结果选择使用的指令
        print('执行一次虚拟密码测试')
        fake_result = self._run_command_l_with_fake_password(filepath)
        # 备忘录 提取内部路径，l或t可以仅测试其中一个文件
        if fake_result is True:  # 可以使用l指令进行后续测试
            print('使用l指令进行密码测试，并在找到密码后进行解压')
            final_result, extract_path = self.extract_after_test_l(filepath, passwords)
        elif fake_result is False:  # 不使用lt指令，直接使用x指令尝试解压
            print('直接使用x指令尝试解压')
            final_result, extract_path = self.extract_with_test_x(filepath, passwords)
        else:  # 压缩文件存在致命错误，不进行后续操作
            print('虚拟密码测试检测出文件存在问题，不进行后续测试')
            final_result = fake_result
            extract_path=None

        return final_result,   extract_path

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

        # 如果处理成功，则进行进一步处理
        if isinstance(result_7zip, Result7zip.Success):
            # 根据对应模式移动临时文件夹下的文件/文件夹
            temp_folder = function_7zip.get_temp_dirpath(part_extract_to)  # 要移动的文件夹
            parent_folder = os.path.dirname(temp_folder)  # 移动至该文件夹下
            if isinstance(self.extract_model, ModelExtract.Smart):
                extract_path = function_move.move_to_smart(temp_folder, parent_folder)
            elif isinstance(self.extract_model, ModelExtract.SameFolder):
                extract_path = function_move.move_to_same_dirname(temp_folder, parent_folder)
            elif isinstance(self.extract_model, ModelExtract.Direct):
                extract_path = function_move.move_to_no_deal(temp_folder, parent_folder)
            else:
                extract_path=None
            # 是否解散文件夹（仅在解压结果为文件夹时才执行）
            if self.is_break_folder:
                if os.path.isdir(extract_path):
                    if isinstance(self.break_folder_model, ModelBreakFolder.MoveToTop):
                        extract_path = function_file.break_folder_top(extract_path)
                    elif isinstance(self.break_folder_model, ModelBreakFolder.MoveBottom):
                        extract_path = function_file.break_folder_bottom(extract_path)
                    elif isinstance(self.break_folder_model, ModelBreakFolder.MoveFiles):
                        extract_path = function_file.break_folder_files(extract_path)
                    else:
                        pass
            # 是否删除原文件
            if self.is_delete_file:
                lzytools.file.delete( file,send_to_trash=True)

            print("处理文件:",file,"处理结果",result_7zip,"解压路径",extract_path)
            return result_7zip, extract_path
        else:
            return result_7zip, None


    def extract_after_test_l(self, filepath: str, passwords: list):
        """使用l命令进行测试，并在搜索到正确密码后执行解压操作，返回最终结果类"""
        # 先测试，找到密码后再解压
        final_result = None  # 最终结果
        extract_path = None  # 如果成功处理，则为解压后最终的路径
        for index_pw, pw in enumerate(passwords, start=1):
            self.SignalPwIndex.emit(index_pw)
            final_result = function_7zip.process_7zip_l(_7ZIP_PATH, filepath, pw)
            if isinstance(final_result, Result7zip.Success):
                print('搜索到正确密码，执行解压操作')
                true_password = pw
                final_result,extract_path = self.extract(filepath, true_password)
                break

        return final_result, extract_path

    def extract_with_test_x(self, filepath: str, passwords: list):
        """使用x指令进行密码测试，并返回最终结果类"""
        # 进行一次特殊处理，有些内部文件名未加密的压缩文件，在使用x命令测试时会遍历所有文件，而不是仅检查其中的一部分文件，在这种情况下使用t命令的速度更快
        # 所以先用虚拟密码和t指令测试一次，计算其耗时，再和后续的x指令耗时相比较，如果t指令耗时较短则使用t指令进行后续测试
        start_time = time.time()
        final_result = function_7zip.process_7zip_t(_7ZIP_PATH, filepath, _FAKE_PASSWORD)
        runtime_t = time.time() - start_time  # t命令的耗时

        extract_path = None  # 如果成功处理，则为解压后最终的路径
        # 使用x命令解压
        for index_pw, pw in enumerate(passwords, start=1):
            self.SignalPwIndex.emit(index_pw)
            final_result, extract_path = self.extract(filepath, pw)
            if isinstance(final_result, Result7zip.Success):
                break

        return final_result, extract_path
