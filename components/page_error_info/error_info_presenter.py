# ???????????
import lzytools

from components.page_error_info.error_info_viewer import ErrorInfoViewer


class ErrorInfoPresenter:
    """???????????"""

    def __init__(self, viewer: ErrorInfoViewer, model=None):
        self.viewer = viewer
        self.model = model

    def append_info(self, info: str):
        """?????"""
        if info == '^':
            pass
        else:
            text_time = lzytools.time.get_current_time()
            info = f'{text_time}: {info}'
            self.viewer.append_info(info)
