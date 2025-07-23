# 设置文件的通用方法
import components.page_setting


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
