# 密码模块的模型组件
# 用于配置文件的具体方法，包括读取、修改、保存、获取等
import os
import pickle
import time

from PySide6.QtWidgets import QApplication

DB_FILEPATH = 'password.pkl'
_OUTPUT_FILE = 'password_output.txt'


class PasswordModel:
    """密码模块的模型组件"""

    def __init__(self):
        self.password_db = self._read_db()

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

    def update_password(self, text: str):
        """更新密码本"""
        # 考虑两端可能存在空格的密码，添加密码时同时添加原始和去除空格的两种格式
        pws = [i for i in text.split('\n') if i.strip()]
        pws_strip = [i.strip() for i in pws if i.strip() not in pws]  # 为了保持密码的顺序，不使用set进行去重
        pws += pws_strip
        # 写入密码本
        self.password_db.add_passwords(pws)

    def count_password(self) -> str:
        """统计密码本信息"""
        pws = self.password_db.get_passwords()
        info_1 = '更新：一个密码占一行，点击“更新密码”。\n'
        info_2 = f'当前密码本存储密码数：{len(pws)}\n'
        info_pw10 = '\n'.join(pws[:10])
        info_3 = f'常用密码预览：\n{info_pw10}'
        info_join = info_1 + info_2 + info_3
        return info_join

    @staticmethod
    def _read_db():
        """读取密码本"""
        if os.path.exists(DB_FILEPATH):
            with open(DB_FILEPATH, 'rb') as f:
                return pickle.load(f)
        else:
            return DBPassword()


class DBPassword(dict):
    """密码本类"""

    def __init__(self):
        super().__init__(self)
        if not os.path.exists(DB_FILEPATH):
            with open(DB_FILEPATH, 'wb') as f:
                pickle.dump(self, f)

    def get_passwords(self) -> list:
        """读取密码本，提取排序后的密码"""
        pws = self.keys()
        # 按密码使用次数、最后使用时间降序排序"""
        pws_sorted = sorted(pws, key=lambda x: (self[x].get_use_count(), self[x].get_last_use_time()), reverse=True)
        return pws_sorted

    def add_password(self, password: str):
        """添加单个密码"""
        if password not in self:
            self[password] = Password(password)
        else:
            pw_class: Password = self[password]
            pw_class.update_use_time()
        self.save()

    def add_passwords(self, passwords: list):
        """添加多个密码"""
        for pw in passwords:
            if pw not in self:
                self[pw] = Password(pw)
            else:
                pw_class: Password = self[pw]
                pw_class.update_use_time()
        self.save()

    def output_db(self):
        """导出密码本"""
        pws = self.get_passwords()
        with open(_OUTPUT_FILE, 'w', encoding='utf-8') as ow:
            ow.write('\n'.join(pws))

    @staticmethod
    def open_output_file():
        """打开导出的密码本"""
        os.startfile(_OUTPUT_FILE)

    def update_use_count(self, password: str):
        """更新单个密码使用次数"""
        if password not in self:
            self.add_password(password)
        pw_class: Password = self[password]
        pw_class.update_use_count()
        self.save()

    def save(self):
        """保存"""
        with open(DB_FILEPATH, 'wb') as f:
            pickle.dump(self, f)


class Password(dict):
    """单个密码类"""

    def __init__(self, password: str):
        super().__init__(self)
        self['password'] = str(password)  # 密码
        self['add_time'] = time.time()  # 添加时间
        self['last_use_time'] = time.time()  # 最后使用时间
        self['use_count'] = 0  # 使用次数

    def get_password(self) -> str:
        """获取密码"""
        return self['password']

    def get_add_time(self) -> float:
        """获取添加时间"""
        return self['add_time']

    def get_last_use_time(self) -> float:
        """获取最后使用时间"""
        return self['last_use_time']

    def get_use_count(self) -> int:
        """获取使用次数"""
        return self['use_count']

    def update_use_count(self):
        """更新使用次数"""
        self['use_count'] += 1
        self['last_use_time'] = time.time()

    def update_use_time(self):
        """更新最后使用时间"""
        self['last_use_time'] = time.time()
