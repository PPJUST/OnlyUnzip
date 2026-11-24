# 历史模块的模型组件

import os
import time
from typing import Tuple, Union

from common import function_history
from common.class_7zip import Result7zip, TYPES_RESULT_7ZIP
from common.class_file_info import FileInfo
from common.function_7zip import FAKE_PASSWORD

DATETIME_FORMAT = '%Y.%m.%d %H:%M:%S'
SEPARATOR = '\n■'


class HistoryModel:
    """历史模块的模型组件"""

    @staticmethod
    def analyse_7zip_result(file_info: FileInfo) -> Tuple[str, Tuple[int, int, int], Union[str, None]]:
        """分析7zip结果类
        :return: (行文本, 对应颜色, 正确密码)"""
        result = file_info.get_7zip_result()
        password = HistoryModel._get_right_password(result)

        parts = [
            time.strftime(DATETIME_FORMAT, time.localtime()),
            os.path.basename(file_info.filepath),
            result.return_text
        ]
        if password:
            parts.append('解压密码：' + password)

        text: str = SEPARATOR.join(parts)
        return text, result.color, password

    @staticmethod
    def _get_right_password(result: TYPES_RESULT_7ZIP) -> Union[str, None]:
        """获取正确密码，仅成功且非虚拟密码时返回"""
        if not isinstance(result, Result7zip.Success):
            return None
        if result.password == FAKE_PASSWORD:
            return None
        return result.password

    @staticmethod
    def save_7zip_result(file_info: FileInfo):
        """保存7zip结果类到本地"""
        function_history.save_to_result(file_info)

    @staticmethod
    def search_cache(search_text: str):
        """搜索缓存对应的文本"""
        return function_history.search_cache(search_text)
