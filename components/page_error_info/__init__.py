# ??????
from .error_info_presenter import ErrorInfoPresenter
from .error_info_viewer import ErrorInfoViewer


def get_viewer() -> ErrorInfoViewer:
    """?????Viewer"""
    return ErrorInfoViewer()


def get_presenter() -> ErrorInfoPresenter:
    """?????Presenter"""
    viewer = ErrorInfoViewer()
    presenter = ErrorInfoPresenter(viewer)
    return presenter
