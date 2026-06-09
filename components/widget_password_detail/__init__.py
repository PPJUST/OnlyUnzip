# 密码管理器页模块
from .password_detail_model import PasswordDetailModel
from .password_detail_presenter import PasswordDetailPresenter
from .password_detail_viewer import PasswordDetailViewer


def get_presenter() -> PasswordDetailPresenter:
    """获取模块的Presenter"""
    viewer = PasswordDetailViewer()
    model = PasswordDetailModel()
    presenter = PasswordDetailPresenter(viewer, model)
    return presenter
