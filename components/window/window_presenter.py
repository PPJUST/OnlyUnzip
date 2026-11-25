# 主窗口的桥梁组件

import sys

import lzytools
from lzytools_Qt import ObjectEmittingStream

from common import function_7zip, function_subprocess
from common.class_7zip import ModelArchive
from common.class_file_info import FileInfoList
from common.class_result_collector import ResultCollector
from components import page_home, page_password, page_setting, page_history, page_about, page_password_manager, \
    dialog_temp_password, page_error_info
from components.window.thread_queue_receiver import ThreadQueueReceiver
from components.window.window_model import WindowModel
from components.window.window_viewer import WindowViewer


class WindowPresenter:
    """主窗口的桥梁组件"""

    def __init__(self, viewer: WindowViewer, model: WindowModel):
        self.viewer = viewer
        self.model = model

        self.app_title_default = 'OnlyUnzip'  # 程序默认标题
        self.result_collector = ResultCollector()
        self.passwords_used = []  # 本次运行中使用成功的密码
        self.is_user_stop = False  # 用户是否主动终止任务

        self._setup_stderr()
        self._setup_pages()
        self._setup_queue_receiver()
        self._restore_window_setting()
        self._bind_page_signals()
        self._bind_model_signal()

    def _setup_stderr(self):
        """打包运行时把标准错误输出显示到报错页面"""
        is_packed = getattr(sys, 'frozen', False) or getattr(sys, '_nuitka', False) or '__compiled__' in globals()
        if not is_packed:
            return
        self.stderr_stream = ObjectEmittingStream()
        self.stderr_stream.TextWritten.connect(self.show_stderr_info)
        sys.stderr = self.stderr_stream

    def _setup_pages(self):
        """创建各个页面组件并添加到主窗口"""
        self.page_home = page_home.get_presenter()
        self.viewer.add_page('home', self.page_home.viewer)

        self.page_password = page_password.get_presenter()
        self.viewer.add_page('password', self.page_password.viewer)

        self.page_setting = page_setting.get_presenter()
        self.viewer.add_page('setting', self.page_setting.viewer)

        self.page_history = page_history.get_presenter()
        self.viewer.add_page('history', self.page_history.viewer)

        self.page_error_info = page_error_info.get_presenter()
        self.viewer.add_page('error', self.page_error_info.viewer)

        self.page_about = page_about.get_viewer()
        self.viewer.add_page('about', self.page_about)

        self.page_password_manager = page_password_manager.get_presenter()
        self.viewer.add_page('password_manager', self.page_password_manager.viewer)

        self.dialog_temp_password = dialog_temp_password.get_presenter()

    def _setup_queue_receiver(self):
        """启动接收解压进度的线程"""
        self.queue_receiver = ThreadQueueReceiver()
        self.queue_receiver.Data.connect(self.update_extract_progress)
        self.queue_receiver.start()

    def _bind_page_signals(self):
        """绑定页面组件的信号"""
        self.page_setting.SignalTopWindow.connect(self.top_window)
        self.page_setting.SignalLockSize.connect(self.lock_size)
        self.page_setting.SignalChangeArchiveModel.connect(self.set_app_title_suffix)

        self.page_home.FileInfo.connect(self.accept_file_info_list)
        self.page_home.SignalNoFiles.connect(self.finished_by_no_files)
        self.page_home.SignalExistsTempFolder.connect(self.finished_by_temp_folder)
        self.page_home.SignalError7ZipPath.connect(self.finished_by_error_7zip_path)
        self.page_home.UserStop.connect(self.finished_by_user_stop)
        self.page_home.UserStopAfter.connect(self.finished_by_user_stop_after_current)
        self.page_home.OpenAbout.connect(self.open_about)
        self.page_home.OpenTempPassword.connect(self.open_temp_password)
        self.page_home.AskUpdateSetting.connect(self.set_home_setting)
        self.page_home.ChangeSettingArchiveModel.connect(self.page_setting.change_archive_model)
        self.page_home.ChangeSettingTryUnknownFiletype.connect(self.page_setting.change_unknown_filetype)
        self.page_home.ChangeSettingRecursiveExtract.connect(self.page_setting.change_recursive_extract)
        self.page_home.ChangeSettingDeleteOrigin.connect(self.page_setting.change_delete_file)
        self.page_home.ChangeSettingTopWindow.connect(self.page_setting.change_top_window)

        self.page_password.OpenPasswordManager.connect(self.open_password_manager)
        self.page_password_manager.SignalDeleted.connect(self.deleted_passwords)
        self.dialog_temp_password.WriteToDB.connect(self.write_temp_pws_to_db)

        self.viewer.PageChanged.connect(self._page_changed)

    def _bind_model_signal(self):
        """绑定模型信号，转发给对应组件"""
        self.model.SignalCurrentFile.connect(self.page_home.set_current_file)
        self.model.SignalTaskCount.connect(self.page_home.set_task_count)
        self.model.SignalTaskCount.connect(self.viewer.set_progress_count)
        self.model.SignalTaskIndex.connect(self.page_home.set_task_index)
        self.model.SignalTaskIndex.connect(self.viewer.set_progress_index)
        self.model.SignalCurrentPw.connect(self.page_home.set_current_password)
        self.model.SignalPwCount.connect(self.page_home.set_password_count)
        self.model.SignalPwIndex.connect(self.page_home.set_password_index)
        self.model.SignalResult.connect(self.page_history.collection_history)
        self.model.SignalFinish.connect(self.finished)
        self.model.StepInfo.connect(self.page_home.set_current_file_step_tip)

    def accept_paths_from_cmd(self, paths: list):
        """接收命令行参数"""
        self.viewer.show_indeterminate_progress()
        self.is_user_stop = False
        self.page_home.drop_paths(paths)

    def accept_file_info_list(self, file_info: FileInfoList):
        """接收文件信息类，传递给模型组件"""
        self.viewer.show_indeterminate_progress()
        self.is_user_stop = False
        # 锁定设置项并禁用主页的拖入功能，防止任务执行中被修改
        self.page_setting.lock_setting()
        self.page_home.banned_drop()
        self.set_model_passwords()
        self.show_page_test_or_extract()
        self.model.accept_files(file_info)

    def set_model_passwords(self):
        """传递密码组件的密码列表给模型组件"""
        passwords = self.page_password.get_passwords()
        temp_passwords = self.dialog_temp_password.get_passwords()
        # 密码顺序：本次使用过的密码 + 临时密码 + 密码本
        joined = self.passwords_used + temp_passwords + passwords
        joined = lzytools.common.dedup_list(joined)
        self.model.set_passwords(joined)

    def show_page_test_or_extract(self):
        """把主页显示为测试页或解压页"""
        archive_model = self.page_setting.model.get_model_archive()
        if isinstance(archive_model, ModelArchive.Test):
            self.page_home.set_info_testing()
        elif isinstance(archive_model, ModelArchive.Extract):
            self.page_home.set_info_extracting()
        self.viewer.hide_button_error_info()

    def show_stderr_info(self, info: str):
        """显示报错信息"""
        self.viewer.show_error_progress()
        self.page_home.set_info_error()
        self.page_error_info.append_info(info)
        self.viewer.open_page('error')
        self.viewer.show_button_error_info()

    def open_about(self):
        self.viewer.open_page('about')

    def open_temp_password(self):
        self.dialog_temp_password.exec()

    def set_home_setting(self):
        """设置主页悬浮按钮所需的选项参数"""
        archive_model = self.page_setting.model.get_model_archive()
        try_unknown_filetype = self.page_setting.model.get_try_unknown_filetype_is_enable()
        delete_file = self.page_setting.model.get_delete_file_is_enable()
        recursive_extract = self.page_setting.model.get_recursive_extract_is_enable()
        top_window = self.page_setting.model.get_top_window_is_enable()

        self.page_home.update_setting(archive_model=archive_model,
                                      try_unknown_filetype=try_unknown_filetype,
                                      recursive_extract=recursive_extract,
                                      delete_origin=delete_file,
                                      top_window=top_window)

    def write_temp_pws_to_db(self, passwords):
        """将临时密码写入密码本"""
        self.page_password.update_password(passwords)

    def _reset_after_task(self, is_error=False):
        """任务结束后的通用处理：更新进度、解锁设置、恢复拖入功能"""
        if is_error:
            self.viewer.show_error_progress()
        else:
            self.viewer.show_finish_progress()
        self.page_setting.unlock_setting()
        self.page_home.allowed_drop()

    def _show_finish_info(self):
        """在主页显示当前批次的处理结果"""
        result_info_simple, file_info_detail = self.result_collector.get_result_info()
        self.page_home.set_info_finished(result_info_simple, result_info_tip=file_info_detail)

    def _filter_temp_passwords(self, passwords):
        """剔除不需要写入密码本的临时密码"""
        db_passwords = self.page_password.get_passwords()
        temp_passwords = self.dialog_temp_password.get_passwords()
        result = []
        for password in passwords:
            if password in temp_passwords and password not in db_passwords:
                continue
            result.append(password)
        return result

    def finished(self, results: FileInfoList):
        """处理结束信号"""
        self._reset_after_task()
        self.collect_result(results)

        # 记录本次使用成功的密码，并更新密码次数
        passwords_success = results.get_success_passwords()
        self.passwords_used += passwords_success
        print('处理成功的密码', passwords_success)
        filter_passwords = self._filter_temp_passwords(passwords_success)
        if filter_passwords:
            self.page_password.update_use_count(filter_passwords)
            self.page_password.show_pw_count_info()

        # 成功处理完文件后，根据设置决定是否递归解压
        print('接收结束信号参数', results)
        if not self.is_user_stop and not results.is_user_stop() and results.count_success():
            if self.page_setting.model.get_recursive_extract_is_enable():
                success_filepaths = results.get_success_files()
                self.page_home.drop_paths(success_filepaths, is_recursive=True)
                return
        self._show_finish_info()

    def finished_by_no_files(self):
        """提前终止：主页模块没有需要处理的文件"""
        self._reset_after_task()
        # 没有处理任何文件时显示 Skip；递归解压后无文件可解压时显示正常结果
        if not self.result_collector.get_count_all_result():
            self.page_home.set_info_skip()
        else:
            self._show_finish_info()

    def finished_by_temp_folder(self, path: str = ''):
        """提前终止：主页模块检测到临时文件夹"""
        self._reset_after_task(is_error=True)
        self.page_home.set_info_exists_temp_folder(path)

    def finished_by_error_7zip_path(self, path: str = ''):
        """提前终止：主页模块检测到 7zip 路径错误"""
        self._reset_after_task(is_error=True)
        self.page_home.set_info_error_7zip_path()

    def finished_by_user_stop(self):
        """提前终止：用户主动终止"""
        self._reset_after_task()
        self._show_finish_info()
        self._stop_running_task()
        process = function_7zip.get_running_process()
        function_subprocess.stop_process(process)

    def finished_by_user_stop_after_current(self):
        """提前终止：用户主动终止（完成当前任务后再终止）"""
        # 子线程仍在执行，任务结束信号到达后再统一解锁设置
        self.viewer.show_finish_progress()
        self._stop_running_task()

    def _stop_running_task(self):
        """标记用户终止状态并通知模型停止任务"""
        self.is_user_stop = True
        self.model.stop_task()

    def update_extract_progress(self, progress: int):
        """更新解压进度"""
        self.page_home.set_progress_extract(progress)

    def collect_result(self, results: FileInfoList):
        """收集结果，用于展示当前批次任务的结果情况"""
        for file_info in results.get_file_infos():
            result = file_info.get_7zip_result()
            self.result_collector.add_result(result)

    def top_window(self, is_enable: bool):
        """设置窗口置顶"""
        if is_enable:
            self.viewer.top_window()
        else:
            self.viewer.disable_top_window()

    def lock_size(self, is_enable: bool):
        """锁定窗口大小"""
        if is_enable:
            self.viewer.lock_size()
            self.page_setting.model.set_lock_size_width(self.viewer.width())
            self.page_setting.model.set_lock_size_height(self.viewer.height())
        else:
            self.viewer.disable_lock_size()

    def set_default_app_title(self, title: str):
        """设置默认程序标题"""
        self.app_title_default = title
        self.viewer.setWindowTitle(title)
        self.set_app_title_suffix()

    def set_app_title_suffix(self):
        """在程序标题后添加后缀：[T] 测试 / [E] 解压"""
        archive_model = self.page_setting.get_archive_model()
        suffix = ''
        if isinstance(archive_model, ModelArchive.Test):
            suffix = '[T]'
        elif isinstance(archive_model, ModelArchive.Extract):
            suffix = '[E]'
        self.viewer.setWindowTitle(f'{self.app_title_default} {suffix}')

    def _restore_window_setting(self):
        """根据设置恢复窗口置顶和尺寸状态"""
        is_top_window = self.page_setting.model.get_top_window_is_enable()
        self.top_window(is_top_window)

        is_lock_size = self.page_setting.model.get_lock_size_is_enable()
        if is_lock_size:
            width = self.page_setting.model.get_lock_size_width()
            height = self.page_setting.model.get_lock_size_height()
            self.viewer.resize(width, height)
        self.lock_size(is_lock_size)

    def open_password_manager(self):
        """打开密码管理器"""
        self.viewer.open_page('password_manager')
        self.page_password_manager.update_count()
        self.page_password_manager.hidden_preview()

    def deleted_passwords(self):
        """删除密码后更新相关信息"""
        self.page_password.reload()
        self.page_password.show_pw_count_info()
        self.open_password_manager()

    def _page_changed(self):
        """切换页面后的操作"""
        self.page_home.hide_float_button()
