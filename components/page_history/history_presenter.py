# ?????????
from common import function_history
from common.class_7zip import RESULT_STATE_ALL, CLASS_RESULT_7ZIP, RESULT_STATE_CACHE
from common.class_file_info import FileInfo
from components.page_history.history_model import HistoryModel
from components.page_history.history_viewer import HistoryViewer


class HistoryPresenter:
    """?????????"""

    def __init__(self, viewer: HistoryViewer, model: HistoryModel):
        self.viewer = viewer
        self.model = model

        # ????????
        function_history.check_history_file()
        function_history.move_history_file()

        # ????
        self.viewer.HistoryFilter.connect(self.filter_result)

    def collection_history(self, file_info: FileInfo):
        """??????,??viewer???"""
        print('??7zip????,???????')
        print('?????:', file_info)
        info, color, password = self.model.analyse_7zip_result(file_info)
        print('????:', info, color, password)
        self.viewer.add_record(info, color, password, file_info)
        self._save_history(file_info)

    def filter_result(self, result_state: str, search_text: str):
        """????"""
        # ?????????(???????????)
        if not search_text:
            self.viewer.show_all_history()
        else:
            # ???????????????????
            result_class = []
            # ???????,?????????
            if result_state == RESULT_STATE_ALL:
                result_class = CLASS_RESULT_7ZIP
            # ???????,???????,???viewer?,?????????
            elif result_state == RESULT_STATE_CACHE:
                infos = self.model.search_cache(search_text)
                color = (0, 0, 0)
                for info in infos:
                    self.viewer.add_record(info, color)
                result_class = CLASS_RESULT_7ZIP
            # ??,?????????
            else:
                for class_ in CLASS_RESULT_7ZIP:
                    class_state = class_.result_state
                    if class_state == result_state:
                        result_class.append(class_)

            self.viewer.filter_history(result_class, search_text)

    def _save_history(self, file_info: FileInfo):
        """?????????"""
        self.model.save_7zip_result(file_info)
