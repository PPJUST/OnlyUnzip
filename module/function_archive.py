# 压缩文件相关方法

import os
import re
import subprocess
from typing import Union

import filetype

from constant import _PATH_7ZIP
from module import function_normal
from module.class_state import State7zResult


def find_volume_archives(files_list: list) -> dict:
    """
    检查传入文件列表，提取出符合分卷压缩文件规则的文件，转换为{第一个分卷压缩包:(全部分卷)..}格式
    :param files_list: list类型，文件列表
    :return: dict类型，{A压缩文件第一个分卷包路径:(A压缩文件全部分卷路径), ...}
    """
    function_normal.print_function_info()
    # 将文件按所在目录分类
    parent_folder_dict = {}  # {文件父目录:(A文件, B文件), ...}，仅匹配同一文件夹下的分卷压缩文件
    for file in files_list:
        parent_folder = os.path.split(file)[0]
        if parent_folder not in parent_folder_dict:
            parent_folder_dict[parent_folder] = set()
        parent_folder_dict[parent_folder].add(file)

    # 按目录逐个处理内部文件
    volume_archive_dict = {}  # {A压缩文件第一个分卷包路径:(A压缩文件全部分卷路径), ...}
    for parent_folder in parent_folder_dict:
        files = parent_folder_dict[parent_folder]
        # 逐个判断是否符合分卷规则
        for file in files:
            filename = os.path.split(file)[1]
            first_volume_filename = is_volume_archive(filename)
            if first_volume_filename:
                first_volume_archive = os.path.normpath(os.path.join(parent_folder, first_volume_filename))
            else:
                continue

            # 不处理第一个分卷包不存在的情况，后续会提示“缺失分卷”
            # if not os.path.exists(first_volume_archive):
            #     continue

            if first_volume_archive not in volume_archive_dict:
                volume_archive_dict[first_volume_archive] = set()
            volume_archive_dict[first_volume_archive].add(file)  # {示例.7z.001:(示例.7z.001,示例.7z.002)}

        # 在文件夹内识别其他文件，补全分卷压缩文件分卷
        listdir = os.listdir(parent_folder)
        for filename_check in listdir:
            filepath = os.path.normpath(os.path.join(parent_folder, filename_check))
            first_volume_filename = is_volume_archive(filename_check)
            if first_volume_filename:
                first_volume_archive = os.path.normpath(os.path.join(parent_folder, first_volume_filename))
                if first_volume_archive in volume_archive_dict:
                    volume_archive_dict[first_volume_archive].add(filepath)

    return volume_archive_dict


def is_volume_archive(filename: str) -> Union[str, bool]:
    """
    判断传入的文本是否符合分卷压缩文件的规则，是则返回生成第一个分卷包的文件名
    :return: 第一个分卷包的文件名 或 False
    """
    function_normal.print_function_info()
    pattern_7z = r"^(.+)\.7z\.\d+$"
    pattern_rar = r"^(.+)\.part(\d+)\.rar$"
    pattern_rar_without_suffix = r"^(.+)\.part(\d+)$"
    pattern_zip = r"^(.+)\.zip$"
    pattern_zip_volume = r"^(.+)\.z\d+$"
    pattern_zip_type2 = r"^(.+)\.zip\.\d+$"

    # 匹配7z正则
    if re.match(pattern_7z, filename):
        filetitle = re.match(pattern_7z, filename).group(1)
        first_volume_filename = filetitle + '.7z.001'
    # 匹配rar正则
    elif re.match(pattern_rar, filename):
        filetitle = re.match(pattern_rar, filename).group(1)
        number_type = len(re.match(pattern_rar, filename).group(2))  # 解决part1.rar和part01.rar的情况
        first_volume_filename = filetitle + f'.part{str(1).zfill(number_type)}.rar'
    # 匹配无后缀的rar正则（rar分卷文件无后缀也能直接解压）
    elif re.match(pattern_rar_without_suffix, filename):
        filetitle = re.match(pattern_rar_without_suffix, filename).group(1)
        number_type = len(re.match(pattern_rar_without_suffix, filename).group(2))
        first_volume_filename = filetitle + f'.part{str(1).zfill(number_type)}'
    # 匹配zip正则（zip分卷文件的第一个包一般都是.zip后缀，所以.zip后缀直接分类为分卷压缩文件）
    elif re.match(pattern_zip, filename):
        filetitle = re.match(pattern_zip, filename).group(1)
        first_volume_filename = filetitle + r'.zip'
    # 匹配zip分卷正则
    elif re.match(pattern_zip_volume, filename):
        filetitle = re.match(pattern_zip_volume, filename).group(1)
        first_volume_filename = filetitle + r'.zip'
    # 匹配zip格式2正则
    elif re.match(pattern_zip_type2, filename):
        filetitle = re.match(pattern_zip_type2, filename).group(1)
        first_volume_filename = filetitle + r'.zip.001'
    else:
        return False

    return first_volume_filename


