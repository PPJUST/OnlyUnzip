# 报错信息模块的桥梁组件
import lzytools

from components.page_error_info.error_info_viewer import ErrorInfoViewer

# 单独出现的 '^' 为无效信息，不需要显示
IGNORED_INFO = '^'


class ErrorInfoPresenter:
    """报错信息模块的桥梁组件"""

    def __init__(self, viewer: ErrorInfoViewer):
        self.viewer = viewer

    def append_info(self, info: str):
        """添加一条带时间的报错信息

        :param info: 原始报错信息
        """
        if info == IGNORED_INFO:
            return

        text_time = lzytools.time.get_current_time()
        text = f'{text_time}: {info}'
        self.viewer.append_info(text)
