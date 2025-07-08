# 历史模块的桥梁组件
from common.class_7zip import Result7zip
from common.class_file_info import FileInfo
from components.page_history.history_model import HistoryModel
from components.page_history.history_viewer import HistoryViewer


class HistoryPresenter:
    """历史模块的桥梁组件"""

    def __init__(self, viewer: HistoryViewer, model: HistoryModel):
        self.viewer = viewer
        self.model = model

    def collection_history(self, file_info: FileInfo):
        """收集处理结果，并在viewer上显示"""
        print('接收7zip处理结果，并显示在历史页')
        print('接收的结果：',file_info)
        info, color, password = self.model.analyse_7zip_result(file_info)
        print('分析结果：',info, color, password)
        self.viewer.add_record(info, color, password)
