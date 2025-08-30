# 主窗口的桥梁组件
import os

import lzytools.file

from common import function_7zip, function_subprocess
from common.class_7zip import ModelArchive
from common.class_file_info import FileInfoList
from common.class_result_collector import ResultCollector
from components import page_home, page_password, page_setting, page_history, page_about
from components.window.thread_queue_receiver import ThreadQueueReceiver
from components.window.window_model import WindowModel
from components.window.window_viewer import WindowViewer


class WindowPresenter:
    """主窗口的桥梁组件"""

    def __init__(self, viewer: WindowViewer, model: WindowModel):
        self.viewer = viewer
        self.model = model

        # 程序标题
        self.app_title_default = 'OnlyUnzip'  # 程序默认标题

        # 结果收集类
        self.result_collector = ResultCollector()

        # 添加各个组件的实例对象
        self.page_home = page_home.get_presenter()
        self.viewer.add_page_home(self.page_home.viewer)
        self.page_password = page_password.get_presenter()
        self.viewer.add_page_password(self.page_password.viewer)
        self.page_setting = page_setting.get_presenter()
        self.viewer.add_page_setting(self.page_setting.viewer)
        self.page_history = page_history.get_presenter()
        self.viewer.add_page_history(self.page_history.viewer)
        self.page_about = page_about.get_viewer()
        self.viewer.add_page_about(self.page_about)

        # 绑定接收线程
        self.queue_receiver = ThreadQueueReceiver()
        self.queue_receiver.Data.connect(self.update_extract_progress)
        self.queue_receiver.start()

        # 传参
        self.set_model_setting()

        # 修改窗口属性
        self._get_window_setting()

        # 绑定信号
        self.page_setting.SignalTopWindow.connect(self.top_window)
        self.page_setting.SignalLockSize.connect(self.lock_size)
        self.page_setting.SignalChangeArchiveModel.connect(self.set_app_title_suffix)
        self.page_home.FileInfo.connect(self.accept_file_info_list)  # 接收文件信息类
        self.page_home.SignalNoFiles.connect(self.finished_by_no_files)
        self.page_home.SignalExistsTempFolder.connect(self.finished_by_temp_folder)
        self.page_home.UserStop.connect(self.finished_by_user_stop)
        self.page_home.OpenAbout.connect(self.open_about)
        self._bind_model_signal()

    def accept_paths_from_cmd(self, paths: list):
        """接收命令行参数"""
        self.page_home.drop_paths(paths)

    def accept_file_info_list(self, file_info: FileInfoList):
        """接收文件信息类，传递给模型组件"""
        # 锁定设置项，防止被修改
        self.page_setting.lock_setting()
        # 传递文件信息类前传递必要参数
        self.set_model_passwords()
        self.set_model_setting()
        # 传递给模型组件
        self.show_page_test_or_extract()
        self.model.accept_files(file_info)

    def set_model_passwords(self):
        """传递密码组件的密码列表给模型组件"""
        passwords = self.page_password.get_passwords()
        self.model.set_passwords(passwords)

    def set_model_setting(self):
        """传递设置组件的设置项给模型组件"""
        archive_model = self.page_setting.model.get_model_archive()
        self.model.set_archive_model(archive_model)

        read_pw_from_filename = self.page_setting.model.get_read_password_from_filename_is_enable()
        self.model.set_is_read_password_from_filename(read_pw_from_filename)

        is_write_filename = self.page_setting.model.get_write_filename_is_enable()
        write_filename_left_part = self.page_setting.model.get_write_filename_left_word()
        write_filename_right_part = self.page_setting.model.get_write_filename_right_word()
        write_filename_position = self.page_setting.model.get_write_filename_position()
        self.model.set_is_write_filename(is_write_filename)
        self.model.set_write_filename_left_word(write_filename_left_part)
        self.model.set_write_filename_right_word(write_filename_right_part)
        self.model.set_write_filename_position(write_filename_position)

        extract_model = self.page_setting.model.get_model_extract()
        self.model.set_extract_model(extract_model)

        delete_file = self.page_setting.model.get_delete_file_is_enable()
        self.model.set_is_delete_file(delete_file)

        recursive_extract = self.page_setting.model.get_recursive_extract_is_enable()
        self.model.set_is_recursive_extract(recursive_extract)

        cover_model = self.page_setting.model.get_model_cover()
        self.model.set_cover_model(cover_model)

        is_break_folder = self.page_setting.model.get_break_folder_is_enable()
        break_folder_model = self.page_setting.model.get_break_folder_model()
        self.model.set_is_break_folder(is_break_folder)
        self.model.set_break_folder_model(break_folder_model)

        is_extract_to_folder = self.page_setting.model.get_extract_output_folder_is_enable()
        extract_output_folder = self.page_setting.model.get_extract_output_folder_path()
        self.model.set_is_extract_to_folder(is_extract_to_folder)
        self.model.set_extract_output_folder(extract_output_folder)

        is_filter = self.page_setting.model.get_extract_filter_is_enable()
        filter_rule = self.page_setting.model.get_extract_filter_rules()
        self.model.set_is_filter(is_filter)
        self.model.set_filter_rules(filter_rule)

    def show_page_test_or_extract(self):
        """显示主页为测试页或解压页"""
        archive_model = self.page_setting.model.get_model_archive()
        if isinstance(archive_model, ModelArchive.Test):
            self.page_home.set_info_testing()
        elif isinstance(archive_model, ModelArchive.Extract):
            self.page_home.set_info_extracting()

    def open_about(self):
        self.viewer.open_page_about()

    def finished(self, results: FileInfoList):
        """处理结束信号"""
        # 解锁设置项
        self.page_setting.unlock_setting()

        # 接收到结束信号后，先传递给收集器，收集处理结果
        self.collect_result(results)

        # 如果有解压成功的文件，则增加对应密码的使用次数
        passwords_success = results.get_success_passwords()
        print('处理成功的密码', passwords_success)
        if passwords_success:
            self.page_password.update_use_count(passwords_success)
            self.page_password.show_pw_count_info()

        # 如果有成功处理的文件，则判断是否进行递归解压
        print('接收结束信号参数', results)
        if results.count_success():
            is_recursive_extract = self.page_setting.model.get_recursive_extract_is_enable()
            # 进行递归解压，并累计处理结果
            if is_recursive_extract:
                success_filepaths = results.get_success_files()
                self.page_home.drop_paths(success_filepaths, is_recursive=True)
            # 如果不需要进行递归解压，则结束本批次任务，显示结束信息
            else:
                result_info_simple, file_info_detail = self.result_collector.get_result_info()
                self.page_home.set_info_finished(result_info_simple, result_info_tip=file_info_detail)
        else:
            result_info_simple, file_info_detail = self.result_collector.get_result_info()
            self.page_home.set_info_finished(result_info_simple, result_info_tip=file_info_detail)

    def finished_by_no_files(self):
        """提前终止：由于主页模块信号-没有需要处理的文件"""
        # 解锁设置项
        self.page_setting.unlock_setting()
        # 如果没有处理任何文件就结束，则直接显示Skip提示，否则显示正常计数信息（递归解压到没有需要解压的文件）
        if not self.result_collector.get_count_all_result():
            self.page_home.set_info_skip()
        else:
            finish_info_simple, file_info_detail = self.result_collector.get_result_info()
            self.page_home.set_info_finished(finish_info_simple, result_info_tip=file_info_detail)

    def finished_by_temp_folder(self, path: str = ''):
        """提前终止：由于主页模块信号-存在临时文件夹"""
        # 解锁设置项
        self.page_setting.unlock_setting()

        self.page_home.set_info_exists_temp_folder(path)

    def finished_by_user_stop(self):
        """提前终止：用户主动终止"""
        # 解锁设置项
        self.page_setting.unlock_setting()
        # 更新主页信息
        finish_info_simple, file_info_detail = self.result_collector.get_result_info()
        self.page_home.set_info_finished(finish_info_simple, result_info_tip=file_info_detail)
        # 终止调用线程
        self.model.stop_task()
        process = function_7zip.get_running_process()
        function_subprocess.stop_process(process)

    def update_extract_progress(self, progress: int):
        """更新解压进度"""
        self.page_home.set_progress_extract(progress)

    def collect_result(self, results: FileInfoList):
        """收集结果，用于展示当前批次任务的结果情况"""
        for file_info in results.get_file_infos():
            result = file_info.get_7zip_result()
            self.result_collector.add_result(result)

    def delete_temp_folder_if_exists(self, results: FileInfoList):
        """删除可能存在的临时文件夹"""
        for file_info in results.get_file_infos():
            extract_path = file_info.extract_path
            # 临时解压文件夹只会在解压结果目录的同级目录中
            if extract_path:
                parent_folder = os.path.dirname(extract_path)
                temp_folder = function_7zip.get_temp_dirpath(parent_folder)
                if os.path.exists(temp_folder):
                    lzytools.file.delete_empty_folder(temp_folder, send_to_trash=False)

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
        """在程序标题后添加后缀：[测试]/[解压]"""
        print(1)
        archive_model = self.page_setting.get_archive_model()
        suffix = ''
        if isinstance(archive_model, ModelArchive.Test):
            suffix = '[测试]'
        elif isinstance(archive_model, ModelArchive.Extract):
            suffix = '[解压]'

        new_title = f'{self.app_title_default} {suffix}'
        self.viewer.setWindowTitle(new_title)

    def _get_window_setting(self):
        """提取window相关设置"""
        is_top_window = self.page_setting.model.get_top_window_is_enable()
        self.top_window(is_top_window)

        is_lock_size = self.page_setting.model.get_lock_size_is_enable()
        if is_lock_size:
            width = self.page_setting.model.get_lock_size_width()
            height = self.page_setting.model.get_lock_size_height()
            self.viewer.resize(width, height)
        self.lock_size(is_lock_size)

    def _bind_model_signal(self):
        """绑定模型信号，链接到其他组件"""
        self.model.SignalCurrentFile.connect(self.page_home.set_current_file)
        self.model.SignalTaskCount.connect(self.page_home.set_task_count)
        self.model.SignalTaskIndex.connect(self.page_home.set_task_index)
        self.model.SignalCurrentPw.connect(self.page_home.set_current_password)
        self.model.SignalPwCount.connect(self.page_home.set_password_count)
        self.model.SignalPwIndex.connect(self.page_home.set_password_index)
        self.model.SignalResult.connect(self.page_history.collection_history)
        self.model.SignalStart.connect(None)
        self.model.SignalFinish.connect(self.finished)
        self.model.StepInfo.connect(self.page_home.set_current_file_step_tip)
