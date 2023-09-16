"""
存放项目需要用到的静态方法
"""
import inspect
import os
import re
import string
import time
import shutil
from typing import Union
import random

import filetype


def get_folder_size(path: str) -> int:
    """获取单个文件夹的总大小，返回int值，单位为字节B"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for i in filenames:
            filepath = os.path.join(dirpath, i)
            size += os.path.getsize(filepath)
    return size


def is_archive(filepath: str) -> bool:
    """判断文件是否是压缩包，返回bool值"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    if not os.path.exists(filepath):
        print(f'{filepath} 不存在')
        return False
    elif os.path.isdir(filepath):
        print(f'{filepath} 为文件夹，无法判断')
        return False
    else:
        file_suffix = os.path.splitext(filepath)[1]  # 提取文件后缀名

        archive_type = ['zip', 'tar', 'rar', 'gz', '7z', 'xz']  # filetype库支持的压缩文件后缀名
        suffix_type = ['.zip', '.tar', '.rar', '.gz', '.7z', '.xz', '.iso']  # 通过后缀名判断是否为压缩文件

        kind = filetype.guess(filepath)
        if kind is None:
            type_kind = None
        else:
            type_kind = kind.extension

        print(f'文件【{filepath}】的文件类型为【{type_kind}】')
        if type_kind in archive_type or file_suffix.lower() in suffix_type:  # filetype库+后缀名
            return True
        else:
            return False


def get_archive_filetitle(filepath: str) -> str:
    """提取传入文件的文件名（不含后缀），返回str值"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    if not os.path.exists(filepath):
        return f'{filepath} 不存在'
    elif os.path.isdir(filepath):
        return f'{filepath} 为文件夹，无法判断'
    else:
        filetitle = os.path.split(os.path.splitext(filepath)[0])[1]  # 兜底的不含后缀文件名

        re_rar = r"^(.+)\.part\d+\.rar$"  # 分卷压缩文件的命名规则
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip = r"^(.+)\.zip$"
        re_zip_type2 = r"^(.+)\.zip.\d+$"
        re_rules = [re_rar, re_7z, re_zip, re_zip_type2]
        filename = os.path.split(filepath)[1]
        for rule in re_rules:
            try:
                filetitle = re.match(rule, filename).group(1)
                break
            except:
                continue

        return filetitle


def get_filetitle(filepath: str) -> str:
    """提取传入文件的文件名（不含后缀），返回str值"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    if os.path.isdir(filepath):
        filetitle = os.path.splitext(filepath)[1]
    else:
        filetitle = os.path.split(os.path.splitext(filepath)[0])[1]  # 兜底的不含后缀文件名

        re_rar = r"^(.+)\.part\d+\.rar$"  # 分卷压缩文件的命名规则
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip = r"^(.+)\.zip$"
        re_zip_type2 = r"^(.+)\.zip.\d+$"
        re_rules = [re_rar, re_7z, re_zip, re_zip_type2]
        filename = os.path.split(filepath)[1]
        for rule in re_rules:
            try:
                filetitle = re.match(rule, filename).group(1)
                break
            except:
                continue

    return filetitle


def delete_folder_if_empty(folder: str) -> str:
    """如果传入的文件夹为空文件夹，则删除（不经过回收站）"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
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
            for i in all_dirpath[::-1]:  # 取得路径后从后往前逐级删除
                os.rmdir(i)
    else:
        return '文件夹不为空或出错'


def get_deepest_dirpath(dirpath: str) -> str:
    """检查传入文件夹路径的深度，找出最后一级含多文件/文件夹的文件夹，并返回路径str值"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    if len(os.listdir(dirpath)) == 1:
        the_path = os.path.normpath(os.path.join(dirpath, os.listdir(dirpath)[0]))
        if os.path.isfile(the_path):  # 如果文件夹下只有一个文件，并且是文件
            deepest_path = the_path
            return deepest_path
        else:  # 临时文件夹下只有一个文件，但是是文件夹，则递归
            return get_deepest_dirpath(the_path)
    else:
        deepest_path = dirpath
        return deepest_path


