"""密码本数据的读写与管理。"""

import configparser
import os
import pickle
import shutil
import time

import lzytools

BACKUP_PATH = 'backup'
DB_FILEPATH = 'password.pkl'
_OUTPUT_FILE = 'password_output.txt'
SECONDS_PER_DAY = 86400
BACKUP_TIME_FORMAT = '%Y-%m-%d_%H.%M.%S'


class Password(dict):
    """单个密码记录。继承 dict 是为了兼容旧版本序列化的数据。"""

    def __init__(self, password: str):
        super().__init__()
        now = time.time()
        self['password'] = str(password)  # 密码
        self['add_time'] = now  # 添加时间
        self['last_use_time'] = now  # 最后使用时间
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

    def add_use_count_once(self):
        """增加一次使用次数，并更新最后使用时间"""
        self['use_count'] += 1
        self['last_use_time'] = time.time()

    def update_use_time(self):
        """更新最后使用时间"""
        self['last_use_time'] = time.time()


class DBPassword(dict):
    """密码本类：键为密码文本，值为对应的 Password 对象。继承 dict 是为了兼容旧版本数据。"""

    def __init__(self):
        super().__init__()
        if not os.path.exists(DB_FILEPATH):
            self.save()

    def _touch_password(self, password: str):
        """添加密码；若已存在则只更新最后使用时间。"""
        if password in self:
            self[password].update_use_time()
        else:
            self[password] = Password(password)

    def _filter_by_days(self, get_time, day_interval: int, is_inside: bool):
        """按指定时间与当天的间隔天数筛选密码，返回密码列表。"""
        now = time.time()
        result = []
        for password, info in self.items():
            diff_day = int((now - get_time(info)) // SECONDS_PER_DAY)
            if is_inside:
                matched = diff_day <= day_interval
            else:
                matched = diff_day >= day_interval
            if matched:
                result.append(password)
        return result

    def get_passwords(self) -> list:
        """按使用次数、最后使用时间降序返回所有密码。"""
        return sorted(
            self.keys(),
            key=lambda password: (
                self[password].get_use_count(),
                self[password].get_last_use_time(),
            ),
            reverse=True,
        )

    def get_passwords_class(self):
        """获取密码本中所有的 Password 对象。"""
        return self.values()

    def get_passwords_count(self) -> int:
        """获取密码本的密码数量。"""
        return len(self)

    def get_last_update_time(self) -> float:
        """获取最近一次使用时间；密码本为空时返回 0。"""
        if not self:
            return 0
        return max(info.get_last_use_time() for info in self.values())

    def delete_passwords(self, delete_passwords: list):
        """删除指定密码，删除前先备份密码本。"""
        backup_file(DB_FILEPATH)
        for password in delete_passwords:
            if password in self:
                del self[password]
        self.save()

    def add_password(self, password: str):
        """添加单个密码。"""
        self._touch_password(password)
        self.save()

    def add_passwords(self, passwords: list):
        """添加多个密码。"""
        for password in passwords:
            self._touch_password(password)
        self.save()

    def add_use_count_once(self, password: str):
        """增加一次密码的使用次数。"""
        self._touch_password(password)
        self[password].add_use_count_once()
        self.save()

    def filter_use_count(self, min_use_count: int, max_use_count: int) -> list:
        """筛选使用次数在指定范围内（包含边界）的密码。"""
        result = []
        for password, info in self.items():
            use_count = info.get_use_count()
            if min_use_count <= use_count <= max_use_count:
                result.append(password)
        return result

    def filter_add_time(self, day_interval: int, is_inside: bool = True) -> list:
        """按首次添加时间与当天的间隔天数筛选密码。"""
        return self._filter_by_days(
            lambda info: info.get_add_time(), day_interval, is_inside
        )

    def filter_last_use_time(self, day_interval: int, is_inside: bool = True) -> list:
        """按最后使用时间与当天的间隔天数筛选密码。"""
        return self._filter_by_days(
            lambda info: info.get_last_use_time(), day_interval, is_inside
        )

    def output_db(self):
        """导出密码本。"""
        with open(_OUTPUT_FILE, 'w', encoding='utf-8') as output_file:
            output_file.write('\n'.join(self.get_passwords()))

    @staticmethod
    def open_output_file():
        """打开导出的密码本。"""
        os.startfile(_OUTPUT_FILE)

    def save(self):
        """保存密码本。"""
        with open(DB_FILEPATH, 'wb') as file:
            pickle.dump(self, file)


def read_db(db_file: str = DB_FILEPATH):
    """读取密码本，文件不存在时创建空密码本。"""
    if os.path.exists(db_file):
        with open(db_file, 'rb') as file:
            return pickle.load(file)
    return DBPassword()


def backup_file(file_path: str):
    """备份密码文件，并清理超出数量限制的旧备份。"""
    check_backup_file_exists()

    filename = os.path.basename(file_path)
    name, extension = os.path.splitext(filename)
    timestamp = lzytools.time.get_current_time(BACKUP_TIME_FORMAT)
    new_filename = f'{name}_{timestamp}{extension}'
    new_path = os.path.join(BACKUP_PATH, new_filename)
    shutil.copy2(file_path, new_path)

    delete_backup_over_limit()


def get_backup_files() -> list:
    """获取所有备份文件的路径。"""
    return lzytools.file.get_files_in_paths([BACKUP_PATH])


def delete_backup_over_limit(limit: int = 20):
    """删除超出数量限制的备份文件（备份文件名含时间，倒序排列即新文件在前）。"""
    backup_files = sorted(get_backup_files(), reverse=True)
    for file in backup_files[limit:]:
        os.remove(file)


def check_backup_file_exists():
    """确保备份文件夹存在。"""
    os.makedirs(BACKUP_PATH, exist_ok=True)


def read_passwords_from_files(files) -> list:
    """从文件中提取密码，依次尝试 pickle、ini、txt 三种格式。"""
    readers = [
        _read_passwords_from_pickle,
        _read_passwords_from_ini,
        _read_passwords_from_txt,
    ]

    passwords = []
    for file in files:
        if not os.path.isfile(file):
            continue
        for read_passwords in readers:
            try:
                passwords.extend(read_passwords(file))
                break
            except Exception:
                # 当前格式读取失败，尝试下一种格式
                continue

    return lzytools.common.dedup_list(passwords)


def _read_passwords_from_txt(txt_file: str) -> list:
    """从 txt 文件中读取密码，每行视为一个密码。"""
    with open(txt_file, 'r', encoding='utf-8') as file:
        return file.readlines()


def _read_passwords_from_pickle(pickle_file: str) -> list:
    """从 pickle 文件中读取密码，兼容新旧版本的密码本格式。"""
    with open(pickle_file, 'rb') as file:
        data = pickle.load(file)

    # v2.0.0 版本的密码本格式（DBPassword 类）
    if isinstance(data, DBPassword):
        return data.get_passwords()
    # v1.3.0~1.6.1 版本的密码本格式（dict 类）
    if isinstance(data, dict):
        return list(data.keys())
    return []


def _read_passwords_from_ini(ini_file: str) -> list:
    """从 ini 文件中读取密码"""
    config = configparser.ConfigParser()
    config.read(ini_file, encoding='utf-8')
    sections = config.sections()
    if not sections:
        raise ValueError('ini 文件中没有配置节')
    return sections
