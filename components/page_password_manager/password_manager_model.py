# 密码管理器模块的模型组件
from common import function_password
from common.function_password import DBPassword


class PasswordManagerModel:
    """密码管理器模块的模型组件"""

    def __init__(self):
        self.password_db: DBPassword = function_password.read_db()

    def get_passwords(self):
        """获取密码本中所有密码"""
        return self.password_db.get_passwords()

    def delete_passwords(self, delete_passwords: list):
        """删除密码本中的指定密码"""
        self.password_db.delete_passwords(delete_passwords)

    def filter_use_count(self, min_use_count: int, max_use_count: int):
        """过滤密码本，只保留使用次数在指定范围内的密码"""
        return self.password_db.filter_use_count(min_use_count, max_use_count)

    def filter_add_time(self, day_interval: int, is_inside: bool = True):
        """过滤密码本，只保留首次添加时间在指定天数范围内的密码（以当日为基数）
        :param day_interval: 天数间隔
        :param is_inside: 筛选天数间隔内，否则筛选天数间隔外"""
        return self.password_db.filter_add_time(day_interval, is_inside)

    def filter_last_use_time(self, day_interval: int, is_inside: bool = True):
        """过滤密码本，只保留最后使用时间在指定天数范围内的密码（以当日为基数）
        :param day_interval: 天数间隔
        :param is_inside: 筛选天数间隔内，否则筛选天数间隔外"""
        return self.password_db.filter_last_use_time(day_interval, is_inside)
