import os


def get_first_multi_folder(dirpath: str) -> str:
    """
    检查传入文件夹路径的层级，找出首个含多文件/文件夹的文件夹路径
    :param dirpath: str类型，文件夹路径
    :return: str类型，文件夹路径
    """
    if len(os.listdir(dirpath)) == 1:  # 如果文件夹下只有一个文件/文件夹
        check_path = os.path.normpath(os.path.join(dirpath, os.listdir(dirpath)[0]))
        # 如果是文件，则直接返回
        if os.path.isfile(check_path):
            return check_path
        # 如果是文件夹，则递归
        else:
            return get_first_multi_folder(check_path)
    else:
        return dirpath
