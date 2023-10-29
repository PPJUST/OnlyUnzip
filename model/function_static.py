import inspect
import os
import random
import re
import shutil
import string
import time
from typing import Union

import filetype






def print_function_info(mode: str = 'current'):
    """打印当前/上一个执行的函数信息
    传参：mode 'current'或'last'"""
    import time
    import inspect

    if mode == 'current':
        print(time.strftime('%H:%M:%S ', time.localtime()),
              inspect.getframeinfo(inspect.currentframe().f_back).function)
    elif mode == 'last':
        print(time.strftime('%H:%M:%S ', time.localtime()),
              inspect.getframeinfo(inspect.currentframe().f_back.f_back).function)


def get_folder_size(folder: str) -> int:
    """获取指定文件夹的总大小/byte
    传参：folder 文件夹路径str
    返回值：total_size 总大小int"""
    print_function_info()
    import os

    folder_size = 0
    for dirpath, dirnames, filenames in os.walk(folder):
        for item in filenames:
            filepath = os.path.join(dirpath, item)
            folder_size += os.path.getsize(filepath)
    return folder_size


def get_files_list(dirpath: str) -> list:
    """获取指定文件夹中的所有文件路径list
    传参： dirpath 文件夹路径str
    返回值 filelist 所有文件路径list"""
    print_function_info()
    import os

    filelist = []
    for dirpath, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            file_path = os.path.normpath(os.path.join(dirpath, filename))
            filelist.append(file_path)
    return filelist


def check_filetype(filepath: str) -> bool:
    """检查文件是否存在以及其是否为压缩包，返回bool值"""
    print_function_info()
    if not os.path.exists(filepath):
        print(f'错误：{filepath} 不存在')
    elif os.path.isdir(filepath):
        print(f'错误：{filepath} 为文件夹')
    else:
        # 通过后缀判断
        suffix_type = ['.zip', '.tar', '.rar', '.gz', '.7z', '.xz', '.iso']
        file_suffix = os.path.splitext(filepath)[1]  # 提取文件后缀名
        if file_suffix.lower() in suffix_type:
            return True

        # 通过filetype库判断
        archive_type = ['zip', 'tar', 'rar', 'gz', '7z', 'xz']  # filetype库支持的压缩文件后缀名（部分）
        kind = filetype.guess(filepath)
        if kind is None:
            type_kind = None
        else:
            type_kind = kind.extension
        print(f'文件【{filepath}】的文件类型为【{type_kind}】')
        if type_kind in archive_type:
            return True

    return False  # 兜底


def delete_empty_folder(folder: str):
    """检查文件夹是否为空，是则删除（不经过回收站）"""
    print_function_info()
    if get_folder_size(folder) == 0:
        try:
            os.rmdir(folder)
        except OSError:
            all_dirpath = []
            all_filepath = []
            for dirpath, dirnames, filenames in os.walk(folder):
                all_dirpath.append(dirpath)  # 提取所有文件夹路径
                for filename in filenames:
                    filepath = os.path.normpath(os.path.join(dirpath, filename))
                    all_filepath.append(filepath)
            for i in all_filepath:  # 先删除所有空文件，防止后续删除文件夹时报错
                os.remove(i)
            for i in all_dirpath[::-1]:  # 从后往前逐级删除文件夹
                os.rmdir(i)
    else:
        print(f'{folder} 不为空')


