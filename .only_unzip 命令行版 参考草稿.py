import os
import configparser
import re
import subprocess
import time
import natsort
import winshell
import shutil
import magic
import sys
from tqdm import tqdm

global total_number, rate_file_number, error_number, damage_number
global password_config, sort_passwords, resort_passwords
global fenjuan_dict
global exclude_files, loop_code






def unzip_main_logic(full_path):
    """解压的程序逻辑"""
    select_files, select_dirs = unzip_walk_path(full_path)  # 先提取全部文件列表
    fenjuan_files_dict, normal_files = unzip_class_zip(select_files)  # 区分分卷压缩包
    fenjuan_files = fenjuan_files_dict.keys()  # 提取分卷压缩包的第一个分卷包为列表
    unzip_set_first(fenjuan_files, normal_files)
    if len(normal_files) != 0:
        unzip_run_7zip(normal_files, "normal")
    if len(fenjuan_files) != 0:
        unzip_run_7zip(fenjuan_files, "fenjuan")
    if loop_code:
        return unzip_main_logic(full_path)
    else:
        main_menu()


def unzip_walk_path(full_path):
    """提取文件，返回完整文件路径列表"""
    walk_path_filenames = os.listdir(full_path)
    walk_path_full = []  # 存放遍历文件的完整路径
    for i in walk_path_filenames:
        walk_path_full.append(os.path.join(full_path, i))
    select_files = [i for i in walk_path_full if os.path.isfile(i)]  # 存放提取的文件
    select_dirs = [i for i in walk_path_full if os.path.isdir(i)]  # 存放提取的文件夹
    select_files_only_zip = [x for x in select_files if is_zip_file(x) and x not in exclude_files]  # 提取是压缩包的文件列表，并排除exclude_files内的文件
    # select_files_only_zip = [x for x in select_files if x not in exclude_files]  # 排除exclude_files内的文件
    if len(select_files_only_zip) == 0:
        print("——————没有能够解压的文件——————")
        main_menu()
    else:
        return select_files_only_zip, select_dirs




def unzip_class_zip(files):
    """区分卷压缩包与一般压缩包"""
    global fenjuan_dict
    normal_files = [x for x in files]  # 复制
    re_rar = r"^(.+)\.part\d+\.rar$"  # 4种类压缩文件的命名规则
    re_7z = r"^(.+)\.7z\.\d+$"
    re_zip_top = r"^(.+)\.zip$"
    re_zip_other = r"^(.+)\.z\d+$"
    fenjuan_dict = {}  # 分卷文件字典（键值对为 第一个分卷：全部分卷）
    for i in files:
        if re.match(re_7z, i):  # 匹配7z正则
            prefix = re.match(re_7z, i).group(1) + r'.7z.001'  # 设置字典的键（提取的正则前缀+手工添加后缀）
            if prefix not in fenjuan_dict:  # 如果文件名不在字典内，则添加一个空键值对
                fenjuan_dict[prefix] = set()  # 用集合添加（目的是为了后面的zip分卷，其实用列表更方便）
            fenjuan_dict[prefix].add(i)  # 添加键值对（示例.7z.001：示例.7z.001，示例.7z.002）
            normal_files.remove(i)  # 将新列表中的分卷压缩包剔除
        elif re.match(re_zip_other, i) or re.match(re_zip_top, i):  # 只要是zip后缀的，都视为分卷压缩包，因为解压的都是第一个
            if re.match(re_zip_other, i):
                prefix = re.match(re_zip_other, i).group(1) + r'.zip'
            else:
                prefix = re.match(re_zip_top, i).group(1) + r'.zip'
            if prefix not in fenjuan_dict:
                fenjuan_dict[prefix] = set()
            fenjuan_dict[prefix].add(i)
            fenjuan_dict[prefix].add(prefix)  # zip分卷的特性，第一个分卷包名称是.zip后缀
            normal_files.remove(i)
            if prefix in normal_files:  # zip分卷特性，如果是分卷删除第一个.zip后缀的文件名，所以需要删除多出来的一个zip文件
                normal_files.remove(prefix)
            else:
                pass
        elif re.match(re_rar, i):
            prefix = re.match(re_rar, i).group(1) + r'.part1.rar'
            if prefix not in fenjuan_dict:
                fenjuan_dict[prefix] = set()
            fenjuan_dict[prefix].add(i)
            normal_files.remove(i)

    return fenjuan_dict, normal_files  # fenjuan_full_dict：分卷文件，new_files：不包含分卷的文件


