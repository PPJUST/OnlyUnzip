# ?????
from common.class_7zip import ArchiveRole, Result7zip, TYPES_ARCHIVE_ROLE, TYPES_RESULT_7ZIP


class FileInfo:
    """???????"""

    def __init__(self, filepath: str,
                 file_role: TYPES_ARCHIVE_ROLE,
                 related_files: list = None):
        # ????
        self.filepath = filepath  # ????
        self.file_role: TYPES_ARCHIVE_ROLE = file_role  # ??????,????????????,?????????????
        self.related_files = related_files  # ????????????????,???????????(?????)

        # ???????????????
        if file_role is not ArchiveRole.VolumeMember and not related_files:
            raise Exception('??????????,????????????')

        # ??7zip??????
        self._7zip_result: TYPES_RESULT_7ZIP = None  # 7zip??/??????
        self.password = None  # ????
        self.extract_path = None  # ??????????????,???????

    def set_7zip_result(self, result: TYPES_RESULT_7ZIP):
        """??7zip??/??????"""
        self._7zip_result = result

    def get_7zip_result(self) -> TYPES_RESULT_7ZIP:
        """??7zip??/??????"""
        return self._7zip_result

    def set_password(self, password: str):
        """??????"""
        self.password = password

    def set_extract_path(self, path: str):
        """?????????"""
        self.extract_path = path

    def print_info(self):
        """??????"""
        info_dict = {'filepath': self.filepath,
                     'file_role': self.file_role,
                     'related_files': self.related_files,
                     '7zip_result': self._7zip_result,
                     'password': self.password,
                     'extract_path': self.extract_path
                     }
        print(info_dict)


class FileInfoList:
    """???????"""

    def __init__(self):
        self.files_info = dict()  # ????

    def add_file(self, filepath: str,
                 file_role: TYPES_ARCHIVE_ROLE,
                 related_files=None):
        file_info = FileInfo(filepath, file_role, related_files)
        self.files_info[filepath] = file_info

    def count(self) -> int:
        """????"""
        return len(self.files_info)

    def get_file_info(self, filepath: str) -> FileInfo:
        """??????????"""
        return self.files_info[filepath]

    def get_file_infos(self) -> list[FileInfo]:
        """?????????"""
        return list(self.files_info.values())

    def get_success_files(self):
        """????????????"""
        # ???????,????????
        success = []
        for file_info in self.get_file_infos():
            result = file_info.get_7zip_result()
            if result and isinstance(result, Result7zip.Success):
                extract_path = file_info.extract_path
                if extract_path:
                    success.append(extract_path)

        return success

    def get_success_passwords(self):
        """?????????"""
        passwords = []
        for file_info in self.get_file_infos():
            result = file_info.get_7zip_result()
            if result and isinstance(result, Result7zip.Success):
                passwords.append(file_info.password)
        return passwords

    def count_success(self):
        """?????????"""
        count = 0
        for file_info in self.get_file_infos():
            result = file_info.get_7zip_result()
            if result and isinstance(result, Result7zip.Success):
                count += 1
        return count

    def is_user_stop(self):
        """????????"""
        for file_info in self.get_file_infos():
            result = file_info.get_7zip_result()
            if result and isinstance(result, Result7zip.UserStopped):
                return True
        return False
