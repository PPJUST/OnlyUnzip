# 密码模块的模型组件
# 用于配置文件的具体方法，包括读取、修改、保存、获取等
from typing import Union

from PySide6.QtWidgets import QApplication

from common import function_password
# 显式导入密码本相关的类，读取旧版本的密码本时需要
from common.function_password import DB_FILEPATH, DBPassword, Password

_ = Password  # 占位，避免 Password 被判定为未使用


class PasswordModel:
    """密码模块的模型组件"""

    def __init__(self):
        self.password_db: DBPassword = function_password.read_db()

    def reload(self):
        """重新加载密码本"""
        self.password_db = function_password.read_db()

    def get_passwords(self):
        """获取密码列表"""
        pws = self.password_db.get_passwords()
        # 剔除临时密码
        if "无密码" in pws:
            pws.remove("无密码")
        return pws

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
        if not password:
            return

        # 更新前备份一次密码
        function_password.backup_file(DB_FILEPATH)

        if isinstance(password, (list, set)):
            pws = list(password)
        elif isinstance(password, str):
            # 一个密码占一行，空白行不加入密码本
            pws = []
            for line in password.split('\n'):
                if line.strip():
                    pws.append(line)

            # 同时加入去掉两端空格的版本，保持原有顺序且不重复
            stripped_pws = []
            for pw in pws:
                stripped = pw.strip()
                if stripped not in pws:
                    stripped_pws.append(stripped)
            pws = pws + stripped_pws
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

        lines = [
            '添加方法：一个密码占一行，点击“更新密码本”。',
            '直接拖入旧版本的密码本文件，可以读取其中的密码',
            '',
            f'当前存储的密码数量：{len(pws)}',
            '',
        ]

        # 只预览前 10 个密码
        preview = '\n'.join(pws[:10])
        lines.append('常用密码预览：\n' + preview)
        return '\n'.join(lines)

    def drop_files(self, files):
        """处理拖入的文件"""
        return function_password.read_passwords_from_files(files)
