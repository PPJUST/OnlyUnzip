# 设置文件的通用方法
import os
import re

import components.page_setting


def get_pre_filter_model():
    """获取当前的文件预筛选模式 默认/黑名单/白名单"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_model_pre_filter()


def get_pre_filter_black_list():
    """获取当前的文件预筛选黑名单规则"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_model_pre_filter_blacklist_rule()


def filter_by_black_list(files: list[str]):
    """根据文件预筛选黑名单规则，筛选传入文件"""
    files_filter = files.copy()
    black_list = get_pre_filter_black_list()
    patterns = [re.compile(rule, flags=re.IGNORECASE) for rule in black_list]
    for file in files:
        filename = os.path.basename(file)
        for pattern in patterns:
            if pattern.search(filename):
                files_filter.remove(file)
                break

    return files_filter


def get_pre_filter_white_list():
    """获取当前的文件预筛选白名单规则"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_model_pre_filter_whitelist_rule()


def filter_by_white_list(files: list[str]):
    """根据文件预筛选白名单规则，筛选传入文件"""
    files_filter = []
    white_list = get_pre_filter_white_list()
    patterns = [re.compile(rule, flags=re.IGNORECASE) for rule in white_list]
    for file in files:
        filename = os.path.basename(file)
        for pattern in patterns:
            if pattern.search(filename):
                files_filter.append(file)
                break

    return files_filter


def get_archive_model():
    """获取当前的压缩文件处理模式 解压/测试"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_model_archive()


def get_extract_output_folder():
    """获取解压输出目录，若未启用则返回空"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_extract_output_folder_path()


def get_is_try_unknown_filetype():
    """获取是否尝试处理未知格式的文件"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_try_unknown_filetype_is_enable()


def get_7zip_path():
    """获取指定的7zip路径，若未指定则返回空"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_7zip_path()