def get_nodup_filename(path: str, target_dirpath: str) -> str:
    """生成传入的文件或文件夹在指定文件夹中没有重复的文件名（添加自定义后缀）
    传参：path 文件或文件夹路径str
    target_dirpath 指定文件夹路径str
    返回值：new_filename 无重复的文件名（非完整路径，仅文件名）
    """
    print_function_info()
    import os

    if os.path.isfile(path):
        filetitle = os.path.split(os.path.splitext(path)[0])[1]
        suffix = os.path.splitext(path)[1]
    else:
        filename = os.path.split(path)[1]
        filetitle = filename
        suffix = ''

    add_suffix = ' -New'  # 添加的后缀格式
    # 剔除原文件名中已包含的后缀 -New
    check = filetitle.rfind(add_suffix)
    if check != -1 and filetitle[check + len(add_suffix):].isdigit():
        new_filetitle = filetitle[0:check]
    else:
        new_filetitle = filetitle
    new_filename = new_filetitle + suffix
    temp_filename = new_filetitle + add_suffix + '1' + suffix
    # 生成无重复的文件名
    count = 0
    # 一直累加循环直到不存在同名（同级目录也要检查，防止改名报错）
    while os.path.exists(os.path.join(target_dirpath, new_filename)) or os.path.exists(
            os.path.join(os.path.split(path)[0], temp_filename)):
        count += 1
        new_filename = f'{filetitle}{add_suffix}{count}{suffix}'
        temp_filename = new_filename
    return new_filename


def get_filetitle(filepath: str) -> str:
    """提取传入文件的不含后缀的文件名"""
    print_function_info()
    if os.path.isdir(filepath):
        filetitle = os.path.splitext(filepath)[1]
    else:
        filetitle = os.path.split(os.path.splitext(filepath)[0])[1]  # 兜底

        re_rar = r"^(.+)\.part(\d+)\.rar$"
        re_rar_without_suffix = r"^(.+)\.part(\d+)$"
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip = r"^(.+)\.zip$"
        re_zip_volume = r"^(.+)\.z\d+$"
        re_zip_type2 = r"^(.+)\.zip\.\d+$"
        re_rules = [re_rar, re_rar_without_suffix, re_7z, re_zip, re_zip_volume, re_zip_type2]
        filename = os.path.split(filepath)[1]
        for rule in re_rules:
            try:
                filetitle = re.match(rule, filename).group(1)
                break
            except:
                continue

    return filetitle

def get_deepest_dirpath(dirpath: str) -> str:
    """检查传入文件夹路径的深度，找出最后一级含多文件/文件夹的文件夹
    传参：dirpath 文件夹路径str
    返回值：deepest_path 最深的文件夹路径str"""
    print_function_info()
    import os

    if len(os.listdir(dirpath)) == 1:
        the_path = os.path.normpath(os.path.join(dirpath, os.listdir(dirpath)[0]))
        if os.path.isfile(the_path):  # 如果文件夹下只有一个文件，并且是文件
            deepest_path = the_path
            return deepest_path
        else:  # 临时文件夹下只有一个文件，但是是文件夹，则递归
            return get_deepest_dirpath(the_path)
    else:
        deepest_path = dirpath
        return deepest_path


