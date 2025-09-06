# 设置模块的桥梁组件
# 用于接收Viewer的信号，并在选项修改时通过Model修改本地配置文件，并通知Viewer更新
from PySide6.QtCore import QObject, Signal

from common.class_7zip import ModelArchive, ModelExtract
from components.page_setting.setting_model import SettingModel
from components.page_setting.setting_viewer import SettingViewer


class SettingPresenter(QObject):
    """设置模块的桥梁组件"""
    SignalTopWindow = Signal(bool, name='是否置顶窗口')
    SignalLockSize = Signal(bool, name='是否锁定窗口大小')
    SignalChangeArchiveModel = Signal(object, name='修改压缩文件处理模式')

    def __init__(self, viewer: SettingViewer, model: SettingModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # 初始化
        self._load_setting()  # 注意 必须在绑定信号前加载初始设置更新UI，否则更新时会触发对应信号
        self._bind_signal()

    def get_archive_model(self):
        """获取当前的压缩文件处理模式 解压/测试"""
        return self.model.get_model_archive()

    def get_extract_output_folder(self):
        """获取解压输出目录，若未启用则返回空"""
        is_enable = self.model.get_extract_output_folder_is_enable()
        path = self.model.get_extract_output_folder_path()
        if is_enable and path:
            return path
        else:
            return None

    def get_is_try_unknown_filetype(self):
        """获取是否尝试处理未知格式的文件"""
        return self.model.get_try_unknown_filetype_is_enable()

    def update_filename_with_pw_preview(self):
        """更新密码写入文件名的预览"""
        self.viewer.set_setting_write_filename_preview(self.model.get_write_filename_preview())

    def lock_setting(self):
        """锁定设置项，禁止被修改"""
        self.viewer.lock()

    def unlock_setting(self):
        """解锁设置项，可以被修改"""
        self.viewer.unlock()

    def _bind_signal(self):
        """绑定Viewer信号"""
        self.viewer.ChangeArchiveModelTest.connect(self.model.set_model_archive_test)
        self.viewer.ChangeArchiveModelTest.connect(self.SignalChangeArchiveModel.emit)
        self.viewer.ChangeArchiveModelExtract.connect(self.model.set_model_archive_extract)
        self.viewer.ChangeArchiveModelExtract.connect(self.SignalChangeArchiveModel.emit)
        self.viewer.ChangeTryUnknownFiletype.connect(self.model.set_try_unknown_filetype_is_enable)
        self.viewer.ChangeReadPasswordFromFilename.connect(self.model.set_read_password_from_filename_is_enable)
        self.viewer.ChangeWriteFilename.connect(self.model.set_write_filename_is_enable)
        self.viewer.ChangeWriteFilenameLeftPart.connect(self.model.set_write_filename_left_word)
        self.viewer.ChangeWriteFilenameLeftPart.connect(self.update_filename_with_pw_preview)
        self.viewer.ChangeWriteFilenameRightPart.connect(self.model.set_write_filename_right_word)
        self.viewer.ChangeWriteFilenameRightPart.connect(self.update_filename_with_pw_preview)
        self.viewer.ChangeWriteFilenamePosition.connect(self.model.set_write_filename_position)
        self.viewer.ChangeWriteFilenamePosition.connect(self.update_filename_with_pw_preview)
        self.viewer.ChangeExtractModelSmart.connect(self.model.set_model_extract_smart)
        self.viewer.ChangeExtractModelDirect.connect(self.model.set_model_extract_direct)
        self.viewer.ChangeExtractModelSameFolder.connect(self.model.set_model_extract_same_folder)
        self.viewer.ChangeDeleteFile.connect(self.model.set_delete_file_is_enable)
        self.viewer.ChangeRecursiveExtract.connect(self.model.set_recursive_extract_is_enable)
        self.viewer.ChangeCoverModel.connect(self.model.set_model_cover)
        self.viewer.ChangeBreakFolder.connect(self.model.set_break_folder_is_enable)
        self.viewer.ChangeBreakFolderModel.connect(self.model.set_break_folder_model)
        self.viewer.ChangeExtractOutputFolder.connect(self.model.set_extract_output_folder_is_enable)
        self.viewer.ChangeExtractOutputFolderPath.connect(self.model.set_extract_output_folder_path)
        self.viewer.ChangeExtractFilter.connect(self.model.set_extract_filter_is_enable)
        self.viewer.ChangeExtractFilterRule.connect(self.model.set_extract_filter_rules)
        self.viewer.ChangeTopWindow.connect(self.model.set_top_window_is_enable)
        self.viewer.ChangeTopWindow.connect(self.SignalTopWindow.emit)
        self.viewer.ChangeLockSize.connect(self.model.set_lock_size_is_enable)
        self.viewer.ChangeLockSize.connect(self.SignalLockSize.emit)

    def _load_setting(self):
        """加载初始设置，更新Viewer"""
        archive_model = self.model.get_model_archive()
        if isinstance(archive_model, ModelArchive.Test):
            self.viewer.set_setting_model_test()
        elif isinstance(archive_model, ModelArchive.Extract):
            self.viewer.set_setting_model_extract()
        else:
            raise Exception(archive_model, "错误的设置项")

        self.viewer.set_setting_is_try_unknown_filetype(self.model.get_try_unknown_filetype_is_enable())
        self.viewer.set_setting_is_read_password_from_filename(self.model.get_read_password_from_filename_is_enable())

        self.viewer.set_setting_write_filename(self.model.get_write_filename_is_enable())
        self.viewer.set_setting_write_filename_left_part(self.model.get_write_filename_left_word())
        self.viewer.set_setting_write_filename_right_part(self.model.get_write_filename_right_word())
        self.viewer.set_setting_write_filename_position(self.model.get_write_filename_position_str())
        self.viewer.set_setting_write_filename_preview(self.model.get_write_filename_preview())

        extract_model = self.model.get_model_extract()
        if isinstance(extract_model, ModelExtract.Smart):
            self.viewer.set_setting_extract_model_smart()
        elif isinstance(extract_model, ModelExtract.Direct):
            self.viewer.set_setting_extract_model_direct()
        elif isinstance(extract_model, ModelExtract.SameFolder):
            self.viewer.set_setting_extract_model_same_folder()
        else:
            raise Exception(extract_model, "错误的设置项")

        self.viewer.set_setting_delete_file(self.model.get_delete_file_is_enable())

        self.viewer.set_setting_recursive_extract(self.model.get_recursive_extract_is_enable())

        self.viewer.set_setting_cover_model(self.model.get_model_cover_str())

        self.viewer.set_setting_break_folder(self.model.get_break_folder_is_enable())
        self.viewer.set_setting_break_folder_model(self.model.get_break_folder_model_str())

        self.viewer.set_setting_extract_to_folder(self.model.get_extract_output_folder_is_enable())
        self.viewer.set_setting_extract_output_folder(self.model.get_extract_output_folder_path())

        self.viewer.set_setting_filter(self.model.get_extract_filter_is_enable())

        self.viewer.set_setting_filter_rule(self.model.get_extract_filter_rules_str())

        self.viewer.set_top_window(self.model.get_top_window_is_enable())

        self.viewer.set_lock_size(self.model.get_lock_size_is_enable())
