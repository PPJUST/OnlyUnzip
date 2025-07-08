class ModelArchive:
    """压缩包处理模式，解压/测试"""

    class Extract:
        """解压"""
        value = 'extract'

    class Test:
        """测试"""
        value = 'test'


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
    """zip调用结果"""

    class Success:
        """成功"""
        return_code = 0
        return_text = '成功'  # success
        _7zip_return = 'No error'
        color = [0, 0, 0]

        def __init__(self, password: str=None):
            self.password = password

    class Skip:
        """跳过"""
        return_code = None
        return_text = '跳过'  # skip
        _7zip_return = 'Skip'
        color = [255, 215, 0]

    class Warning:
        """非致命错误"""
        return_code = 1
        return_text = '文件被占用'  # file occupied一般情况下是文件被占用
        _7zip_return = 'Warning (Non fatal error(s)).'
        color = [128, 0, 0]

    class WrongPassword:
        """密码错误"""
        return_code = 2
        return_text = '未找到密码'  # wrong password
        _7zip_return = 'Fatal error'
        color = [178, 34, 34]

    class MissingVolume:
        """缺失分卷包"""
        return_code = 2
        return_text = '缺失分卷'  # missing volume
        _7zip_return = 'Fatal error'
        color = [205, 92, 92]

    class WrongFiletype:
        """错误的文件类型（不是压缩文件）"""
        return_code = 2
        return_text = '错误的文件类型'  # wrong filetype
        _7zip_return = 'Fatal error'
        color = [255, 99, 71]

    class UnknownError:
        """未知错误"""
        return_code = 2
        return_text = '未知错误'  # unknown error
        _7zip_return = 'Fatal error'
        color = [220, 20, 60]

        def __init__(self, error_text: str):
            self.error_text = error_text

    class ErrorCommand:
        """7zip命令行错误"""
        return_code = 7
        return_text = '错误的命令行'  # command line error
        _7zip_return = 'Command line error'
        color = [240, 128, 128]

    class NotEnoughMemory:
        """没有足够的硬盘空间"""
        return_code = 8
        return_text = '磁盘空间不足'  # Not enough memory
        _7zip_return = 'Not enough memory for operation'
        color = [250, 128, 114]

    class UserStopped:
        """用户主动停止"""
        return_code = 255
        return_text = '用户终止操作'  # user stopped
        _7zip_return = 'User stopped the process_7zip'
        color = [255, 160, 122]


class Position:
    """位置"""

    class Left:
        """左端"""
        text = '最左端'
    class Right:
        """左端"""
        text = '最右端'
