import os
import configparser
import shutil
import time
from typing import Tuple
import natsort
import re
from model.function_static import print_function_info

config_file = 'config.ini'
backup_dir = 'backup'


"""
变更记录
nested_folders->un_nest_dir
nested_zip->un_nest_archive
delete_zip->delete_archive
check_zip->check_filetype
skip_suffix->exclude_rule
unzip_to_folder->output_dir

优化命名 压缩包zip改archive 解压unzip改为extract
"""

# exclude_rule在传递时以str格式传递，实际使用时再转换为list
latest_setting = {'mode': 'extract',
                 'un_nest_dir': True,
                 'un_nest_archive': False,
                 'delete_archive': True,
                 'check_filetype': True,
                 'exclude_rule': '',
                 'output_dir': ''
                  }


def check_config():
    """检查配置文件，若本地不存在则新建"""
    print_function_info()
    if not os.path.exists(config_file):
        with open(config_file, 'w', encoding='utf-8') as cw:
            cw.write('[DEFAULT]')

        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        # config.add_section('DEFAULT')
        for key,value in latest_setting.items():
            config.set('DEFAULT', key, str(value))

        config.write(open(config_file, 'w', encoding='utf-8'))

    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)


def read_setting()->dict:
    """读取配置文件中的设置项，返回一个dict（将config还原为latest_config格式）"""
    print_function_info()
    config_dict = {}

    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    for key in config['DEFAULT']:
        value_str = config.get('DEFAULT', key)
        try:
            value_eval = eval(value_str)  # 利用eval转换为其原有格式
        except NameError:  # 如果原本是字符串，则会报错
            value_eval = value_str
        except SyntaxError:  # 如果为空，则会报错
            value_eval = value_str

        config_dict[key] = value_eval

    return config_dict

def update_setting(config_dict:dict):
    """更新配置文件的设置项"""
    print_function_info()
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    for key, value in config_dict.items():
        config.set('DEFAULT', key, str(value))

    config.write(open(config_file, 'w', encoding='utf-8'))

def backup_config():
    """备份配置文件"""
    print_function_info()
    nwe_filename = f'config {time.strftime("%Y_%m_%d %H_%M_%S ", time.localtime())}.ini'
    shutil.copyfile(config_file, f'{backup_dir}/{nwe_filename}')

def read_pw() -> Tuple[list, list]:
    """读取配置文件中的密码，并排序后返回两种list"""
    print_function_info()
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    all_pw = config.sections()
    pw_sorted = []  # 最终排序结果
    pw_sorted_with_count = []  # 带次数的排序结果

    for pw in all_pw:
        pw_sorted_with_count.append(config.get(pw, 'use_count') + ' - ' + pw)  # 使用次数 - 密码
    pw_sorted_with_count = natsort.natsorted(pw_sorted_with_count)[::-1]  # 按数字大小降序排序

    for i in pw_sorted_with_count:
        pw_sorted.append(re.search(r' - (.+)', i).group(1))  # 正则提取' - 后的密码

    return pw_sorted, pw_sorted_with_count

def export_pw(with_number: bool = False):
    """导出当前密码到本地
    传参：with_number 密码后是否添加使用次数"""
    print_function_info()
    pw_sorted, pw_sorted_with_count = read_pw()

    with open('密码导出.txt', 'w', encoding='utf-8') as pw:
        if with_number:
            pw.write("\n".join(pw_sorted_with_count))
        else:
            pw.write("\n".join(pw_sorted))


def update_pw(pw_list:list):
    """更新配置文件中的密码"""
    print_function_info()
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')
    old_pw = config.sections()
    for pw in pw_list:
        if pw not in old_pw:
            config.add_section(pw)
            config.set(pw, 'use_count', '0')
            old_pw.append(pw)

    config.write(open(config_file, 'w', encoding='utf-8'))

def add_pw_count(pw: str):
    """在配置文件中将对应的解压密码使用次数+1"""
    print_function_info()
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    old_count = int(config.get(pw, 'use_count'))
    config.set(pw, 'use_count', str(old_count + 1))
    config.write(open(config_file, 'w', encoding='utf-8'))

