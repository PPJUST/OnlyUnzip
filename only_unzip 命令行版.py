import os
import configparser
import natsort
import re
import subprocess
import winshell
import shutil


def input_path():
    """输入文件夹路径"""
    full_path = input("输入压缩包所在文件夹的完整路径：")
    if not os.path.exists(full_path):
        print("——————路径不存在，请重新输入——————")
        return input_path()
    elif os.path.isfile(full_path):
        print("——————该路径不是文件夹，请重新输入——————")
        return input_path()
    elif len(os.listdir(full_path)) == 0:
        print("——————文件夹为空，请重新输入——————")
        return input_path()
    else:
        unzip_main_logic(full_path)  # 解压主程序


def read_password():
    """读取密码"""
    global password_config, sort_passwords, resort_passwords
    password_config = configparser.ConfigParser()  # 注意大小写
    password_config.read("password.ini", encoding='utf-8')  # 配置文件的路径

    # 按密码的使用次数排序
    passwords = password_config.sections()  # 获取section
    sort_passwords = []  # 设置空列表，方便后续排序操作
    resort_passwords = []  # 最终排序结果
    for password in passwords:  # 遍历全部密码
        sort_passwords.append(password_config.get(password, 'number') + ' - ' + password)  # value - section ，使用次数 - 密码
    list_temp1 = reversed(natsort.natsorted(sort_passwords))  # 按数字大小降序排序
    list_temp2 = [x for x in list_temp1]
    sort_passwords = list_temp2
    for i in sort_passwords:
        resort_passwords.append(re.search(r' - (.+)', i).group(1))  # 正则提取 - 后的section


def add_password():
    """新增密码"""
    input_password = input("输入需要新增的密码，一个一行\n")
    new_password_temp = input_password.split('\n')
    new_password = [x for x in new_password_temp if x != '']
    for i in new_password:
        if i not in password_config.sections():
            password_config.add_section(i)
            password_config.set(i, 'number', '0')
    password_config.write(open('password.ini', 'w', encoding='utf-8'))
    read_password()  # 重新读取
    main()


def show_password():
    """显示密码"""
    for i in sort_passwords:
        re_findall = re.findall("(.+) - (.+)", i)[0]  # 反转 使用次数 - 密码，显示为 密码 - 使用次数
        print(f'{re_findall[1]} - 次数：{re_findall[0]}')
    main()


def export_password():
    """导出密码"""
    with open("password_export.txt", "w", encoding="utf-8") as pw:
        pw.write("\n".join(resort_passwords))
    main()


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


def unzip_walk_path(full_path):
    """提取文件，返回完整文件路径列表"""
    walk_path_filenames = os.listdir(full_path)
    walk_path_full = []  # 存放遍历文件的完整路径
    for i in walk_path_filenames:
        walk_path_full.append(os.path.join(full_path, i))
    select_files = [i for i in walk_path_full if os.path.isfile(i)]  # 存放提取的文件
    select_dirs = [i for i in walk_path_full if os.path.isdir(i)]  # 存放提取的文件夹
    return select_files, select_dirs


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
    return filename


def get_original_size(file, ftype):
    """统计原文件大小"""
    if ftype == "normal":
        size = os.path.getsize(file)
    else:
        size = 0
        for i in fenjuan_dict[file]:
            size += os.path.getsize(i)
    return size


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
    global total_number, rate_file_number, error_number, damage_number
    zip_path = './7-Zip/7z.exe'  # 7zip路径
    rate_file_number = 0
    for file in files_list:
        rate_file_number += 1
        print(f"——————正在解压第{rate_file_number}个文件，文件名：{os.path.split(file)[1]}，总进度{rate_file_number}/{total_number}——————")
        file_directory = os.path.split(file)[0]  # 文件的父目录
        file_name_without_suffix = pick_filename(file, ftype)  # 单独的没有后缀的文件名
        temporary_folder = os.path.join(file_directory, "UnzipTempFolder")  # 临时存放解压结果的文件夹
        unzip_path = os.path.join(temporary_folder, file_name_without_suffix)  # 解压到临时文件下与文件同名的文件夹中
        password_try_number = 0  # 密码尝试次数
        for password in resort_passwords:
            zip_command = [zip_path, "x", "-p" + password, "-y", file, "-o" + unzip_path, "-slt"]  # 组合完整7z指令
            unzip_result = subprocess.run(zip_command)
            if unzip_result.returncode != 0:
                password_try_number += 1  # 返回码不为0则解压失败，密码失败次数+1
            elif unzip_result.returncode == 0:
                print(f"——————成功解压第{rate_file_number}个文件，文件名：{os.path.split(file)[1]}，密码：{password}——————")
                original_size = get_original_size(file, ftype)  # 原文件大小
                unzip_size = get_result_size(unzip_path)  # 压缩结果大小
                if unzip_size < original_size * 0.95:  # 解压后文件大小如果小于原文件95%，则说明压缩包损坏
                    winshell.delete_file(unzip_path, no_confirm=True)  # 删除解压结果
                    damage_number += 1  # 计数+1
                    print(f"——————{os.path.split(file)[1]} 经检验已损坏（解压文件大小<解压前文件的95%）——————")
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
    print(f"★完成全部解压操作，成功：{total_number - error_number}个，失败：{error_number}个，文件损坏：{damage_number}个")
    if get_result_size(temporary_folder) == 0:
        winshell.delete_file(temporary_folder, no_confirm=True)
    else:
        print("——————注意：临时文件夹不为空，请检查——————")
    main()


def get_result_size(path):
    """获取文件夹大小"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


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


def main():
    hello = """
————————————————————————————————————
★★★功能选项：
1. 输入文件夹路径，并开始解压
2. 新增密码
3. 查看全部密码（按使用次数排列）
4. 导出密码文件
5. 退出
"""
    print(hello)
    input_code = int(input("★★★输入数字进入相应功能："))
    if input_code == 1:
        input_path()
    elif input_code == 2:
        add_password()
    elif input_code == 3:
        show_password()
    elif input_code == 4:
        export_password()
    elif input_code == 5:
        exit(1)
    else:
        print("——————无对应功能，请重新输入——————")
        return main()


if __name__ == "__main__":
    print("★★★欢迎使用 only_unzip")
    print("★★★更新日期：230405")
    read_password()
    main()
