# 密码模块的模型组件
# 用于配置文件的具体方法，包括读取、修改、保存、获取等
from typing import Union

from PySide6.QtWidgets import QApplication

from common import function_password
from common.function_password import DB_FILEPATH, DBPassword, Password  # 必须添加DBPassword, Password类

_ = Password  # 占位，防止未导入Password


class PasswordModel:
    """密码模块的模型组件"""

    def __init__(self):
        self.password_db: DBPassword = function_password.read_db()

    def reload(self):
        """重新加载密码本"""
        self.password_db = function_password.read_db()

    def get_passwords(self):
        """获取密码列表"""
        return self.password_db.get_passwords()

    @staticmethod
    def read_clipboard():
        """读取剪切板，并返回读取的内容"""
        clipboard = QApplication.clipboard()
        return clipboard.text()

    def output_password(self):
        """导出密码本到本地"""
        self.password_db.output_db()

    def open_password(self):
        """打开导出的密码文件"""
        self.password_db.open_output_file()

    def update_password(self, password: Union[str, list]):
        """更新密码本"""
        if password:
            # 更新前备份一次密码
            function_password.backup_file(DB_FILEPATH)
            if isinstance(password, (list, set)):
                pws = password
            elif isinstance(password, str):
                # 考虑两端可能存在空格的密码，添加密码时同时添加原始和去除空格的两种格式
                pws = [i for i in password.split('\n') if i.strip()]
                pws_strip = [i.strip() for i in pws if i.strip() not in pws]  # 为了保持密码的顺序，不使用set进行去重
                pws += pws_strip
            else:
                return
                # 写入密码本
            self.password_db.add_passwords(pws)

    def add_use_count_once(self, passwords: Union[str, list]):
        """增加一次密码的使用次数"""
        if isinstance(passwords, str):
            passwords = [passwords]
        for pw in passwords:
            self.password_db.add_use_count_once(pw)

    def count_password(self) -> str:
        """统计密码本信息"""
        pws = self.password_db.get_passwords()
        info_1 = '添加方法：一个密码占一行，点击“更新密码本”。\n'
        info_4 = '直接拖入旧版本的密码本文件，可以读取其中的密码\n'
        info_2 = f'当前存储的密码数量：{len(pws)}\n'
        info_pw10 = '\n'.join(pws[:10])
        info_3 = f'常用密码预览：\n{info_pw10}'
        info_join = info_1 + info_4 + '\n' + info_2 + '\n' + info_3
        return info_join

    def drop_files(self, files):
        """处理拖入的文件"""
        passwords_in_files = function_password.read_passwords_from_files(files)
        return passwords_in_files
