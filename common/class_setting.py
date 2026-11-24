# 设置的模型组件
# 用于配置文件的具体方法，包括读取、修改、保存、获取等
import configparser
import os
from typing import Any, Union

from common.class_7zip import ModelArchive, Position, ModelExtract, ModelCoverFile, ModelBreakFolder, \
    TYPES_MODEL_ARCHIVE, TYPES_MODEL_BREAK_FOLDER, TYPES_POSITION, TYPES_MODEL_COVER_FILE, TYPES_MODEL_EXTRACT, \
    TYPES_MODEL_PRE_FILTER, ModelPreFilter

_CONFIG_FILE = 'setting.ini'  # 配置文件的相对路径（默认在主程序的同目录下）
_FILTER_RULE_SEPARATOR = '丨'  # 解压过滤规则在配置文件中的分隔符


class ModelSetting:
    """设置的模型组件（单例，对外提供全部设置项的读写接口）"""

    _instance = None
    _is_init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._is_init:
            return
        self._is_init = True

        self._check_config_exists()
        self.config = configparser.ConfigParser()
        self.config.read(_CONFIG_FILE, encoding='utf-8')

        # 实例化各设置项子类
        self._model_archive = _ChildSettingModelArchive(self.config)
        self._model_pre_filter = _ChildSettingModelPreFilter(self.config)
        self._try_unknown_filetype = _ChildSettingTryUnknownFiletype(self.config)
        self._read_password_from_filename = _ChildSettingReadPasswordFromFilename(self.config)
        self._write_filename = _ChildSettingWriteFilename(self.config)
        self._model_extract = _ChildSettingModelExtract(self.config)
        self._recursive_extract = _ChildSettingRecursiveExtract(self.config)
        self._process_file_after_extract_success = _ChildSettingProcessFileAfterExtractSuccess(self.config)
        self._delete_file = _ChildSettingDeleteFile(self.config)
        self._move_origin_file_after_success = _ChildSettingMoveOriginFileAfterSuccess(self.config)
        self._write_filename_after_extract_success = _ChildSettingWriteFilenameAfterExtractSuccess(self.config)
        self._insert_char_to_filename_after_success = _ChildSettingInsertCharToFilenameAfterSuccess(self.config)
        self._process_file_after_extract_failure = _ChildSettingProcessFileAfterExtractFailure(self.config)
        self._move_origin_file_after_failure = _ChildSettingMoveOriginFileAfterFailure(self.config)
        self._insert_char_to_filename_after_failure = _ChildSettingInsertCharToFilenameAfterFailure(self.config)
        self._mode_cover_file = _ChildSettingModelCover(self.config)
        self._break_folder = _ChildSettingBreakFolder(self.config)
        self._extract_output_folder = _ChildSettingExtractOutputFolder(self.config)
        self._extract_filter = _ChildSettingExtractFilter(self.config)
        self._7zip_path = _ChildSetting7ZipPath(self.config)
        self._top_window = _ChildSettingTopWindow(self.config)
        self._lock_size = _ChildSettingLockSize(self.config)

    @staticmethod
    def _check_config_exists():
        """检查配置文件是否存在，不存在则创建空文件"""
        if not os.path.exists(_CONFIG_FILE):
            with open(_CONFIG_FILE, 'w', encoding='utf-8'):
                pass

    # 压缩包处理模式
    def get_model_archive(self):
        return self._model_archive.read()

    def set_model_archive(self, model: TYPES_MODEL_ARCHIVE):
        self._model_archive.set(model)

    def set_model_archive_extract(self):
        self.set_model_archive(ModelArchive.Extract())

    def set_model_archive_test(self):
        self.set_model_archive(ModelArchive.Test())

    # 文件预筛选模式
    def get_model_pre_filter(self):
        return self._model_pre_filter.read_mode()

    def set_model_pre_filter(self, model: TYPES_MODEL_PRE_FILTER):
        self._model_pre_filter.set_mode(model)

    def set_model_pre_filter_default(self):
        self.set_model_pre_filter(ModelPreFilter.Default())

    def set_model_pre_filter_blacklist(self):
        self.set_model_pre_filter(ModelPreFilter.BlackList())

    def set_model_pre_filter_whitelist(self):
        self.set_model_pre_filter(ModelPreFilter.WhiteList())

    def get_model_pre_filter_blacklist_rule(self):
        return self._model_pre_filter.read_black_list()

    def set_model_pre_filter_blacklist_rule(self, rule: list[str]):
        self._model_pre_filter.set_black_list(rule)

    def get_model_pre_filter_whitelist_rule(self):
        return self._model_pre_filter.read_white_list()

    def set_model_pre_filter_whitelist_rule(self, rule: list[str]):
        self._model_pre_filter.set_white_list(rule)

    # 通用开关
    def get_try_unknown_filetype_is_enable(self):
        return self._try_unknown_filetype.read()

    def set_try_unknown_filetype_is_enable(self, is_enable: bool):
        self._try_unknown_filetype.set(is_enable)

    def get_read_password_from_filename_is_enable(self):
        return self._read_password_from_filename.read()

    def set_read_password_from_filename_is_enable(self, is_enable: bool):
        self._read_password_from_filename.set(is_enable)

    # 将密码写入文件名
    def get_write_filename_is_enable(self):
        return self._write_filename.read_is_enable()

    def set_write_filename_is_enable(self, is_enable: bool):
        self._write_filename.set_is_enable(is_enable)

    def get_write_filename_left_word(self):
        return self._write_filename.read_left_word()

    def set_write_filename_left_word(self, word: str):
        self._write_filename.set_left_word(word)

    def get_write_filename_right_word(self):
        return self._write_filename.read_right_word()

    def set_write_filename_right_word(self, word: str):
        self._write_filename.set_right_word(word)

    def get_write_filename_position(self):
        return self._write_filename.read_position()

    def get_write_filename_position_str(self):
        return self.get_write_filename_position().text

    def set_write_filename_position(self, position: TYPES_POSITION):
        self._write_filename.set_position(position)

    def get_write_filename_preview(self):
        return self._write_filename.get_preview()

    # 解压模式
    def get_model_extract(self):
        return self._model_extract.read()

    def set_model_extract(self, model: TYPES_MODEL_EXTRACT):
        self._model_extract.set(model)

    def set_model_extract_smart(self):
        self.set_model_extract(ModelExtract.Smart())

    def set_model_extract_direct(self):
        self.set_model_extract(ModelExtract.Direct())

    def set_model_extract_same_folder(self):
        self.set_model_extract(ModelExtract.SameFolder())

    def get_recursive_extract_is_enable(self):
        return self._recursive_extract.read()

    def set_recursive_extract_is_enable(self, is_enable: bool):
        self._recursive_extract.set(is_enable)

    # 解压成功后的文件处理
    def get_process_file_after_extract_success_is_enable(self):
        return self._process_file_after_extract_success.read()

    def set_process_file_after_extract_success_is_enable(self, is_enable: bool):
        self._process_file_after_extract_success.set(is_enable)

    def get_delete_file_is_enable(self):
        return self._delete_file.read()

    def set_delete_file_is_enable(self, is_enable: bool):
        self._delete_file.set(is_enable)

    def get_move_origin_file_after_success_is_enable(self):
        return self._move_origin_file_after_success.read_is_enable()

    def set_move_origin_file_after_success_is_enable(self, is_enable: bool):
        self._move_origin_file_after_success.set_is_enable(is_enable)

    def get_move_origin_file_after_success_path(self):
        return self._move_origin_file_after_success.read_path()

    def set_move_origin_file_after_success_path(self, path: str):
        self._move_origin_file_after_success.set_path(path)

    def get_write_filename_after_extract_success_is_enable(self):
        return self._write_filename_after_extract_success.read()

    def set_write_filename_after_extract_success_is_enable(self, is_enable: bool):
        self._write_filename_after_extract_success.set(is_enable)

    def get_insert_char_to_filename_after_success_is_enable(self):
        return self._insert_char_to_filename_after_success.read_is_enable()

    def set_insert_char_to_filename_after_success_is_enable(self, is_enable: bool):
        self._insert_char_to_filename_after_success.set_is_enable(is_enable)

    def get_insert_char_to_filename_after_success_position(self):
        return self._insert_char_to_filename_after_success.read_position()

    def get_insert_char_to_filename_after_success_position_str(self):
        return self._insert_char_to_filename_after_success.read_position().text

    def set_insert_char_to_filename_after_success_position(self, position: str):
        self._insert_char_to_filename_after_success.set_position(position)

    def get_insert_char_to_filename_after_success_char(self):
        return self._insert_char_to_filename_after_success.read_char()

    def set_insert_char_to_filename_after_success_char(self, char: str):
        self._insert_char_to_filename_after_success.set_char(char)

    # 解压失败后的文件处理
    def get_process_file_after_extract_failure_is_enable(self):
        return self._process_file_after_extract_failure.read()

    def set_process_file_after_extract_failure_is_enable(self, is_enable: bool):
        self._process_file_after_extract_failure.set(is_enable)

    def get_move_origin_file_after_failure_is_enable(self):
        return self._move_origin_file_after_failure.read_is_enable()

    def set_move_origin_file_after_failure_is_enable(self, is_enable: bool):
        self._move_origin_file_after_failure.set_is_enable(is_enable)

    def get_move_origin_file_after_failure_path(self):
        return self._move_origin_file_after_failure.read_path()

    def set_move_origin_file_after_failure_path(self, path: str):
        self._move_origin_file_after_failure.set_path(path)

    def get_insert_char_to_filename_after_failure_is_enable(self):
        return self._insert_char_to_filename_after_failure.read_is_enable()

    def set_insert_char_to_filename_after_failure_is_enable(self, is_enable: bool):
        self._insert_char_to_filename_after_failure.set_is_enable(is_enable)

    def get_insert_char_to_filename_after_failure_position(self):
        return self._insert_char_to_filename_after_failure.read_position()

    def get_insert_char_to_filename_after_failure_position_str(self):
        return self._insert_char_to_filename_after_failure.read_position().text

    def set_insert_char_to_filename_after_failure_position(self, position: str):
        self._insert_char_to_filename_after_failure.set_position(position)

    def get_insert_char_to_filename_after_failure_char(self):
        return self._insert_char_to_filename_after_failure.read_char()

    def set_insert_char_to_filename_after_failure_char(self, char: str):
        self._insert_char_to_filename_after_failure.set_char(char)

    # 覆盖模式
    def get_model_cover(self):
        return self._mode_cover_file.read()

    def get_model_cover_str(self):
        return self.get_model_cover().text

    def set_model_cover(self, model: TYPES_MODEL_COVER_FILE):
        self._mode_cover_file.set(model)

    # 解散文件夹
    def get_break_folder_is_enable(self):
        return self._break_folder.read_is_enable()

    def set_break_folder_is_enable(self, is_enable: bool):
        self._break_folder.set_is_enable(is_enable)

    def get_break_folder_model(self):
        return self._break_folder.read_model()

    def get_break_folder_model_str(self):
        return self.get_break_folder_model().text

    def set_break_folder_model(self, model: TYPES_MODEL_BREAK_FOLDER):
        self._break_folder.set_model(model)

    # 解压输出目录
    def get_extract_output_folder_is_enable(self):
        return self._extract_output_folder.read_is_enable()

    def set_extract_output_folder_is_enable(self, is_enable: bool):
        self._extract_output_folder.set_is_enable(is_enable)

    def get_extract_output_folder_path(self):
        return self._extract_output_folder.read_path()

    def set_extract_output_folder_path(self, path: str):
        self._extract_output_folder.set_path(path)

    # 解压过滤器
    def get_extract_filter_is_enable(self):
        return self._extract_filter.read_is_enable()

    def set_extract_filter_is_enable(self, is_enable: bool):
        self._extract_filter.set_is_enable(is_enable)

    def get_extract_filter_rules(self):
        return self._extract_filter.read_rules()

    def get_extract_filter_rules_str(self):
        return self._extract_filter.read_rules_str()

    def set_extract_filter_rules(self, rules: str):
        self._extract_filter.set_rules(rules)

    # 主程序与窗口设置
    def get_7zip_path(self):
        return self._7zip_path.read()

    def set_7zip_path(self, path: str):
        self._7zip_path.set(path)

    def get_top_window_is_enable(self):
        return self._top_window.read()

    def set_top_window_is_enable(self, is_enable: bool):
        self._top_window.set(is_enable)

    def get_lock_size_is_enable(self):
        return self._lock_size.read_is_enable()

    def set_lock_size_is_enable(self, is_enable: bool):
        self._lock_size.set_is_enable(is_enable)

    def get_lock_size_height(self):
        return self._lock_size.read_height()

    def set_lock_size_height(self, height: int):
        self._lock_size.set_height(height)

    def get_lock_size_width(self):
        return self._lock_size.read_width()

    def set_lock_size_width(self, width: int):
        self._lock_size.set_width(width)