def un_nest_folders(origin_folder: str, target_folder: str = None, mode_nested: bool = True) -> str:
    """解除文件夹的嵌套
    将指定文件夹中的最深一级非空文件夹移动到目标文件夹中，并返回最终路径str

    传参：origin_folder 原始文件夹路径str
    可选传参：
    target_folder 移动到目标文件夹，默认移动到原始文件夹的父目录中（即同级）
    mode_nested 是否处理嵌套文件夹，默认处理；可选False，不处理套娃文件夹，仅做1次下级移动操作
    返回值：final_path 最终的路径str
    """
    print_function_info()
    import os
    import shutil
    import time
    import random
    import string

    # 如果目标文件夹不存在，则新建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 根据选项提取需要移动的文件/文件夹路径
    if mode_nested:  # 提取最深一级
        need_move_path = get_deepest_dirpath(origin_folder)
    else:  # 仅下级
        number_in_folder = len(os.listdir(origin_folder))
        if number_in_folder == 1:
            need_move_path = os.path.normpath(os.path.join(origin_folder, os.listdir(origin_folder)[0]))
        else:
            need_move_path = origin_folder

    # 检查需移动的路径和目标文件夹是否一致，如果一致，则不进行后续操作
    if need_move_path == target_folder:
        return need_move_path

    # 提取文件名，生成目标文件夹下无重复的文件/文件夹名
    if target_folder:
        final_folder = target_folder
    else:
        final_folder = os.path.split(origin_folder)[0]
    new_filename = get_nodup_filename(need_move_path, final_folder)

    # 先改名，再移动
    old_path_with_newname = os.path.normpath(os.path.join(os.path.split(need_move_path)[0], new_filename))
    try:
        try:
            os.rename(need_move_path, old_path_with_newname)
        except PermissionError:  # 如果报错【PermissionError: [WinError 5] 拒绝访问。】，可能是找无重名占用了，等0.5秒让系统处理完
            time.sleep(0.5)
            os.rename(need_move_path, old_path_with_newname)
    except PermissionError:  # 如果上述方法还不能解决占用问题，则直接移动到随机生成的文件夹中
        old_path_with_newname = need_move_path
        random_ascii = ''.join(random.choices(string.ascii_lowercase, k=6))  # 随机6位小写字母
        final_folder = os.path.normpath(
            os.path.join(final_folder, os.path.split(need_move_path)[1] + f'_{random_ascii}'))

    try:
        shutil.move(old_path_with_newname, final_folder)
    except OSError:  # 如果报错【OSError: [WinError 145] 目录不是空的。】，原路径下有残留的空文件夹，则尝试直接删除
        delete_empty_folder(need_move_path)

    # 组合最终路径
    final_path = os.path.normpath(os.path.join(final_folder, new_filename))
    delete_empty_folder(origin_folder)  # 如果原文件夹为空，则删除

    return final_path


def check_temp_folder(check_path: Union[list, str]) -> bool:
    """传入路径列表list，检查对应路径的同级/下级文件夹中是否存在临时文件夹（前一次解压未正常删除的）
    如果存在临时文件夹并且其中有相应文件/文件夹，则返回False，并终止下一步操作"""
    print_function_info()
    if type(check_path) is str:
        check_path = [check_path]

    all_temp_folder = set()  # 所有可能存在的临时文件夹路径（添加后缀自动生成，非真实路径）

    for path in check_path:
        if os.path.isfile(path):
            temp_folder = os.path.normpath(os.path.join(os.path.split(path)[0], 'UnzipTempFolder'))
            all_temp_folder.add(temp_folder)
        else:
            temp_folder = os.path.normpath(os.path.join(path, 'UnzipTempFolder'))
            all_temp_folder.add(temp_folder)
    for folder in all_temp_folder:
        if os.path.exists(folder) and os.listdir(folder):
            return False
    return True

def check_filetitle(filetitle:str)->str:
    """检查文件名首尾是否有空格和."""
    print_function_info()
    while filetitle[0] in [' ', '.'] or filetitle[-1] in [' ', '.']:
        filetitle = filetitle.strip()
        filetitle = filetitle.strip('.')

    return filetitle

