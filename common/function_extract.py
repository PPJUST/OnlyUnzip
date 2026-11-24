"""临时解压文件夹的查找与删除。"""

import os
from typing import Optional, Sequence, Union

import lzytools
import natsort

TEMP_EXTRACT_FOLDER = 'UnzipTempFolder'  # 临时解压文件夹名称

PathInput = Union[str, Sequence[str]]
TempFolderResult = tuple[bool, Optional[str]]


def is_exists_temp_folder(paths: PathInput) -> TempFolderResult:
    """检查是否存在包含数据的临时解压文件夹，并返回第一个匹配的路径。"""
    for temp_folder in _create_temp_folder_paths(paths):
        if _is_non_empty_path(temp_folder):
            return True, temp_folder
    return False, None


def delete_temp_folder(paths: PathInput) -> None:
    """删除传入路径对应的临时解压文件夹。"""
    for temp_folder in _create_temp_folder_paths(paths):
        if os.path.exists(temp_folder):
            lzytools.file.delete(temp_folder, send_to_trash=False)


def _create_temp_folder_paths(paths: PathInput) -> list[str]:
    """生成去重且按自然顺序排序的临时解压文件夹路径。"""
    path_list = [paths] if isinstance(paths, str) else paths
    temp_folders = {_get_temp_folder_path(path) for path in path_list}
    return natsort.os_sorted(temp_folders)


def _get_temp_folder_path(path: str) -> str:
    """获取文件所在目录或传入目录下的临时解压文件夹路径。"""
    parent_folder = os.path.dirname(path) if os.path.isfile(path) else path
    return os.path.join(parent_folder, TEMP_EXTRACT_FOLDER)


def _is_non_empty_path(path: str) -> bool:
    """判断路径是否存在且包含数据。"""
    return os.path.exists(path) and bool(lzytools.file.get_size(path))
