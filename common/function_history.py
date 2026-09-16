import os
import shutil
import time

from common.class_7zip import Result7zip
from common.class_file_info import FileInfo
from common.function_7zip import FAKE_PASSWORD

HISTORY_FILE = 'history.txt'
HISTORY_CACHE = 'history_cache'  # 历史记录以每日的文件备份保存


def check_history_file():
    """检查历史文件是否存在"""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            today = time.strftime('%Y-%m-%d', time.localtime())
            f.write(today + '\n' * 2)

    if not os.path.exists(HISTORY_CACHE):
        os.mkdir(HISTORY_CACHE)


def move_history_file():
    """移动每日历史文件"""
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history_date = f.readline().strip()
        f.close()

    today = time.strftime('%Y-%m-%d', time.localtime())
    if history_date != today:
        shutil.move(HISTORY_FILE, os.path.normpath(os.path.join(HISTORY_CACHE, f'{history_date}.txt')))
        check_history_file()


def save_to_result(file_info: FileInfo):
    """保存文件信息类到本地"""
    filepath = file_info.filepath

    _7zip_result = file_info.get_7zip_result().return_text

    if _7zip_result == Result7zip.Success.return_text:
        if file_info.password:
            if file_info.password == FAKE_PASSWORD:
                password = '无密码'
            else:
                password = file_info.password
        else:
            password = ''

    if file_info.extract_path:
        is_success_unzip = '是'
    else:
        is_success_unzip = '否'

    _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    info = (f'文件路径：{filepath}\n'
            f'处理结果：{_7zip_result}\n'
            f'文件密码：{password}\n'
            f'是否完成解压：{is_success_unzip}\n'
            f'处理时间：{_time}\n'
            f'{'-' * 20}\n')

    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(info)
