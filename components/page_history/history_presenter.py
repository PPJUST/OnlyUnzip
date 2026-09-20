# 历史模块的桥梁组件
from common import function_history
from common.class_7zip import RESULT_STATE_ALL, CLASS_RESULT_7ZIP, RESULT_STATE_CACHE
from common.class_file_info import FileInfo
from components.page_history.history_model import HistoryModel
from components.page_history.history_viewer import HistoryViewer


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
        print('接收7zip处理结果，并显示在历史页')
        print('接收的结果：', file_info)
        info, color, password = self.model.analyse_7zip_result(file_info)
        print('分析结果：', info, color, password)
        self.viewer.add_record(info, color, password, file_info)
        self._save_history(file_info)

    def filter_result(self, result_state: str, search_text: str):
        """过滤结果"""
        # 先检查是否需要过滤（空文本为不过滤历史记录）
        if not search_text:
            self.viewer.show_all_history()
        else:
            # 将需要搜索的结果状态转换为自定义结果类
            result_class = []
            # 如果选择了全部，则选择全部的结果类
            if result_state == RESULT_STATE_ALL:
                result_class = CLASS_RESULT_7ZIP
            # 如果选择了缓存，则读取本地缓存，添加到viewer后，再选择全部的结果类
            elif result_state == RESULT_STATE_CACHE:
                infos = self.model.search_cache(search_text)
                color = (0, 0, 0)
                for info in infos:
                    self.viewer.add_record(info, color)
                result_class = CLASS_RESULT_7ZIP
            # 否则，仅选择需要的结果类
            else:
                for class_ in CLASS_RESULT_7ZIP:
                    class_state = class_.result_state
                    if class_state == result_state:
                        result_class.append(class_)

            self.viewer.filter_history(result_class, search_text)

    def _save_history(self, file_info: FileInfo):
        """保存处理结果到本地"""
        self.model.save_7zip_result(file_info)
