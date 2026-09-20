# 历史模块的模型组件

import os
import time
from typing import Tuple, Union

from common import function_history
from common.class_7zip import Result7zip
from common.class_file_info import FileInfo
from common.function_7zip import FAKE_PASSWORD


class HistoryModel:
    """历史模块的模型组件"""

    def __init__(self):
        pass

    @staticmethod
    def analyse_7zip_result(file_info: FileInfo) -> Tuple[str, Tuple[int, int, int], Union[str, None]]:
        """分析7zip结果类
        :return: (行文本, 对应颜色, 正确密码)"""
        split_word = '\n■'
        part_time = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())
        part_filetitle = os.path.basename(file_info.filepath)
        _7zip_result = file_info._7zip_result
        part_7zip_result = _7zip_result.return_text
        color = _7zip_result.color
        text_join = (part_time +
                     split_word + part_filetitle +
                     split_word + part_7zip_result)

        # 只在解压结果为成功时才添加密码文本行和返回密码
        if isinstance(_7zip_result, Result7zip.Success):
            password = _7zip_result.password
            if password == FAKE_PASSWORD:
                return text_join, color, None
            else:
                text_join += (split_word + '解压密码：' + password)
                return text_join, color, password
        else:
            return text_join, color, None

    @staticmethod
    def save_7zip_result(file_info: FileInfo):
        """保存7zip结果类到本地"""
        function_history.save_to_result(file_info)

    @staticmethod
    def search_cache(search_text: str):
        """搜索缓存对应的文本"""
        return function_history.search_cache(search_text)
