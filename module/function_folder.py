import os
import shutil

from module.function_static import create_nodup_filename


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

def handling_nested_folder(dirpath:str, is_retain_itself=False):
    """处理嵌套文件夹，将其内容移动到顶层文件夹
    :param dirpath: str类型，文件夹路径
    :param is_retain_itself: bool类型，是否保留传入的文件夹（即解套至该文件夹之下而非之上）
    """
    # 找到首个多重文件夹
    first_multi_folder = get_first_multi_folder(dirpath)
    # 如果传入的文件夹就是首个多重文件夹，则直接返回
    if first_multi_folder == os.path.normpath(dirpath):
        return first_multi_folder
    # 移动该文件夹
    parent_folder, original_dirname = os.path.split(first_multi_folder)
    if is_retain_itself:  # 移动至顶层文件夹之下
        nodup_dirname = create_nodup_filename(first_multi_folder,dirpath)
        new_path_renamed =  os.path.join(parent_folder,nodup_dirname)
        os.rename(first_multi_folder,new_path_renamed)
        shutil.move(new_path_renamed, dirpath)
        new_path_final = os.path.normpath(os.path.join(dirpath,nodup_dirname))
        # 删除原文件夹
        for i in os.listdir(dirpath):
            fullpath = os.path.normpath(os.path.join(dirpath, i))
            if fullpath != new_path_final:
                os.remove(fullpath)
    else:# 移动至顶层文件夹之上
        top_folder = os.path.split(dirpath)[0]
        nodup_dirname = create_nodup_filename(first_multi_folder, top_folder)
        new_path_renamed = os.path.join(parent_folder, nodup_dirname)
        os.rename(first_multi_folder, new_path_renamed)
        shutil.move(new_path_renamed, top_folder)
        new_path_final = os.path.normpath(os.path.join(top_folder, nodup_dirname))
        # 删除原文件夹
        os.remove(dirpath)

    return new_path_final




