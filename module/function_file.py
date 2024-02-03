# 文件/文件夹操作的相关方法

import os
import re
import shutil

import send2trash

from module import function_normal


def get_folder_size(folder: str) -> int:
    """
    获取指定文件夹的总大小/byte
    :param folder: str类型，文件夹路径
    :return: int类型，总字节大小
    """
    function_normal.print_function_info()
    folder_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for item in filenames:
            filepath = os.path.join(dirpath, item)
            folder_size += os.path.getsize(filepath)

    return folder_size


def get_files_list(folder: str) -> list:
    """
    获取指定文件夹中的所有文件路径
    :param folder: str类型，文件夹路径
    :return: list类型，所有文件路径的列表
    """
    function_normal.print_function_info()
    filelist = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.normpath(os.path.join(dirpath, filename))
            filelist.append(file_path)

    return filelist


def get_first_multi_folder(dirpath: str) -> str:
    """
    检查传入文件夹路径的层级，找出首个含多文件/文件夹的文件夹路径或唯一的文件路径
    :param dirpath: str类型，文件夹路径
    :return: str类型，文件夹路径或文件路径
    """
    function_normal.print_function_info()
    if len(os.listdir(dirpath)) == 1:  # 如果文件夹下只有一个文件/文件夹
        check_path = os.path.normpath(os.path.join(dirpath, os.listdir(dirpath)[0]))
        # 如果是文件，则直接返回
        if os.path.isfile(check_path):
            return check_path
        # 如果是文件夹，则递归
        else:
            return get_first_multi_folder(check_path)
    else:
        return dirpath


def handling_nested_folder(dirpath: str, is_retain_itself=False):
    """处理嵌套文件夹，将其内容移动到顶层文件夹
    :param dirpath: str类型，文件夹路径
    :param is_retain_itself: bool类型，是否保留传入的文件夹（即解套至该文件夹之下而非之上）
    """
    function_normal.print_function_info()
    # 找到首个多重文件夹
    first_multi_folder = get_first_multi_folder(dirpath)
    # 如果传入的文件夹就是首个多重文件夹，则直接返回
    if first_multi_folder == os.path.normpath(dirpath):
        return first_multi_folder
    # 移动该文件夹
    if is_retain_itself:  # 移动至顶层文件夹之下
        new_path = move_file(first_multi_folder, dirpath)
        # 删除原文件夹
        for i in os.listdir(dirpath):
            fullpath = os.path.normpath(os.path.join(dirpath, i))
            if fullpath != new_path:
                delete_empty_folder(fullpath)

        return new_path
    else:  # 移动至顶层文件夹之上
        top_folder = os.path.split(dirpath)[0]
        new_path = move_file(first_multi_folder, top_folder)
        # 删除原文件夹
        delete_empty_folder(dirpath)

        return new_path


def move_file(path, target_folder) -> str:
    """移动文件/文件夹至指定目录下
    :param path: 需要移动的文件/文件夹路径
    :param target_folder: 目标文件夹路径
    :return: 移动后的文件/文件夹路径"""
    function_normal.print_function_info()
    # 为了防止文件名重复而报错，先改名再移动
    parent_folder, _ = os.path.split(path)
    nodup_name = create_nodup_filename(path, target_folder)
    new_path_renamed = os.path.join(parent_folder, nodup_name)
    os.rename(path, new_path_renamed)
    shutil.move(new_path_renamed, target_folder)

    new_path_final = os.path.normpath(os.path.join(target_folder, nodup_name))
    return new_path_final


def create_nodup_filename(path: str, target_dirpath: str, add_suffix: str = ' -New') -> str:
    """
    生成传入的文件或文件夹在指定文件夹中没有重复的文件名（添加自定义后缀）
    :param path: 文件或文件夹路径str
    :param target_dirpath: 指定文件夹路径str
    :param add_suffix: 自定义后缀
    :return: str，无重复的文件名（非完整路径，仅文件名）
    """
    function_normal.print_function_info()
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
    function_normal.print_function_info()
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
        rules = [pattern_7z, pattern_rar, pattern_rar_without_suffix, pattern_zip, pattern_zip_volume,
                 pattern_zip_type2]
        filename = os.path.split(path)[1]
        for rule in rules:
            if re.match(rule, filename):
                filetitle = re.match(rule, filename).group(1)
                break

    # 处理文件两端多余的空格和.
    while filetitle[0] in [' ', '.'] or filetitle[-1] in [' ', '.']:
        filetitle = filetitle.strip()
        filetitle = filetitle.strip('.')

    return filetitle


def delete_empty_folder(folder: str) -> bool:
    """检查文件夹是否为空，是则删除"""
    function_normal.print_function_info()
    if os.path.exists(folder) and get_folder_size(folder) == 0:
        send2trash.send2trash(folder)
        return True
    else:
        return False