def get_filelist(dirpath: str) -> list:
    """获取指定文件夹下的所有文件路径，返回list值"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    filelist = []
    for dirpath, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            file_path = os.path.normpath(os.path.join(dirpath, filename))
            filelist.append(file_path)
    return filelist


def get_no_dup_filename(filepath: str, the_dirpath: str) -> str:
    """生成指定文件路径的文件/文件夹在指定文件夹中没有重复名的文件名（如重复添加后缀 -new1）"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    if os.path.isfile(filepath):
        filename = os.path.split(filepath)[1]
        filetitle = os.path.split(os.path.splitext(filepath)[0])[1]
        suffix = os.path.splitext(filepath)[1]
    else:
        filename = os.path.split(filepath)[1]
        filetitle = filename
        suffix = ''

    # 可能需要考虑原有文件夹中添加后缀-new1后的重名情况
    new_filename = filename
    count = 0
    while os.path.exists(os.path.join(the_dirpath, new_filename)):  # 一直累加循环直到不存在同名
        count += 1
        new_filename = f"{filetitle} -new{count}{suffix}"

    return new_filename


def process_nested_folders(folder: str, target_folder: str = None, mode=True) -> str:
    """传入文件夹路径folder参数，将最深一级非空文件夹移动到target_folder中（处理套娃文件夹），并返回最终路径str
    可选参数
    mode:默认True，处理套娃文件夹；可选Flase，不处理套娃文件夹，仅做1次基础移动操作
    target_folder:目标移动文件夹，若为空则移动到folder的父目录下"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    # 提取需要移动的文件/文件夹路径
    if mode:
        need_move_path = get_deepest_dirpath(folder)  # 需要移动的文件夹/文件的路径
    else:
        number_in_folder = len(os.listdir(folder))
        if number_in_folder == 1:
            need_move_path = os.path.normpath(os.path.join(folder, os.listdir(folder)[0]))
        else:
            need_move_path = folder  # 需要移动的文件夹/文件的路径

    if need_move_path == folder:  # 如果一致，则不进行后续操作
        return need_move_path
    need_move_filename = os.path.split(need_move_path)[1]  # 需要移动的文件夹/文件的文件名

    # 生成目标文件夹下无重名文件/文件夹名称，移动后生成最终路径
    if target_folder:
        final_folder = target_folder
    else:
        final_folder = os.path.split(folder)[0]  # folder的父目录（移动到该目录下）
    if need_move_filename.lower() not in [x.lower() for x in os.listdir(final_folder)]:  # 如果没有重名的文件/文件夹
        try:
            shutil.move(need_move_path, final_folder)  # 有时报错OSError: [WinError 145] 目录不是空的。
        except OSError:
            delete_folder_if_empty(need_move_path)
        new_path = os.path.normpath(os.path.join(final_folder, need_move_filename))  # 最终路径
    else:
        new_filename = get_no_dup_filename(need_move_path, final_folder)  # 最终文件名
        old_path_with_newname = os.path.normpath(os.path.join(os.path.split(need_move_path)[0], new_filename))
        try:
            try:
                os.rename(need_move_path, old_path_with_newname)  # 有时报错PermissionError: [WinError 5] 拒绝访问。
            except PermissionError:
                time.sleep(1)  # 备忘录-拒绝访问不知道哪里占用了，可能是找非重名文件夹，等1秒让系统处理完
                os.rename(need_move_path, old_path_with_newname)
        except PermissionError:  # 如果等1秒还不能解决占用问题，则直接移动到生成的文件夹中
            # 修改变量
            old_path_with_newname = need_move_path
            random_ascii = ''.join(random.choices(string.ascii_lowercase, k=6))  # 随机6位小写字母
            final_folder = os.path.normpath(
                os.path.join(final_folder, os.path.split(need_move_path)[1] + f' -{random_ascii}'))

        try:
            shutil.move(old_path_with_newname, final_folder)  # 有时报错OSError: [WinError 145] 目录不是空的。
        except OSError:
            delete_folder_if_empty(need_move_path)
        new_path = os.path.normpath(os.path.join(final_folder, new_filename))  # 最终路径

    delete_folder_if_empty(folder)  # 如果原文件夹为空，则删除

    return new_path


def get_first_split_archive_filetitle(filename: str) -> Union[str, bool]:
    """通过传入的文件名，判断其是否符合分卷压缩包规则并生成第一个分卷包名，返回str或bool值"""
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    re_rar = r"^(.+)\.part(\d+)\.rar$"  # 分卷压缩文件的命名规则
    re_7z = r"^(.+)\.7z\.\d+$"
    re_zip_first = r"^(.+)\.zip$"
    re_zip = r"^(.+)\.z\d+$"
    re_zip_type2 = r"^(.+)\.zip\.\d+$"

    # 匹配7z正则
    if re.match(re_7z, filename):
        archive_filetitle = re.match(re_7z, filename).group(1)  # 提取文件名
        first_split_archive_filetitle = archive_filetitle + r'.7z.001'  # 生成第一个分卷压缩包名
    # 匹配rar正则
    elif re.match(re_rar, filename):
        archive_filetitle = re.match(re_rar, filename).group(1)
        number_type = len(re.match(re_rar, filename).group(2))

        first_split_archive_filetitle = archive_filetitle + rf'.part{str(1).zfill(number_type)}.rar'
    # 匹配zip格式2正则
    elif re.match(re_zip_type2, filename):
        archive_filetitle = re.match(re_zip_type2, filename).group(1)  # 提取文件名
        first_split_archive_filetitle = archive_filetitle + r'.zip.001'
    # 匹配zip正则
    elif re.match(re_zip, filename) or re.match(re_zip_first, filename):  # 只要是zip后缀的，都视为分卷压缩包，因为第一个包都是.zip后缀
        if re.match(re_zip, filename):
            archive_filetitle = re.match(re_zip, filename).group(1)
        else:
            archive_filetitle = re.match(re_zip_first, filename).group(1)
        first_split_archive_filetitle = archive_filetitle + r'.zip'
    else:
        return False

    return first_split_archive_filetitle


def get_split_archive_dict(filelist: list) -> dict:
    """传入文件路径列表list，提取其中符合分卷压缩包命名规则的文件，并扩展到其所在文件夹，补全完整的分卷压缩包分卷
    返回分卷压缩包dict {A压缩包第一个分卷包路径:(A压缩包全部分卷路径), ...}
    """
    print(time.strftime("%Y.%m.%d %H:%M:%S ", time.localtime()), inspect.currentframe().f_code.co_name)  # 打印当前运行函数名
    split_archive_dict = {}  # 最终结果
    # 按文件所在的父文件夹建立字典 {文件父文件夹:(A文件, B文件), ...}
    folder_dict = {}
    for file in filelist:
        parent_folder = os.path.split(file)[0]
        if parent_folder not in folder_dict:
            folder_dict[parent_folder] = set()  # 用集合添加，便于去重
        folder_dict[parent_folder].add(file)
    # 按文件夹逐个处理其中的文件
    for parent_folder in folder_dict:
        files_set = folder_dict[parent_folder]
        filenames_in_parent_folder = os.listdir(parent_folder)
        # 利用正则匹配分卷压缩包
        all_filenames = [os.path.split(i)[1] for i in files_set]  # 提取出文件名

        for filename in all_filenames:
            full_filepath = os.path.normpath(os.path.join(parent_folder, filename))  # 还原当前处理文件的完整文件路径
            first_split_archive_filetitle = get_first_split_archive_filetitle(filename)
            if first_split_archive_filetitle:
                first_split_archive = os.path.normpath(os.path.join(parent_folder, first_split_archive_filetitle))
            else:
                break

            # 处理识别出来的第一个分卷包
            if first_split_archive not in split_archive_dict:  # 如果文件名不在字典内，则添加一个空键值对
                split_archive_dict[first_split_archive] = set()  # 用集合添加，方便去重
            split_archive_dict[first_split_archive].add(full_filepath)  # 添加键值对 {示例.7z.001:(示例.7z.001,示例.7z.002)}
            split_archive_dict[first_split_archive].add(first_split_archive)
        # 扩展压缩包识别范围，补全完整的分卷压缩包分卷
        for check_filename in filenames_in_parent_folder:
            full_path = os.path.normpath(os.path.join(parent_folder, check_filename))
            check_title = get_first_split_archive_filetitle(check_filename)
            if check_title:
                check_path = os.path.normpath(os.path.join(parent_folder, check_title))
            else:
                break

            if check_path in split_archive_dict:
                split_archive_dict[check_path].add(full_path)

    return split_archive_dict
