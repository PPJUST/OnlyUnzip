# 一般方法

import inspect
import os
import shutil
import time
from typing import Union

import send2trash

from constant import _BACKUP_FOLDER, _TEMP_FOLDER, _PASSWORD_FILE, _HISTORY_FILE, _HISTORY_FILE_MAX_SIZE, \
    _TIME_STAMP
from module import function_password, function_config, function_archive


def print_function_info(mode: str = 'current'):
    """
    打印当前/上一个执行的函数信息
    :param mode: str类型，'current' 或 'last'
    """
    # pass

    if mode == 'current':
        print(time.strftime('%H:%M:%S ', time.localtime()),
              inspect.getframeinfo(inspect.currentframe().f_back).function)
    elif mode == 'last':
        print(time.strftime('%H:%M:%S ', time.localtime()),
              inspect.getframeinfo(inspect.currentframe().f_back.f_back).function)


def check_default_files():
    """检查默认文件夹/文件是否存在"""
    # 检查备份文件夹
    if not os.path.exists(_BACKUP_FOLDER):
        os.mkdir(_BACKUP_FOLDER)
    # 检查密码数据库
    if not os.path.exists(_PASSWORD_FILE):
        function_password.create_default_password_file()
    # 检查配置文件
    function_config.create_default_config()


def save_history(text: str):
    """保存文本到历史记录文件中"""
    # 检查历史记录文件大小是否超限
    if os.path.exists(_HISTORY_FILE) and os.path.getsize(_HISTORY_FILE) > _HISTORY_FILE_MAX_SIZE:
        _backup_history()
    # 写入记录
    with open(_HISTORY_FILE, 'a', encoding='utf-8') as f:
        f.write(text + '\n')


def _backup_history():
    """备份历史记录"""
    time_text = time.strftime(_TIME_STAMP, time.localtime())
    original_filetitle = os.path.basename(os.path.splitext(_HISTORY_FILE)[0])
    suffix = os.path.splitext(_HISTORY_FILE)[1]
    new_filepath = os.path.normpath(os.path.join(_BACKUP_FOLDER, original_filetitle + time_text + suffix))
    shutil.move(_HISTORY_FILE, new_filepath)


def is_temp_folder_exists(check_path: Union[list, str]) -> bool:
    """检查传入路径的同级文件夹中是否存在临时文件夹（上一次解压未正常删除的）"""
    print_function_info()
    # 统一格式
    if type(check_path) is str:
        check_path = [check_path]

    # 获取所有可能存在的临时文件夹虚拟路径（添加后缀生成，非真实路径）
    temp_folders = set()
    for path in check_path:
        if os.path.isfile(path):
            join_path = os.path.join(os.path.dirname(path), _TEMP_FOLDER)
            temp_folders.add(join_path)
        else:
            join_path = os.path.join(path, _TEMP_FOLDER)
            temp_folders.add(join_path)

    # 逐个检查虚拟路径
    for path in temp_folders:
        if os.path.exists(path) and os.listdir(path):  # 路径存在且
            return True

    return False


def get_folder_size(folder: str) -> int:
    """
    获取指定文件夹的总大小/byte
    :param folder: str类型，文件夹路径
    :return: int类型，总字节大小
    """
    print_function_info()
    folder_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for item in filenames:
            filepath = os.path.join(dirpath, item)
            folder_size += os.path.getsize(filepath)

    return folder_size


def get_files(folder: str) -> list:
    """
    获取指定文件夹中的所有文件路径
    :param folder: str类型，文件夹路径
    :return: list类型，所有文件路径的列表
    """
    print_function_info()
    files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            file_path = os.path.normpath(os.path.join(dirpath, filename))
            files.append(file_path)

    return files


def get_files_in_paths(paths: list):
    """提取输入路径列表中所有文件路径"""
    files = set()
    for path in paths:
        if os.path.exists(path):
            if os.path.isfile(path):
                files.add(path)
            else:
                walk_files = get_files(path)
                files.update(walk_files)
    # 统一路径格式
    files = [os.path.normpath(i) for i in files]
    return files


