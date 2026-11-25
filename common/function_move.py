import os
import shutil
from typing import List, Optional

import lzytools
import lzytools_archive

from common import function_file


def move_to_smart(
        dirpath: str,
        target_dirpath: str,
        dirname_: Optional[str] = None
) -> str:
    """移动内部文件至指定文件夹（智能模式）。

    :param dirpath: 需要检查的文件夹
    :param target_dirpath: 移动至目标文件夹
    :param dirname_: 指定的文件夹名称，特殊情况使用
    :return: 移动后的路径
    """
    # 找出最深一级的存在多文件的文件夹/或文件
    deepest_file = lzytools.file.get_first_multi_file_dirpath(dirpath)

    if os.path.normpath(deepest_file) == os.path.normpath(dirpath):
        # 最深一级就是顶层目录本身：先在临时文件夹内新建一层，再整体移出，
        # 否则临时文件夹会成为解压文件夹的外部目录
        if not dirname_:
            raise ValueError('智能模式需要指定文件夹名称')

        dirname_ = _get_available_dirname(dirpath, dirname_)
        move_dirpath = os.path.normpath(os.path.join(dirpath, dirname_))
        _move_inside_file_to_folder(deepest_file, move_dirpath)
        moved_files = function_file.move_file_to_folder(move_dirpath, target_dirpath)
    else:
        # 直接移动找到的文件/文件夹
        moved_files = function_file.move_file_to_folder(deepest_file, target_dirpath)

    # 本次只移动一个路径，取第一个结果即可
    return list(moved_files.values())[0]


def move_to_no_deal(dirpath: str, target_dirpath: str) -> str:
    """移动内部文件至指定文件夹（不做处理）。

    :param dirpath: 需要检查的文件夹
    :param target_dirpath: 移动至目标文件夹
    :return: 移动后的路径
    """
    # 逻辑类似智能模式，但不搜索最深的文件，直接移动一级目录内的子项
    files = _get_child_paths(dirpath)
    moved_files = function_file.move_file_to_folder(files, target_dirpath)

    # 调用方只需要一个结果，取第一个移动后的路径
    return list(moved_files.values())[0]


def move_to_same_dirname(
        dirpath: str,
        target_dirpath: str,
        dirname_: Optional[str] = None
) -> str:
    """移动内部文件至指定文件夹的同名目录中。

    :param dirpath: 需要检查的文件夹
    :param target_dirpath: 移动至目标文件夹
    :param dirname_: 指定的文件夹名称
    :return: 移动后的路径
    """
    if not dirname_:
        # 未指定名称时，取原文件夹的名称（剔除压缩文件后缀）
        dirname_ = lzytools_archive.get_filetitle(os.path.basename(dirpath))

    # 检查目标目录中是否存在同名文件夹
    if lzytools.file.is_dup_filename(dirname_, target_dirpath):
        dirname_ = lzytools.file.create_nodup_filename_standard_digital_suffix(
            filetitle=dirname_,
            check_dirpath=target_dirpath
        )

    dirpath_ = os.path.normpath(os.path.join(target_dirpath, dirname_))
    os.mkdir(dirpath_)

    # 原目录下只有一个同名子文件夹时，移动该子文件夹的内容，避免多套一层目录
    inside = os.listdir(dirpath)
    if len(inside) == 1 and inside[0] == dirname_:
        child_filepath = os.path.normpath(os.path.join(dirpath, inside[0]))
        return _move_inside_file_to_folder(child_filepath, dirpath_)

    return _move_inside_file_to_folder(dirpath, dirpath_)


def _move_inside_file_to_folder(origin_dirpath: str, target_dirpath: str) -> str:
    """移动一个文件夹内部的文件到另一个文件夹。

    :param origin_dirpath: 原文件夹路径
    :param target_dirpath: 目标文件夹路径
    :return: 目标文件夹路径
    """
    if os.path.normpath(origin_dirpath) == os.path.normpath(target_dirpath):
        return target_dirpath
    if not os.path.exists(origin_dirpath):
        raise FileNotFoundError(f'目录不存在: {origin_dirpath}')
    if not os.path.exists(target_dirpath):
        os.mkdir(target_dirpath)

    files = _get_child_paths(origin_dirpath)
    try:
        _move_files(files, target_dirpath)
    except FileNotFoundError:
        # Windows 会修剪 os.mkdir() 创建的文件夹名两端的空格和右端的点，
        # 导致 shutil.move() 按原名找不到目标目录
        # 2025.09.28 修复两端空格；2026.01.13 修复右端的点
        actual_target = _find_trimmed_target(target_dirpath)
        _move_files(files, actual_target)

    return target_dirpath


def _get_child_paths(dirpath: str) -> List[str]:
    """返回文件夹内一级子项的完整路径。"""
    filenames = os.listdir(dirpath)
    return [os.path.normpath(os.path.join(dirpath, filename)) for filename in filenames]


def _move_files(files: List[str], target_dirpath: str) -> None:
    """将文件/文件夹逐个移动到目标文件夹。"""
    for file in files:
        shutil.move(file, target_dirpath)


def _find_trimmed_target(target_dirpath: str) -> str:
    """返回 Windows 修剪文件夹名后实际存在的空目标文件夹。"""
    dirname_ = os.path.basename(target_dirpath)
    parent_dirpath = os.path.dirname(target_dirpath)

    # 依次尝试：两端空格、右端空格/点、左端空格
    trimmed_names = [
        dirname_.strip().rstrip('.').strip(),
        dirname_.rstrip().rstrip('.').rstrip(),
        dirname_.lstrip().rstrip('.')
    ]
    for name in trimmed_names:
        candidate = os.path.normpath(os.path.join(parent_dirpath, name))
        if os.path.isdir(candidate) and not os.listdir(candidate):
            return candidate

    raise FileNotFoundError(f'未找到可用的目标文件夹: {target_dirpath}')


def _get_available_dirname(dirpath: str, dirname: str) -> str:
    """返回文件夹内可用的新建文件夹名称。"""
    # 2026.09.16 修复：一级目录中同时存在多个文件，且存在与压缩文件同名的文件夹时，
    # 新建文件夹会与已有文件夹冲突，需先生成不重名的名称
    filenames = os.listdir(dirpath)
    if len(filenames) >= 2 and dirname.lower() in filenames:
        return lzytools.file.create_nodup_filename_standard_digital_suffix(
            filetitle=dirname,
            check_dirpath=dirpath
        )
    return dirname
