# 压缩文件拆分类
import os
from typing import Tuple, Dict

import lzytools

from common.class_7zip import ArchiveRole, TYPES_ARCHIVE_ROLE


class ArchiveSpliter:
    """压缩文件拆分类 普通压缩文件/分卷压缩文件"""

    def __init__(self):
        self.archives = []  # 压缩文件列表（如果是分卷压缩文件，则仅包含首个分卷包）
        self._archive_members: Dict[str, list] = dict()  # 压缩文件成员字典，格式为{首个文件:[该组的所有文件], ...}
        self._archive_roles: Dict[str, TYPES_ARCHIVE_ROLE] = dict()  # 压缩文件角色字典，格式为{文件路径:压缩文件角色类, ...}

    def analyse_files(self, files: list):
        """处理文件列表
        :param files: 需要拆分的文件列表"""
        # 重置
        self.archives = []
        self._archive_members = dict()
        # 先拆分为普通压缩文件和分卷压缩文件
        normal_archives, volume_archives = self._split(files)
        print('普通压缩文件和分卷压缩文件', normal_archives, volume_archives)
        # 普通压缩文件写入对象
        for archive in normal_archives:
            self.archives.append(archive)
            self._archive_members[archive] = [archive]
            self._archive_roles[archive] = ArchiveRole.Normal()
        # 进一步处理分卷压缩文件
        first_volume_archives, volume_members = self._analyse_volume_archive(volume_archives)
        # 分卷压缩文件写入对象
        for i in first_volume_archives:
            if i not in self.archives:
                self.archives.append(i)
                self._archive_members[i] = volume_members[i]
            else:
                self._archive_members[i].extend(volume_members[i])
            self._archive_roles[i] = ArchiveRole.VolumeFirst()
        for i in volume_members:
            if i not in self._archive_roles:
                self._archive_roles[i] = ArchiveRole.VolumeMember()

    def is_has_archives(self) -> bool:
        """判断是否存在压缩文件"""
        return len(self.archives) > 0

    def get_role(self, filepath: str):
        """获取文件路径对应的压缩文件角色"""
        return self._archive_roles[filepath]

    def get_files(self):
        """获取文件列表（每组的首个文件）"""
        return self.archives.copy()

    def get_members(self, filepath: str):
        """获取文件路径对应的压缩文件成员列表"""
        return self._archive_members[filepath].copy()

    @staticmethod
    def _split(files) -> Tuple[list, list]:
        """"按类型拆分压缩文件
        :return: 普通压缩文件列表，分卷压缩文件列表"""
        volume_archives = []
        normal_archives = []
        for file in files:
            if lzytools.archive.is_volume_archive_by_filename(os.path.basename(file)):
                volume_archives.append(file)
            else:
                normal_archives.append(file)
        return normal_archives, volume_archives

    @staticmethod
    def _analyse_volume_archive(volume_archives: list) -> Tuple[list, dict]:
        """"进一步处理分卷压缩文件
        :return: 首个分卷包列表，分卷包成员字典（格式为{首个文件:[该组的所有文件], ...}）"""
        parent_dirpaths = set()  # 父目录集合，用于后续补充缺失的分卷包
        first_volumes = []  # 各个分卷组的首个分卷包列表
        members = {}  # 分卷成员字典，格式为{首个文件:[该组的所有文件], ...}
        # 合并同一组分卷
        for file in volume_archives:
            # 生成对应的虚拟的首个压缩卷路径，并作为匹配的key
            virtual_first_volume_filename = lzytools.archive.guess_first_volume_archive_filename(file)
            virtual_first_volume_path = os.path.normpath(
                os.path.join(os.path.dirname(file), virtual_first_volume_filename))
            if virtual_first_volume_path not in first_volumes:
                first_volumes.append(virtual_first_volume_path)
                members[virtual_first_volume_path] = []
            members[virtual_first_volume_path].append(file)
            parent_dirpaths.add(os.path.dirname(file))

        # 补充缺失的分卷包
        for dirpath in parent_dirpaths:
            listdir = [os.path.normpath(os.path.join(dirpath, i)) for i in os.listdir(dirpath)]
            for path in listdir:
                virtual_first_volume_filename = lzytools.archive.guess_first_volume_archive_filename(path)
                if virtual_first_volume_filename:
                    virtual_first_volume_path = os.path.normpath(os.path.join(dirpath, virtual_first_volume_filename))
                    if virtual_first_volume_path in first_volumes and path not in members[virtual_first_volume_path]:
                        members[virtual_first_volume_path].append(path)

        return first_volumes, members
