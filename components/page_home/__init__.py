# ????
from .home_model import HomeModel
from .home_presenter import HomePresenter
from .home_viewer import HomeViewer


def get_presenter() -> HomePresenter:
    """?????Presenter"""
    viewer = HomeViewer()
    model = HomeModel()
    presenter = HomePresenter(viewer, model)
    return presenter
