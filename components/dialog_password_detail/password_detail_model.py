# 密码详情表的模型组件
import lzytools.time


class PasswordDetailModel:
    """密码详情表的模型组件，负责把原始数据转换成界面要显示的文本。"""

    def get_display_values(self, password_info: tuple) -> list:
        """把一条密码记录转换成表格各列要显示的文本。

        :param password_info: 一条记录，依次为密码str、使用次数int、添加时间str、最后使用时间str
        :return: 与表头顺序一致的文本列表
        """
        password, use_count, add_time, last_use_time = password_info

        values = [
            str(password),
            str(use_count),
            lzytools.time.convert_duration_to_date(add_time),
            lzytools.time.convert_duration_to_date(last_use_time),
        ]
        return values
