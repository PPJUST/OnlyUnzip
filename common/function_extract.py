import os
from typing import Union, Tuple

import lzytools.file
import natsort

TEMP_EXTRACT_FOLDER = 'UnzipTempFolder'  # 临时解压文件夹名称


def is_exists_temp_folder(paths: Union[list, str]) -> Tuple[bool, Union[str, None]]:
    """检查传入路径的同级目录中是否存在临时解压文件夹"""
    temp_folders = _create_temp_folder_path(paths)

    # 检查生成的路径是否存在
    for path in temp_folders:
        if os.path.exists(path) and lzytools.file.get_size(path):  # 路径存在且为空
            print('存在临时文件夹且不为空', path, os.listdir(path))
            return True, path

    return False, None


def delete_temp_folder(paths: Union[list, str]):
    """删除传入路径的同级目录中存在的临时解压文件夹"""
    temp_folders = _create_temp_folder_path(paths)

    # 检查生成的路径是否存在
    for path in temp_folders:
        if os.path.exists(path):
            os.remove(path)


def _create_temp_folder_path(paths: Union[list, str]) -> list:
    """生成传入路径中的文件的所在目录的临时解压文件夹路径（虚拟的路径，仅供测试）
    :return: 生成的虚拟路径列表"""
    # 统一格式
    if isinstance(paths, str):
        paths = [paths]

    # 生成临时解压文件夹虚拟路径（添加后缀生成，非真实路径）
    temp_folders = set()
    for path in paths:
        if os.path.isfile(path):
            join_path = os.path.join(os.path.dirname(path), TEMP_EXTRACT_FOLDER)
            temp_folders.add(join_path)
        else:
            join_path = os.path.join(path, TEMP_EXTRACT_FOLDER)
            temp_folders.add(join_path)

    # 路径排序
    temp_folders = natsort.os_sorted(temp_folders)

    return temp_folders
