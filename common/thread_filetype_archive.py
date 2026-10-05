# 检查文件类型是否是压缩文件的子线程
import os

import lzytools_archive
from PySide6.QtCore import QThread, Signal


class ThreadFiletypeArchive(QThread):
    """检查文件类型是否是压缩文件的子线程"""
    Archives = Signal(list, name='压缩文件列表')

    def __init__(self, ):
        super().__init__()
        self.files = []  # 需要检查的文件列表

    def set_files(self, files: list):
        self.files = files

    def run(self):
        archive_files = []
        for file in self.files:
            if not is_exclude_file_extension(file):
                # v2.2.1：先尝试智能后缀修复，确保后缀正确后再识别
                # 即使文件头能识别为压缩文件，如果后缀异常（如 .rar删除），也需要先修正
                current_file = try_fix_archive_extension(file) or file

                if lzytools_archive.is_archive_by_filename(os.path.basename(current_file)):
                    archive_files.append(current_file)
                elif os.path.exists(current_file) and lzytools_archive.is_archive(current_file):
                    archive_files.append(current_file)

        self.files.clear()

        self.Archives.emit(archive_files)


def is_exclude_file_extension(filename: str):
    """在识别压缩文件时，排除指定文件扩展名"""
    _exclude_file_extension = ['exe', 'apk', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'ppt']

    file_extension = os.path.splitext(filename)[1].strip().strip('.').strip()
    if file_extension.lower() in _exclude_file_extension:
        return True

    return False


# 常见压缩文件后缀（不含点）
_ARCHIVE_EXTS = ['7z', 'zip', 'rar', 'tar', 'gz', 'bz2', 'xz', 'iso']


def _fix_ext_part(ext_part: str):
    """
    修正后缀部分，返回修正后的后缀（不含点），无法修正返回None。
    策略：
    1. 删除中文字符
    2. 删除多余字符，保留常见压缩后缀的字符
    3. 补全缺失字符（如 .7 → .7z）
    """
    if not ext_part:
        return None

    ext_part = ext_part.lower()

    # 策略1：删除中文字符，只保留ASCII
    ext_ascii = ''.join(c for c in ext_part if ord(c) < 128)
    if not ext_ascii:
        return None

    # 策略2：精确匹配（删除多余字符后）
    for ae in _ARCHIVE_EXTS:
        if ext_ascii == ae:
            return ae
        # 检查是否包含所有必要字符，且多余字符不超过3个
        if set(ae).issubset(set(ext_ascii)) and len(ext_ascii) <= len(ae) + 3:
            # 按顺序提取匹配的字符
            result = []
            ae_chars = list(ae)
            for c in ext_ascii:
                if c in ae_chars:
                    result.append(c)
                    ae_chars.remove(c)
            if ''.join(result) == ae:
                return ae

    # 策略3：补全缺失字符（如 .7 → .7z）
    for ae in _ARCHIVE_EXTS:
        if ext_ascii and ae.startswith(ext_ascii) and len(ext_ascii) < len(ae):
            return ae

    return None


def _extract_volume_number(part: str):
    """
    从分卷编号部分提取数字，删除中文字符和其他非数字字符。
    如 '001 删除中文' → '001'，'00去2除' → '002'
    """
    digits = ''.join(c for c in part if c.isdigit())
    return digits if digits else None


def try_fix_archive_extension(filepath: str):
    """
    智能修正压缩文件后缀。
    如果修正后能识别为压缩文件，则重命名文件并返回新路径；否则返回None。

    支持的修正：
    - 删除后缀中的中文字符
    - 删除后缀中的多余字符（如 .7szc → .7z）
    - 补全缺失字符（如 .7 → .7z）
    - 分卷文件（如 .7z.001、.7szc.002）
    - 分卷编号中的中文（如 .7z.001删除中文 → .7z.001）
    """
    if not os.path.exists(filepath):
        return None

    dirname = os.path.dirname(filepath)
    basename = os.path.basename(filepath)

    # 分割文件名部分
    parts = basename.split('.')
    if len(parts) < 2:
        return None

    new_basename = None

    # 检查是否是分卷文件（如 file.7z.001, file.7szc.002, file.7z.001删除中文）
    if len(parts) >= 3:
        # 从最后一部分提取分卷编号（删除中文字符和其他非数字字符）
        volume_num = _extract_volume_number(parts[-1])
        if volume_num:
            # 分卷文件：修正倒数第二部分（压缩类型）
            fixed_ext = _fix_ext_part(parts[-2])
            need_fix_ext = fixed_ext is not None and fixed_ext != parts[-2].lower()
            need_fix_volume = volume_num != parts[-1]

            if need_fix_ext or need_fix_volume:
                ext_to_use = fixed_ext if need_fix_ext else parts[-2]
                new_parts = parts[:-2] + [ext_to_use, volume_num]
                new_basename = '.'.join(new_parts)
        else:
            # 不是分卷文件（最后一部分不是数字），当作普通文件处理，修正最后一部分
            # 例如：片尾logo.part2.rar删除 → 片尾logo.part2.rar
            fixed_ext = _fix_ext_part(parts[-1])
            if fixed_ext and fixed_ext != parts[-1].lower():
                new_parts = parts[:-1] + [fixed_ext]
                new_basename = '.'.join(new_parts)
    else:
        # 普通文件：修正最后一部分
        fixed_ext = _fix_ext_part(parts[-1])
        if fixed_ext and fixed_ext != parts[-1].lower():
            new_parts = parts[:-1] + [fixed_ext]
            new_basename = '.'.join(new_parts)

    if not new_basename or new_basename == basename:
        return None

    new_filepath = os.path.join(dirname, new_basename)

    # 检查目标文件是否已存在
    if os.path.exists(new_filepath):
        return None

    try:
        # 验证修正后的文件名是否能识别为压缩文件
        if not lzytools_archive.is_archive_by_filename(new_basename):
            # 额外检查：修正后的后缀是否是常见的压缩后缀
            # 因为 lzytools_archive 可能无法识别 part2.rar 这种分卷命名格式
            new_ext = os.path.splitext(new_basename)[1].strip('.').lower()
            if new_ext not in _ARCHIVE_EXTS:
                return None

        # 重命名文件
        os.rename(filepath, new_filepath)
        print(f'[智能后缀修复] {basename} → {new_basename}')
        return new_filepath
    except Exception as e:
        print(f'[智能后缀修复] 失败: {e}')
        return None