def get_first_volume_archive_filetitle(filename: str) -> Union[str, bool]:
    """通过传入的文件名，判断其是否符合分卷压缩包规则并生成第一个分卷包名，返回提取的不含后缀文件名str或bool值"""
    print_function_info()
    re_rar = r"^(.+)\.part(\d+)\.rar$"
    re_rar_without_suffix = r"^(.+)\.part(\d+)$"
    re_7z = r"^(.+)\.7z\.\d+$"
    re_zip = r"^(.+)\.zip$"
    re_zip_volume = r"^(.+)\.z\d+$"
    re_zip_type2 = r"^(.+)\.zip\.\d+$"

    # 匹配7z正则
    if re.match(re_7z, filename):
        archive_filetitle = re.match(re_7z, filename).group(1)  # 提取文件名
        first_volume_archive_filetitle = archive_filetitle + r'.7z.001'  # 生成第一个分卷压缩包名
    # 匹配rar正则
    elif re.match(re_rar, filename):
        archive_filetitle = re.match(re_rar, filename).group(1)
        number_type = len(re.match(re_rar, filename).group(2))
        first_volume_archive_filetitle = archive_filetitle + rf'.part{str(1).zfill(number_type)}.rar'
    # 匹配无后缀的rar正则
    elif re.match(re_rar_without_suffix, filename):
        archive_filetitle = re.match(re_rar_without_suffix, filename).group(1)
        number_type = len(re.match(re_rar_without_suffix, filename).group(2))
        first_volume_archive_filetitle = archive_filetitle + rf'.part{str(1).zfill(number_type)}'
    # 匹配zip正则
    elif re.match(re_zip_volume, filename) or re.match(re_zip, filename):  # 一般的zip分卷包的第一个包都是.zip后缀，所以都是为分卷即可
        if re.match(re_zip_volume, filename):
            archive_filetitle = re.match(re_zip_volume, filename).group(1)
        else:
            archive_filetitle = re.match(re_zip, filename).group(1)
        first_volume_archive_filetitle = archive_filetitle + r'.zip'
    # 匹配zip格式2正则
    elif re.match(re_zip_type2, filename):
        archive_filetitle = re.match(re_zip_type2, filename).group(1)  # 提取文件名
        first_volume_archive_filetitle = archive_filetitle + r'.zip.001'
    else:
        return False

    return first_volume_archive_filetitle


def get_volume_archive_dict(filelist: list) -> dict:
    """传入文件路径列表list，提取其中符合分卷压缩包命名规则的文件，并扩展到其所在文件夹，补全完整的分卷压缩包分卷
    返回分卷压缩包dict {A压缩包第一个分卷包路径:(A压缩包全部分卷路径), ...}"""
    print_function_info()
    volume_archive_dict = {}  # 最终结果

    folder_dict = {}  # 按文件所在的父文件夹建立字典 {文件父文件夹:(A文件, B文件), ...}
    for file in filelist:
        parent_folder = os.path.split(file)[0]
        if parent_folder not in folder_dict:
            folder_dict[parent_folder] = set()
        folder_dict[parent_folder].add(file)
    # 按文件夹逐个处理其中的文件
    for parent_folder in folder_dict:
        files_set = folder_dict[parent_folder]
        filenames_in_parent_folder = os.listdir(parent_folder)
        # 利用正则匹配分卷压缩包
        all_filenames = [os.path.split(i)[1] for i in files_set]  # 提取出文件名
        for filename in all_filenames:
            full_filepath = os.path.normpath(os.path.join(parent_folder, filename))  # 还原当前处理文件的完整文件路径
            first_volume_archive_filetitle = get_first_volume_archive_filetitle(filename)
            if first_volume_archive_filetitle:
                first_volume_archive = os.path.normpath(os.path.join(parent_folder, first_volume_archive_filetitle))
            else:
                break

            # 处理识别出来的第一个分卷包
            if first_volume_archive not in volume_archive_dict:  # 如果文件名不在字典内，则添加一个空键值对
                volume_archive_dict[first_volume_archive] = set()
            volume_archive_dict[first_volume_archive].add(full_filepath)  # 添加键值对 {示例.7z.001:(示例.7z.001,示例.7z.002)}
            volume_archive_dict[first_volume_archive].add(first_volume_archive)
        # 扩展压缩包识别范围，补全完整的分卷压缩包分卷
        for check_filename in filenames_in_parent_folder:
            full_path = os.path.normpath(os.path.join(parent_folder, check_filename))
            check_title = get_first_volume_archive_filetitle(check_filename)
            if check_title:
                check_path = os.path.normpath(os.path.join(parent_folder, check_title))
                if check_path in volume_archive_dict:
                    volume_archive_dict[check_path].add(full_path)

    return volume_archive_dict