class _ModuleChildSetting:
    """设置项的公共基类：统一处理配置文件的读取与保存"""

    def __init__(self, config: configparser.ConfigParser):
        """:param config: 配置文件的 ConfigParser 对象"""
        self.config = config

    def _read_key(self, section: str, key: str, default_value):
        """读取设置项，失败时返回默认值"""
        return self.config.get(section, key, fallback=default_value)

    def _set_value(self, section: str, key: str, value):
        """写入设置项并立即保存到配置文件"""
        if section not in self.config:
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        with open(_CONFIG_FILE, 'w', encoding='utf-8') as config_file:
            self.config.write(config_file)

    def _read_bool(self, section: str, key: str, default_value: bool) -> bool:
        """读取“是否启用”类设置项"""
        value = self._read_key(section, key, default_value)
        if isinstance(value, bool):
            return value
        if value == 'True':
            return True
        if value == 'False':
            return False
        raise ValueError(section, key, '无效的设置项值')

    def _set_bool(self, section: str, key: str, value: bool):
        """写入“是否启用”类设置项"""
        self._set_value(section, key, str(value))

    def _read_model(self, section: str, key: str, models: list[type], default_value) -> Any:
        """读取模式类设置项，把配置文件中的文本还原为对应的模型类实例

        同时兼容 .value（英文）和 .text（中文）两种存储格式。
        """
        value = self._read_key(section, key, default_value)
        for model in models:
            if isinstance(value, model):
                return value
            if value == getattr(model, 'value', None):
                return model()
            if value == getattr(model, 'text', None):
                return model()
        raise ValueError(section, key, '无效的设置项值')

    def _set_model(self, section: str, key: str, value):
        """写入模式类设置项，接受模型类实例或字符串"""
        if isinstance(value, str):
            text = value
        elif hasattr(value, 'text'):
            text = value.text
        else:
            text = value.value
        self._set_value(section, key, text)


