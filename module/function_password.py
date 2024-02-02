# 密码数据库的相关方法

import os
import pickle
import shutil
import time

from constant import _PASSWORD_FILE, _PASSWORD_EXPORT, _BACKUP_FOLDER
from module import function_normal


def create_empty_keywords():
    """创建初始空密码数据库"""
    function_normal.print_function_info()
    with open(_PASSWORD_FILE, 'wb') as f:
        pickle.dump({}, f)


def read_passwords(pickle_file=_PASSWORD_FILE) -> list:
    """读取密码，按使用次数排序后返回"""
    function_normal.print_function_info()
    with open(pickle_file, 'rb') as f:
        password_dict = pickle.load(f)

    # 排序
    sorted_keys = sorted(password_dict, key=password_dict.get, reverse=True)
    sorted_passwords = list(sorted_keys)

    return sorted_passwords


def export_passwords():
    """导出明文密码"""
    function_normal.print_function_info()
    passwords = read_passwords()

    with open(_PASSWORD_EXPORT, 'w', encoding='utf-8') as pw:
        pw.write("\n".join(passwords))


def update_passwords(passwords: list):
    """更新密码"""
    function_normal.print_function_info()
    # 密码数据库格式说明：存储一个dict，键为密码str，值为对应的使用次数int
    # 读取
    with open(_PASSWORD_FILE, 'rb') as f:
        password_dict = pickle.load(f)

    # 添加
    for pw in passwords:
        if pw not in password_dict:
            password_dict[pw] = 0

    # 保存
    with open(_PASSWORD_FILE, 'wb') as f:
        pickle.dump(password_dict, f)


def add_pw_count(pw: str):
    """在配置文件中将对应的解压密码使用次数+1"""
    function_normal.print_function_info()
    if pw:
        with open(_PASSWORD_FILE, 'rb') as f:
            password_dict = pickle.load(f)

        # 使用次数+1
        password_dict[pw] += 1

        with open(_PASSWORD_FILE, 'wb') as f:
            pickle.dump(password_dict, f)


def backup_passwords():
    """备份密码数据库"""
    function_normal.print_function_info()
    time_text = time.strftime("%Y%m%d %H_%M_%S", time.localtime())
    copy_filename = f'{time_text}.'.join(_PASSWORD_FILE.split('.'))
    copy_path = os.path.join(_BACKUP_FOLDER, copy_filename)
    shutil.copyfile(_PASSWORD_FILE, copy_path)