def pick_filename(file, ftype):
    """提取文件名"""
    if ftype == "normal":
        filename = os.path.split(os.path.splitext(file)[0])[1]  # 单独的没有后缀的文件名
    else:
        re_rar = r"^(.+)\.part\d+\.rar$"  # 4种类压缩文件的命名规则
        re_7z = r"^(.+)\.7z\.\d+$"
        re_zip_top = r"^(.+)\.zip$"

        if re.match(re_7z, file):
            full_filename = re.match(re_7z, file).group(1)
        elif re.match(re_zip_top, file):
            full_filename = re.match(re_zip_top, file).group(1)
        elif re.match(re_rar, file):
            full_filename = re.match(re_rar, file).group(1)
        filename = os.path.split(full_filename)[1]
    return filename.strip()





def delete_original(file, ftype):
    """删除原文件"""
    if ftype == "normal":
        winshell.delete_file(file, no_confirm=True)  # 删除原文件到回收站
    else:
        for i in fenjuan_dict[file]:
            winshell.delete_file(i, no_confirm=True)  # 删除原文件到回收站


def unzip_set_first(fenjuan_files, normal_files):
    """调用7zip解压-初始设置部分"""
    global total_number, rate_file_number, error_number, damage_number
    total_number = len(fenjuan_files) + len(normal_files)  # 总文件数
    rate_file_number = 0  # 到第几个文件了
    error_number = 0  # 解压失败的文件数
    damage_number = 0  # 损坏的压缩文件数


