import os
import shutil
from typing import Dict, List, Union

import lzytools


def move_file_to_folder(
        files_need_move: Union[str, List[str]],
        target_dirpath: str
) -> Dict[str, str]:
    """移动文件/文件夹到目标目录。

    :param files_need_move: 需要移动的路径，支持单个路径或路径列表
    :param target_dirpath: 目标文件夹路径
    :return: 原路径到新路径的映射
    """
    # 统一处理单个路径和路径列表
    if isinstance(files_need_move, str):
        files_need_move = [files_need_move]

    moved_files: Dict[str, str] = {}
    for file in files_need_move:
        # 目标目录位于待移动路径内部时跳过，避免把父目录移动到自身内部
        if lzytools.file.is_subpath(file, target_dirpath):
            continue

        filename = os.path.basename(file)
        no_dup_name = _get_no_duplicate_name(file, filename, target_dirpath)
        new_filepath = os.path.normpath(os.path.join(target_dirpath, no_dup_name))

        shutil.move(file, new_filepath)
        moved_files[file] = new_filepath

    return moved_files


def _get_no_duplicate_name(file: str, filename: str, target_dirpath: str) -> str:
    """返回目标目录中不重名的文件/文件夹名称。"""
    if not lzytools.file.is_dup_filename(filename, target_dirpath):
        return filename

    # 文件夹名称可能包含“.”，按整体处理，避免被误判为文件后缀
    if os.path.isdir(file):
        return lzytools.file.create_nodup_filename_standard_digital_suffix(
            filetitle=filename,
            check_dirpath=target_dirpath
        )

    filetitle, file_extension = os.path.splitext(filename)
    return lzytools.file.create_nodup_filename_standard_digital_suffix(
        filetitle=filetitle,
        check_dirpath=target_dirpath,
        filename_extension=file_extension
    )


def break_folder_bottom(dirpath: str) -> str:
    """解散文件夹：将最底层首个非空文件夹移到顶层目录之外。

    :param dirpath: 需要解散的顶层文件夹路径
    :return: 移动后的路径；无需移动时返回原路径
    """
    deepest_file = lzytools.file.get_first_multi_file_dirpath(dirpath)

    # 最深一级就是顶层目录本身，无需移动
    if os.path.normpath(deepest_file) == os.path.normpath(dirpath):
        return dirpath

    parent_dirpath = os.path.dirname(dirpath)
    moved_files = move_file_to_folder(deepest_file, parent_dirpath)

    # 顶层目录已为空，删除该目录
    if os.path.isdir(dirpath) and not os.listdir(dirpath):
        os.rmdir(dirpath)

    # 本次只移动一个路径，取第一个结果即可
    return list(moved_files.values())[0]


def break_folder_top(dirpath: str) -> str:
    """解散文件夹：将最底层首个非空文件夹下的内容移到顶层目录。

    :param dirpath: 需要解散的顶层文件夹路径
    :return: 顶层文件夹路径
    """
    deepest_file = lzytools.file.get_first_multi_file_dirpath(dirpath)

    move_file_to_folder(deepest_file, dirpath)

    # 删除移动后留下的空目录；若 deepest_file 是文件，该调用不会产生操作
    lzytools.file.delete_empty_folder(deepest_file, send_to_trash=False)

    return dirpath


def break_folder_files(dirpath: str) -> str:
    """解散文件夹：将所有文件移到顶层目录下，并删除空的子文件夹。

    :param dirpath: 需要解散的顶层文件夹路径
    :return: 顶层文件夹路径
    """
    files = lzytools.file.get_files_in_dir(dirpath)

    for file in files:
        move_file_to_folder(file, dirpath)

    lzytools.file.delete_empty_folder(dirpath)

    return dirpath
