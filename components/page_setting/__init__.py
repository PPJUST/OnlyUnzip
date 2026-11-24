# 设置页模块
from components.page_setting.setting_model import SettingModel
from components.page_setting.setting_presenter import SettingPresenter
from components.page_setting.setting_viewer import SettingViewer


def get_presenter() -> SettingPresenter:
    """创建并返回设置模块的 Presenter"""
    viewer = SettingViewer()
    model = SettingModel()
    return SettingPresenter(viewer, model)
