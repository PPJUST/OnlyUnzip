# 主页模块的桥梁组件
import os
import re
from typing import Union

from PySide6.QtCore import QObject, Signal

from common import function_extract, function_7zip, function_setting
from common.class_7zip import ModelArchive, ModelPreFilter, TYPES_MODEL_ARCHIVE
from common.class_file_info import FileInfoList
from common.thread_filetype_archive import ThreadCheckFiletype
from components.page_home.home_model import HomeModel
from components.page_home.home_viewer import HomeViewer
from components.page_home.res.icon_base64 import (
    ICON_COMPLETE,
    ICON_EXTRACT,
    ICON_EXTRACTING,
    ICON_LOGO_PIXEL,
    ICON_SKIP,
    ICON_STOPPED,
    ICON_TEST,
    ICON_TESTING,
    ICON_WARNING,
    ICON_WARNING_YELLOW,
)


class HomePresenter(QObject):
    """主页模块的桥梁组件，负责连接界面组件和模型组件。"""

    UserStop = Signal(name="用户主动停止（立即终止")
    UserStopAfter = Signal(name="用户主动停止（等待当前文件完成后终止）")
    FileInfo = Signal(FileInfoList, name="提取的文件信息类")
    SignalNoFiles = Signal(name="没有需要处理的文件")
    SignalExistsTempFolder = Signal(str, name="存在临时文件夹，接收临时文件夹路径参数")
    SignalError7ZipPath = Signal(name="7zip路径错误")
    OpenAbout = Signal(name="打开关于页")
    OpenTempPassword = Signal(name="打开临时密码页")
    AskUpdateSetting = Signal(name="请求更新选项参数")

    # 主页左上角显示的便捷选项
    ChangeSettingArchiveModel = Signal(object, name="设置模式选项")
    ChangeSettingTryUnknownFiletype = Signal(bool, name="设置处理未知格式文件选项")
    ChangeSettingRecursiveExtract = Signal(bool, name="设置递归解压选项")
    ChangeSettingDeleteOrigin = Signal(bool, name="设置删除源文件选项")
    ChangeSettingTopWindow = Signal(bool, name="设置置顶选项")

    def __init__(self, viewer: HomeViewer, model: HomeModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # 统计变量
        self._task_count = 0
        self._task_index = 0
        self._password_count = 0
        self._password_index = 0

        self.set_icon_home()

        # 检查文件类型的子线程，防止堵塞界面线程
        self.thread_check_filetype = ThreadCheckFiletype()
        self.thread_check_filetype.Archives.connect(self.deal_archive_files)

        self._bind_signals()

    def _bind_signals(self):
        """绑定界面组件和模型组件的信号"""
        self.viewer.UserStop.connect(self.UserStop.emit)
        self.viewer.UserStopAfter.connect(self.UserStopAfter.emit)
        self.viewer.DropFiles.connect(self.drop_paths)
        self.viewer.OpenAbout.connect(self.OpenAbout.emit)
        self.viewer.OpenTempPassword.connect(self.OpenTempPassword.emit)
        self.viewer.AskUpdateSetting.connect(self.AskUpdateSetting.emit)
        self.viewer.ChangeSettingArchiveModel.connect(self.ChangeSettingArchiveModel.emit)
        self.viewer.ChangeSettingTryUnknownFiletype.connect(self.ChangeSettingTryUnknownFiletype.emit)
        self.viewer.ChangeSettingRecursiveExtract.connect(self.ChangeSettingRecursiveExtract.emit)
        self.viewer.ChangeSettingDeleteOrigin.connect(self.ChangeSettingDeleteOrigin.emit)
        self.viewer.ChangeSettingTopWindow.connect(self.ChangeSettingTopWindow.emit)

        self.model.RuntimeTotal.connect(self.set_runtime_total)
        self.model.RuntimeCurrent.connect(self.set_runtime_current)

    def _is_7zip_available(self) -> bool:
        """检查7zip路径是否有效"""
        path = function_7zip.get_7zip_path()
        if not path:
            return False
        return os.path.exists(path)

    def _check_temp_folder(self, files: list):
        """检查是否存在非空的临时解压文件夹，返回是否存在和文件夹路径"""
        archive_model = function_setting.get_archive_model()
        if not isinstance(archive_model, ModelArchive.Extract):
            return False, ''

        self.set_step_notice("检查临时文件夹中...")
        target_path = function_setting.get_extract_output_folder()
        if target_path:
            return function_extract.is_exists_temp_folder(target_path)
        return function_extract.is_exists_temp_folder(files)

    def drop_paths(self, paths: list, is_recursive: bool = False):
        """拖入文件
        :param paths: 文件路径
        :param is_recursive: 是否是递归解压模式进行的源文件操作"""
        if not self._is_7zip_available():
            self.SignalError7ZipPath.emit()
            return

        if not is_recursive:
            self.model.start_timing()

        self.set_step_notice("搜索文件中...")
        files = self.model.get_files(paths)
        if not files:
            self.SignalNoFiles.emit()
            return

        is_temp_exists, temp_path = self._check_temp_folder(files)
        if is_temp_exists:
            self.SignalExistsTempFolder.emit(temp_path)
            return

        self.set_step_notice("检查文件类型中...")
        filter_mode = function_setting.get_pre_filter_model()
        files_pre_filter = self.pre_filter_files(files, filter_mode)

        # filetype库无法正确识别分卷压缩包，且读取文件头检查类型较慢，
        # 因此先按文件名筛选，再在子线程中检查文件头
        is_try_unknown_filetype = function_setting.get_is_try_unknown_filetype()
        if not is_try_unknown_filetype:
            self.thread_check_filetype.set_files(files_pre_filter)
            self.thread_check_filetype.start()
        else:
            self.deal_archive_files(files_pre_filter)

    def deal_archive_files(self, archives: list):
        """处理压缩文件"""
        archive_spliter = self.model.split_volume_archive(archives)
        if not archive_spliter.is_has_archives():
            self.SignalNoFiles.emit()
            return

        file_info_list = FileInfoList()
        for file in archive_spliter.get_files():
            role = archive_spliter.get_role(file)
            group_files = archive_spliter.get_members(file)
            file_info_list.add_file(file, role, group_files)

        self.FileInfo.emit(file_info_list)

    def pre_filter_files(self, files: list, filter_mode: ModelPreFilter):
        """预筛选文件"""
        if isinstance(filter_mode, ModelPreFilter.Default):
            return files
        if isinstance(filter_mode, ModelPreFilter.BlackList):
            return function_setting.filter_by_black_list(files)
        if isinstance(filter_mode, ModelPreFilter.WhiteList):
            return function_setting.filter_by_white_list(files)
        raise ValueError('未知的预筛选模式')

    def banned_drop(self):
        """禁止拖入文件"""
        self.viewer.banned_drop()
        # 主页悬浮按钮的控制跟随是否允许拖入
        self.set_float_button_enable(False)

    def allowed_drop(self):
        """允许拖入文件"""
        self.viewer.allowed_drop()
        # 主页悬浮按钮的控制跟随是否允许拖入
        self.set_float_button_enable(True)

    def update_setting(self, archive_model: TYPES_MODEL_ARCHIVE,
                       try_unknown_filetype: bool,
                       recursive_extract: bool,
                       delete_origin: bool,
                       top_window: bool):
        """更新选项参数"""
        self.viewer.update_setting(archive_model=archive_model,
                                   try_unknown_filetype=try_unknown_filetype,
                                   recursive_extract=recursive_extract,
                                   delete_origin=delete_origin,
                                   top_window=top_window)

    def hide_float_button(self):
        """隐藏主页左上角的悬浮按钮"""
        self.viewer.hide_float_button()

    def set_float_button_enable(self, is_enable: bool):
        """设置悬浮按钮是否可用"""
        self.viewer.set_float_button_enable(is_enable)

    # 主页

    def turn_page_welcome(self):
        """切换到欢迎页"""
        self.viewer.turn_page_welcome()

    # 步骤提示页

    def set_step_notice(self, notice: str):
        """设置步骤提示"""
        self.viewer.set_step_notice(notice)

    # 测试与解压页

    def set_task_count(self, count: int):
        """设置总进度：任务总数"""
        self._task_count = count

    def set_task_index(self, index: int):
        """设置总进度：当前任务索引"""
        self._task_index = index
        self.viewer.set_progress_total(f'{self._task_index}/{self._task_count}')
        # 更新当前文件的用时
        self.model.reset_current_time()

    def set_current_file(self, filepath: str):
        """设置当前处理的文件名"""
        filename = os.path.basename(filepath)
        self.viewer.set_current_file(filename, tooltip=filepath)

    def set_runtime_total(self, runtime: str):
        """设置总运行时间 0:00:00
        :param runtime: "0:00:00"格式的字符串"""
        self.viewer.set_runtime_total(runtime)

    def set_runtime_current(self, runtime: str):
        """设置当前文件的运行时间 0:00:00
        :param runtime: "0:00:00"格式的字符串"""
        self.viewer.set_runtime_current(runtime)

    def set_password_count(self, count: int):
        """设置密码进度：总数"""
        self._password_count = count

    def set_password_index(self, index: int):
        """设置密码进度：当前索引"""
        self._password_index = index
        self.viewer.set_progress_test(f'{self._password_index}/{self._password_count}')

    def set_current_password(self, password: str):
        """设置当前测试的密码"""
        self.viewer.set_current_password(password)

    def set_progress_extract(self, progress: int):
        """设置解压的进度 1%
        :param progress: 0~100的整数"""
        self.viewer.set_progress_extract(progress)

    def set_current_file_step_tip(self, tip: str):
        """设置当前处理的文件的步骤提示"""
        self.viewer.set_current_file_step_tip(tip)

    # 结果页

    def show_time_final(self):
        """设置全部任务结束后的总耗时"""
        self.viewer.show_time_final()

    def show_process_count(self, count: Union[int, str]):
        """设置处理的文件数量"""
        self.viewer.show_process_count(count)

    def show_result_count(self, result_info: str, result_info_tip: str = ''):
        """设置处理结果的统计"""
        self.viewer.show_result_count(result_info, result_info_tip)

    # 具体运行状态

    def _show_test_page(self):
        """切换到测试和解压页"""
        self.viewer.turn_page_test_and_extract()
        self.viewer.set_child_page_test()

    def set_info_testing(self):
        """设置运行状态：测试中"""
        self.set_icon_testing()
        self._show_test_page()

    def set_info_extracting(self):
        """设置运行状态：解压中"""
        self.set_icon_extracting()
        self._show_test_page()

    def set_info_skip(self):
        """设置运行状态：跳过（没有需要处理的文件时）"""
        self.set_icon_skip()
        self.model.stop_timing()
        self.set_step_notice("没有需要处理的文件时")

    def set_info_exists_temp_folder(self, path: str = ''):
        """设置运行状态：终止（存在非空的临时解压文件夹）"""
        self.set_icon_warning()
        self.model.stop_timing()
        info = "存在临时解压文件夹，请检查相关目录"
        if path:
            info = info + '<br>' + f'<a href="file:///{path}">点击打开对应临时文件夹</a>'
        self.set_step_notice(info)

    def set_info_error_7zip_path(self):
        """设置运行状态：终止（7zip路径错误）"""
        self.set_icon_warning()
        self.model.stop_timing()
        self.set_step_notice("7Zip路径错误，请检查自定义路径")

    @staticmethod
    def _count_processed(result_info_tip: str) -> int:
        """从结果详情中提取处理数量并求和"""
        numbers = re.findall(r'\d+', result_info_tip)
        total = 0
        for number in numbers:
            total += int(number)
        return total

    def _show_final_result(self, result_info: str, result_info_tip: str):
        """显示结束后的计时和结果信息"""
        self.model.stop_timing()
        self.show_time_final()
        self.show_result_count(result_info, result_info_tip)
        self.show_process_count(self._count_processed(result_info_tip))

    def set_info_finished(self, result_info: str, result_info_tip: str = ''):
        """设置运行状态：完成所有任务"""
        self.set_icon_complete()
        self._show_final_result(result_info, result_info_tip)

    def show_info_stop(self, result_info: str, result_info_tip: str = ''):
        """设置运行状态：用户中断"""
        self.set_icon_stop()
        self._show_final_result(result_info, result_info_tip)

    def set_info_error(self):
        """设置运行状态：报错"""
        self.set_icon_error()
        self.model.stop_timing()
        self.set_step_notice("遇到致命性报错，请检查报错页并反馈\n重启程序后可再次使用")

    # 图标方法

    def set_icon_home(self):
        """设置主页图标"""
        self.viewer.set_icon(ICON_LOGO_PIXEL)

    def set_icon_complete(self):
        """设置完成图标"""
        self.viewer.set_icon(ICON_COMPLETE)

    def set_icon_skip(self):
        """设置跳过图标"""
        self.viewer.set_icon(ICON_SKIP)

    def set_icon_stop(self):
        """设置停止图标"""
        self.viewer.set_icon(ICON_STOPPED)

    def set_icon_warning(self):
        """设置警告图标"""
        self.viewer.set_icon(ICON_WARNING)

    def set_icon_extract(self):
        """设置解压模式图标"""
        self.viewer.set_gif_icon(ICON_EXTRACT)

    def set_icon_test(self):
        """设置测试模式图标"""
        self.viewer.set_gif_icon(ICON_TEST)

    def set_icon_extracting(self):
        """设置解压中图标"""
        self.viewer.set_gif_icon(ICON_EXTRACTING)

    def set_icon_testing(self):
        """设置测试中图标"""
        self.viewer.set_gif_icon(ICON_TESTING)

    def set_icon_error(self):
        """设置错误图标"""
        self.viewer.set_icon(ICON_WARNING_YELLOW)