class _ModuleChildSettingSingleEnable(_ModuleChildSetting):
    """抽象类：仅包含“是否启用”的设置项模板"""

    def __init__(self, config, section: str, key: str, default_value: bool):
        super().__init__(config)
        self.section = section
        self.key = key
        self._default_value = default_value

    def read(self) -> bool:
        return self._read_bool(self.section, self.key, self._default_value)

    def set(self, value: bool):
        self._set_bool(self.section, self.key, value)


class _ModuleChildSettingSingleText(_ModuleChildSetting):
    """抽象类：仅包含纯文本的设置项模板"""

    def __init__(self, config, section: str, key: str, default_value: str):
        super().__init__(config)
        self.section = section
        self.key = key
        self._default_value = default_value

    def read(self) -> str:
        return self._read_key(self.section, self.key, self._default_value)

    def set(self, value: str):
        self._set_value(self.section, self.key, value)


class _ModuleChildSettingModel(_ModuleChildSetting):
    """抽象类：仅包含单个模式选项的设置项模板"""

    def __init__(self, config, section: str, key: str, models: list[type], default_value):
        super().__init__(config)
        self.section = section
        self.key = key
        self.models = models
        self._default_value = default_value

    def read(self):
        return self._read_model(self.section, self.key, self.models, self._default_value)

    def set(self, value):
        self._set_model(self.section, self.key, value)


