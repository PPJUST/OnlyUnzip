# 配置文件相关方法

import configparser
import os

from constant import _CONFIG_FILE


class Config:
    def __init__(self):
        # 设置初始参数
        self.mode = 'extract'  # 模式，解压或测试
        self.handling_nested_folder = True  # 是否处理嵌套文件夹
        self.handling_nested_archive = False  # 是否处理嵌套压缩文件
        self.delete_original_file = False  # 是否删除解压的原文件
        self.check_filetype = True  # 是否检查文件类型（即是否仅处理压缩包）
        self.exclude_rules = []  # 解压时排除文件的后缀列表（在配置文件中以|为间隔转换为字符串存储）
        self.output_folder = ''  # 指定解压到某文件夹的路径

        # 初始化
        self._reset_config()

    def _reset_config(self):
        """从配置文件中读取并更新参数"""
        if not os.path.exists(_CONFIG_FILE):
            with open(_CONFIG_FILE, 'w', encoding='utf-8') as cw:
                cw.write('[DEFAULT]')

            config = configparser.ConfigParser()
            config.read(_CONFIG_FILE, encoding='utf-8')
            config.set('DEFAULT', 'mode', self.mode)
            config.set('DEFAULT', 'handling_nested_folder', str(self.handling_nested_folder))
            config.set('DEFAULT', 'handling_nested_archive', str(self.handling_nested_archive))
            config.set('DEFAULT', 'delete_original_file', str(self.delete_original_file))
            config.set('DEFAULT', 'check_filetype', str(self.check_filetype))
            config.set('DEFAULT', 'exclude_rules', ' '.join(self.exclude_rules))
            config.set('DEFAULT', 'output_folder', self.output_folder)
            config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))
        else:
            config = configparser.ConfigParser()
            config.read(_CONFIG_FILE, encoding='utf-8')

            self.mode = config.get('DEFAULT', 'mode')
            self.handling_nested_folder = eval(config.get('DEFAULT', 'handling_nested_folder'))
            self.handling_nested_archive = eval(config.get('DEFAULT', 'handling_nested_archive'))
            self.delete_original_file = eval(config.get('DEFAULT', 'delete_original_file'))
            self.check_filetype = eval(config.get('DEFAULT', 'check_filetype'))
            self.exclude_rules = config.get('DEFAULT', 'exclude_rules').split(' ')
            self.output_folder = config.get('DEFAULT', 'output_folder')

    @staticmethod
    def update_config_mode(setting_item: str):
        config = configparser.ConfigParser()
        config.read(_CONFIG_FILE, encoding='utf-8')
        config.set('DEFAULT', 'mode', setting_item)
        config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))

    @staticmethod
    def update_config_handling_nested_folder(setting_item: bool):
        config = configparser.ConfigParser()
        config.read(_CONFIG_FILE, encoding='utf-8')
        config.set('DEFAULT', 'handling_nested_folder', str(setting_item))
        config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))

    @staticmethod
    def update_config_handling_nested_archive(setting_item: bool):
        config = configparser.ConfigParser()
        config.read(_CONFIG_FILE, encoding='utf-8')
        config.set('DEFAULT', 'handling_nested_archive', str(setting_item))
        config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))

    @staticmethod
    def update_config_delete_original_file(setting_item: bool):
        config = configparser.ConfigParser()
        config.read(_CONFIG_FILE, encoding='utf-8')
        config.set('DEFAULT', 'delete_original_file', str(setting_item))
        config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))

    @staticmethod
    def update_config_check_filetype(setting_item: bool):
        config = configparser.ConfigParser()
        config.read(_CONFIG_FILE, encoding='utf-8')
        config.set('DEFAULT', 'check_filetype', str(setting_item))
        config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))

    @staticmethod
    def update_exclude_rules(setting_item: str):
        config = configparser.ConfigParser()
        config.read(_CONFIG_FILE, encoding='utf-8')
        config.set('DEFAULT', 'exclude_rules', setting_item)
        config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))

    @staticmethod
    def update_config_output_folder(setting_item: str):
        config = configparser.ConfigParser()
        config.read(_CONFIG_FILE, encoding='utf-8')
        config.set('DEFAULT', 'output_folder', setting_item)
        config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))
