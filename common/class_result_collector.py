# 7zip结果收集类
from common.class_7zip import Result7zip, TYPES_RESULT_7ZIP

SUCCESS_NAME = '成功'

# 结果类型与显示名称的对应关系，列表顺序即详细文本的显示顺序
RESULT_TYPES = [
    (Result7zip.Success, SUCCESS_NAME),
    (Result7zip.Skip, '跳过'),
    (Result7zip.Warning, '文件占用'),
    (Result7zip.WrongPassword, '密码错误'),
    (Result7zip.MissingVolume, '缺失分卷'),
    (Result7zip.WrongFiletype, '文件类型错误'),
    (Result7zip.UnknownError, '未知错误'),
    (Result7zip.ErrorCommand, '命令行错误'),
    (Result7zip.NotEnoughMemory, '磁盘空间不足'),
    (Result7zip.UserStopped, '用户停止'),
]


class ResultCollector:
    """7zip结果收集类，按结果类型统计数量"""

    def __init__(self):
        # 用字典统一管理各类结果，避免为每种结果类型重复编写代码
        self._results = {}
        for result_type, name in RESULT_TYPES:
            self._results[name] = []

    def add_result(self, result: TYPES_RESULT_7ZIP):
        """添加结果"""
        for result_type, name in RESULT_TYPES:
            if isinstance(result, result_type):
                self._results[name].append(result)
                return

    def get_result_info(self):
        """获取两种格式的结果文本
        :return: 精简文本，详细文本"""
        info_simple = self._get_result_info_simple()
        info_detail = self._get_result_info_detail()
        # 提取文本后重置计数
        self._reset()
        return info_simple, info_detail

    def get_count_all_result(self) -> int:
        """获取所有结果的计数"""
        count = 0
        for name in self._results:
            count += len(self._results[name])
        return count

    def _get_result_info_simple(self):
        """获取精简的结果文本，仅区分成功和失败"""
        success_count = len(self._results[SUCCESS_NAME])
        fail_count = self.get_count_all_result() - success_count
        return f'成功:{success_count}, 失败:{fail_count}'

    def _get_result_info_detail(self):
        """获取详细的结果文本"""
        lines = []
        for result_type, name in RESULT_TYPES:
            lines.append(f'{name}:{len(self._results[name])}')
        return '\n'.join(lines) + '\n'

    def _reset(self):
        """清空已收集的结果"""
        for result_type, name in RESULT_TYPES:
            self._results[name] = []