class _ChildSettingModelArchive(_ModuleChildSettingModel):
    """设置项 压缩包处理模式"""

    def __init__(self, config):
        super().__init__(
            config,
            section='ModelArchive',
            key='model',
            models=[ModelArchive.Extract, ModelArchive.Test],
            default_value=ModelArchive.Test(),
        )


class _ChildSettingModelPreFilter(_ModuleChildSetting):
    """设置项 文件预筛选模式"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ModelPreFilter'
        # 模式
        self.key_mode = 'model'
        self._default_value_mode = ModelPreFilter.Default()
        # 黑名单规则（以双管道符间隔）
        self.key_black_list = 'black_list'
        self._default_value_black_list = r'\.xls$||\.xlsx$||\.xlsm$||\.doc$||\.docx$||\.docm$||\.ppt$||\.pptx$||\.pptm$||\.csv$||\.odt$||\.ods$||\.odp$||\.epub$||\.kmz$||\.cbz$||\.ipa$||\.jar$||\.war$||\.ear$||\.aar$||\.xpi$||\.crx$||\.vsix$||\.nupkg$||\.whl$||\.apk$||\.exe$||\.appx$||\.msix$||\.aab$||\.xapk$||\.vpk$||\.pck$||\.ba2$||\.love$||\.mcpack$||\.mcworld$||\.bsa$||\.mpq$||\.sav$||\.dat$||\.pak$||\.quicksave$||\.autosave$'
        # 白名单规则（以双管道符间隔）
        self.key_white_list = 'white_list'
        self._default_value_white_list = r'\.zip$||\.xz$||\.7z$||\.rar$||\.tar$||\.iso$||\.gz$||\.arj$||\.cramfs$||\.bzip2$||\.cab$||\.dmg$||\.wim$||\.gzip$||\.chm$||\.ext$||\.ar$||\.cpio$||\.\d+$||\.part\d+$||\.z\d+$'

    def read_mode(self) -> TYPES_MODEL_PRE_FILTER:
        models = [ModelPreFilter.Default, ModelPreFilter.BlackList, ModelPreFilter.WhiteList]
        return self._read_model(self.section, self.key_mode, models, self._default_value_mode)

    def set_mode(self, value: TYPES_MODEL_PRE_FILTER):
        self._set_model(self.section, self.key_mode, value)

    def read_black_list(self) -> list[str]:
        return self._read_rules(self.key_black_list, self._default_value_black_list)

    def set_black_list(self, value: list[str]):
        self._set_rules(self.key_black_list, value)

    def read_white_list(self) -> list[str]:
        return self._read_rules(self.key_white_list, self._default_value_white_list)

    def set_white_list(self, value: list[str]):
        self._set_rules(self.key_white_list, value)

    def _read_rules(self, key: str, default_value: str) -> list[str]:
        """读取以双管道符间隔的规则列表"""
        value = self._read_key(self.section, key, default_value)
        return [rule for rule in value.split('||') if rule]

    def _set_rules(self, key: str, value: list[str]):
        self._set_value(self.section, key, '||'.join(value))


class _ChildSettingTryUnknownFiletype(_ModuleChildSettingSingleEnable):
    """设置项 是否处理未知格式"""

    def __init__(self, config):
        super().__init__(config, section='TryUnknownFiletype', key='is_enable', default_value=False)


class _ChildSettingReadPasswordFromFilename(_ModuleChildSettingSingleEnable):
    """设置项 是否从文件名中读取密码"""

    def __init__(self, config):
        super().__init__(config, section='ReadPasswordFromFilename', key='is_enable', default_value=False)


class _ChildSettingWriteFilename(_ModuleChildSetting):
    """设置项 将密码写入文件名"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'WriteFilename'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 密码文本格式 左侧字符
        self.key_left_word = 'left_word'
        self._default_value_left_word = ''
        # 密码文本格式 右侧字符
        self.key_right_word = 'right_word'
        self._default_value_right_word = ''
        # 密码文本格式 位置
        self.key_position = 'position'
        self._default_value_position = Position.Left()

    def get_preview(self) -> str:
        """获取密码写入文件名的示例"""
        position = self.read_position()
        left_part = self.read_left_word()
        right_part = self.read_right_word()
        if isinstance(position, Position.Left) and not right_part:  # 防止密码与文件名之间没有间隔符号
            right_part = ' '
        elif isinstance(position, Position.Right) and not left_part:
            left_part = ' '
        password_part = f'{left_part}密码{right_part}'
        filename_part = '源文件名'
        if isinstance(position, Position.Left):
            return f'{password_part}{filename_part}'
        if isinstance(position, Position.Right):
            return f'{filename_part}{password_part}'
        return '错误的设置参数'

    def read_is_enable(self) -> bool:
        return self._read_bool(self.section, self.key_is_enable, self._default_value_is_enable)

    def set_is_enable(self, value: bool):
        self._set_bool(self.section, self.key_is_enable, value)

    def read_left_word(self) -> str:
        return self._read_key(self.section, self.key_left_word, self._default_value_left_word)

    def set_left_word(self, value: str):
        self._set_value(self.section, self.key_left_word, value)

    def read_right_word(self) -> str:
        return self._read_key(self.section, self.key_right_word, self._default_value_right_word)

    def set_right_word(self, value: str):
        self._set_value(self.section, self.key_right_word, value)

    def read_position(self) -> TYPES_POSITION:
        models = [Position.Left, Position.Right]
        return self._read_model(self.section, self.key_position, models, self._default_value_position)

    def set_position(self, value: Union[TYPES_POSITION, str]):
        self._set_model(self.section, self.key_position, value)


