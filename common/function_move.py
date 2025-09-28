import os
import shutil

import lzytools.archive
import lzytools.file

from common import function_file


def move_to_smart(dirpath: str, target_dirpath: str, dirname_=None):
    """移动内部文件至指定文件夹（智能模式）
    :param dirpath: 需要检查的文件夹
    :param target_dirpath: 移动至目标文件夹
    :param dirname_: 指定的文件夹名称，特殊情况使用"""
    # 找出最深一级的存在多文件的文件夹/或文件
    deepest_file = lzytools.file.get_first_multi_file_dirpath(dirpath)

    # 如果找到的文件夹是其自身，则需要新建一个文件夹，移动到该文件夹下
    # （传入的dirpath路径为临时文件夹的路径，如果为其自身会导致该临时文件夹作为解压文件夹的外部文件夹）
    if deepest_file == dirpath:
        # 先新建指定文件名的文件夹，将内部文件移动至该文件夹下，然后在移动到外部
        move_dirpath = os.path.normpath(os.path.join(dirpath, dirname_))
        _move_inside_file_to_folder(deepest_file, move_dirpath)
        new_file_dict = function_file.move_file_to_folder(move_dirpath, target_dirpath)
    else:
        # 移动找到的文件
        new_file_dict = function_file.move_file_to_folder(deepest_file, target_dirpath)

    move_path: str = list(new_file_dict.values())[0]  # 仅处理一个文件，value即为最终的路径
    return move_path


def move_to_no_deal(dirpath: str, target_dirpath):
    """移动内部文件至指定文件夹（不做处理的）
    :param dirpath: 需要检查的文件夹
    :param target_dirpath: 移动至目标文件夹"""
    # 逻辑类似于智能模式，但是不需要搜索最深的文件，直接移动即可
    # 遍历一级目录内的文件
    files = [os.path.normpath(os.path.join(dirpath, i)) for i in os.listdir(dirpath)]

    # 移动
    new_file_dict = function_file.move_file_to_folder(files, target_dirpath)

    move_path: str = list(new_file_dict.values())[0]  # 仅处理一个文件，value即为最终的路径
    return move_path


def move_to_same_dirname(dirpath: str, target_dirpath, dirname_=None):
    """移动内部文件至指定文件夹的同名目录中
    :param dirpath: 需要检查的文件夹
    :param target_dirpath: 移动至目标文件夹
    :param dirname_: 指定的文件夹名称"""

    if not dirname_:  # 不指定文件夹名称时，读取文件夹的名称
        ft_ = os.path.basename(dirpath)
        dirname_ = lzytools.archive.get_filetitle(ft_)
    else:
        dirname_ = dirname_[:]  # 复制，防止修改源对象

    # 检查文件夹名是否重复
    is_dup = lzytools.file.is_dup_filename(dirname_, target_dirpath)
    if is_dup:
        dirname_ = lzytools.file.create_nodup_filename_standard_digital_suffix(dirname_, target_dirpath)

    # 组合文件夹，并新建
    dirpath_ = os.path.normpath(os.path.join(target_dirpath, dirname_))
    os.mkdir(dirpath_)

    # 如果原目录下仅有一个文件夹且文件名与目标文件夹同名，则移动该子文件夹下的文件
    inside = os.listdir(dirpath)
    if len(inside) == 1 and inside[0] == dirname_:
        child_filepath = os.path.normpath(os.path.join(dirpath, inside[0]))
        move_path = _move_inside_file_to_folder(child_filepath, dirpath_)
    else:
        move_path = _move_inside_file_to_folder(dirpath, dirpath_)

    return move_path


def _move_inside_file_to_folder(origin_dirpath: str, target_dirpath: str):
    """移动一个文件夹内部的文件到另一个文件夹"""
    if os.path.normpath(origin_dirpath) == os.path.normpath(target_dirpath):
        return target_dirpath
    if not os.path.exists(origin_dirpath):
        raise Exception(origin_dirpath, '目录不存在')
    if not os.path.exists(target_dirpath):
        os.mkdir(target_dirpath)

    # 提取原目录文件
    filenames = os.listdir(origin_dirpath)
    files = [os.path.normpath(os.path.join(origin_dirpath, i)) for i in filenames]

    # 移动
    try:
        for file in files:
            shutil.move(file, target_dirpath)
    except FileNotFoundError:
        # 2025.09.28 修复两端文件名存在空格时的bug
        # bug原因：os.mkdir()创建的文件夹名由于Windows的文件名修剪机制，不会包含两端空格

        # 检查目标文件夹两端是否存在空格，并剔除后检查文件夹是否存在并且是否为空
        filename_strip = os.path.basename(target_dirpath).strip()
        filename_rstrip = os.path.basename(target_dirpath).rstrip()
        filename_lstrip = os.path.basename(target_dirpath).lstrip()
        parent_dirpath = os.path.dirname(target_dirpath)
        target_dirpath_strip = os.path.normpath(os.path.join(parent_dirpath, filename_strip))
        target_dirpath_rstrip = os.path.normpath(os.path.join(parent_dirpath, filename_rstrip))
        target_dirpath_lstrip = os.path.normpath(os.path.join(parent_dirpath, filename_lstrip))
        if os.path.exists(target_dirpath_strip) and not os.listdir(target_dirpath_strip):
            for file in files:
                shutil.move(file, target_dirpath_strip)
        elif os.path.exists(target_dirpath_rstrip) and not os.listdir(target_dirpath_rstrip):
            for file in files:
                shutil.move(file, target_dirpath_rstrip)
        elif os.path.exists(target_dirpath_lstrip) and not os.listdir(target_dirpath_lstrip):
            for file in files:
                shutil.move(file, target_dirpath_lstrip)
        else:
            raise Exception('未知错误')
    return target_dirpath
