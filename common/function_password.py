import os
import shutil

import lzytools.common
import lzytools.file

BACKUP_PATH = 'backup'


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


def delete_backup_over_limit(limit: int = 10):
    backup_files = sorted(get_backup_files(), reverse=True)
    count = len(backup_files)
    if count > limit:
        delete_files = backup_files[limit:]
        for file in delete_files:
            os.remove(file)


def check_backup_file_exists():
    if not os.path.exists(BACKUP_PATH):
        os.mkdir(BACKUP_PATH)