class _ChildSettingModelExtract(_ModuleChildSettingModel):
    """设置项 解压模式"""

    def __init__(self, config):
        super().__init__(
            config,
            section='ModelExtract',
            key='model',
            models=[ModelExtract.Smart, ModelExtract.Direct, ModelExtract.SameFolder],
            default_value=ModelExtract.Smart(),
        )


class _ChildSettingRecursiveExtract(_ModuleChildSettingSingleEnable):
    """设置项 是否递归解压"""

    def __init__(self, config):
        super().__init__(config, section='RecursiveExtract', key='is_enable', default_value=False)


class _ChildSettingProcessFileAfterExtractSuccess(_ModuleChildSettingSingleEnable):
    """设置项 解压成功后是否进行源文件操作"""

    def __init__(self, config):
        super().__init__(config, section='ProcessFileAfterExtractSuccess', key='is_enable', default_value=False)


class _ChildSettingDeleteFile(_ModuleChildSettingSingleEnable):
    """设置项 是否删除源文件"""

    def __init__(self, config):
        super().__init__(config, section='DeleteFile', key='is_enable', default_value=False)


class _ChildSettingMoveOriginFileAfterSuccess(_ModuleChildSetting):
    """设置项 解压成功后移动源文件"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'MoveOriginFileAfterSuccess'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 移动目录
        self.key_path = 'path'
        self._default_value_path = ''

    def read_is_enable(self) -> bool:
        return self._read_bool(self.section, self.key_is_enable, self._default_value_is_enable)

    def set_is_enable(self, value: bool):
        self._set_bool(self.section, self.key_is_enable, value)

    def read_path(self) -> str:
        return self._read_key(self.section, self.key_path, self._default_value_path)

    def set_path(self, value: str):
        self._set_value(self.section, self.key_path, value)


class _ChildSettingWriteFilenameAfterExtractSuccess(_ModuleChildSettingSingleEnable):
    """设置项 解压成功后是否将解压密码写入源文件的文件名"""

    def __init__(self, config):
        super().__init__(config, section='WriteFilenameAfterExtractSuccess', key='is_enable', default_value=False)


class _ChildSettingInsertCharToFilenameAfterSuccess(_ModuleChildSetting):
    """设置项 解压成功后向文件名中添加指定文本"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'InsertCharToFilenameAfterSuccess'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 添加的文本
        self.key_char = 'char'
        self._default_value_char = ''
        # 添加的位置
        self.key_position = 'position'
        self._default_value_position = Position.Left()

    def read_is_enable(self) -> bool:
        return self._read_bool(self.section, self.key_is_enable, self._default_value_is_enable)

    def set_is_enable(self, value: bool):
        self._set_bool(self.section, self.key_is_enable, value)

    def read_char(self) -> str:
        return self._read_key(self.section, self.key_char, self._default_value_char)

    def set_char(self, value: str):
        self._set_value(self.section, self.key_char, value)

    def read_position(self) -> TYPES_POSITION:
        models = [Position.Left, Position.Right]
        return self._read_model(self.section, self.key_position, models, self._default_value_position)

    def set_position(self, value: Union[TYPES_POSITION, str]):
        self._set_model(self.section, self.key_position, value)


