"""7zip 相关的模式定义、结果类型及类型别名。

模式类既会被实例化，也会作为类对象传递给设置项和列表，
因此保留类属性的定义方式，避免影响现有调用。
"""

from typing import Union

_FAKE_PASSWORD = 'FAKEPASSWORD'
_NO_PASSWORD = '无密码'

RESULT_STATE_SUCCESS = '成功'
RESULT_STATE_SKIP = '跳过'
RESULT_STATE_FAIL = '失败'


class ModelArchive:
    """压缩包处理模式，解压/测试"""

    class Extract:
        """解压"""
        value = 'extract'

    class Test:
        """测试"""
        value = 'test'


class ModelPreFilter:
    """文件预筛选模式，默认/黑名单/白名单"""

    class Default:
        """默认"""
        value = 'default'

    class BlackList:
        """黑名单"""
        value = 'blacklist'

    class WhiteList:
        """白名单"""
        value = 'whitelist'


class ModelExtract:
    """解压模式，智能解压/解压到同名文件夹/直接解压"""

    class Smart:
        """智能解压"""
        value = 'smart'

    class SameFolder:
        """解压到同名文件夹"""
        value = 'same_folder'

    class Direct:
        """直接解压"""
        value = 'direct'


class ModelCoverFile:
    """文件覆盖模式，跳过/覆盖/重命名新文件/重命名旧文件"""

    class Skip:
        """跳过"""
        text = '跳过重复文件'
        value = 'skip'
        switch = '-aos'

    class Overwrite:
        """覆盖"""
        text = '覆盖重复文件'
        value = 'overwrite'
        switch = '-aoa'

    class RenameNew:
        """重命名新文件"""
        text = '重命名新文件'
        value = 'rename_new'
        switch = '-aou'

    class RenameOld:
        """重命名旧文件"""
        text = '重命名旧文件'
        value = 'rename_old'
        switch = '-aot'


class ModelBreakFolder:
    """解散文件夹的模式"""

    class MoveBottom:
        """移动最底层的首个非空文件夹到顶层目录之外（并删除空的顶层目录）"""
        text = '移动底层文件夹'
        value = 'move_bottom'

    class MoveToTop:
        """移动最底层的首个非空文件夹下的文件到顶层目录之下（保持文件层级结构，并删除空的该底层文件夹）"""
        text = '移动到顶层目录'
        value = 'move_to_top'

    class MoveFiles:
        """移动所有文件到顶层目录之下（并删除空的子文件夹）"""
        text = '仅移动文件'
        value = 'move_files'


class ArchiveRole:
    """压缩包角色，普通压缩包/分卷压缩包（首个分卷）/分卷压缩包（非首个的成员）"""

    class Normal:
        """普通压缩包"""

    class VolumeFirst:
        """分卷压缩包（首个分卷）"""

    class VolumeMember:
        """分卷压缩包（非首个的成员）"""


class Model7zip:
    """7zip命令模式，l/t/x"""

    class L:
        """l，列表命令"""
        value = 'l'

    class T:
        """t，测试命令"""
        value = 't'

    class X:
        """x，解压命令"""
        value = 'x'


