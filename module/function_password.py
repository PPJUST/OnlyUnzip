# 密码数据库的相关方法
# 密码数据库格式说明：存储一个dict，键为密码str，值为对应的使用次数int

import os
import pickle
import shutil
import time
from typing import Union

from constant import _PASSWORD_FILE, _PASSWORD_EXPORT, _BACKUP_FOLDER, _TIME_STAMP
from module import function_normal


def create_default_password_file():
    """创建默认密码文件"""
    function_normal.print_function_info()
    with open(_PASSWORD_FILE, 'wb') as f:
        pickle.dump({}, f)


def read_password(password_file=_PASSWORD_FILE) -> list:
    """读取密码，按使用次数排序后返回列表"""
    function_normal.print_function_info()
    # 读取
    with open(password_file, 'rb') as f:
        password_dict = pickle.load(f)
    # 排序
    passwords = sorted(password_dict, key=password_dict.get, reverse=True)
    passwords = list(passwords)

    return passwords


def export_password():
    """导出明文密码"""
    function_normal.print_function_info()
    passwords = read_password()

    with open(_PASSWORD_EXPORT, 'w', encoding='utf-8') as pw:
        pw.write('\n'.join(passwords))


def open_export():
    """打开导出的密码文件"""
    os.startfile(_PASSWORD_EXPORT)


def update_password(key: Union[list, str]):
    """更新密码"""
    function_normal.print_function_info()
    _backup_password()
    # 统一格式
    if isinstance(key, str):
        key = [key]
    # 读取
    with open(_PASSWORD_FILE, 'rb') as f:
        password_dict = pickle.load(f)
    # 添加
    for pw in key:
        if pw not in password_dict:
            password_dict[pw] = 0
        else:
            password_dict[pw] += 1
    # 保存
    with open(_PASSWORD_FILE, 'wb') as f:
        pickle.dump(password_dict, f)


def _backup_password():
    """备份密码数据库"""
    function_normal.print_function_info()
    time_text = time.strftime(_TIME_STAMP, time.localtime())
    original_filetitle = os.path.basename(os.path.splitext(_PASSWORD_FILE)[0])
    suffix = os.path.splitext(_PASSWORD_FILE)[1]
    new_filepath = os.path.normpath(os.path.join(_BACKUP_FOLDER, original_filetitle + time_text + suffix))
    shutil.copyfile(_PASSWORD_FILE, new_filepath)
