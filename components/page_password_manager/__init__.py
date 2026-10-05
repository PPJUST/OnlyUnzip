# ????????
from .password_manager_model import PasswordManagerModel
from .password_manager_presenter import PasswordManagerPresenter
from .password_manager_viewer import PasswordManagerViewer


def get_presenter() -> PasswordManagerPresenter:
    """?????Presenter"""
    viewer = PasswordManagerViewer()
    model = PasswordManagerModel()
    presenter = PasswordManagerPresenter(viewer, model)
    return presenter
