# 文件信息类
from typing import Tuple

from common.class_7zip import ArchiveRole, Result7zip



class FileInfo:
    """单个文件信息类"""

    def __init__(self, filepath: str,
                 file_role: Tuple[ArchiveRole.Normal, ArchiveRole.VolumeFirst, ArchiveRole.VolumeMember],
                 related_files=None):
        # 一般属性
        self.filepath = filepath  # 文件路径
        self.file_role: Tuple[
            ArchiveRole.Normal, ArchiveRole.VolumeFirst, ArchiveRole.VolumeMember] = file_role  # 该文件的角色，是首个分卷包还是内部分卷，处理时仅处理首个分卷包角色
        self.related_files = related_files  # 文件角色为普通或首个分卷包时使用，同一组内的其他分卷文件（包含其自身）

        # 非分卷成员角色强制输入关联文件
        if file_role is not ArchiveRole.VolumeMember and not related_files:
            raise Exception('文件信息类初始化错误，分卷压缩包未输入关联文件')

        # 调用7zip后设置的属性
        self._7zip_result: Result7zip = None  # 7zip测试/解压解压结果
        self.password = None  # 文件密码
        self.extract_path = None  # 仅在解压模式且成功解压时使用，解压结果的路径

    def set_7zip_result(self, result: Result7zip):
        """设置7zip测试/解压解压结果"""
        self._7zip_result = result

    def get_7zip_result(self)->Result7zip:
        """获取7zip测试/解压解压结果"""
        return self._7zip_result
    def set_password(self, password: str):
        """设置文件密码"""
        self.password = password

    def set_extract_path(self, path: str):
        """设置解压结果的路径"""
        self.extract_path = path

    def print_info(self):
        """打印内部信息"""
        info_dict = {'filepath': self.filepath,
                     'file_role': self.file_role,
                     'related_files': self.related_files,
                     '7zip_result': self._7zip_result,
                     'password': self.password,
                     'extract_path': self.extract_path
                     }


class FileInfoList:
    """文件信息类列表"""

    def __init__(self):
        self.files_info = dict()  # 归集字典

    def add_file(self, filepath: str,
                 file_role: Tuple[ArchiveRole.Normal, ArchiveRole.VolumeFirst, ArchiveRole.VolumeMember],
                 related_files=None):
        file_info = FileInfo(filepath, file_role, related_files)
        self.files_info[filepath] = file_info

    def count(self)->int:
        """统计个数"""
        return len(self.files_info)

    def get_file_infos(self)->list[FileInfo]:
        """获取文件信息类列表"""
        return list(self.files_info.values())

    def get_success_files(self):
        """获取处理成功的文件的路径"""
        # 如果是解压模式，则为解压后的路径
        success = []
        for file_info in self.get_file_infos():
            result = file_info.get_7zip_result()
            if result and isinstance(result, Result7zip.Success):
                extract_path = file_info.extract_path
                if extract_path:
                    success.append(extract_path)

        return success



    def count_success(self):
        """统计处理成功的个数"""
        count = 0
        for file_info in self.get_file_infos():
            result  = file_info.get_7zip_result()
            if result and isinstance(result, Result7zip.Success):
                count += 1
        return count