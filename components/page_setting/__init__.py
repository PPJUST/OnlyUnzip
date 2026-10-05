# ?????
from components.page_setting.setting_model import SettingModel
from components.page_setting.setting_presenter import SettingPresenter
from components.page_setting.setting_viewer import SettingViewer


def get_presenter() -> SettingPresenter:
    """?????Presenter"""
    viewer = SettingViewer()
    model = SettingModel()
    presenter = SettingPresenter(viewer, model)
    return presenter
