# 历史模块的桥梁组件
from common.class_7zip import RESULT_STATE_ALL, CLASS_RESULT_7ZIP
from common.class_file_info import FileInfo
from components.page_history.history_model import HistoryModel
from components.page_history.history_viewer import HistoryViewer


# todo 历史记录优化，写入log

class HistoryPresenter:
    """历史模块的桥梁组件"""

    def __init__(self, viewer: HistoryViewer, model: HistoryModel):
        self.viewer = viewer
        self.model = model

        # 绑定信号
        self.viewer.HistoryFilter.connect(self.filter_result)

    def collection_history(self, file_info: FileInfo):
        """收集处理结果，并在viewer上显示"""
        print('接收7zip处理结果，并显示在历史页')
        print('接收的结果：', file_info)
        info, color, password = self.model.analyse_7zip_result(file_info)
        print('分析结果：', info, color, password)
        self.viewer.add_record(info, color, password, file_info)

    def filter_result(self, result_state: str, search_text: str):
        """过滤结果"""
        # 先检查是否需要过滤（全部+空文本则为不过滤历史记录）
        if result_state == RESULT_STATE_ALL and not search_text:
            self.viewer.show_all_history()
        else:
            # 将需要搜索的结果状态转换为自定义结果类
            result_class = []
            if result_state == RESULT_STATE_ALL:
                result_class = CLASS_RESULT_7ZIP
            else:
                for class_ in CLASS_RESULT_7ZIP:
                    class_state = class_.result_state
                    if class_state == result_state:
                        result_class.append(class_)

            self.viewer.filter_history(result_class, search_text)
