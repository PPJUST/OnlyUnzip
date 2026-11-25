# 密码管理器模块的模型组件
# 负责读取密码本并提供查询、筛选和删除操作，不依赖界面
from common import function_password
from common.function_password import DBPassword


class PasswordManagerModel:
    """密码管理器模块的模型组件"""

    def __init__(self):
        self.password_db: DBPassword = function_password.read_db()

    # region 查询
    def get_passwords(self) -> list:
        """获取所有密码（按使用次数、最后使用时间降序排列）"""
        return self.password_db.get_passwords()

    def get_password_infos(self) -> list:
        """获取每条密码的详情，供详情窗口显示。

        每条记录依次为：密码、使用次数、添加时间、最后使用时间。
        """
        password_infos = []
        for info in self.password_db.get_passwords_class():
            password_info = (
                info.get_password(),
                info.get_use_count(),
                info.get_add_time(),
                info.get_last_use_time(),
            )
            password_infos.append(password_info)
        return password_infos

    # endregion

    # region 筛选与删除
    def delete_passwords(self, delete_passwords: list):
        """删除密码本中的指定密码"""
        self.password_db.delete_passwords(delete_passwords)

    def filter_use_count(self, min_use_count: int, max_use_count: int) -> list:
        """筛选使用次数在指定范围内（含边界）的密码"""
        return self.password_db.filter_use_count(min_use_count, max_use_count)

    def filter_add_time(self, day_interval: int, is_inside: bool = True) -> list:
        """按添加时间筛选密码，以当天为基准。

        :param day_interval: 天数间隔
        :param is_inside: 为 True 筛选间隔内，为 False 筛选间隔外
        """
        return self.password_db.filter_add_time(day_interval, is_inside)

    def filter_last_use_time(self, day_interval: int, is_inside: bool = True) -> list:
        """按最后使用时间筛选密码，以当天为基准。

        :param day_interval: 天数间隔
        :param is_inside: 为 True 筛选间隔内，为 False 筛选间隔外
        """
        return self.password_db.filter_last_use_time(day_interval, is_inside)
    # endregion
