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


def read_password_from_files(files: list):
    """从文件列表中读取文件名中可能包含的密码"""
    pws_joined = set()
    for file in files:
        filename = function_normal.get_filetitle(file)
        pws = _read_password_from_filename(filename)
        pws_joined.update(pws)

    return list(pws_joined)


def _read_password_from_filename(filename: str):
    """从文件名中读取可能包含的密码
    :param filename: str，不含后缀的文件名"""
    pws = set()
    # 密码类型 - 整个文件名
    pws.add(filename)
    # 密码类型 - 以空格为分隔符，拆分文件名
    split = filename.split(' ')
    pws.update(split)
    # 密码类型 - 拆分的文件名字段，剔除标识符#
    pws.update(_deal_split_set(split, left_edge_str='#'))
    # 密码类型 - 拆分的文件名字段，剔除标识符@
    pws.update(_deal_split_set(split, left_edge_str='@'))
    # 密码类型 - 拆分的文件名字段，剔除标识符【】
    pws.update(_deal_split_set(split, left_edge_str='【', right_edge_str='】'))
    # 密码类型 - 拆分的文件名字段，剔除标识符[]
    pws.update(_deal_split_set(split, left_edge_str='[', right_edge_str=']'))
    # 密码类型 - 拆分的文件名字段，剔除标识符()
    pws.update(_deal_split_set(split, left_edge_str='(', right_edge_str=')'))
    # 密码类型 - 拆分的文件名字段，剔除文本"密码"
    pws.update(_deal_split_set(split, left_edge_str='密码'))
    # 密码类型 - 拆分的文件名字段，剔除文本"密码："
    pws.update(_deal_split_set(split, left_edge_str='密码：'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压"
    pws.update(_deal_split_set(split, left_edge_str='解压'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压："
    pws.update(_deal_split_set(split, left_edge_str='解压：'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压码"
    pws.update(_deal_split_set(split, left_edge_str='解压码'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压码："
    pws.update(_deal_split_set(split, left_edge_str='解压码：'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压密码"
    pws.update(_deal_split_set(split, left_edge_str='解压密码'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压密码："
    pws.update(_deal_split_set(split, left_edge_str='解压密码：'))
    # 密码类型 - 拆分的文件名字段，剔除文本"pw"
    pws.update(_deal_split_set(split, left_edge_str='pw'))
    # 密码类型 - 拆分的文件名字段，剔除文本"pw："
    pws.update(_deal_split_set(split, left_edge_str='pw：'))

    return pws


def _deal_split_set(splits: Union[list, set], left_edge_str: str = '', right_edge_str: str = ''):
    """处理拆分的字符段"""
    f_splits = set()  # 处理结果
    for i in splits:
        i: str
        if len(i) <= len(left_edge_str) + len(right_edge_str):  # 大于左右两端字符数才进行处理
            continue

        if left_edge_str:
            if i.startswith(left_edge_str):
                i = i[len(left_edge_str):]
            else:
                continue

        if right_edge_str:
            if i.endswith(right_edge_str):
                i = i[:-len(right_edge_str)]
            else:
                continue

        f_splits.add(i)

    return f_splits
