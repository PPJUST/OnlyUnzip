import os


def get_folder_size(folder: str) -> int:
    """
    获取指定文件夹的总大小/byte
    :param folder: str类型，文件夹路径
    :return: int类型，总字节大小
    """
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
    filelist = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.normpath(os.path.join(dirpath, filename))
            filelist.append(file_path)

    return filelist
