# 报错信息模块
from components.page_error_info.error_info_presenter import ErrorInfoPresenter
from components.page_error_info.error_info_viewer import ErrorInfoViewer


def get_presenter() -> ErrorInfoPresenter:
    """创建并返回报错信息模块的 Presenter"""
    viewer = ErrorInfoViewer()
    return ErrorInfoPresenter(viewer)
