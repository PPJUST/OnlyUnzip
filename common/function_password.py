import configparser
import os
import pickle
import shutil
import time

import lzytools.common
import lzytools.file

BACKUP_PATH = 'backup'

DB_FILEPATH = 'password.pkl'
_OUTPUT_FILE = 'password_output.txt'


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
        # 按密码使用次数、最后使用时间降序排序
        pws_sorted = sorted(pws, key=lambda x: (self[x].get_use_count(), self[x].get_last_use_time()), reverse=True)
        return pws_sorted

    def delete_passwords(self, delete_passwords: list):
        """删除指定密码"""
        backup_file(DB_FILEPATH)  # 删除前备份密码

        for pw in delete_passwords:
            if pw in self:
                del self[pw]
        self.save()

    def get_passwords_count(self):
        """获取密码本的密码数量"""
        return len(self)

    def get_last_update_time(self):
        """获取密码本最后的更新时间"""
        pws = self.keys()
        pws_sorted = sorted(pws, key=lambda x: (self[x].get_last_use_time()), reverse=True)
        last_update_time = self[pws_sorted[0]].get_last_use_time()
        return last_update_time

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

    def add_use_count_once(self, password: str):
        """增加一次密码的使用次数"""
        if password not in self:
            self.add_password(password)
        pw_class: Password = self[password]
        pw_class.add_use_count_once()
        self.save()

    def filter_use_count(self, min_use_count: int, max_use_count: int):
        """过滤密码本，只保留使用次数在指定范围内（包含本数）的密码"""
        pws_filter = []
        for pw in self.keys():
            use_count = self[pw].get_use_count()
            if min_use_count <= use_count <= max_use_count:
                pws_filter.append(pw)

        return pws_filter

    def filter_add_time(self, day_interval: int, is_inside: bool = True):
        """过滤密码本，只保留首次添加时间在指定天数范围内（包含本数）的密码（以当日为基数）
        :param day_interval: 天数间隔
        :param is_inside: 筛选天数间隔内，否则删除天数间隔外"""
        now = time.time()
        pws_filter = []
        for pw in self.keys():
            add_time = self[pw].get_add_time()
            diff_sec = now - add_time
            diff_day = int(diff_sec // 86400)
            if is_inside:
                if diff_day <= day_interval:
                    pws_filter.append(pw)
            else:
                if diff_day >= day_interval:
                    pws_filter.append(pw)

        return pws_filter

    def filter_last_use_time(self, day_interval: int, is_inside: bool = True):
        """过滤密码本，只保留最后使用时间在指定天数范围内（包含本数）的密码（以当日为基数）
        :param day_interval: 天数间隔
        :param is_inside: 筛选天数间隔内，否则删除天数间隔外"""
        now = time.time()
        pws_filter = []
        for pw in self.keys():
            last_use_time = self[pw].get_last_use_time()
            diff_sec = now - last_use_time
            diff_day = int(diff_sec // 86400)
            if is_inside:
                if diff_day <= day_interval:
                    pws_filter.append(pw)
            else:
                if diff_day >= day_interval:
                    pws_filter.append(pw)

        return pws_filter

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

    def add_use_count_once(self):
        """增加一次密码的使用次数"""
        self['use_count'] += 1
        self['last_use_time'] = time.time()

    def update_use_time(self):
        """更新最后使用时间"""
        self['last_use_time'] = time.time()


def read_db(db_file: str = DB_FILEPATH):
    """读取密码本"""
    if os.path.exists(db_file):
        with open(db_file, 'rb') as f:
            return pickle.load(f)
    else:
        return DBPassword()


def backup_file(file_path: str):
    """备份密码文件"""
    check_backup_file_exists()
    filename = os.path.basename(file_path)
    filetitle, extension = os.path.splitext(filename)
    part_time = lzytools.common.get_current_time('%Y-%m-%d_%H.%M.%S')
    new_filename = filetitle + '_' + part_time + extension
    new_path = os.path.join(BACKUP_PATH, new_filename)
    shutil.copy2(file_path, new_path)
    # 检查备份文件数量，如果超限则删除最旧的
    delete_backup_over_limit()


def get_backup_files():
    """获取所有备份文件的路径"""
    return lzytools.file.get_files_in_paths([BACKUP_PATH])


def delete_backup_over_limit(limit: int = 20):
    """删除超出数量限制的备份文件（先删除创建时间更早的）"""
    backup_files = sorted(get_backup_files(), reverse=True)
    count = len(backup_files)
    if count > limit:
        delete_files = backup_files[limit:]
        for file in delete_files:
            os.remove(file)


def check_backup_file_exists():
    """检查备份文件夹是否存在"""
    if not os.path.exists(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)


def read_passwords_from_files(files):
    """从文件中提取密码"""
    # 提取文件
    files = [i for i in files if os.path.isfile(i)]
    # 尝试读取密码
    pws = []
    for file in files:
        try:  # 尝试按pickle文件读取
            pws += _read_passwords_from_pickle(file)
        except:
            try:  # 尝试按ini文件读取
                pws += _read_passwords_from_ini(file)
            except:
                try:  # 尝试按txt文件读取
                    pws += _read_passwords_from_txt(file)
                except:
                    pass

    lzytools.common.dedup_list(pws)
    return pws


def _read_passwords_from_txt(txt_file: str) -> list:
    """从txt文件中读取密码"""
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return lines


def _read_passwords_from_pickle(pickle_file: str):
    """从pickle文件中读取密码"""
    try:
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
            # v2.0.0版本的密码本格式（DBPassword类）
            if isinstance(data, DBPassword):
                pws = data.get_passwords()
                return pws
            # v1.3.0~1.6.1版本的密码本格式（Dict类）
            if isinstance(data, dict):
                pws = list(data.keys())
                return pws
        return []
    except:
        return []


def _read_passwords_from_ini(ini_file: str):
    """从ini文件中读取密码"""
    # v1.0.0~1.2.2版本的密码本格式（ini格式）
    try:
        config = configparser.ConfigParser()
        config.read(ini_file, encoding='utf-8')  # 配置文件的路径
        sections = config.sections()
        if sections:
            return sections
        return []
    except:
        return []
