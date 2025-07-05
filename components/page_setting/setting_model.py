# 设置模块的模型组件
# 用于配置文件的具体方法，包括读取、修改、保存、获取等
import configparser
import os
from typing import Union

from common.class_7zip import ModelArchive, Position, ModelExtract, ModelCoverFile, ModelBreakFolder

_CONFIG_FILE = 'setting.ini'  # 配置文件的相对路径（默认在主程序的同目录下）


class SettingModel:
    """设置模块的模型组件"""

    def __init__(self):
        # 检查配置文件是否存在
        self._check_config_exists()

        # 读取配置文件实例对象
        self.config = configparser.ConfigParser()
        self.config.read(_CONFIG_FILE, encoding='utf-8')

        # 实例设置项子类
        self._model_archive = _ChildSettingModelArchive(self.config)
        self._try_unknown_filetype = _ChildSettingTryUnknownFiletype(self.config)
        self._write_filename = _ChildSettingWriteFilename(self.config)
        self._model_extract = _ChildSettingModelExtract(self.config)
        self._delete_file = _ChildSettingDeleteFile(self.config)
        self._recursive_extract = _ChildSettingRecursiveExtract(self.config)
        self._mode_cover_file = _ChildSettingModelCover(self.config)
        self._break_folder = _ChildSettingBreakFolder(self.config)
        self._extract_output_folder = _ChildSettingExtractOutputFolder(self.config)
        self._extract_filter = _ChildSettingExtractFilter(self.config)
        self._top_window = _ChildSettingTopWindow(self.config)
        self._lock_size = _ChildSettingLockSize(self.config)

    @staticmethod
    def _check_config_exists():
        """检查配置文件是否存在"""
        if not os.path.exists(_CONFIG_FILE):
            with open(_CONFIG_FILE, 'w', encoding='utf-8'):
                pass

    def get_model_archive(self):
        return self._model_archive.read()

    def set_model_archive(self, model: Union[ModelArchive.Test, ModelArchive.Extract]):
        self._model_archive.set(model)

    def set_model_archive_extract(self):
        self.set_model_archive(ModelArchive.Extract())

    def set_model_archive_test(self):
        self.set_model_archive(ModelArchive.Test())

    def get_try_unknown_filetype_is_enable(self):
        return self._try_unknown_filetype.read()

    def set_try_unknown_filetype_is_enable(self, is_enable: bool):
        self._try_unknown_filetype.set(is_enable)

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

    def set_write_filename_position(self, position: Union[Position.Left, Position.Right]):
        self._write_filename.set_position(position)

    def get_write_filename_preview(self):
        return self._write_filename.get_preview()

    def get_model_extract(self):
        return self._model_extract.read()

    def set_model_extract(self, model: Union[ModelExtract.Smart, ModelExtract.Direct, ModelExtract.SameFolder]):
        self._model_extract.set(model)

    def set_model_extract_smart(self):
        self.set_model_extract(ModelExtract.Smart())

    def set_model_extract_direct(self):
        self.set_model_extract(ModelExtract.Direct())

    def set_model_extract_same_folder(self):
        self.set_model_extract(ModelExtract.SameFolder())

    def get_delete_file_is_enable(self):
        return self._delete_file.read()

    def set_delete_file_is_enable(self, is_enable: bool):
        self._delete_file.set(is_enable)

    def get_recursive_extract_is_enable(self):
        return self._recursive_extract.read()

    def set_recursive_extract_is_enable(self, is_enable: bool):
        self._recursive_extract.set(is_enable)

    def get_model_cover(self):
        return self._mode_cover_file.read()

    def get_model_cover_str(self):
        return self.get_model_cover().text

    def set_model_cover(self, model: Union[
        ModelCoverFile.Overwrite, ModelCoverFile.Skip, ModelCoverFile.RenameNew, ModelCoverFile.RenameOld]):
        self._mode_cover_file.set(model)

    def get_break_folder_is_enable(self):
        return self._break_folder.read_is_enable()

    def set_break_folder_is_enable(self, is_enable: bool):
        self._break_folder.set_is_enable(is_enable)

    def get_break_folder_model(self):
        return self._break_folder.read_model()

    def get_break_folder_model_str(self):
        return self.get_break_folder_model().text

    def set_break_folder_model(self, model: Union[
        ModelBreakFolder.MoveBottom, ModelBreakFolder.MoveToTop, ModelBreakFolder.MoveFiles]):
        self._break_folder.set_model(model)

    def get_extract_output_folder_is_enable(self):
        return self._extract_output_folder.read_is_enable()

    def set_extract_output_folder_is_enable(self, is_enable: bool):
        self._extract_output_folder.set_is_enable(is_enable)

    def get_extract_output_folder_path(self):
        return self._extract_output_folder.read_path()

    def set_extract_output_folder_path(self, path: str):
        self._extract_output_folder.set_path(path)

    def get_extract_filter_is_enable(self):
        return self._extract_filter.read_is_enable()

    def set_extract_filter_is_enable(self, is_enable: bool):
        self._extract_filter.set_is_enable(is_enable)

    def get_extract_filter_rules(self):
        return self._extract_filter.read_rules()

    def set_extract_filter_rules(self, rules: str):
        self._extract_filter.set_rules(rules)

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
    """抽象类：设置项"""

    def __init__(self, config: configparser.ConfigParser):
        """:param config: 配置文件的ConfigParser对象"""
        self.config = config

    def _read_key(self, section: str, key: str, default_value):
        """读取对应设置项的值，如果失败则返回默认值"""
        return self.config.get(section, key, fallback=default_value)

    def _set_value(self, section: str, key: str, value: str):
        """设置设置项"""
        if section not in self.config:
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self.config.write(open(_CONFIG_FILE, 'w', encoding='utf-8'))


