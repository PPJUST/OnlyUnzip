# 7zip结果收集类
from common.class_7zip import Result7zip


class ResultCollector:
    """7zip结果收集类"""

    def __init__(self):
        self._success = []
        self._skip = []
        self._warning = []
        self._wrong_password = []
        self._missing_volume = []
        self._wrong_filetype = []
        self._unknown_error = []
        self._error_command = []
        self._not_enough_memory = []
        self._user_stopped = []

    def add_result(self, result: Result7zip):
        """添加结果"""
        if isinstance(result, Result7zip.Success):
            self._success.append(result)
        elif isinstance(result, Result7zip.Skip):
            self._skip.append(result)
        elif isinstance(result, Result7zip.Warning):
            self._warning.append(result)
        elif isinstance(result, Result7zip.WrongPassword):
            self._wrong_password.append(result)
        elif isinstance(result, Result7zip.MissingVolume):
            self._missing_volume.append(result)
        elif isinstance(result, Result7zip.WrongFiletype):
            self._wrong_filetype.append(result)
        elif isinstance(result, Result7zip.UnknownError):
            self._unknown_error.append(result)
        elif isinstance(result, Result7zip.ErrorCommand):
            self._error_command.append(result)
        elif isinstance(result, Result7zip.NotEnoughMemory):
            self._not_enough_memory.append(result)
        elif isinstance(result, Result7zip.UserStopped):
            self._user_stopped.append(result)

    def get_result_info(self):
        """获取两种格式的结果文本
        :return: 精简文本，详细文本"""
        return self._get_result_info_simple(), self._get_result_info_detail()
    def _get_result_info_simple(self):
        """获取精简的结果文本，仅区分成功和失败"""
        success_count = len(self._success)
        fail_count = (len(self._skip) +
                      len(self._warning) +
                      len(self._wrong_password) +
                      len(self._missing_volume) +
                      len(self._wrong_filetype) +
                      len(self._unknown_error) +
                      len(self._error_command) +
                      len(self._not_enough_memory) +
                      len(self._user_stopped))
        return f'成功:{success_count}, 失败:{fail_count}'

    def _get_result_info_detail(self):
        """获取详细的结果文本"""
        return (f'成功:{len(self._success)}\n'
                f'跳过:{len(self._skip)}\n'
                f'文件占用:{len(self._warning)}\n'
                f'密码错误:{len(self._wrong_password)}\n'
                f'缺失分卷:{len(self._missing_volume)}\n'
                f'文件类型错误:{len(self._wrong_filetype)}\n'
                f'未知错误:{len(self._unknown_error)}\n'
                f'命令行错误:{len(self._error_command)}\n'
                f'磁盘空间不足:{len(self._not_enough_memory)}\n'
                f'用户停止:{len(self._user_stopped)}\n')


    def reset(self):
        """重置结果"""
        self._success.clear()
        self._skip.clear()
        self._warning.clear()
        self._wrong_password.clear()
        self._missing_volume.clear()
        self._wrong_filetype.clear()
        self._unknown_error.clear()
        self._error_command.clear()
        self._not_enough_memory.clear()
        self._user_stopped.clear()
