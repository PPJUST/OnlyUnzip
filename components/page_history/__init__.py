# 历史页模块
from .history_model import HistoryModel
from .history_presenter import HistoryPresenter
from .history_viewer import HistoryViewer


def get_presenter() -> HistoryPresenter:
    """获取模块的Presenter"""
    viewer = HistoryViewer()
    model = HistoryModel()
    presenter = HistoryPresenter(viewer, model)
    return presenter
