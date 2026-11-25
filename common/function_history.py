import os
import shutil
import time

from common.class_7zip import Result7zip
from common.class_file_info import FileInfo
from common.function_7zip import FAKE_PASSWORD

HISTORY_FILE = 'history.txt'
HISTORY_CACHE = 'history_cache'  # 历史记录以每日的文件备份保存
SEPARATOR = '-' * 20 + '\n'  # 间隔符
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
NO_PASSWORD_TEXT = '无密码'


def _get_today():
    """获取当天日期字符串"""
    return time.strftime(DATE_FORMAT, time.localtime())


def _read_file(filepath):
    """读取历史文件，并按间隔符拆分为多条记录"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().split(SEPARATOR)


def check_history_file():
    """检查历史文件和缓存目录是否存在"""
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            f.write(_get_today() + '\n' * 2)

    if not os.path.exists(HISTORY_CACHE):
        os.mkdir(HISTORY_CACHE)


def read_history_file(filename: str):
    """读取指定的历史文件；缓存中存在同名文件时优先读取缓存"""
    if not filename.endswith('.txt'):
        filename = filename + '.txt'

    cache_filepath = os.path.join(HISTORY_CACHE, filename)
    if os.path.exists(cache_filepath):
        return _read_file(cache_filepath)

    return _read_file(HISTORY_FILE)


def read_all_history():
    """读取当前历史文件和所有缓存历史文件"""
    histories = _read_file(HISTORY_FILE)

    for filename in os.listdir(HISTORY_CACHE):
        if filename.endswith('.txt'):
            cache_filepath = os.path.join(HISTORY_CACHE, filename)
            histories.extend(_read_file(cache_filepath))

    return histories


def move_history_file():
    """日期变化时，将旧记录移动到缓存目录"""
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        history_date = f.readline().strip()

    if history_date == _get_today():
        return

    cache_filepath = os.path.join(HISTORY_CACHE, history_date + '.txt')
    shutil.move(HISTORY_FILE, os.path.normpath(cache_filepath))
    check_history_file()


def _get_password_text(file_info: FileInfo, result_text: str):
    """获取写入历史记录的密码文本"""
    password = ''
    if result_text != Result7zip.Success.return_text:
        return password
    if not file_info.password:
        return password
    if file_info.password == FAKE_PASSWORD:
        return NO_PASSWORD_TEXT
    return file_info.password


def save_to_result(file_info: FileInfo):
    """保存文件信息类到本地"""
    filepath = file_info.filepath
    result_text = file_info.get_7zip_result().return_text
    password = _get_password_text(file_info, result_text)

    if file_info.extract_path:
        is_success_unzip = '是'
    else:
        is_success_unzip = '否'

    current_time = time.strftime(DATETIME_FORMAT, time.localtime())

    lines = [
        f'文件路径：{filepath}',
        f'处理结果：{result_text}',
        f'文件密码：{password}',
        f'是否完成解压：{is_success_unzip}',
        f'处理时间：{current_time}',
    ]
    info = '\n'.join(lines) + '\n' + SEPARATOR

    with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(info)


def search_cache(search_text: str):
    """搜索缓存对应的文本"""
    histories = read_all_history()

    matched_histories = []
    for history in histories:
        if search_text in history:
            matched_histories.append(history)

    return matched_histories
