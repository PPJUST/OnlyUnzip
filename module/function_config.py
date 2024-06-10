# 配置文件相关方法

import configparser
import os

from constant import _CONFIG_FILE


def create_default_config():
    """创建默认配置文件"""
    if not os.path.exists(_CONFIG_FILE):
        with open(_CONFIG_FILE, 'w', encoding='utf-8') as _:
            config = configparser.ConfigParser()
            config.read(_CONFIG_FILE, encoding='utf-8')

            config.add_section('OPTION')
            config.set('OPTION', 'mode_extract', 'True')  # 解压模式
            config.set('OPTION', 'mode_test', 'False')  # 测试模式
            config.set('OPTION', 'smart_extract', 'True')  # 智能解压
            config.set('OPTION', 'extract_to_folder', 'False')  # 解压至同名文件夹
            config.set('OPTION', 'delete_file', 'False')  # 解压后删除源文件
            config.set('OPTION', 'handle_multi_folder', 'True')  # 处理多层嵌套文件夹
            config.set('OPTION', 'handle_multi_archive', 'True')  # 处理多层嵌套压缩包
            config.set('OPTION', 'check_filetype', 'True')  # 检查文件类型（仅处理压缩包）
            config.set('OPTION', 'output_folder', '')  # 解压至指定目录
            config.set('OPTION', 'filter_suffix', '')  # 解压时排除的文件后缀

            config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))


def _get_value_normal(section, key):
    """获取指定section的key的value（原始格式）"""
    config = configparser.ConfigParser()
    config.read(_CONFIG_FILE, encoding='utf-8')
    value = config.get(section, key)
    return eval(value)


def _get_value_str(section, key):
    """获取指定section的key的value（文本格式）"""
    config = configparser.ConfigParser()
    config.read(_CONFIG_FILE, encoding='utf-8')
    value = config.get(section, key)
    return value


def _reset_value(section, key, value):
    """设置指定section的key的value"""
    config = configparser.ConfigParser()
    config.read(_CONFIG_FILE, encoding='utf-8')
    if isinstance(value, (list, set)):
        value = ' '.join(value)
    config.set(section, key, str(value))
    config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))


class GetSetting:

    @staticmethod
    def mode_extract():
        return _get_value_normal('OPTION', 'mode_extract')

    @staticmethod
    def mode_test():
        return _get_value_normal('OPTION', 'mode_test')

    @staticmethod
    def smart_extract():
        return _get_value_normal('OPTION', 'smart_extract')

    @staticmethod
    def extract_to_folder():
        return _get_value_normal('OPTION', 'extract_to_folder')

    @staticmethod
    def delete_file():
        return _get_value_normal('OPTION', 'delete_file')

    @staticmethod
    def handle_multi_folder():
        return _get_value_normal('OPTION', 'handle_multi_folder')

    @staticmethod
    def handle_multi_archive():
        return _get_value_normal('OPTION', 'handle_multi_archive')

    @staticmethod
    def check_filetype():
        return _get_value_normal('OPTION', 'check_filetype')

    @staticmethod
    def output_folder():
        return _get_value_str('OPTION', 'output_folder')

    @staticmethod
    def filter_suffix():
        return _get_value_str('OPTION', 'filter_suffix')


class ResetSetting:

    @staticmethod
    def mode_extract(value):
        _reset_value('OPTION', 'mode_extract', value)

    @staticmethod
    def mode_test(value):
        _reset_value('OPTION', 'mode_test', value)

    @staticmethod
    def smart_extract(value):
        _reset_value('OPTION', 'smart_extract', value)

    @staticmethod
    def extract_to_folder(value):
        _reset_value('OPTION', 'extract_to_folder', value)

    @staticmethod
    def delete_file(value):
        _reset_value('OPTION', 'delete_file', value)

    @staticmethod
    def handle_multi_folder(value):
        _reset_value('OPTION', 'handle_multi_folder', value)

    @staticmethod
    def handle_multi_archive(value):
        _reset_value('OPTION', 'handle_multi_archive', value)

    @staticmethod
    def check_filetype(value):
        _reset_value('OPTION', 'check_filetype', value)

    @staticmethod
    def output_folder(value):
        _reset_value('OPTION', 'output_folder', value)

    @staticmethod
    def filter_suffix(value):
        _reset_value('OPTION', 'filter_suffix', value)
