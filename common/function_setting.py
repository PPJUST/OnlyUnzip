# 设置文件的通用方法，仅用于读取部分选项
import os
import re

from common import class_setting


def _get_setting():
    """获取设置对象"""
    return class_setting.ModelSetting()


def _compile_patterns(rules: list[str]) -> list[re.Pattern[str]]:
    """将规则字符串编译为正则表达式对象"""
    patterns: list[re.Pattern[str]] = []
    for rule in rules:
        pattern = re.compile(rule, flags=re.IGNORECASE)
        patterns.append(pattern)
    return patterns


def _is_match(filename: str, patterns: list[re.Pattern[str]]) -> bool:
    """判断文件名是否命中任意一条规则"""
    for pattern in patterns:
        if pattern.search(filename):
            return True
    return False


def get_pre_filter_model():
    """获取当前的文件预筛选模式 默认/黑名单/白名单"""
    setting = _get_setting()
    return setting.get_model_pre_filter()


def get_pre_filter_black_list():
    """获取当前的文件预筛选黑名单规则"""
    setting = _get_setting()
    return setting.get_model_pre_filter_blacklist_rule()


def filter_by_black_list(files: list[str]) -> list[str]:
    """根据文件预筛选黑名单规则，剔除命中的文件"""
    files_filter: list[str] = []
    patterns = _compile_patterns(get_pre_filter_black_list())
    for file in files:
        filename = os.path.basename(file)
        if not _is_match(filename, patterns):
            files_filter.append(file)
    return files_filter


def get_pre_filter_white_list():
    """获取当前的文件预筛选白名单规则"""
    setting = _get_setting()
    return setting.get_model_pre_filter_whitelist_rule()


def filter_by_white_list(files: list[str]) -> list[str]:
    """根据文件预筛选白名单规则，保留命中的文件"""
    files_filter: list[str] = []
    patterns = _compile_patterns(get_pre_filter_white_list())
    for file in files:
        filename = os.path.basename(file)
        if _is_match(filename, patterns):
            files_filter.append(file)
    return files_filter


def get_archive_model():
    """获取当前的压缩文件处理模式 解压/测试"""
    setting = _get_setting()
    return setting.get_model_archive()


def get_extract_output_folder():
    """获取解压输出目录的设置值，未设置时返回空"""
    setting = _get_setting()
    return setting.get_extract_output_folder_path()


def get_is_try_unknown_filetype():
    """获取是否尝试处理未知格式的文件"""
    setting = _get_setting()
    return setting.get_try_unknown_filetype_is_enable()


def get_7zip_path():
    """获取指定的7zip路径，若未指定则返回空"""
    setting = _get_setting()
    return setting.get_7zip_path()
