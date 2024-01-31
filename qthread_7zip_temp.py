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
import module.function_filetype
import module.function_password
from constant import _PATH_7ZIP
from module import function_normal
from module.function_config import Config

os.environ["PYTHONIOENCODING"] = "UTF-8"
config_file = 'config.ini'
backup_dir = 'backup'


class ExtractQthread(QThread):
    signal_update_ui = Signal(str, list)  # 发送更新主程序ui的信号，发送的list格式：代码, 数据
    signal_extracted_files = Signal(list)  # 发送所有解压出的文件路径list
    signal_stop = Signal()  # 中止操作的信号

    def __init__(self):
        super().__init__()


    @staticmethod
    def save_pw_history(history_dict: dict = None):
        """保存记录到本地"""
        function_static.print_function_info()
        history_filetitle = '历史记录'
        history_suffix = '.txt'
        history_filename = history_filetitle + history_suffix

        if os.path.exists(history_filename) and os.path.getsize(history_filename) > 100 * 1024:  # 历史记录超过100kb则重置
            new_history_file = f'{backup_dir}/{history_filetitle} {time.strftime("%Y_%m_%d %H_%M_%S ", time.localtime())}{history_suffix}'
            shutil.move(history_filename, new_history_file)

        with open(history_filename, 'a', encoding='utf-8') as ha:
            add_text = ''
            for key in history_dict:
                add_text += f'■日期：{time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())} ' \
                            f'■文件路径：{key} ' \
                            f'■解压密码：{history_dict[key]}\n' \
                            f'--------------------------------------------\n'
            ha.write(add_text)
