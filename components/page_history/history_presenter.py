# 历史模块的桥梁组件
from common.class_file_info import FileInfo
from components.page_history.history_model import HistoryModel
from components.page_history.history_viewer import HistoryViewer


# todo 历史记录优化，写入log+添加筛选功能+删除功能+搜索功能（搜索功能需要支持文件名、父目录）
# todo 右键菜单添加更多选项，例如打开解压路径

class HistoryPresenter:
    """历史模块的桥梁组件"""

    def __init__(self, viewer: HistoryViewer, model: HistoryModel):
        self.viewer = viewer
        self.model = model

    def collection_history(self, file_info: FileInfo):
        """收集处理结果，并在viewer上显示"""
        print('接收7zip处理结果，并显示在历史页')
        print('接收的结果：', file_info)
        info, color, password = self.model.analyse_7zip_result(file_info)
        print('分析结果：', info, color, password)
        self.viewer.add_record(info, color, password)
