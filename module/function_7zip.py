# 调用7zip的相关方法

import subprocess

from constant import _PATH_7ZIP, _PASSWORD_FAKE, _COLOR_SKIP, _COLOR_ERROR, _COLOR_WARNING, _COLOR_SUCCESS


def call_7zip(command_type: str, filepath: str, password: str, check_path_inside=None):
    """调用7zip的l和t命令，返回测试结果
    :param command_type: 7zip的command，l/t
    :param filepath: 文件路径
    :param password: 需要测试的密码
    :param check_path_inside: 指定测试的内部文件路径（只在t指令时使用）"""
    command = [_PATH_7ZIP,
               command_type,
               filepath,
               "-p" + password]
    if command_type == 't' and check_path_inside:  # 只在t指令使用，l指令不需要，t指令中使用时可以加快速度
        command.append(check_path_inside)
    print('测试 7zip命令', command)
    process = subprocess.run(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             creationflags=subprocess.CREATE_NO_WINDOW,
                             text=True,
                             universal_newlines=True)

    """
    7zip Exit Codes
    0	没有错误
    1	警告（非致命错误，例如被占用）
    2	致命错误
    7	命令行错误
    8	内存不足，无法进行操作
    255	用户已停止进程
    """
    # 处理返回码
    if process.returncode == 0:  # 没有错误
        result_class = Result7zip.Success(filepath, password)
    elif process.returncode == 1:  # 警告（非致命错误，例如被占用）
        result_class = Result7zip.FileOccupied(filepath)
    elif process.returncode == 2:  # 致命错误
        stderr = str(process.stderr) + str(process.stdout)  # 错误信息在输出流中
        # 读取输出流
        print('【7zip测试信息：', stderr, '】')  # 测试用
        # if not stderr:  # 处理自解压文件时，返回的stderr流可能为空
        #     result_class = Result7zip.WrongPassword(filepath)
        # 备忘录-如何更好的处理自解压文件
        if 'Wrong password' in stderr:
            result_class = Result7zip.WrongPassword(filepath)
        elif 'Missing volume' in stderr:
            result_class = Result7zip.MissingVolume(filepath)
        elif 'Cannot open the file as' in stderr:  # 备忘录-如果是这个报错可能可以按其指定的文件类型进行测试
            result_class = Result7zip.NotArchiveOrDamaged(filepath)
        else:  # 兜底
            result_class = Result7zip.UnknownError(filepath)
    elif process.returncode == 8:  # 内存不足，无法进行操作
        result_class = Result7zip.NotEnoughSpace(filepath)
    else:  # 兜底
        result_class = Result7zip.UnknownError(filepath)

    # 处理输出流
    archive_info_dict = get_info_from_stdout(process.stdout)

    return result_class, archive_info_dict


def test_fake_password(file):
    """使用临时密码测试文件，判断是否进行进一步操作
    :return: True: 可以使用l命令进行后续测试;
            False: 无法使用l命令进行后续测试;
            Result7zip类: 文件本身存在问题.
    """
    result_class, archive_info_dict = call_7zip('l', file, _PASSWORD_FAKE)
    # 返回密码错误，则该压缩文件已加密且可以使用l命令进行后续测试
    if isinstance(result_class, Result7zip.WrongPassword):
        return True, archive_info_dict
    # 返回成功，则该压缩文件无法使用l命令进行后续测试（内部文件名未加密或无密码时无法使用l命令测试密码，需要使用t/x）
    elif isinstance(result_class, Result7zip.Success):
        return False, archive_info_dict
    # 返回其他类型，则该压缩文件本身存在问题，中断后续操作
    # 返回文件占用/非压缩文件/空间不足/缺失分卷/未知错误，则说明文件本身存在问题
    else:
        return result_class, archive_info_dict