class _ModuleChildSettingSingleEnable(_ModuleChildSetting):
    """抽象类：设置项，仅是否启用的选项模版"""

    def __init__(self, config, section: str, key: str, default_value: bool):
        super().__init__(config)
        self.section = section
        self.key = key
        self._default_value = default_value

    def read(self) -> bool:
        """读取设置项"""
        value = self._read_key(self.section, self.key, self._default_value)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key, '无效的设置项值')

    def set(self, value: bool):
        """设置设置项"""
        self._set_value(self.section, self.key, str(value))


class _ModuleChildSettingSingleText(_ModuleChildSetting):
    """抽象类：设置项，纯文本项的选项模版"""

    def __init__(self, config, section: str, key: str, default_value: str):
        super().__init__(config)
        self.section = section
        self.key = key
        self._default_value = default_value

    def read(self) -> str:
        """读取设置项"""
        return self._read_key(self.section, self.key, self._default_value)

    def set(self, value: str):
        """设置设置项"""
        self._set_value(self.section, self.key, str(value))


class _ChildSettingModelArchive(_ModuleChildSetting):
    """设置项 压缩包处理模式"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ModelArchive'
        self.key = 'model'
        self._default_value = ModelArchive.Test()

    def read(self) -> Union[ModelArchive.Test, ModelArchive.Extract]:
        """读取设置项"""
        value = self._read_key(self.section, self.key, self._default_value)
        # 将读取的文本值转换为对应的自定义类
        if isinstance(value, (ModelArchive.Test, ModelArchive.Extract)):
            return value
        elif value == ModelArchive.Test.value:
            return ModelArchive.Test()
        elif value == ModelArchive.Extract.value:
            return ModelArchive.Extract()
        else:
            raise ValueError(self.section, self.key, '无效的设置项值')

    def set(self, value: Union[ModelArchive.Test, ModelArchive.Extract]):
        """设置设置项"""
        value_str = value.value
        self._set_value(self.section, self.key, value_str)


class _ChildSettingTryUnknownFiletype(_ModuleChildSettingSingleEnable):
    """设置项 是否处理未知格式"""

    def __init__(self, config):
        super().__init__(config, section='TryUnknownFiletype', key='is_enable', default_value=False)


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
        left_word = self.read_left_word()
        right_word = self.read_right_word()
        position = self.read_position()
        pw_part = f"{left_word}密码{right_word}"
        filename_part = "原文件名"
        if position == Position.Left():
            return f"{pw_part}{filename_part}"
        else:
            return f"{filename_part}{pw_part}"

    def read_is_enable(self) -> bool:
        """读取设置项 是否启用"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '无效的设置项值')

    def set_is_enable(self, value: bool):
        """设置设置项 是否启用"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_left_word(self) -> str:
        """读取设置项 密码左侧字符"""
        return self._read_key(self.section, self.key_left_word, self._default_value_left_word)

    def set_left_word(self, value: str):
        """设置设置项 密码左侧字符"""
        self._set_value(self.section, self.key_left_word, str(value))

    def read_right_word(self) -> str:
        """读取设置项 密码右侧字符"""
        return self._read_key(self.section, self.key_right_word, self._default_value_right_word)

    def set_right_word(self, value: str):
        """设置设置项 密码右侧字符"""
        self._set_value(self.section, self.key_right_word, str(value))

    def read_position(self) -> Union[Position.Left, Position.Right]:
        """读取设置项 密码位置"""
        value = self._read_key(self.section, self.key_position, self._default_value_position)
        if isinstance(value, (Position.Left, Position.Right)):
            return value
        elif value == Position.Left.text:
            return Position.Left()
        elif value == Position.Right.text:
            return Position.Right()
        else:
            raise ValueError(self.section, self.key_position, '无效的设置项值')

    def set_position(self, value: Union[Position.Left, Position.Right]):
        """设置设置项 密码位置"""
        value_str = value.text
        self._set_value(self.section, self.key_position, value_str)


class _ChildSettingModelExtract(_ModuleChildSetting):
    """设置项 解压模式"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ModelExtract'
        self.key = 'model'
        self._default_value = ModelExtract.Smart()

    def read(self) -> Union[ModelExtract.Smart, ModelExtract.Direct, ModelExtract.SameFolder]:
        """读取设置项"""
        value = self._read_key(self.section, self.key, self._default_value)
        # 将读取的文本值转换为对应的自定义类
        if isinstance(value, (ModelExtract.Smart, ModelExtract.Direct, ModelExtract.SameFolder)):
            return value
        elif value == ModelExtract.Smart.value:
            return ModelExtract.Smart()
        elif value == ModelExtract.Direct.value:
            return ModelExtract.Direct()
        elif value == ModelExtract.SameFolder.value:
            return ModelExtract.SameFolder()
        else:
            raise ValueError(self.section, self.key, '无效的设置项值')

    def set(self, value: Union[ModelExtract.Smart, ModelExtract.Direct, ModelExtract.SameFolder]):
        """设置设置项"""
        value_str = value.value
        self._set_value(self.section, self.key, value_str)