class _ChildSettingProcessFileAfterExtractFailure(_ModuleChildSettingSingleEnable):
    """设置项 解压失败后是否进行源文件操作"""

    def __init__(self, config):
        super().__init__(config, section='ProcessFileAfterExtractFailure', key='is_enable', default_value=False)


class _ChildSettingMoveOriginFileAfterFailure(_ModuleChildSetting):
    """设置项 解压失败后移动源文件"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'MoveOriginFileAfterFailure'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 移动目录
        self.key_path = 'path'
        self._default_value_path = ''

    def read_is_enable(self) -> bool:
        return self._read_bool(self.section, self.key_is_enable, self._default_value_is_enable)

    def set_is_enable(self, value: bool):
        self._set_bool(self.section, self.key_is_enable, value)

    def read_path(self) -> str:
        return self._read_key(self.section, self.key_path, self._default_value_path)

    def set_path(self, value: str):
        self._set_value(self.section, self.key_path, value)


class _ChildSettingInsertCharToFilenameAfterFailure(_ModuleChildSetting):
    """设置项 解压失败后向文件名中添加指定文本"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'InsertCharToFilenameAfterFailure'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 添加的文本
        self.key_char = 'char'
        self._default_value_char = ''
        # 添加的位置
        self.key_position = 'position'
        self._default_value_position = Position.Left()

    def read_is_enable(self) -> bool:
        return self._read_bool(self.section, self.key_is_enable, self._default_value_is_enable)

    def set_is_enable(self, value: bool):
        self._set_bool(self.section, self.key_is_enable, value)

    def read_char(self) -> str:
        return self._read_key(self.section, self.key_char, self._default_value_char)

    def set_char(self, value: str):
        self._set_value(self.section, self.key_char, value)

    def read_position(self) -> TYPES_POSITION:
        models = [Position.Left, Position.Right]
        return self._read_model(self.section, self.key_position, models, self._default_value_position)

    def set_position(self, value: Union[TYPES_POSITION, str]):
        self._set_model(self.section, self.key_position, value)


