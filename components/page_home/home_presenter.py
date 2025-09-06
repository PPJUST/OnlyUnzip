# 主页模块的桥梁组件
import os
import re
from typing import Union

from PySide6.QtCore import Signal, QObject

from common import function_setting, function_extract
from common.class_7zip import ModelArchive
from common.class_file_info import FileInfoList
from common.thread_filetype_archive import ThreadFiletypeArchive
from components.page_home.home_model import HomeModel
from components.page_home.home_viewer import HomeViewer
from components.page_home.res.icon_base64 import *


class HomePresenter(QObject):
    """主页模块的桥梁组件"""
    UserStop = Signal(name="用户主动停止")
    FileInfo = Signal(FileInfoList, name='提取的文件信息类')
    SignalNoFiles = Signal(name='没有需要处理的文件')
    SignalExistsTempFolder = Signal(str, name='存在临时文件夹，接收临时文件夹路径参数')
    OpenAbout = Signal(name="打开关于页")
    OpenTempPassword = Signal(name="打开临时密码页")

    def __init__(self, viewer: HomeViewer, model: HomeModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # 统计变量
        self._task_count: int = 0
        self._task_index: int = 0
        self._password_count: int = 0
        self._password_index: int = 0

        # 初始化
        self.set_icon_home()

        # 检查文件类型的子线程（防止堵塞ui线程）
        self.thread_check_filetype = ThreadFiletypeArchive()
        self.thread_check_filetype.Archives.connect(self.deal_archive_files)

        # 绑定信号
        self.viewer.UserStop.connect(self.UserStop.emit)
        self.viewer.DropFiles.connect(self.drop_paths)
        self.viewer.OpenAbout.connect(self.OpenAbout.emit)
        self.viewer.OpenTempPassword.connect(self.OpenTempPassword.emit)
        self.model.RuntimeTotal.connect(self.set_runtime_total)
        self.model.RuntimeCurrent.connect(self.set_runtime_current)

    def drop_paths(self, paths: list, is_recursive: bool = False):
        """拖入文件
        :param paths: 文件路径
        :param is_recursive: 是否是递归解压模式进行的文件操作"""
        print('接收文件列表，进行后续处理')
        # 启动模型组件的定时器
        if not is_recursive:
            self.model.start_timing()
        # 提取路径中包含的所有文件
        self.set_step_notice("""搜索文件中...""")
        files = self.model.get_files(paths)
        # 如果没有提取到文件，则不需要进行后续处理，直接终止
        if not files:
            self.SignalNoFiles.emit()
            return

        # 如果是解压模式，则检查文件路径同目录中是否存在解压用临时文件夹，如果存在且不为空文件夹，则直接终止
        archive_model = function_setting.get_archive_model()
        if isinstance(archive_model, ModelArchive.Extract):
            self.set_step_notice("""检查临时文件夹中...""")
            # 如果指定了解压输出目录，则只需要检查该目录
            target_path = function_setting.get_extract_output_folder()
            if target_path:
                is_temp_exists, temp_path = function_extract.is_exists_temp_folder(target_path)
            else:  # 否则检查所有文件所在路径
                is_temp_exists, temp_path = function_extract.is_exists_temp_folder(files)
            if is_temp_exists:
                self.SignalExistsTempFolder.emit(temp_path)
                return

        # 如果勾选了仅处理压缩文件，则进行一次筛选，剔除非压缩文件
        self.set_step_notice("""检查文件类型中...""")
        is_try_unknown_filetype = function_setting.get_is_try_unknown_filetype()
        # filetype库无法正确识别分卷压缩包的文件类型，并且通过读取文件头检查文件类型的方法速度较慢
        # 所以先检查文件名再进行文件头检查
        # 待优化：文件较多时，读取文件头速度较慢，会堵塞UI线程（先仅用文件名判断的方法）
        if not is_try_unknown_filetype:
            self.thread_check_filetype.set_files(files)
            self.thread_check_filetype.start()
        else:
            self.deal_archive_files(files)

    def deal_archive_files(self, archives: list):
        """处理压缩文件"""
        # 区分普通压缩文件和分卷压缩文件，便于后续处理
        archive_spliter = self.model.split_volume_archive(archives)

        # 如果没有需要处理的文件，则直接终止
        if not archive_spliter.is_has_archives():
            self.SignalNoFiles.emit()
            return

        # 将分类对象转换为文件信息类
        file_info_list = FileInfoList()
        for file in archive_spliter.get_files():
            role = archive_spliter.get_role(file)
            group_files = archive_spliter.get_members(file)
            file_info_list.add_file(file, role, group_files)

        # 发送信号，传递文件信息类
        self.FileInfo.emit(file_info_list)

    def banned_drop(self):
        """禁止拖入文件"""
        self.viewer.banned_drop()

    def allowed_drop(self):
        """允许拖入文件"""
        self.viewer.allowed_drop()

    """主页"""

    def turn_page_welcome(self):
        """切换到欢迎页"""
        self.viewer.turn_page_welcome()

    """步骤提示页"""

    def set_step_notice(self, notice: str):
        """设置步骤提示"""
        self.viewer.set_step_notice(notice)

    """测试与解压页"""

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

    """结果页"""

    def show_time_final(self):
        """设置全部任务结束后的总耗时"""
        self.viewer.show_time_final()

    def show_process_count(self, count: Union[int, str]):
        """设置处理的文件数量"""
        self.viewer.show_process_count(count)

    def show_result_count(self, result_info: str, result_info_tip: str = ''):
        """设置处理结果的统计"""
        self.viewer.show_result_count(result_info, result_info_tip)

    """具体运行状态"""

    def set_info_testing(self):
        """设置运行状态 测试中"""
        # 修改图标
        self.set_icon_testing()
        # 显示为测试页
        self.viewer.turn_page_test_and_extract()
        self.viewer.set_child_page_test()

    def set_info_extracting(self):
        """设置运行状态 解压中"""
        # 修改图标
        self.set_icon_extracting()
        # 显示为测试页
        self.viewer.turn_page_test_and_extract()
        self.viewer.set_child_page_test()  # 不设置为解压页，在读取到解压进度时自动设置

    def set_info_skip(self):
        """设置运行状态 跳过（没有需要处理的文件时）"""
        # 修改图标
        self.set_icon_skip()
        # 停止计时器
        self.model.stop_timing()
        # 显示步骤信息
        self.set_step_notice("没有需要处理的文件时")

    def set_info_exists_temp_folder(self, path: str = ''):
        """设置运行状态 终止（存在非空的临时解压文件夹）"""
        # 修改图标
        self.set_icon_warning()
        # 停止计时器
        self.model.stop_timing()
        # 显示步骤信息
        info = "存在临时解压文件夹，请检查相关目录"
        if path:
            link_text = f'<a href="file:///{path}">点击打开对应临时文件夹</a>'
            info = info + '<br>' + link_text
        self.set_step_notice(info)

    def set_info_finished(self, result_info: str, result_info_tip: str = ''):
        """设置运行状态 完成所有任务，结束"""
        # 修改图标
        self.set_icon_complete()
        # 停止计时器
        self.model.stop_timing()
        # 显示结果信息
        self.show_time_final()
        self.show_result_count(result_info, result_info_tip)
        # 根据结果文本提取总数
        numbers = re.findall(r'\d+', result_info_tip)
        total_sum = sum(int(num) for num in numbers)
        self.show_process_count(total_sum)

    def show_info_stop(self, result_info: str, result_info_tip: str = ''):
        """设置运行状态 用户中断"""
        # 修改图标
        self.set_icon_stop()
        # 停止计时器
        self.model.stop_timing()
        # 显示结果信息
        self.show_time_final()
        self.show_result_count(result_info, result_info_tip)
        # 根据结果文本提取总数
        numbers = re.findall(r'\d+', result_info_tip)
        total_sum = sum(int(num) for num in numbers)
        self.show_process_count(total_sum)

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