class _ChildSettingDeleteFile(_ModuleChildSettingSingleEnable):
    """设置项 是否删除原文件"""

    def __init__(self, config):
        super().__init__(config, section='DeleteFile', key='is_enable', default_value=False)


class _ChildSettingRecursiveExtract(_ModuleChildSettingSingleEnable):
    """设置项 是否递归解压"""

    def __init__(self, config):
        super().__init__(config, section='RecursiveExtract', key='is_enable', default_value=False)

    def set(self, value: bool):
        """设置设置项"""
        self._set_value(self.section, self.key, str(value))


class _ChildSettingModelCover(_ModuleChildSetting):
    """设置项 覆盖模式"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ModelCover'
        self.key = 'model'
        self._default_value = ModelCoverFile.Overwrite()

    def read(self) -> Union[
        ModelCoverFile.Overwrite, ModelCoverFile.Skip, ModelCoverFile.RenameNew, ModelCoverFile.RenameOld]:
        """读取设置项"""
        value = self._read_key(self.section, self.key, self._default_value)
        # 将读取的文本值转换为对应的自定义类
        if isinstance(value, (ModelCoverFile.Overwrite, ModelCoverFile.Skip, ModelCoverFile.RenameNew,
                              ModelCoverFile.RenameOld)):
            return value
        elif value == ModelCoverFile.Overwrite.text:
            return ModelCoverFile.Overwrite()
        elif value == ModelCoverFile.Skip.text:
            return ModelCoverFile.Skip()
        elif value == ModelCoverFile.RenameNew.text:
            return ModelCoverFile.RenameNew()
        elif value == ModelCoverFile.RenameOld.text:
            return ModelCoverFile.RenameOld()
        else:
            raise ValueError(self.section, self.key, '无效的设置项值')

    def set(self, value: Union[
        ModelCoverFile.Overwrite, ModelCoverFile.Skip, ModelCoverFile.RenameNew, ModelCoverFile.RenameOld]):
        """设置设置项"""
        if not isinstance(value, str):
            value = value.value
        self._set_value(self.section, self.key, value)


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
        self._default_value_model = ModelBreakFolder.MoveBottom()

    def read_is_enable(self) -> bool:
        """读取设置项 是否启用"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '无效的设置项值')

    def set_is_enable(self, value: bool):
        """设置设置项 是否启用"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_model(self) -> Union[ModelBreakFolder.MoveBottom, ModelBreakFolder.MoveToTop, ModelBreakFolder.MoveFiles]:
        """读取设置项 解散模式"""
        value = self._read_key(self.section, self.key_model, self._default_value_model)
        # 将读取的文本值转换为对应的自定义类
        if isinstance(value, (ModelBreakFolder.MoveBottom, ModelBreakFolder.MoveToTop, ModelBreakFolder.MoveFiles)):
            return value
        elif value == ModelBreakFolder.MoveBottom.text:
            return ModelBreakFolder.MoveBottom()
        elif value == ModelBreakFolder.MoveToTop.text:
            return ModelBreakFolder.MoveToTop()
        elif value == ModelBreakFolder.MoveFiles.text:
            return ModelBreakFolder.MoveFiles()
        else:
            raise ValueError(self.section, self.key_model, '无效的设置项值')

    def set_model(self,
                  value: Union[ModelBreakFolder.MoveBottom, ModelBreakFolder.MoveToTop, ModelBreakFolder.MoveFiles]):
        """设置设置项 解散模式"""
        if not isinstance(value, str):
            value = value.value
        self._set_value(self.section, self.key_model, value)


class _ChildSettingExtractOutputFolder(_ModuleChildSetting):
    """设置项 解压输出目录"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ExtractOutputFolder'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 解散模式
        self.key_path = 'path'
        self._default_value_path = ''

    def read_is_enable(self) -> bool:
        """读取设置项 是否启用"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '无效的设置项值')

    def set_is_enable(self, value: bool):
        """设置设置项 是否启用"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_path(self) -> str:
        """读取设置项 解压输出目录"""
        return self._read_key(self.section, self.key_path, self._default_value_path)

    def set_path(self, value: str):
        """设置设置项 解压输出目录"""
        self._set_value(self.section, self.key_path, value)