def is_archive(filepath: str, use_filetype: bool = True) -> bool:
    """
    判断文件是否为压缩文件
    :param filepath: str类型，文件路径
    :param use_filetype: bool类型，是否使用filetype库进行额外判断
    :return: bool类型，是否为压缩包
    """
    function_normal.print_function_info()
    if not os.path.exists(filepath):
        return False
    elif os.path.isdir(filepath):
        return False
    else:
        # 先通过文件后缀判断
        file_suffix = os.path.splitext(filepath)[1][1:].lower()  # 提取文件后缀名（不带.）
        archive_suffix = ['zip', 'rar', '7z', 'tar', 'gz', 'xz', 'iso']
        if file_suffix in archive_suffix:
            return True

        # 再通过filetype判断
        if use_filetype:
            archive_type = ['zip', 'tar', 'rar', 'gz', '7z', 'xz']  # filetype库支持的压缩文件后缀名
            kind = filetype.guess(filepath)
            if kind is None:
                return False
            else:
                type_kind = kind.extension
                if type_kind in archive_type:
                    return True

        return False


def is_zip_archive(filepath: str) -> bool:
    """单独判断文件是否为zip格式压缩文件"""
    function_normal.print_function_info()
    archive_type = ['zip']
    kind = filetype.guess(filepath)
    if kind is None:
        return False
    else:
        type_kind = kind.extension
        if type_kind in archive_type:
            return True

    return False


def subprocess_run_7z(command_type, file, password):
    """使用run调用7z，仅用于l和t命令"""
    function_normal.print_function_info()
    command = [_PATH_7ZIP,
               command_type,
               file,
               "-p" + password,
               '-bse2']
    process = subprocess.run(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             creationflags=subprocess.CREATE_NO_WINDOW,
                             text=True,
                             universal_newlines=True)

    """7z.exe返回值代码
    Code码	含义
    0	没有错误
    1	警告（非致命错误，例如被占用）
    2	致命错误
    7	命令行错误
    8	内存不足，无法进行操作
    255	用户已停止进程
    """

    if process.returncode == 0:
        result = State7zResult.Success(file, password)
    elif process.returncode == 1:
        result = State7zResult.FileOccupied(file)
    elif process.returncode == 2:
        stderr = str(process.stderr)
        if not stderr:  # 处理自解压文件时，返回的stderr流可能为空
            result = State7zResult.WrongPassword(file)
        elif 'Wrong password' in stderr:
            result = State7zResult.WrongPassword(file)
        elif 'Missing volume' in stderr or 'Unexpected end of archive' in stderr:
            result = State7zResult.MissingVolume(file)
        elif 'Cannot open the file as' in stderr:
            result = State7zResult.NotArchiveOrDamaged(file)
        else:
            result = State7zResult.UnknownError(file)
    elif process.returncode == 8:
        result = State7zResult.NotEnoughSpace(file)
    else:
        result = State7zResult.UnknownError(file)

    return result


def subprocess_7z_l(file, password):
    """调用7z的l指令"""
    function_normal.print_function_info()
    result = subprocess_run_7z('l', file, password)

    return result


def subprocess_7z_t(file, password):
    """调用7z的t指令"""
    function_normal.print_function_info()
    result = subprocess_run_7z('t', file, password)

    return result
