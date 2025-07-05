# 密码页模块
from .password_model import PasswordModel
from .password_presenter import PasswordPresenter
from .password_viewer import PasswordViewer


def get_presenter() -> PasswordPresenter:
    """获取模块的Presenter"""
    viewer = PasswordViewer()
    model = PasswordModel()
    presenter = PasswordPresenter(viewer, model)
    return presenter
