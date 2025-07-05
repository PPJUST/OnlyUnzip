# 历史页模块
from .window_model import WindowModel
from .window_presenter import WindowPresenter
from .window_viewer import WindowViewer


def get_presenter() -> WindowPresenter:
    """获取模块的Presenter"""
    viewer = WindowViewer()
    model = WindowModel()
    presenter = WindowPresenter(viewer, model)
    return presenter