class Result7zip:
    """7zip处理结果
    7zip Exit Codes
    0	没有错误
    1	警告（非致命错误，例如被占用）
    2	致命错误
    7	命令行错误
    8	内存不足，无法进行操作
    255	用户已停止进程"""

    class _Template:
        def __init__(self, file, text, color):
            self.file = file
            self.text = text
            self.color = color

    class Skip(_Template):
        """跳过（通过filetype库判断后，不通过7zip调用返回结果判断）"""

        def __init__(self, file):
            super().__init__(file, '跳过', _COLOR_SKIP)

    class WrongPassword(_Template):
        """密码错误"""

        def __init__(self, file):
            super().__init__(file, '密码错误', _COLOR_ERROR)

    class MissingVolume(_Template):
        """缺少分卷"""

        def __init__(self, file):
            super().__init__(file, '缺少分卷', _COLOR_ERROR)

    class NotArchiveOrDamaged(_Template):
        """不是压缩文件或文件已经损坏"""

        def __init__(self, file):
            super().__init__(file, '不是压缩文件或文件已经损坏', _COLOR_ERROR)

    class UnknownError(_Template):
        """未知错误"""

        def __init__(self, file):
            super().__init__(file, '未知错误', _COLOR_ERROR)

    class FileOccupied(_Template):
        """文件被占用"""

        def __init__(self, file):
            super().__init__(file, '文件被占用', _COLOR_WARNING)

    class NotEnoughSpace(_Template):
        """磁盘空间不足"""

        def __init__(self, file):
            super().__init__(file, '磁盘空间不足', _COLOR_WARNING)

    class Success(_Template):
        """成功"""

        def __init__(self, file, password):
            super().__init__(file, '成功', _COLOR_SUCCESS)
            self.password = password if password != _PASSWORD_FAKE else ''


class Collect7zipResult:
    """收集7zip的调用结果，并进行统计"""
    _instance = None
    _is_init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_init:
            super().__init__()
            self._is_init = True

            self._result_dict = dict()  # 结果字典，key为文件路径，value为Result7zip对象

    def reset_count(self):
        """重置计数"""
        self._result_dict.clear()

    def collect(self, result_class):
        """收集结果"""
        file = result_class.file
        self._result_dict[file] = result_class

    def get_result_text(self):
        """获取结果文本"""
        wrong_password = 0  # 密码错误
        missing_volume = 0  # 缺少分卷
        not_archive_or_damaged = 0  # 不是压缩文件或文件已经损坏
        unknown_error = 0  # 未知错误
        file_occupied = 0  # 文件被占用
        not_enough_space = 0  # 磁盘空间不足
        success = 0  # 成功

        for result_class in self._result_dict.values():
            if isinstance(result_class, Result7zip.WrongPassword):
                wrong_password += 1
            elif isinstance(result_class, Result7zip.MissingVolume):
                missing_volume += 1
            elif isinstance(result_class, Result7zip.NotArchiveOrDamaged):
                not_archive_or_damaged += 1
            elif isinstance(result_class, Result7zip.UnknownError):
                unknown_error += 1
            elif isinstance(result_class, Result7zip.FileOccupied):
                file_occupied += 1
            elif isinstance(result_class, Result7zip.NotEnoughSpace):
                not_enough_space += 1
            elif isinstance(result_class, Result7zip.Success):
                success += 1

        count_success = success
        count_wrong_password = wrong_password
        count_error = missing_volume + not_archive_or_damaged + unknown_error + file_occupied + not_enough_space
        join_text = f'成功:{count_success} 失败:{count_wrong_password} 错误:{count_error}'

        return join_text


def get_info_from_stdout(stdout_text):
    """从7zip的stdout中获取相关信息"""
    data_dict = {'filetype': None, 'paths': None}
    text_split = stdout_text.splitlines()
    # 提取文件类型
    cut_ = [i for i in text_split if i.startswith('Type = ')]
    if cut_:
        cut_text = [i for i in text_split if i.startswith('Type = ')][0]
        filetype = cut_text[len('Type = '):]
        data_dict['filetype'] = filetype
    # 提取内部文件路径
    start_index = None
    end_index = None
    for index, i in enumerate(text_split):
        if i.startswith('   Date'):
            start_index = index
        if i.startswith('----------'):
            end_index = index
    if start_index or end_index:
        column_name_index = text_split[start_index].find('Name')
        cut_text = text_split[start_index + 2:end_index]
        paths = [i[column_name_index:] for i in cut_text if 'D....' not in i]
        data_dict['paths'] = paths

    return data_dict