class _ChildSettingExtractFilter(_ModuleChildSetting):
    """设置项 解压过滤器"""

    def __init__(self, config):
        super().__init__(config)
        self.section = 'ExtractFilter'
        # 是否启用
        self.key_is_enable = 'is_enable'
        self._default_value_is_enable = False
        # 解散模式
        self.key_rules = 'rules'
        self._default_value_rules = ''

    def read_is_enable(self) -> bool:
        """读取设置项 是否启用"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '无效的设置项值')

    def set_is_enable(self, value: bool):
        """设置设置项 是否启用"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_rules(self) -> str:
        """读取设置项 过滤规则"""
        return self._read_key(self.section, self.key_rules, self._default_value_rules)

    def set_rules(self, value: str):
        """设置设置项 过滤规则"""
        self._set_value(self.section, self.key_rules, value)


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
        self._default_value_is_enable = False
        # 窗口高度
        self.key_height = 'height'
        self._default_value_height = 600
        # 窗口宽度
        self.key_width = 'width'
        self._default_value_width = 400

    def read_is_enable(self) -> bool:
        """读取设置项 是否启用"""
        value = self._read_key(self.section, self.key_is_enable, self._default_value_is_enable)
        if isinstance(value, bool):
            return value
        elif value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            raise ValueError(self.section, self.key_is_enable, '无效的设置项值')

    def set_is_enable(self, value: bool):
        """设置设置项 是否启用"""
        self._set_value(self.section, self.key_is_enable, str(value))

    def read_height(self) -> int:
        """读取设置项 窗口高度"""
        value = self._read_key(self.section, self.key_height, self._default_value_height)
        return int(value)

    def set_height(self, value: int):
        """设置设置项窗口高度"""
        self._set_value(self.section, self.key_height, str(value))

    def read_width(self) -> int:
        """读取设置项 窗口宽度"""
        value = self._read_key(self.section, self.key_width, self._default_value_width)
        return int(value)

    def set_width(self, value: int):
        """设置设置项 窗口宽度"""
        self._set_value(self.section, self.key_width, str(value))
