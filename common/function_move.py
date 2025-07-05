import os

import lzytools.file

from common import function_file

TEMP_EXTRACT_FOLDER = 'UnzipTempFolder'


def move_to_smart(dirpath: str, target_dirpath:str):
    """移动内部文件至指定文件夹（智能模式）
    :param dirpath: 需要检查的文件夹
    :param target_dirpath: 移动至目标文件夹"""
    # 找出最深一级的存在多文件的文件夹/或文件
    deepest_file = lzytools.file.get_first_multi_file_dirpath(dirpath)

    # 移动找到的文件
    new_file_dict = function_file.move_file_to_folder(deepest_file, target_dirpath)

    move_path:str = list(new_file_dict.values())[0]  # 仅处理一个文件，value即为最终的路径
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

    move_path :str = list(new_file_dict.values())[0]  # 仅处理一个文件，value即为最终的路径
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

    # 移动
    move_path :str  = move_to_smart(dirpath, dirpath_)

    return move_path
