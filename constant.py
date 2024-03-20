# 存放常量
import os

# 程序所在路径
_PROGRAM_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/'

# 图标
_ICON_FOLDER = _PROGRAM_FOLDER + 'icon/'
_ICON_TEST = _ICON_FOLDER + 'state_test.png'
_ICON_EXTRACT = _ICON_FOLDER + 'state_extract.png'
_ICON_TEST_GIF = _ICON_FOLDER + 'state_test_gif.gif'
_ICON_EXTRACT_GIF = _ICON_FOLDER + 'state_extract_gif.gif'
_ICON_MAIN = _ICON_FOLDER + 'icon_main.ico'
_ICON_DEFAULT = _ICON_FOLDER + 'state_default.png'
_ICON_DEFAULT_WITH_OUTPUT = _ICON_FOLDER + 'state_default_with_output.png'
_ICON_ERROR = _ICON_FOLDER + 'state_error.png'
_ICON_FINISH = _ICON_FOLDER + 'state_finish.png'
_ICON_STOP = _ICON_FOLDER + 'button_stop.png'
_ICON_DROP = _ICON_FOLDER + 'state_drop.png'
_ICON_PAGE_EXTRACT = _ICON_FOLDER + 'page_extract.png'
_ICON_PAGE_HOME = _ICON_FOLDER + 'page_home.png'
_ICON_PAGE_HISTORY = _ICON_FOLDER + 'page_history.png'
_ICON_PAGE_PASSWORD = _ICON_FOLDER + 'page_password.png'
_ICON_PAGE_SETTING = _ICON_FOLDER + 'page_setting.png'
_ICON_SKIP = _ICON_FOLDER + 'state_skip.png'
_ICON_STOP_STATE = _ICON_FOLDER + 'state_stop.png'

# 程序目录内文件
_CONFIG_FILE = _PROGRAM_FOLDER + 'config.ini'
_BACKUP_FOLDER = _PROGRAM_FOLDER + 'backup'
_PASSWORD_FILE = _PROGRAM_FOLDER + 'password.pickle'  # 密码数据库格式说明：存储一个dict，键为密码str，值为对应的使用次数int
_PASSWORD_EXPORT = _PROGRAM_FOLDER + '密码导出.txt'
_HISTORY_FILE = _PROGRAM_FOLDER + 'history.txt'
_PATH_7ZIP = _PROGRAM_FOLDER + '7-Zip/7z.exe'

# 程序设置项
_COLOR_SKIP = (128, 128, 128)
_COLOR_ERROR = (254, 67, 101)
_COLOR_WARNING = (255, 215, 0)
_COLOR_SUCCESS = (0, 0, 0)
_HISTORY_FILE_MAX_SIZE = 10240  # 历史记录文件大小的最大值（单位：字节）

# 临时文件
_UNZIP_TEMP_FOLDER = 'UnzipTempFolder'
_PASSWORD_NONE = 'NonePassword'  # 用于测试是否存在密码的临时密码
