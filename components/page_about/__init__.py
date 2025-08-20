# 关于模块
from .viewer import AboutViewer


def get_viewer() -> AboutViewer:
    """获取模块的Viewer"""
    return AboutViewer()
