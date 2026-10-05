# ??????
from .temp_password_model import TempPasswordModel
from .temp_password_presenter import TempPasswordPresenter
from .temp_password_viewer import TempPasswordViewer


def get_presenter() -> TempPasswordPresenter:
    """?????Presenter"""
    viewer = TempPasswordViewer()
    model = TempPasswordModel()
    presenter = TempPasswordPresenter(viewer, model)
    return presenter