class _ChildSettingModelCover(_ModuleChildSettingModel):
    """设置项 覆盖模式"""

    def __init__(self, config):
        super().__init__(
            config,
            section='ModelCover',
            key='model',
            models=[ModelCoverFile.Overwrite, ModelCoverFile.Skip,
                    ModelCoverFile.RenameNew, ModelCoverFile.RenameOld],
            default_value=ModelCoverFile.Overwrite(),
        )


class _ChildSettingBreakFolder(_ModuleChildSetting):
    """设置项 解散文件夹"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'BreakFolder'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 解散模式
        self.key_model = 'model'
        self._default_value_model = ModelBreakFolder.MoveToTop()

    def read_is_enable(self) -> bool:
        return self._read_bool(self.section, self.key_is_enable, self._default_value_is_enable)

    def set_is_enable(self, value: bool):
        self._set_bool(self.section, self.key_is_enable, value)

    def read_model(self) -> TYPES_MODEL_BREAK_FOLDER:
        models = [ModelBreakFolder.MoveBottom, ModelBreakFolder.MoveToTop, ModelBreakFolder.MoveFiles]
        return self._read_model(self.section, self.key_model, models, self._default_value_model)

    def set_model(self, value: TYPES_MODEL_BREAK_FOLDER):
        self._set_model(self.section, self.key_model, value)


class _ChildSettingExtractOutputFolder(_ModuleChildSetting):
    """设置项 解压输出目录"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ExtractOutputFolder'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 输出目录
        self.key_path = 'path'
        self._default_value_path = ''

    def read_is_enable(self) -> bool:
        return self._read_bool(self.section, self.key_is_enable, self._default_value_is_enable)

    def set_is_enable(self, value: bool):
        self._set_bool(self.section, self.key_is_enable, value)

    def read_path(self) -> str:
        return self._read_key(self.section, self.key_path, self._default_value_path)

    def set_path(self, value: str):
        self._set_value(self.section, self.key_path, value)


