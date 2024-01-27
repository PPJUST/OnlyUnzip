import configparser
import re
from typing import Tuple

import natsort

from constant import _CONFIG_FILE
from module.function_static import print_function_info


def read_pw() -> Tuple[list, list]:
    """读取配置文件中的密码，并排序后返回两种list"""
    print_function_info()
    config = configparser.ConfigParser()
    config.read(_CONFIG_FILE, encoding='utf-8')

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


def update_pw(pw_list: list):
    """更新配置文件中的密码"""
    print_function_info()
    config = configparser.ConfigParser()
    config.read(_CONFIG_FILE, encoding='utf-8')
    old_pw = config.sections()
    for pw in pw_list:
        if pw not in old_pw:
            config.add_section(pw)
            config.set(pw, 'use_count', '0')
            old_pw.append(pw)

    config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))


def add_pw_count(pw: str):
    """在配置文件中将对应的解压密码使用次数+1"""
    print_function_info()
    config = configparser.ConfigParser()
    config.read(_CONFIG_FILE, encoding='utf-8')

    old_count = int(config.get(pw, 'use_count'))
    config.set(pw, 'use_count', str(old_count + 1))
    config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))
