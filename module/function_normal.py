# 一般方法

import inspect
import os
import shutil
import time
from typing import Union

from constant import _BACKUP_FOLDER, _UNZIP_TEMP_FOLDER, _PASSWORD_FILE, _HISTORY_FILE, _HISTORY_FILE_MAX_SIZE, \
    _PROGRAM_FOLDER
from module import function_password
from module.function_config import Config


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
    print_function_info()
    if not os.path.exists(_BACKUP_FOLDER):
        os.mkdir(_BACKUP_FOLDER)

    if not os.path.exists(_PASSWORD_FILE):
        function_password.create_empty_keywords()

    Config()


def is_temp_folder_exists(check_path: Union[list, str]) -> bool:
    """检查传入路径的同级文件夹中是否存在临时文件夹（前一次解压未正常删除的）"""
    print_function_info()
    if type(check_path) is str:
        check_path = [check_path]

    temp_folders = set()  # 所有可能存在的临时文件夹路径（添加后缀自动生成，非真实路径）

    for path in check_path:
        if os.path.isfile(path):
            dirpath = os.path.join(os.path.split(path)[0], _UNZIP_TEMP_FOLDER)
            temp_folders.add(dirpath)
        else:
            dirpath = os.path.join(path, _UNZIP_TEMP_FOLDER)
            temp_folders.add(dirpath)

    for folder in temp_folders:
        if os.path.exists(folder) and os.listdir(folder):
            return True

    return False


def save_history(text: str):
    """保存历史记录"""
    if os.path.exists(_HISTORY_FILE) and os.path.getsize(_HISTORY_FILE) > _HISTORY_FILE_MAX_SIZE:
        backup_history()
    with open(_HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(text + '\n')


def backup_history():
    """备份历史记录"""
    time_text = time.strftime("%Y%m%d %H_%M_%S", time.localtime())
    temp_filename = _HISTORY_FILE.replace(_PROGRAM_FOLDER, '')
    copy_filename = temp_filename.replace('.txt', f'{time_text}.txt')
    copy_path = os.path.normpath(os.path.join(_BACKUP_FOLDER, copy_filename))
    shutil.move(_HISTORY_FILE, copy_path)
