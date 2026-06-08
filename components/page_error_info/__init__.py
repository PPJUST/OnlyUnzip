# 报错信息模块
from .error_info_presenter import ErrorInfoPresenter
from .error_info_viewer import ErrorInfoViewer


def get_viewer() -> ErrorInfoViewer:
    """获取模块的Viewer"""
    return ErrorInfoViewer()


def get_presenter() -> ErrorInfoPresenter:
    """获取模块的Presenter"""
    viewer = ErrorInfoViewer()
    presenter = ErrorInfoPresenter(viewer)
    return presenter
