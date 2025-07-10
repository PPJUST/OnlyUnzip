# 历史模块的模型组件

import os
import time
from typing import Tuple, Union

from common.class_7zip import Result7zip
from common.class_file_info import FileInfo


class HistoryModel:
    """历史模块的模型组件"""

    def __init__(self):
        pass

    @staticmethod
    def analyse_7zip_result(file_info: FileInfo) -> Tuple[str, Tuple[int, int, int], Union[str, None]]:
        """分析7zip结果类
        :return: (行文本, 对应颜色, 正确密码)"""
        split_line = '-' * 16
        split_word = '\n■'
        part_time = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())
        part_filetitle = os.path.basename(file_info.filepath)
        _7zip_result = file_info._7zip_result
        part_7zip_result = _7zip_result.return_text
        color = _7zip_result.color
        password = _7zip_result.password
        text_join = (split_line +
                     split_word + part_time +
                     split_word + part_filetitle +
                     split_word + part_7zip_result)

        # 只在解压结果为成功时才添加密码文本行和返回密码
        if isinstance(_7zip_result, Result7zip.Success):
            text_join += (split_word + '解压密码：' + password)
            return text_join, color, password
        else:
            return text_join, color, None
