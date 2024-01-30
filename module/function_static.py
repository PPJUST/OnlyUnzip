import inspect
import os
import random
import re
import shutil
import string
import time
from typing import Union

from constant import _BACKUP_FOLDER, _Unzip_Temp_Folder
from module.function_config import Config
from module.function_file import get_folder_size
from module.function_folder import get_first_multi_folder


def print_function_info(mode: str = 'current'):
    """
    打印当前/上一个执行的函数信息
    :param mode: str类型，'current' 或 'last'
    """
    # pass

    if mode == 'current':
        print(time.strftime('%H:%M:%S ', time.localtime()),
              inspect.getframeinfo(inspect.currentframe().f_back).function)
    elif mode == 'last':
        print(time.strftime('%H:%M:%S ', time.localtime()),
              inspect.getframeinfo(inspect.currentframe().f_back.f_back).function)

def init_settings():
    """初始化设置文件/文件夹"""
    if not os.path.exists(_BACKUP_FOLDER):
        os.mkdir(_BACKUP_FOLDER)

    Config()

def is_temp_folder_exists(check_path: Union[list, str]) -> bool:
    """检查传入路径的同级文件夹中是否存在临时文件夹（前一次解压未正常删除的）"""
    if type(check_path) is str:
        check_path = [check_path]

    temp_folders = set()  # 所有可能存在的临时文件夹路径（添加后缀自动生成，非真实路径）

    for path in check_path:
        if os.path.isfile(path):
            dirpath = os.path.join(os.path.split(path)[0], _Unzip_Temp_Folder)
            temp_folders.add(dirpath)
        else:
            dirpath = os.path.join(path, _Unzip_Temp_Folder)
            temp_folders.add(dirpath)

    for folder in temp_folders:
        if os.path.exists(folder) and os.listdir(folder):
            return True

    return False


def create_nodup_filename(path: str, target_dirpath: str, add_suffix: str = ' -New') -> str:
    """
    生成传入的文件或文件夹在指定文件夹中没有重复的文件名（添加自定义后缀）
    :param path: 文件或文件夹路径str
    :param target_dirpath: 指定文件夹路径str
    :param add_suffix: 自定义后缀
    :return: str，无重复的文件名（非完整路径，仅文件名）
    """
    if os.path.isfile(path):
        filetitle = os.path.split(os.path.splitext(path)[0])[1]
        suffix = os.path.splitext(path)[1]
    else:
        filename = os.path.split(path)[1]
        filetitle = filename
        suffix = ''

    # 剔除原文件名中已包含的后缀
    check = filetitle.rfind(add_suffix)
    if check != -1 and filetitle[check + len(add_suffix):].isdigit():
        new_filetitle = filetitle[0:check]
    else:
        new_filetitle = filetitle
    new_filename = new_filetitle + suffix
    temp_filename = new_filetitle + add_suffix + '1' + suffix

    # 生成无重复的文件名
    count = 0
    # 一直累加循环直到不存在同名（同级目录也要检查，防止改名报错）
    while os.path.exists(os.path.join(target_dirpath, new_filename)) or os.path.exists(
            os.path.join(os.path.split(path)[0], temp_filename)):
        count += 1
        new_filename = f'{filetitle}{add_suffix}{count}{suffix}'
        temp_filename = new_filename

    return new_filename


def get_filetitle(path: str) -> str:
    """提取路径对应的文件/文件夹不含后缀的文件名"""
    if os.path.isdir(path):
        filetitle = os.path.splitext(path)[1]
    else:
        # 一般情况
        filetitle = os.path.split(os.path.splitext(path)[0])[1]
        # 单独处理压缩文件
        pattern_7z = r"^(.+)\.7z\.\d+$"
        pattern_rar = r"^(.+)\.part(\d+)\.rar$"
        pattern_rar_without_suffix = r"^(.+)\.part(\d+)$"
        pattern_zip = r"^(.+)\.zip$"
        pattern_zip_volume = r"^(.+)\.z\d+$"
        pattern_zip_type2 = r"^(.+)\.zip\.\d+$"
        rules = [pattern_7z, pattern_rar, pattern_rar_without_suffix, pattern_zip, pattern_zip_volume, pattern_zip_type2]
        filename = os.path.split(path)[1]
        for rule in rules:
            try:
                filetitle = re.match(rule, filename).group(1)
                break
            except:
                continue

    # 处理文件两端多余的空格和.
    while filetitle[0] in [' ', '.'] or filetitle[-1] in [' ', '.']:
        filetitle = filetitle.strip()
        filetitle = filetitle.strip('.')

    return filetitle















def delete_empty_folder(folder: str):
    """检查文件夹是否为空，是则删除（不经过回收站）"""
    print_function_info()
    if get_folder_size(folder) == 0:
        try:
            os.rmdir(folder)
        except OSError:
            all_dirpath = []
            all_filepath = []
            for dirpath, dirnames, filenames in os.walk(folder):
                all_dirpath.append(dirpath)  # 提取所有文件夹路径
                for filename in filenames:
                    filepath = os.path.normpath(os.path.join(dirpath, filename))
                    all_filepath.append(filepath)
            for i in all_filepath:  # 先删除所有空文件，防止后续删除文件夹时报错
                os.remove(i)
            for i in all_dirpath[::-1]:  # 从后往前逐级删除文件夹
                os.rmdir(i)
    else:
        print(f'{folder} 不为空')


