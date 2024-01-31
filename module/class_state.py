# 各种状态码的类

from constant import _ICON_DEFAULT, _ICON_FINISH, _COLOR_ERROR, _ICON_ERROR, _COLOR_WARNING, _COLOR_SUCCESS, \
    _ICON_TEST_GIF, _ICON_EXTRACT_GIF, _ICON_STOP


class StateSchedule:
    """状态-进度信息"""

    class _Template:
        def __init__(self, icon):
            self.icon = icon

    class Default(_Template):
        """初始状态"""

        def __init__(self):
            super().__init__(_ICON_DEFAULT)

    class RunningTest(_Template):
        """运行测试"""

        def __init__(self):
            super().__init__(_ICON_TEST_GIF)

    class RunningExtract(_Template):
        """运行解压"""

        def __init__(self):
            super().__init__(_ICON_EXTRACT_GIF)

    class Finish(_Template):
        """结束"""
        def __init__(self):
            super().__init__(_ICON_FINISH)


    class Stop(_Template):
        """终止"""
        def __init__(self):
            super().__init__(_ICON_STOP)


class StateError:
    """状态-错误信息"""

    class _Template:
        def __init__(self, icon, current_file, schedule_state):
            self.icon = icon
            self.current_file = current_file
            self.schedule_state = schedule_state

    class TempFolder(_Template):
        """存在临时文件夹"""

        def __init__(self):
            super().__init__(_ICON_ERROR, '————————————', '存在临时文件夹，请检查目录')

    class NoArchive(_Template):
        """没有压缩文件"""

        def __init__(self):
            super().__init__(_ICON_FINISH, '————————————', '没有需要解压的文件')


class StateUpdateUI:
    """状态-更新界面ui"""

    class _Template:
        def __init__(self, text):
            self.text = text

    class CurrentFile(_Template):
        """当前文件"""

        def __init__(self, text):
            super().__init__(text)

    class ScheduleTotal(_Template):
        """总进度"""

        def __init__(self, text):
            super().__init__(text)

    class ScheduleTest(_Template):
        """测试密码进度"""

        def __init__(self, text):
            super().__init__(text)

    class ScheduleExtract(_Template):
        """解压进度"""

        def __init__(self, text):
            super().__init__(text)


class State7zResult:
    """状态-7z处理结果"""

    class _Template:
        def __init__(self, file, type_text, color):
            self.file = file
            self.color = color
            self.type_text = type_text

    class WrongPassword(_Template):
        """密码错误"""

        def __init__(self, file):
            super().__init__(file, '密码错误', _COLOR_ERROR)

    class MissingVolume(_Template):
        """缺少分卷"""

        def __init__(self, file):
            super().__init__(file, '缺少分卷', _COLOR_ERROR)

    class NotArchiveOrDamaged(_Template):
        """不是压缩文件或文件已经损坏"""

        def __init__(self, file):
            super().__init__(file, '不是压缩文件或文件已经损坏', _COLOR_ERROR)

    class UnknownError(_Template):
        """未知错误"""

        def __init__(self, file):
            super().__init__(file, '未知错误', _COLOR_ERROR)

    class FileOccupied(_Template):
        """文件被占用"""

        def __init__(self, file):
            super().__init__(file, '文件被占用', _COLOR_WARNING)

    class NotEnoughSpace(_Template):
        """磁盘空间不足"""

        def __init__(self, file):
            super().__init__(file, '磁盘空间不足', _COLOR_WARNING)

    class Success(_Template):
        """成功"""

        def __init__(self, file, password):
            super().__init__(file, '成功', _COLOR_SUCCESS)
            self.password = password