def get_first_multi_path(dirpath: str) -> str:
    """检查传入文件夹路径的层级，找出首个含多文件的文件夹路径或单文件路径
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
            return get_first_multi_path(check_path)
    else:
        return dirpath


def create_nodup_filename(path: str, target_dirpath: str, dup_suffix: str = ' -New',
                          target_filetitle: str = None) -> str:
    """生成指定路径对应的文件在目标文件夹中无重复的文件名（可指定目标文件名）
    :param path: str，文件路径或文件夹路径
    :param target_dirpath: str，目标文件夹路径
    :param dup_suffix: 若存在重复文件名则添加的后缀
    :param target_filetitle: str，目标文件名（不含后缀）
    :return: str，无重复的文件名（非完整路径，仅含后缀的文件名）
    """
    # 提取原始文件名
    dirpath = os.path.dirname(path)
    if os.path.isfile(path):
        filetitle = os.path.basename(os.path.splitext(path)[0])
        suffix = os.path.splitext(path)[1]
    else:
        filetitle = os.path.basename(path)
        suffix = ''

    # 剔除原始文件名中的自定义后缀
    index_suffix = filetitle.rfind(dup_suffix)
    if index_suffix != -1 and filetitle[index_suffix + len(dup_suffix):].isdigit():
        filetitle = filetitle[0:index_suffix]

    # 生成目标文件名
    if target_filetitle:
        new_filename = target_filetitle + suffix
        temp_filename = target_filetitle + dup_suffix + '1' + suffix
    else:
        target_filetitle = filetitle
        new_filename = filetitle + suffix
        temp_filename = filetitle + dup_suffix + '1' + suffix
    # 生成无重复的目标文件名
    # 一直循环累加直到不存在相同文件名（同级目录也要检查，防止重命名时报错）
    count = 0
    while os.path.exists(os.path.join(target_dirpath, new_filename)) or os.path.exists(
            os.path.join(dirpath, temp_filename)):
        count += 1
        new_filename = f'{target_filetitle}{dup_suffix}{count}{suffix}'
        temp_filename = new_filename

    return new_filename


def delete_empty_folder(folder: str) -> bool:
    """检查文件夹是否为空，是则删除"""
    print_function_info()
    if os.path.exists(folder) and os.path.isdir(folder) and get_folder_size(folder) == 0:
        shutil.rmtree(folder)
        return True
    else:
        return False


def delete_files(files):
    """删除文件至回收站"""
    print_function_info()
    for file in files:
        file = os.path.normpath(file)
        try:
            send2trash.send2trash(file)
        except OSError:
            # 尝试重新删除
            try:
                for _ in range(10):
                    time.sleep(0.5)
                    if os.path.exists(file):
                        send2trash.send2trash(file)
                    else:
                        break
            except OSError:
                # 放弃删除
                pass


def get_filetitle(path: str) -> str:
    """提取路径的文件标题（不含后缀）"""
    # 先按文件类型直接提取
    if os.path.isdir(path):
        filetitle = os.path.basename(path)
    else:
        filetitle = os.path.basename(os.path.splitext(path)[0])

    # 单独处理分卷压缩文件
    if function_archive.is_volume_archive(path):
        filetitle = function_archive.create_fake_first_volume_path(path, return_filetitle=True)

    # 处理文件标题两端多余的空格和.
    while filetitle[0] in [' ', '.'] or filetitle[-1] in [' ', '.']:
        filetitle = filetitle.strip()
        filetitle = filetitle.strip('.')

    return filetitle


def move_file(path, target_folder=None):
    """移动文件至指定目录"""
    # 提取文件名，生成指定目录下无重复的文件/文件夹名
    target_folder = target_folder if target_folder else os.path.dirname(path)
    if not os.path.exists(target_folder):
        os.mkdir(target_folder)
    filename_nodup = create_nodup_filename(path, target_folder)

    # 先改名
    new_path_nodup = os.path.normpath(os.path.join(os.path.dirname(path), filename_nodup))
    try:
        os.rename(path, new_path_nodup)
    except PermissionError:  # 报错【PermissionError: [WinError 5] 拒绝访问。】，等待0.2秒再次尝试
        time.sleep(0.2)
        os.rename(path, new_path_nodup)

    # 再移动
    try:
        shutil.move(new_path_nodup, target_folder)
    except OSError:  # 报错【OSError: [WinError 145] 目录不是空的。】，原路径下有残留的空文件夹，尝试直接删除
        delete_empty_folder(path)

    # 组合最终路径
    final_path = os.path.normpath(os.path.join(target_folder, filename_nodup))
    # 如果原始文件夹为空，则直接删除
    delete_empty_folder(path)

    return final_path
