# 历史模块的桥梁组件
from common import function_history
from common.class_7zip import RESULT_STATE_ALL, CLASS_RESULT_7ZIP, RESULT_STATE_CACHE
from common.class_file_info import FileInfo
from components.page_history.history_model import HistoryModel
from components.page_history.history_viewer import HistoryViewer

CACHE_TEXT_COLOR = (0, 0, 0)


class HistoryPresenter:
    """历史模块的桥梁组件"""

    def __init__(self, viewer: HistoryViewer, model: HistoryModel):
        self.viewer = viewer
        self.model = model

        # 检查历史记录文件
        function_history.check_history_file()
        function_history.move_history_file()

        # 绑定信号
        self.viewer.HistoryFilter.connect(self.filter_result)

    def collection_history(self, file_info: FileInfo):
        """收集处理结果，并在viewer上显示"""
        print('接收7zip处理结果，并显示在历史页：', file_info)
        info, color, password = self.model.analyse_7zip_result(file_info)
        self.viewer.add_record(info, color, password, file_info)
        self.model.save_7zip_result(file_info)

    def filter_result(self, result_state: str, search_text: str):
        """过滤结果"""
        # 空文本为不过滤历史记录
        if not search_text:
            self.viewer.show_all_history()
            return

        # 缓存记录需要先从本地读出并添加到界面，再按全部结果类筛选
        if result_state == RESULT_STATE_CACHE:
            self._add_cache_records(search_text)
            result_class = CLASS_RESULT_7ZIP
        else:
            result_class = self._get_result_class(result_state)

        self.viewer.filter_history(result_class, search_text)

    def _get_result_class(self, result_state: str) -> list:
        """根据结果状态获取需要筛选的结果类"""
        if result_state == RESULT_STATE_ALL:
            return CLASS_RESULT_7ZIP

        result_class = []
        for class_ in CLASS_RESULT_7ZIP:
            if class_.result_state == result_state:
                result_class.append(class_)
        return result_class

    def _add_cache_records(self, search_text: str):
        """将本地缓存中匹配的记录添加到界面"""
        infos = self.model.search_cache(search_text)
        for info in infos:
            self.viewer.add_record(info, CACHE_TEXT_COLOR)
