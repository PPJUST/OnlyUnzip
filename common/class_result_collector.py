# 7zip?????
from common.class_7zip import Result7zip, TYPES_RESULT_7ZIP


class ResultCollector:
    """7zip?????"""

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

    def add_result(self, result: TYPES_RESULT_7ZIP):
        """????"""
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
        """???????????
        :return: ????,????"""
        info_simple = self._get_result_info_simple()
        info_detail = self._get_result_info_detail()
        # ?????????
        self._reset()
        return info_simple, info_detail

    def get_count_all_result(self) -> int:
        """?????????"""
        count = (len(self._success) +
                 len(self._skip) +
                 len(self._warning) +
                 len(self._wrong_password) +
                 len(self._missing_volume) +
                 len(self._wrong_filetype) +
                 len(self._unknown_error) +
                 len(self._error_command) +
                 len(self._not_enough_memory) +
                 len(self._user_stopped))

        return count

    def _get_result_info_simple(self):
        """?????????,????????"""
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
        return f'??:{success_count}, ??:{fail_count}'

    def _get_result_info_detail(self):
        """?????????"""
        return (f'??:{len(self._success)}\n'
                f'??:{len(self._skip)}\n'
                f'????:{len(self._warning)}\n'
                f'????:{len(self._wrong_password)}\n'
                f'????:{len(self._missing_volume)}\n'
                f'??????:{len(self._wrong_filetype)}\n'
                f'????:{len(self._unknown_error)}\n'
                f'?????:{len(self._error_command)}\n'
                f'??????:{len(self._not_enough_memory)}\n'
                f'????:{len(self._user_stopped)}\n')

    def _reset(self):
        """????"""
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
