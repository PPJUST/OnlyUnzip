# 设置模块的桥梁组件
# 接收 Viewer 的信号，通过 Model 修改本地配置文件，并在必要时通知外部组件
from PySide6.QtCore import QObject, Signal

from common.class_7zip import ModelArchive, ModelExtract, ModelPreFilter, TYPES_MODEL_ARCHIVE
from common.class_setting import ModelSetting
from components.page_setting.setting_viewer import SettingViewer


class SettingPresenter(QObject):
    """设置模块的桥梁组件"""

    SignalTopWindow = Signal(bool, name='是否置顶窗口')
    SignalLockSize = Signal(bool, name='是否锁定窗口大小')
    SignalChangeArchiveModel = Signal(object, name='修改压缩文件处理模式')

    def __init__(self, viewer: SettingViewer, model=None):
        super().__init__()
        self.viewer = viewer
        self.model = ModelSetting()  # 使用独立的设置模型组件

        # 必须先加载初始设置再绑定信号，避免初始化界面时把默认值写回配置文件
        self._load_setting()
        self._bind_signal()

    # region 对外接口
    def get_archive_model(self):
        """获取当前的压缩文件处理模式（解压/测试）"""
        return self.model.get_model_archive()

    def get_extract_output_folder(self):
        """获取解压输出目录，未启用时返回 None"""
        is_enable = self.model.get_extract_output_folder_is_enable()
        path = self.model.get_extract_output_folder_path()
        if is_enable and path:
            return path
        return None

    def get_is_try_unknown_filetype(self):
        """获取是否尝试处理未知格式的文件"""
        return self.model.get_try_unknown_filetype_is_enable()

    def update_filename_with_pw_preview(self):
        """更新密码写入文件名的预览"""
        self.viewer.set_setting_write_filename_preview(self.model.get_write_filename_preview())

    def lock_setting(self):
        """锁定设置项，禁止修改"""
        self.viewer.lock()

    def unlock_setting(self):
        """解锁设置项，允许修改"""
        self.viewer.unlock()

    def change_archive_model(self, archive_model: TYPES_MODEL_ARCHIVE):
        """由主页切换压缩文件处理模式"""
        if isinstance(archive_model, ModelArchive.Test):
            self.viewer.set_setting_model_test()
        elif isinstance(archive_model, ModelArchive.Extract):
            self.viewer.set_setting_model_extract()
        else:
            raise ValueError('未知的压缩包处理模式：{0}'.format(archive_model))

    def change_unknown_filetype(self, is_enable: bool):
        """由主页快捷选项切换是否尝试处理未知格式的文件"""
        self.viewer.set_setting_is_try_unknown_filetype(is_enable)

    def change_recursive_extract(self, is_enable: bool):
        """由主页快捷选项切换是否递归解压"""
        self.viewer.set_setting_recursive_extract(is_enable)

    def change_delete_file(self, is_enable: bool):
        """由主页快捷选项切换是否删除源文件"""
        self.viewer.set_setting_delete_file(is_enable)

    def change_top_window(self, is_enable: bool):
        """由主页快捷选项切换是否置顶窗口"""
        self.viewer.set_top_window(is_enable)

    # endregion

    def _bind_signal(self):
        """把 Viewer 的信号连接到 Model，以及需要转发的外部信号"""
        connections = [
            # 压缩包处理模式
            (self.viewer.ChangeArchiveModelTest, self.model.set_model_archive_test),
            (self.viewer.ChangeArchiveModelTest, self.SignalChangeArchiveModel.emit),
            (self.viewer.ChangeArchiveModelExtract, self.model.set_model_archive_extract),
            (self.viewer.ChangeArchiveModelExtract, self.SignalChangeArchiveModel.emit),
            # 文件预筛选
            (self.viewer.ChangePreFilterModeDefault, self.model.set_model_pre_filter_default),
            (self.viewer.ChangePreFilterModeBlackList, self.model.set_model_pre_filter_blacklist),
            (self.viewer.ChangePreFilterModeBlackListRule, self.model.set_model_pre_filter_blacklist_rule),
            (self.viewer.ChangePreFilterModeWhiteList, self.model.set_model_pre_filter_whitelist),
            (self.viewer.ChangePreFilterModeWhiteListRule, self.model.set_model_pre_filter_whitelist_rule),
            # 通用选项
            (self.viewer.ChangeTryUnknownFiletype, self.model.set_try_unknown_filetype_is_enable),
            (self.viewer.ChangeReadPasswordFromFilename, self.model.set_read_password_from_filename_is_enable),
            # 将密码写入文件名（测试模式）
            (self.viewer.ChangeWriteFilenameT, self.model.set_write_filename_is_enable),
            (self.viewer.ChangeWriteFilenameLeftPart, self.model.set_write_filename_left_word),
            (self.viewer.ChangeWriteFilenameLeftPart, self.update_filename_with_pw_preview),
            (self.viewer.ChangeWriteFilenameRightPart, self.model.set_write_filename_right_word),
            (self.viewer.ChangeWriteFilenameRightPart, self.update_filename_with_pw_preview),
            (self.viewer.ChangeWriteFilenamePosition, self.model.set_write_filename_position),
            (self.viewer.ChangeWriteFilenamePosition, self.update_filename_with_pw_preview),
            # 解压模式
            (self.viewer.ChangeExtractModelSmart, self.model.set_model_extract_smart),
            (self.viewer.ChangeExtractModelDirect, self.model.set_model_extract_direct),
            (self.viewer.ChangeExtractModelSameFolder, self.model.set_model_extract_same_folder),
            (self.viewer.ChangeRecursiveExtract, self.model.set_recursive_extract_is_enable),
            # 解压成功后的源文件操作
            (self.viewer.ChangeProcessFileAfterExtractSuccess,
             self.model.set_process_file_after_extract_success_is_enable),
            (self.viewer.ChangeDeleteFile, self.model.set_delete_file_is_enable),
            (self.viewer.ChangeMoveOriginFileAfterSuccess, self.model.set_move_origin_file_after_success_is_enable),
            (self.viewer.ChangePathMoveOriginFileAfterSuccess, self.model.set_move_origin_file_after_success_path),
            (self.viewer.ChangeWriteFilenameE, self.model.set_write_filename_after_extract_success_is_enable),
            (self.viewer.ChangeInsertCharToFilenameAfterSuccess,
             self.model.set_insert_char_to_filename_after_success_is_enable),
            (self.viewer.ChangeInsertCharToFilenameAfterSuccessPosition,
             self.model.set_insert_char_to_filename_after_success_position),
            (self.viewer.ChangeInsertCharToFilenameAfterSuccessChar,
             self.model.set_insert_char_to_filename_after_success_char),
            # 解压失败后的源文件操作
            (self.viewer.ChangeProcessFileAfterExtractFailure,
             self.model.set_process_file_after_extract_failure_is_enable),
            (self.viewer.ChangeMoveOriginFileAfterFailure, self.model.set_move_origin_file_after_failure_is_enable),
            (self.viewer.ChangePathMoveOriginFileAfterFailure, self.model.set_move_origin_file_after_failure_path),
            (self.viewer.ChangeInsertCharToFilenameAfterFailure,
             self.model.set_insert_char_to_filename_after_failure_is_enable),
            (self.viewer.ChangeInsertCharToFilenameAfterFailurePosition,
             self.model.set_insert_char_to_filename_after_failure_position),
            (self.viewer.ChangeInsertCharToFilenameAfterFailureChar,
             self.model.set_insert_char_to_filename_after_failure_char),
            # 解压设置
            (self.viewer.ChangeCoverModel, self.model.set_model_cover),
            (self.viewer.ChangeBreakFolder, self.model.set_break_folder_is_enable),
            (self.viewer.ChangeBreakFolderModel, self.model.set_break_folder_model),
            (self.viewer.ChangeExtractOutputFolder, self.model.set_extract_output_folder_is_enable),
            (self.viewer.ChangeExtractOutputFolderPath, self.model.set_extract_output_folder_path),
            (self.viewer.ChangeExtractFilter, self.model.set_extract_filter_is_enable),
            (self.viewer.ChangeExtractFilterRule, self.model.set_extract_filter_rules),
            (self.viewer.Change7ZipPath, self.model.set_7zip_path),
            # 窗口设置
            (self.viewer.ChangeTopWindow, self.model.set_top_window_is_enable),
            (self.viewer.ChangeTopWindow, self.SignalTopWindow.emit),
            (self.viewer.ChangeLockSize, self.model.set_lock_size_is_enable),
            (self.viewer.ChangeLockSize, self.SignalLockSize.emit),
        ]
        for signal, slot in connections:
            signal.connect(slot)

    # region 加载初始设置
    def _load_setting(self):
        """分批加载初始设置并更新 Viewer"""
        self._load_archive_model()
        self._load_pre_filter()
        self._load_password_settings()
        self._load_extract_model()
        self._load_extract_success_settings()
        self._load_extract_failure_settings()
        self._load_other_settings()

    def _load_archive_model(self):
        archive_model = self.model.get_model_archive()
        if isinstance(archive_model, ModelArchive.Test):
            self.viewer.set_setting_model_test()
        elif isinstance(archive_model, ModelArchive.Extract):
            self.viewer.set_setting_model_extract()
        else:
            raise ValueError('未知的压缩包处理模式：{0}'.format(archive_model))

    def _load_pre_filter(self):
        pre_filter_model = self.model.get_model_pre_filter()
        if isinstance(pre_filter_model, ModelPreFilter.Default):
            self.viewer.set_setting_pre_filter_mode_default()
        elif isinstance(pre_filter_model, ModelPreFilter.BlackList):
            self.viewer.set_setting_pre_filter_mode_black_list()
        elif isinstance(pre_filter_model, ModelPreFilter.WhiteList):
            self.viewer.set_setting_pre_filter_mode_white_list()
        else:
            raise ValueError('未知的文件预筛选模式：{0}'.format(pre_filter_model))

        self.viewer.set_setting_pre_filter_mode_black_list_rule(
            self.model.get_model_pre_filter_blacklist_rule())
        self.viewer.set_setting_pre_filter_mode_white_list_rule(
            self.model.get_model_pre_filter_whitelist_rule())

    def _load_password_settings(self):
        self.viewer.set_setting_is_try_unknown_filetype(self.model.get_try_unknown_filetype_is_enable())
        self.viewer.set_setting_is_read_password_from_filename(
            self.model.get_read_password_from_filename_is_enable())

        self.viewer.set_setting_write_filename_t(self.model.get_write_filename_is_enable())
        self.viewer.set_setting_write_filename_left_part(self.model.get_write_filename_left_word())
        self.viewer.set_setting_write_filename_right_part(self.model.get_write_filename_right_word())
        self.viewer.set_setting_write_filename_position(self.model.get_write_filename_position_str())
        self.viewer.set_setting_write_filename_preview(self.model.get_write_filename_preview())

    def _load_extract_model(self):
        extract_model = self.model.get_model_extract()
        if isinstance(extract_model, ModelExtract.Smart):
            self.viewer.set_setting_extract_model_smart()
        elif isinstance(extract_model, ModelExtract.Direct):
            self.viewer.set_setting_extract_model_direct()
        elif isinstance(extract_model, ModelExtract.SameFolder):
            self.viewer.set_setting_extract_model_same_folder()
        else:
            raise ValueError('未知的解压模式：{0}'.format(extract_model))

        self.viewer.set_setting_recursive_extract(self.model.get_recursive_extract_is_enable())

    def _load_extract_success_settings(self):
        self.viewer.set_setting_process_file_after_extract_success(
            self.model.get_process_file_after_extract_success_is_enable())
        self.viewer.set_setting_delete_file(self.model.get_delete_file_is_enable())

        self.viewer.set_setting_is_move_origin_file_after_success(
            self.model.get_move_origin_file_after_success_is_enable())
        self.viewer.set_setting_path_move_origin_file_after_success(
            self.model.get_move_origin_file_after_success_path())

        self.viewer.set_setting_write_filename_e(self.model.get_write_filename_after_extract_success_is_enable())

        self.viewer.set_setting_is_insert_char_to_filename_after_success(
            self.model.get_insert_char_to_filename_after_success_is_enable())
        self.viewer.set_setting_position_insert_char_to_filename_after_success(
            self.model.get_insert_char_to_filename_after_success_position_str())
        self.viewer.set_setting_char_insert_char_to_filename_after_success(
            self.model.get_insert_char_to_filename_after_success_char())

    def _load_extract_failure_settings(self):
        self.viewer.set_setting_process_file_after_extract_failure(
            self.model.get_process_file_after_extract_failure_is_enable())

        self.viewer.set_setting_is_move_origin_file_after_failure(
            self.model.get_move_origin_file_after_failure_is_enable())
        self.viewer.set_setting_path_move_origin_file_after_failure(
            self.model.get_move_origin_file_after_failure_path())

        self.viewer.set_setting_is_insert_char_to_filename_after_failure(
            self.model.get_insert_char_to_filename_after_failure_is_enable())
        self.viewer.set_setting_position_insert_char_to_filename_after_failure(
            self.model.get_insert_char_to_filename_after_failure_position_str())
        self.viewer.set_setting_char_insert_char_to_filename_after_failure(
            self.model.get_insert_char_to_filename_after_failure_char())

    def _load_other_settings(self):
        self.viewer.set_setting_cover_model(self.model.get_model_cover_str())
        self.viewer.set_setting_break_folder(self.model.get_break_folder_is_enable())
        self.viewer.set_setting_break_folder_model(self.model.get_break_folder_model_str())

        self.viewer.set_setting_extract_to_folder(self.model.get_extract_output_folder_is_enable())
        self.viewer.set_setting_extract_output_folder(self.model.get_extract_output_folder_path())
        self.viewer.set_setting_filter(self.model.get_extract_filter_is_enable())
        self.viewer.set_setting_filter_rule(self.model.get_extract_filter_rules_str())

        self.viewer.set_setting_7zip_path(self.model.get_7zip_path())
        self.viewer.set_top_window(self.model.get_top_window_is_enable())
        self.viewer.set_lock_size(self.model.get_lock_size_is_enable())
    # endregion
