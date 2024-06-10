# 压缩文件相关方法
import os
import re
from typing import Union

import filetype

from constant import PATTERN_7Z, PATTERN_RAR_WITHOUT_SUFFIX, PATTERN_ZIP, PATTERN_ZIP_VOLUME, PATTERN_ZIP_TYPE2, \
    PATTERN_RAR


def is_archive(filepath: str) -> Union[bool, str]:
    """文件是否为压缩文件
    :param filepath: str类型，文件路径
    :return: 压缩文件类型/False
    """
    archive_type = ['zip', 'tar', 'rar', 'gz', '7z', 'xz', 'iso']
    if not os.path.exists(filepath):
        return False
    elif os.path.isdir(filepath):
        return False
    else:
        # 先通过文件后缀判断
        file_suffix = os.path.splitext(filepath)[1][1:].lower()  # 提取文件后缀名（不带.）
        if file_suffix in archive_type:
            print(filepath, ' 文件类型 ', file_suffix)
            return file_suffix

        # 再通过filetype库判断
        kind = filetype.guess(filepath)
        if kind is None:
            return False
        else:
            type_kind = kind.extension
            if type_kind in archive_type:
                print(filepath, ' 文件类型 ', type_kind)
                return type_kind

        return False


def split_archive(archives: list) -> dict:
    """分离压缩文件（分卷压缩文件与其他）
    :return: dict结构：key为第一个分卷包路径/非分卷则为其本身，value为list，内部元素为其对应的所有分卷包"""
    file_dict = {}  # 结构：key为第一个分卷包路径，value为list，内部元素为其对应的所有分卷包
    # 统一路径格式
    archives = [os.path.normpath(i) for i in archives]
    archives = list(set(archives))
    # 初步区分分卷与非分卷
    volume_archives = []  # 分卷
    for file in archives:
        if is_volume_archive(file):
            volume_archives.append(file)
        else:
            file_dict[file] = set()
            file_dict[file].add(file)

    # 进一步处理分卷，合并同一分卷+补充缺失的分卷包
    # 按文件夹拆分，同一个文件夹下的放一起
    split_folder_dict = {}  # 结构：key为文件夹路径，value为list，内部元素为对应的内部分卷包路径
    for path in volume_archives:
        parent_folder = os.path.dirname(path)
        if parent_folder not in split_folder_dict:
            split_folder_dict[parent_folder] = []
        split_folder_dict[parent_folder].append(path)
    # 逐个处理分卷文件，生成虚拟包名
    dirpath_list = set()  # 用于后续扩展补充缺失分卷包
    for dirpath, files in split_folder_dict.items():
        # 逐个处理分卷包，生成虚拟的第一个分卷包名，合并生成相同虚拟包名的分卷包
        dirpath_list.add(dirpath)
        for file in files:
            first_volume_path = create_fake_first_volume_path(file)
            if first_volume_path not in file_dict:
                file_dict[first_volume_path] = set()
            file_dict[first_volume_path].add(file)
    # 检查同级文件，补充缺失的分卷包
    for dirpath in dirpath_list:
        listdir = [os.path.normpath(os.path.join(dirpath, i)) for i in os.listdir(dirpath)]
        for file in listdir:
            if is_volume_archive(file):
                first_volume_path = create_fake_first_volume_path(file)
                if first_volume_path in file_dict:
                    file_dict[first_volume_path].add(file)

    return file_dict


def is_volume_archive(file):
    """判断是否为分卷压缩文件（通过文件后缀名判断）"""
    filename = os.path.basename(file)
    if (re.match(PATTERN_7Z, filename, flags=re.I)
            or re.match(PATTERN_RAR, filename, flags=re.I)
            or re.match(PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I)
            or re.match(PATTERN_ZIP, filename, flags=re.I)
            or re.match(PATTERN_ZIP_VOLUME, filename, flags=re.I)
            or re.match(PATTERN_ZIP_TYPE2, filename, flags=re.I)):
        return True
    else:
        return False


def create_fake_first_volume_path(file, return_filetitle=False):
    """生成第一个分卷包的虚拟路径"""
    dir_, filename = os.path.split(file)
    filetitle = os.path.splitext(filename)[0]  # 兜底文件标题（不含后缀）
    # test.7z.001/test.7z.002/test.7z.003
    if re.match(PATTERN_7Z, filename, flags=re.I):
        filetitle = re.match(PATTERN_7Z, filename, flags=re.I).group(1)
        first_volume_path = os.path.normpath(os.path.join(dir_, filetitle + '.7z.001'))
    # test.part1.rar/test.part2.rar/test.part3.rar
    elif re.match(PATTERN_RAR, filename, flags=re.I):
        filetitle = re.match(PATTERN_RAR, filename, flags=re.I).group(1)
        number_length = len(re.match(PATTERN_RAR, filename, flags=re.I).group(2))  # 解决part1.rar和part01.rar的情况
        first_volume_path = os.path.normpath(os.path.join(dir_, filetitle + f'.part{"1".zfill(number_length)}.rar'))
    # test.part1/test.part2/test.part3
    elif re.match(PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I):
        filetitle = re.match(PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I).group(1)
        number_length = len(re.match(PATTERN_RAR_WITHOUT_SUFFIX, filename, flags=re.I).group(2))
        first_volume_path = os.path.normpath(os.path.join(dir_, filetitle + f'.part{"1".zfill(number_length)}'))
    # test.zip
    elif re.match(PATTERN_ZIP, filename, flags=re.I):
        first_volume_path = file
    # test.zip/test.z01/test.z02
    elif re.match(PATTERN_ZIP_VOLUME, filename, flags=re.I):
        filetitle = re.match(PATTERN_ZIP_VOLUME, filename, flags=re.I).group(1)
        first_volume_path = os.path.normpath(os.path.join(dir_, filetitle + '.zip'))
    # test.zip.001/test.zip.002/test.zip.003
    elif re.match(PATTERN_ZIP_TYPE2, filename, flags=re.I):
        filetitle = re.match(PATTERN_ZIP_TYPE2, filename, flags=re.I).group(1)
        first_volume_path = os.path.normpath(os.path.join(dir_, filetitle + '.zip.001'))
    else:
        return False

    if return_filetitle:
        return filetitle
    else:
        return os.path.normpath(first_volume_path)
