# 主页模块
from .home_model import HomeModel
from .home_presenter import HomePresenter
from .home_viewer import HomeViewer


def get_presenter() -> HomePresenter:
    """获取模块的Presenter"""
    viewer = HomeViewer()
    model = HomeModel()
    presenter = HomePresenter(viewer, model)
    return presenter