class Result7zip:
    """7zip调用结果"""

    class _ResultBase:
        """所有结果的公共属性，子类只覆盖与公共值不同的属性。"""

        return_code = 2
        return_text = '未知错误'
        _7zip_return = 'Fatal error'
        color = [220, 20, 60]
        result_state = RESULT_STATE_FAIL

    class Success(_ResultBase):
        """成功"""

        return_code = 0
        return_text = '成功'
        _7zip_return = 'No error'
        color = [0, 0, 0]
        result_state = RESULT_STATE_SUCCESS

        def __init__(self, password: str = None):
            if not password or password == _FAKE_PASSWORD:
                password = _NO_PASSWORD
            self.password = password

    class Skip(_ResultBase):
        """跳过"""

        return_code = None
        return_text = '跳过'
        _7zip_return = 'Skip'
        color = [255, 215, 0]
        result_state = RESULT_STATE_SKIP

    class Warning(_ResultBase):
        """非致命错误，一般是文件被占用"""

        return_code = 1
        return_text = '文件被占用'
        _7zip_return = 'Warning (Non fatal error(s)).'
        color = [128, 0, 0]

    class _FatalError(_ResultBase):
        """返回码为 2 的致命错误公共类。"""

    class WrongPassword(_FatalError):
        """密码错误"""

        return_text = '未找到密码'
        color = [178, 34, 34]

    class MissingVolume(_FatalError):
        """缺失分卷包"""

        return_text = '缺失分卷'
        color = [205, 92, 92]

    class WrongFiletype(_FatalError):
        """错误的文件类型（不是压缩文件）"""

        return_text = '错误的文件类型'
        color = [255, 99, 71]

    class UnknownError(_FatalError):
        """未知错误"""

        def __init__(self, error_text: str):
            self.error_text = error_text

    class ErrorCommand(_ResultBase):
        """7zip命令行错误"""

        return_code = 7
        return_text = '错误的命令行'
        _7zip_return = 'Command line error'
        color = [240, 128, 128]

    class NotEnoughMemory(_ResultBase):
        """没有足够的硬盘空间"""

        return_code = 8
        return_text = '磁盘空间不足'
        _7zip_return = 'Not enough memory for operation'
        color = [250, 128, 114]

    class UserStopped(_ResultBase):
        """用户主动停止"""

        return_code = 255
        return_text = '用户终止操作'
        _7zip_return = 'User stopped the process_7zip'
        color = [255, 160, 122]


class Position:
    """位置"""

    class Left:
        """左端"""
        text = '最左端'

    class Right:
        """右端"""
        text = '最右端'


# 类型别名，仅用于类型标注
TYPES_MODEL_ARCHIVE = Union[
    ModelArchive.Extract,
    ModelArchive.Test,
]

TYPES_MODEL_PRE_FILTER = Union[
    ModelPreFilter.Default,
    ModelPreFilter.BlackList,
    ModelPreFilter.WhiteList,
]

TYPES_MODEL_EXTRACT = Union[
    ModelExtract.Smart,
    ModelExtract.SameFolder,
    ModelExtract.Direct,
]

TYPES_MODEL_COVER_FILE = Union[
    ModelCoverFile.Skip,
    ModelCoverFile.Overwrite,
    ModelCoverFile.RenameNew,
    ModelCoverFile.RenameOld,
]

TYPES_MODEL_BREAK_FOLDER = Union[
    ModelBreakFolder.MoveBottom,
    ModelBreakFolder.MoveToTop,
    ModelBreakFolder.MoveFiles,
]

TYPES_ARCHIVE_ROLE = Union[
    ArchiveRole.Normal,
    ArchiveRole.VolumeFirst,
    ArchiveRole.VolumeMember,
]

TYPES_MODEL_7ZIP = Union[
    Model7zip.L,
    Model7zip.T,
    Model7zip.X,
]

TYPES_RESULT_7ZIP = Union[
    Result7zip.Success,
    Result7zip.Skip,
    Result7zip.Warning,
    Result7zip.WrongPassword,
    Result7zip.MissingVolume,
    Result7zip.WrongFiletype,
    Result7zip.UnknownError,
    Result7zip.ErrorCommand,
    Result7zip.NotEnoughMemory,
    Result7zip.UserStopped,
]

TYPES_POSITION = Union[
    Position.Left,
    Position.Right,
]

# 结果类列表，用于按结果类型进行筛选和归类
CLASS_RESULT_7ZIP = [
    Result7zip.Success,
    Result7zip.Skip,
    Result7zip.Warning,
    Result7zip.WrongPassword,
    Result7zip.MissingVolume,
    Result7zip.WrongFiletype,
    Result7zip.UnknownError,
    Result7zip.ErrorCommand,
    Result7zip.NotEnoughMemory,
    Result7zip.UserStopped,
]

RESULT_STATE_ALL = '全部'
RESULT_STATE_CACHE = '缓存'
RESULT_STATES = [
    RESULT_STATE_ALL,
    RESULT_STATE_SUCCESS,
    RESULT_STATE_FAIL,
    RESULT_STATE_SKIP,
    RESULT_STATE_CACHE,
]