def unzip_run_7zip(files_list, ftype):
    """调用7zip解压-开始解压"""
    global rate_file_number, error_number, damage_number, exclude_files
    zip_path = './7-Zip/7z.exe'  # 7zip路径
    rate_file_number = 0
    for file in tqdm(files_list, bar_format='文件进度：{l_bar}{bar}| {n_fmt}/{total_fmt}'):
        rate_file_number += 1
        file_directory = os.path.split(file)[0]  # 文件的父目录
        file_name_without_suffix = pick_filename(file, ftype)  # 单独的没有后缀的文件名
        temporary_folder = os.path.join(file_directory, "UnzipTempFolder")  # 临时存放解压结果的文件夹
        unzip_path = os.path.join(temporary_folder, file_name_without_suffix)  # 解压到临时文件下与文件同名的文件夹中
        password_try_number = 0  # 密码尝试次数
        for password in tqdm(resort_passwords, bar_format='解压密码测试：{l_bar}{bar}| {n_fmt}/{total_fmt}', file=sys.stdout):
            zip_command = [zip_path, "x", "-p" + password, "-y", file, "-o" + unzip_path]  # 组合完整7z指令
            unzip_result = subprocess.run(zip_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            if unzip_result.returncode != 0:
                password_try_number += 1  # 返回码不为0则解压失败，密码失败次数+1
            elif unzip_result.returncode == 0:
                tqdm.write(f"——————成功解压{os.path.split(file)[1]}，解压密码：{password}——————")
                with open('unzip_history.txt', 'a', encoding='utf-8') as history_save:
                    the_history = f'解压日期：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}  解压文件：{os.path.split(file)[1]} 解压密码：{password}\n'
                    history_save.write(the_history)
                original_size = get_original_size(file, ftype)  # 原文件大小
                unzip_size = get_result_size(unzip_path)  # 压缩结果大小
                if unzip_size < original_size * 0.95:  # 解压后文件大小如果小于原文件95%，则说明压缩包损坏
                    winshell.delete_file(unzip_path, no_confirm=True)  # 删除解压结果
                    damage_number += 1  # 计数+1
                    if ftype == 'normal':
                        exclude_files.append(file)
                    else:
                        exclude_files += fenjuan_dict[file]
                    tqdm.write(f"——————{os.path.split(file)[1]} 已删除解压结果，解压文件大小<解压前文件的95%）——————")
                    break  # 退出当前文件循环
                else:
                    right_password_number_add_one(password)  # 成功解压则密码使用次数+1
                    delete_original(file, ftype)  # 删除原文件
                    check_unzip_result(temporary_folder)  # 检查解压结果，处理套娃文件夹
                    if os.path.exists(unzip_path):
                        if get_result_size(unzip_path) == 0:
                            winshell.delete_file(unzip_path, no_confirm=True)
                    break  # 检查完结果后退出循环
        if password_try_number == len(resort_passwords):
            error_number += 1
            if ftype == 'normal':
                exclude_files.append(file)
            else:
                exclude_files += fenjuan_dict[file]
    print(f"★完成全部解压操作，成功：{total_number - error_number}个，失败：{error_number}个，损坏：{damage_number}个")
    if os.path.exists(temporary_folder):
        if get_result_size(temporary_folder) == 0:
            winshell.delete_file(temporary_folder, no_confirm=True)
        else:
            print("——————注意：临时文件夹不为空，请检查——————")
    else:
        pass





def right_password_number_add_one(password):
    """正确的密码次数加1"""
    add_pass = configparser.ConfigParser()  # 注意大小写
    add_pass.read("password.ini", encoding='utf-8')  # 配置文件的路径
    old_number = int(add_pass.get(password, 'number'))
    add_pass.set(password, 'number', str(old_number + 1))  # 次数加1
    add_pass.write(open('password.ini', 'w', encoding='utf-8'))
    read_password()


def get_folder_depth(path):
    """检查文件深度，找出最后一级多文件的文件夹"""
    if len(os.listdir(path)) == 1:
        if os.path.isfile(os.path.join(path, os.listdir(path)[0])):  # 临时文件夹下只有一个文件，并且是文件
            last_path = os.path.join(path, os.listdir(path)[0])
            return last_path
        else:
            return get_folder_depth(os.path.join(path, os.listdir(path)[0]))  # 临时文件夹下只有一个文件，但是文件夹，则递归
    else:
        last_path = path
        return last_path


def rename_recursion(filepath, unzip_folder):
    """递归改名，确保无同名文件"""
    parent_directory = os.path.split(unzip_folder)[0]
    filename_without_suffix = os.path.split(os.path.splitext(filepath)[0])[1]
    suffix = os.path.splitext(filepath)[1]
    count = 1
    while True:
        new_filename = f"{filename_without_suffix} - new{count}{suffix}"
        if new_filename not in os.listdir(parent_directory):
            return new_filename
        else:
            count += 1


def check_unzip_result(result_folder):
    """
    检查解压结果
    主要思路：
    1. 如果解压后文件夹内有多个文件，则移动该文件夹到父目录，结束操作
    2. 如果解压后文件夹内只有一个文件/文件夹，则移动该文件/文件夹到解压文件夹，再次检查
    3. 注意同名文件/文件夹
    """
    need_move_path = get_folder_depth(result_folder)  # 需要移动的文件夹/文件路径
    need_move_filename = os.path.split(need_move_path)[1]  # 需要移动的文件夹/文件名称
    parent_directory = os.path.split(result_folder)[0]  # 临时文件夹的上级目录（原压缩包所在的目录）
    if need_move_filename not in os.listdir(parent_directory):
        shutil.move(need_move_path, parent_directory)
    else:
        rename_filename = rename_recursion(need_move_path, result_folder)
        rename_full_path = os.path.join(os.path.split(need_move_path)[0], rename_filename)
        os.rename(need_move_path, rename_full_path)
        shutil.move(rename_full_path, parent_directory)



