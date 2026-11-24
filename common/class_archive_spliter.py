# 压缩文件拆分类
import os
from typing import Optional

import lzytools_archive

from common.class_7zip import ArchiveRole, TYPES_ARCHIVE_ROLE


class ArchiveSpliter:
    """压缩文件拆分类，处理普通压缩文件和分卷压缩文件。"""

    def __init__(self):
        # 需要处理的压缩文件列表，分卷压缩文件只保留首个分卷
        self.archives: list[str] = []
        # 文件格式：{文件: [该文件所在分组的所有文件]}
        self._archive_members: dict[str, list[str]] = {}
        # 文件格式：{文件: 压缩文件角色}
        self._archive_roles: dict[str, TYPES_ARCHIVE_ROLE] = {}

    def analyse_files(self, files: list[str]):
        """分析文件列表，每次调用都会清空上一次的分析结果。"""
        self._reset_result()

        normal_archives, volume_archives = self._split_archives(files)
        first_volumes, volume_members = self._analyse_volume_archives(volume_archives)

        self._add_normal_archives(normal_archives)
        self._add_volume_archives(first_volumes, volume_members)
        self._add_volume_member_roles(volume_members)

    def is_has_archives(self) -> bool:
        """判断是否存在需要处理的压缩文件。"""
        return len(self.archives) > 0

    def get_role(self, filepath: str) -> TYPES_ARCHIVE_ROLE:
        """获取文件路径对应的压缩文件角色。"""
        return self._archive_roles[filepath]

    def get_files(self) -> list[str]:
        """获取文件列表，分卷压缩文件只返回首个分卷。"""
        return self.archives.copy()

    def get_members(self, filepath: str) -> list[str]:
        """获取文件路径对应的压缩文件成员列表。"""
        return self._archive_members[filepath].copy()

    def _reset_result(self):
        """清空上一次的分析结果。"""
        self.archives = []
        self._archive_members = {}
        self._archive_roles = {}

    def _add_normal_archives(self, normal_archives: list[str]):
        """添加普通压缩文件。"""
        for archive in normal_archives:
            self._add_archive(archive, [archive])
            self._archive_roles[archive] = ArchiveRole.Normal()

    def _add_volume_archives(self, first_volumes: list[str], volume_members: dict[str, list[str]]):
        """添加分卷压缩文件，首个分卷作为待处理文件。"""
        for first_volume in first_volumes:
            members = volume_members[first_volume]
            if first_volume in self._archive_members:
                self._merge_members(first_volume, members)
            else:
                self._add_archive(first_volume, members)
            self._archive_roles[first_volume] = ArchiveRole.VolumeFirst()

    def _add_volume_member_roles(self, volume_members: dict[str, list[str]]):
        """为非首个分卷设置角色。"""
        for filepath in volume_members:
            if filepath not in self._archive_roles:
                self._archive_roles[filepath] = ArchiveRole.VolumeMember()

    def _add_archive(self, filepath: str, members: list[str]):
        """添加一个待处理文件及其分组文件。"""
        if filepath not in self.archives:
            self.archives.append(filepath)
        self._archive_members[filepath] = members.copy()

    def _merge_members(self, filepath: str, members: list[str]):
        """向已有分组中追加文件，并保持文件不重复。"""
        for member in members:
            self._append_unique(self._archive_members[filepath], member)

    @staticmethod
    def _split_archives(files: list[str]) -> tuple[list[str], list[str]]:
        """按文件名拆分普通压缩文件和分卷压缩文件。"""
        normal_archives: list[str] = []
        volume_archives: list[str] = []

        for file in files:
            filename = os.path.basename(file)
            if lzytools_archive.is_volume_archive_by_filename(filename):
                volume_archives.append(file)
            else:
                normal_archives.append(file)

        return normal_archives, volume_archives

    @staticmethod
    def _analyse_volume_archives(volume_archives: list[str]) -> tuple[list[str], dict[str, list[str]]]:
        """合并同一组分卷，并补充该组中缺失的分卷文件。"""
        first_volumes: list[str] = []
        members: dict[str, list[str]] = {}
        parent_dirpaths: list[str] = []

        for file in volume_archives:
            first_volume_path = ArchiveSpliter._get_first_volume_path(file)
            if first_volume_path is None:
                continue

            if first_volume_path not in first_volumes:
                first_volumes.append(first_volume_path)
                members[first_volume_path] = []
            ArchiveSpliter._append_unique(members[first_volume_path], file)

            dirpath = os.path.dirname(file)
            if dirpath not in parent_dirpaths:
                parent_dirpaths.append(dirpath)

        for dirpath in parent_dirpaths:
            ArchiveSpliter._append_missing_volume_members(dirpath, first_volumes, members)

        return first_volumes, members

    @staticmethod
    def _get_first_volume_path(file: str) -> Optional[str]:
        """获取文件对应的首个分卷路径，无法推断时返回 None。"""
        filename = lzytools_archive.guess_first_volume_archive_filename(os.path.basename(file))
        if not filename:
            return None

        dirpath = os.path.dirname(file)
        return os.path.normpath(os.path.join(dirpath, filename))

    @staticmethod
    def _append_missing_volume_members(dirpath: str, first_volumes: list[str],
                                       members: dict[str, list[str]]):
        """从目录中补充缺失的分卷文件。"""
        if not os.path.isdir(dirpath):
            return

        for filename in sorted(os.listdir(dirpath)):
            path = os.path.normpath(os.path.join(dirpath, filename))
            if not os.path.isfile(path):
                continue

            first_volume_path = ArchiveSpliter._get_first_volume_path(path)
            if first_volume_path in first_volumes:
                ArchiveSpliter._append_unique(members[first_volume_path], path)

    @staticmethod
    def _append_unique(items: list[str], item: str):
        """向列表中追加元素，元素已存在时不重复追加。"""
        if item not in items:
            items.append(item)
