import configparser
import os
import pickle
import shutil
import time
from typing import List

import lzytools

BACKUP_PATH = 'backup'

DB_FILEPATH = 'password.pkl'
_OUTPUT_FILE = 'password_output.txt'


class DBPassword(dict):
    """????
    ??password??,?????Password???"""

    def __init__(self):
        super().__init__(self)
        if not os.path.exists(DB_FILEPATH):
            with open(DB_FILEPATH, 'wb') as f:
                pickle.dump(self, f)

    def get_passwords(self) -> list:
        """?????,????????"""
        pws = self.keys()
        # ??????????????????
        pws_sorted = sorted(pws, key=lambda x: (self[x].get_use_count(), self[x].get_last_use_time()), reverse=True)
        return pws_sorted

    def get_passwords_class(self):
        """????????????"""
        values = self.values()
        values: List[Password]
        return values

    def delete_passwords(self, delete_passwords: list):
        """??????"""
        backup_file(DB_FILEPATH)  # ???????

        for pw in delete_passwords:
            if pw in self:
                del self[pw]
        self.save()

    def get_passwords_count(self):
        """??????????"""
        return len(self)

    def get_last_update_time(self):
        """????????????"""
        pws = self.keys()
        pws_sorted = sorted(pws, key=lambda x: (self[x].get_last_use_time()), reverse=True)
        last_update_time = self[pws_sorted[0]].get_last_use_time()
        return last_update_time

    def add_password(self, password: str):
        """??????"""
        if password not in self:
            self[password] = Password(password)
        else:
            pw_class: Password = self[password]
            pw_class.update_use_time()
        self.save()

    def add_passwords(self, passwords: list):
        """??????"""
        for pw in passwords:
            if pw not in self:
                self[pw] = Password(pw)
            else:
                pw_class: Password = self[pw]
                pw_class.update_use_time()
        self.save()

    def output_db(self):
        """?????"""
        pws = self.get_passwords()
        with open(_OUTPUT_FILE, 'w', encoding='utf-8') as ow:
            ow.write('\n'.join(pws))

    @staticmethod
    def open_output_file():
        """????????"""
        os.startfile(_OUTPUT_FILE)

    def add_use_count_once(self, password: str):
        """???????????"""
        if password not in self:
            self.add_password(password)
        pw_class: Password = self[password]
        pw_class.add_use_count_once()
        self.save()

    def filter_use_count(self, min_use_count: int, max_use_count: int):
        """?????,?????????????(????)???"""
        pws_filter = []
        for pw in self.keys():
            use_count = self[pw].get_use_count()
            if min_use_count <= use_count <= max_use_count:
                pws_filter.append(pw)

        return pws_filter

    def filter_add_time(self, day_interval: int, is_inside: bool = True):
        """?????,?????????????????(????)???(??????)
        :param day_interval: ????
        :param is_inside: ???????,?????????"""
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
        """?????,?????????????????(????)???(??????)
        :param day_interval: ????
        :param is_inside: ???????,?????????"""
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
        """??"""
        with open(DB_FILEPATH, 'wb') as f:
            pickle.dump(self, f)


class Password(dict):
    """?????"""

    def __init__(self, password: str):
        super().__init__(self)
        self['password'] = str(password)  # ??
        self['add_time'] = time.time()  # ????
        self['last_use_time'] = time.time()  # ??????
        self['use_count'] = 0  # ????

    def get_password(self) -> str:
        """????"""
        return self['password']

    def get_add_time(self) -> float:
        """??????"""
        return self['add_time']

    def get_last_use_time(self) -> float:
        """????????"""
        return self['last_use_time']

    def get_use_count(self) -> int:
        """??????"""
        return self['use_count']

    def add_use_count_once(self):
        """???????????"""
        self['use_count'] += 1
        self['last_use_time'] = time.time()

    def update_use_time(self):
        """????????"""
        self['last_use_time'] = time.time()


def read_db(db_file: str = DB_FILEPATH):
    """?????"""
    if os.path.exists(db_file):
        with open(db_file, 'rb') as f:
            return pickle.load(f)
    else:
        return DBPassword()


def backup_file(file_path: str):
    """??????"""
    check_backup_file_exists()
    filename = os.path.basename(file_path)
    filetitle, extension = os.path.splitext(filename)
    part_time = lzytools.time.get_current_time('%Y-%m-%d_%H.%M.%S')
    new_filename = filetitle + '_' + part_time + extension
    new_path = os.path.join(BACKUP_PATH, new_filename)
    shutil.copy2(file_path, new_path)
    # ????????,??????????
    delete_backup_over_limit()


def get_backup_files():
    """???????????"""
    return lzytools.file.get_files_in_paths([BACKUP_PATH])


def delete_backup_over_limit(limit: int = 20):
    """?????????????(??????????)"""
    backup_files = sorted(get_backup_files(), reverse=True)
    count = len(backup_files)
    if count > limit:
        delete_files = backup_files[limit:]
        for file in delete_files:
            os.remove(file)


def check_backup_file_exists():
    """???????????"""
    if not os.path.exists(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)


def read_passwords_from_files(files):
    """????????"""
    # ????
    files = [i for i in files if os.path.isfile(i)]
    # ??????
    pws = []
    for file in files:
        try:  # ???pickle????
            pws += _read_passwords_from_pickle(file)
        except:
            try:  # ???ini????
                pws += _read_passwords_from_ini(file)
            except:
                try:  # ???txt????
                    pws += _read_passwords_from_txt(file)
                except:
                    pass

    lzytools.common.dedup_list(pws)
    return pws


def _read_passwords_from_txt(txt_file: str) -> list:
    """?txt???????"""
    with open(txt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    return lines


def _read_passwords_from_pickle(pickle_file: str):
    """?pickle???????"""
    try:
        with open(pickle_file, 'rb') as f:
            data = pickle.load(f)
            # v2.0.0????????(DBPassword?)
            if isinstance(data, DBPassword):
                pws = data.get_passwords()
                return pws
            # v1.3.0~1.6.1????????(Dict?)
            if isinstance(data, dict):
                pws = list(data.keys())
                return pws
        return []
    except:
        return []


def _read_passwords_from_ini(ini_file: str):
    """?ini???????"""
    # v1.0.0~1.2.2????????(ini??)
    try:
        config = configparser.ConfigParser()
        config.read(ini_file, encoding='utf-8')  # ???????
        sections = config.sections()
        if sections:
            return sections
        return []
    except:
        return []


def auto_import_passwords_if_empty():
    """v2.2.1:????????????,?????????password_output.txt"""
    db = read_db()
    pws = db.get_passwords()
    if len(pws) == 0 and os.path.exists(_OUTPUT_FILE):
        try:
            imported_pws = read_passwords_from_files([_OUTPUT_FILE])
            if imported_pws:
                db.add_passwords(imported_pws)
                print(f'??????????:{len(imported_pws)}?')
                return True
        except Exception as e:
            print(f'????????:{e}')
    return False
