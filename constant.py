# 常量
import os
import sys

# 程序路径
_PROGRAM_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/'  # 源码使用
# _PROGRAM_FOLDER = os.path.dirname(sys.argv[0]) + '/'  # 打包使用
print('程序路径', _PROGRAM_FOLDER)

# 程序文件路径
_CONFIG_FILE = _PROGRAM_FOLDER + 'config.ini'
_BACKUP_FOLDER = _PROGRAM_FOLDER + 'backup'
_PASSWORD_FILE = _PROGRAM_FOLDER + 'password.pickle'
_PASSWORD_EXPORT = _PROGRAM_FOLDER + '密码导出.txt'
_HISTORY_FILE = _PROGRAM_FOLDER + 'history.txt'
_PATH_7ZIP = _PROGRAM_FOLDER + '7-Zip/7z.exe'
_ICON_FOLDER = _PROGRAM_FOLDER + 'icon/'

# 图标路径
_ICON_MAIN_DEFAULT = _ICON_FOLDER + 'main_default.png'
_ICON_MAIN_PATH = _ICON_FOLDER + 'main_path.png'
_ICON_DISCONNECT = _ICON_FOLDER + 'disconnect.png'
_ICON_TEST = _ICON_FOLDER + 'test.png'
_ICON_EXTRACT = _ICON_FOLDER + 'extract.png'
_ICON_EXTRACT_GIF = _ICON_FOLDER + 'extract_gif.gif'
_ICON_TEST_GIF = _ICON_FOLDER + 'test_gif.gif'
_ICON_WARNING = _ICON_FOLDER + 'warning.png'
_ICON_ERROR = _ICON_FOLDER + 'error.png'
_ICON_DROP = _ICON_FOLDER + 'drop.png'
_ICON_SKIP = _ICON_FOLDER + 'skip.png'
_ICON_FINISH = _ICON_FOLDER + 'finish.png'
_ICON_SETTING = _ICON_FOLDER + 'setting.png'
_ICON_PASSWORD = _ICON_FOLDER + 'password.png'
_ICON_HOMEPAGE = _ICON_FOLDER + 'homepage.png'
_ICON_HISTORY = _ICON_FOLDER + 'history.png'
_ICON_OPEN_FOLDER = _ICON_FOLDER + 'open_folder.png'
_ICON_APP = _ICON_FOLDER + 'app.ico'
_ICON_CLEAR = _ICON_FOLDER + 'clear.png'
_ICON_STOP = _ICON_FOLDER + 'stop.png'
_ICON_ASK_PATH = _ICON_FOLDER + 'ask_path.png'

# 7zip使用
_TEMP_FOLDER = 'UnzipTempFolder'  # 临时文件夹
_PASSWORD_FAKE = 'FakePassword'  # 用于测试是否存在密码的临时密码

# 状态颜色
_COLOR_SKIP = (128, 128, 128)
_COLOR_ERROR = (254, 67, 101)
_COLOR_WARNING = (255, 215, 0)
_COLOR_SUCCESS = (0, 0, 0)

# 其他
_TIME_STAMP = ' %Y%m%d_%H%M%S'  # 时间戳格式化字符串
_HISTORY_FILE_MAX_SIZE = 10240  # 历史记录文件大小的最大值（单位：字节）

# 分卷压缩包正则
PATTERN_7Z = r'^(.+)\.7z\.\d+$'  # test.7z.001/test.7z.002/test.7z.003
PATTERN_RAR = r'^(.+)\.part(\d+)\.rar$'  # test.part1.rar/test.part2.rar/test.part3.rar
PATTERN_RAR_WITHOUT_SUFFIX = r'^(.+)\.part(\d+)$'  # rar分卷文件无后缀时也能正常解压，test.part1/test.part2/test.part3
PATTERN_ZIP = r'^(.+)\.zip$'  # zip分卷文件的第一个分卷包一般都是.zip后缀，所以.zip后缀直接视为分卷压缩文件 test.zip
PATTERN_ZIP_VOLUME = r'^(.+)\.z\d+$'  # test.zip/test.z01/test.z02
PATTERN_ZIP_TYPE2 = r'^(.+)\.zip\.\d+$'  # test.zip.001/test.zip.002/test.zip.003