class _ChildSettingExtractFilter(_ModuleChildSetting):
    """设置项 解压过滤器"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ExtractFilter'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 过滤规则，直接存储 switch（即包含 -xr! 的规则）
        self.key_rules = 'rules'
        self._default_value_rules = ''

    def read_is_enable(self) -> bool:
        return self._read_bool(self.section, self.key_is_enable, self._default_value_is_enable)

    def set_is_enable(self, value: bool):
        self._set_bool(self.section, self.key_is_enable, value)

    def read_rules(self) -> list[str]:
        """读取过滤规则，转换为 7zip switch 格式"""
        return ['-xr!' + rule for rule in self._read_rule_items()]

    def read_rules_str(self) -> str:
        """读取过滤规则，用于界面显示"""
        return '\n'.join(self._read_rule_items())

    def set_rules(self, value: Union[str, list[str]]):
        """写入过滤规则，接受字符串或列表"""
        if isinstance(value, str):
            value = value.split('\n')
        rules = [rule for rule in value if rule]
        self._set_value(self.section, self.key_rules, _FILTER_RULE_SEPARATOR.join(rules))

    def _read_rule_items(self) -> list[str]:
        """读取过滤规则文本并拆分为列表"""
        setting = self._read_key(self.section, self.key_rules, self._default_value_rules)
        return [rule for rule in setting.split(_FILTER_RULE_SEPARATOR) if rule]


class _ChildSetting7ZipPath(_ModuleChildSettingSingleText):
    """设置项 7zip路径"""

    def __init__(self, config):
        super().__init__(config, section='7ZipPath', key='filepath', default_value='')


class _ChildSettingTopWindow(_ModuleChildSettingSingleEnable):
    """设置项 置顶窗口"""

    def __init__(self, config):
        super().__init__(config, section='TopWindow', key='is_enable', default_value=False)


class _ChildSettingLockSize(_ModuleChildSetting):
    """设置项 锁定窗口尺寸"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'LockSize'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = True
        # 窗口高度
        self.key_height = 'height'
        self._default_value_height = 300
        # 窗口宽度
        self.key_width = 'width'
        self._default_value_width = 300

    def read_is_enable(self) -> bool:
        return self._read_bool(self.section, self.key_is_enable, self._default_value_is_enable)

    def set_is_enable(self, value: bool):
        self._set_bool(self.section, self.key_is_enable, value)

    def read_height(self) -> int:
        return int(self._read_key(self.section, self.key_height, self._default_value_height))

    def set_height(self, value: int):
        self._set_value(self.section, self.key_height, value)

    def read_width(self) -> int:
        return int(self._read_key(self.section, self.key_width, self._default_value_width))

    def set_width(self, value: int):
        self._set_value(self.section, self.key_width, value)
