# 临时密码模块
from .temp_password_model import TempPasswordModel
from .temp_password_presenter import TempPasswordPresenter
from .temp_password_viewer import TempPasswordViewer


def get_presenter() -> TempPasswordPresenter:
    """获取模块的Presenter"""
    viewer = TempPasswordViewer()
    model = TempPasswordModel()
    presenter = TempPasswordPresenter(viewer, model)
    return presenter
