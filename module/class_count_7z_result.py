from module.class_state import State7zResult


class Count7zResult:
    """统计7z调用结果，计数每种情况"""

    def __init__(self):
        self.files_result = {}  # 收集结果，key为文件路径，value为对应的结果类

    def reset_count(self):
        """重置计数"""
        self.files_result = {}

    def collect_result(self, result_class):
        """收集结果"""
        file = result_class.file
        self.files_result[file] = result_class

    def get_result_text(self):
        """获取结果文本"""
        wrong_password = 0
        missing_volume = 0
        not_archive_or_damaged = 0
        unknown_error = 0
        file_occupied = 0
        not_enough_space = 0
        success = 0

        for result_class in self.files_result.values():
            if type(result_class) is State7zResult.WrongPassword:
                wrong_password += 1
            elif type(result_class) is State7zResult.MissingVolume:
                missing_volume +=1
            elif type(result_class) is State7zResult.NotArchiveOrDamaged:
                not_archive_or_damaged +=1
            elif type(result_class) is State7zResult.UnknownError:
                unknown_error +=1
            elif type(result_class) is State7zResult.FileOccupied:
                file_occupied +=1
            elif type(result_class) is State7zResult.NotEnoughSpace:
                not_enough_space +=1
            elif type(result_class) is State7zResult.Success:
                success +=1

        total_count_success = success
        total_count_wrong_password = wrong_password
        total_count_error = missing_volume+not_archive_or_damaged+unknown_error+file_occupied+not_enough_space

        join_text = f'成功:{total_count_success} 失败:{total_count_wrong_password} 错误:{total_count_error}'

        self.reset_count()  # 重置

        return join_text



