# ?????????
import os
import re

import components.page_setting


def get_pre_filter_model():
    """???????????? ??/???/???"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_model_pre_filter()


def get_pre_filter_black_list():
    """???????????????"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_model_pre_filter_blacklist_rule()


def filter_by_black_list(files: list[str]):
    """????????????,??????"""
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
    """???????????????"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_model_pre_filter_whitelist_rule()


def filter_by_white_list(files: list[str]):
    """????????????,??????"""
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
    """????????????? ??/??"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_model_archive()


def get_extract_output_folder():
    """????????,????????"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_extract_output_folder_path()


def get_is_try_unknown_filetype():
    """???????????????"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_try_unknown_filetype_is_enable()


def get_7zip_path():
    """?????7zip??,????????"""
    setting_presenter = components.page_setting.get_presenter().model
    return setting_presenter.get_7zip_path()
