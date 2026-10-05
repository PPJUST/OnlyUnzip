# ?????
from .window_model import WindowModel
from .window_presenter import WindowPresenter
from .window_viewer import WindowViewer


def get_presenter() -> WindowPresenter:
    """?????Presenter"""
    viewer = WindowViewer()
    model = WindowModel()
    presenter = WindowPresenter(viewer, model)
    return presenter
