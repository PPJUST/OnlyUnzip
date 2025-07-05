import os
import shutil
from typing import Union

import lzytools


def move_file_to_folder(file_move: Union[str, list], target_dirpath: str) -> dict:
    """移动文件/文件夹
    :param file_move: 需要移动的文件/文件夹路径
    :param target_dirpath: 移动至目标文件夹
    :return: 新旧文件路径对应的字典"""
    # 统一格式
    if isinstance(file_move, str):
        file_move = [file_move]

    # 检查需要移动的文件/文件夹在目标目录中是否存在重复的文件名
    file_dict = dict()  # 新旧文件路径对应的字典
    for file in file_move:
        filename = os.path.basename(file)
        is_dup = lzytools.file.is_dup_filename(filename, target_dirpath)
        if is_dup:
            # 区分文件与文件夹，两种类型的命名方式不同（主要是为了防止文件夹名称中带.时误判为后缀名的情况）
            if os.path.isdir(file):
                no_dup_name = lzytools.file.create_nodup_filename_standard_digital_suffix(filename, target_dirpath)
            else:
                filetitle, file_extension = os.path.splitext(filename)
                no_dup_name = lzytools.file.create_nodup_filename_standard_digital_suffix(filetitle=filetitle,
                                                                                          filename_extension=file_extension,
                                                                                          check_dirpath=target_dirpath)
        else:
            no_dup_name = filename

        # 组合新的文件/文件夹路径
        new_filepath = os.path.normpath(os.path.join(target_dirpath, no_dup_name))

        # 移动
        shutil.move(file, new_filepath)
        file_dict[file] = new_filepath

    return file_dict


def break_folder_bottom(dirpath: str):
    """解散文件夹
    移动最底层的首个非空文件夹到顶层目录之外（并删除空的顶层目录）"""
    # 找出最深一级的存在多文件的文件夹/或文件
    deepest_file = lzytools.file.get_first_multi_file_dirpath(dirpath)

    # 移动到目录之外
    parent_dirpath = os.path.dirname(dirpath)
    new_file_dict = move_file_to_folder(deepest_file, parent_dirpath)

    # 如果顶层目录为空，则删除
    if not lzytools.file.get_size(dirpath):
        os.remove(dirpath)

    move_path: str = list(new_file_dict.values())[0]  # 仅处理一个文件，value即为最终的路径
    return move_path


def break_folder_top(dirpath: str):
    """解散文件夹
    移动最底层的首个非空文件夹下的文件到顶层目录之下（保持文件层级结构，并删除空的该底层文件夹）"""
    # 找出最深一级的存在多文件的文件夹/或文件
    deepest_file = lzytools.file.get_first_multi_file_dirpath(dirpath)

    # 移动到目录之下
    new_file_dict = move_file_to_folder(deepest_file, dirpath)

    # 如果底层目录为空，则删除
    if not lzytools.file.get_size(deepest_file):
        os.remove(deepest_file)

    move_path: str = dirpath  # 文件夹未变动，不需要重新赋值
    return move_path


def break_folder_files(dirpath: str):
    """解散文件夹
    移动所有文件到顶层目录之下（并删除空的子文件夹）"""
    # 提取文件清单
    files = lzytools.file.get_files_in_dir(dirpath)

    # 逐个移动
    for file in files:
        move_file_to_folder(file, dirpath)

    move_path: str = dirpath  # 文件夹未变动，不需要重新赋值
    return move_path
