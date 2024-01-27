import os

import filetype


def is_archive(filepath:str, use_filetype:bool=True)->bool:
    """
    判断文件是否为压缩文件
    :param filepath: str类型，文件路径
    :param use_filetype: bool类型，是否使用filetype库进行额外判断
    :return: bool类型，是否为压缩包
    """
    if not os.path.exists(filepath):
        return False
    elif os.path.isdir(filepath):
        return False
    else:
        # 先通过文件后缀判断
        file_suffix = os.path.splitext(filepath)[1][1:].lower()  # 提取文件后缀名（不带.）
        archive_suffix = ['zip', 'rar', '7z', 'tar', 'gz', 'xz', 'iso']
        if file_suffix in archive_suffix:
            return True

        # 再通过filetype判断
        if use_filetype:
            archive_type = ['zip', 'tar', 'rar', 'gz', '7z', 'xz']  # filetype库支持的压缩文件后缀名
            kind = filetype.guess(filepath)
            if kind is None:
                return False
            else:
                type_kind = kind.extension
                if type_kind in archive_type:
                    return True

        return False


def is_zip_archive(filepath: str) -> bool:
    """单独判断文件是否为zip格式压缩文件"""
    archive_type = ['zip']
    kind = filetype.guess(filepath)
    if kind is None:
        return False
    else:
        type_kind = kind.extension
        if type_kind in archive_type:
            return True

    return False
