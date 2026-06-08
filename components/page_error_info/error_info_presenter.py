# 报错信息模块的桥梁组件
import lzytools

from components.page_error_info.error_info_viewer import ErrorInfoViewer


class ErrorInfoPresenter:
    """报错信息模块的桥梁组件"""

    def __init__(self, viewer: ErrorInfoViewer, model=None):
        self.viewer = viewer
        self.model = model

    def append_info(self, info: str):
        """添加信息行"""
        text_time = lzytools.time.get_current_time()
        info = f'{text_time}: {info}\n'
        self.viewer.append_info(info)
