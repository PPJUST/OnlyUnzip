# 主页模块的桥梁组件
import os

import lzytools
from PySide6.QtCore import Signal, QObject

from common import function_setting, function_extract
from common.class_7zip import ModelArchive
from common.class_file_info import FileInfoList
from components.page_home.home_model import HomeModel
from components.page_home.home_viewer import HomeViewer
from components.page_home.res.icon_base64 import *


class HomePresenter(QObject):
    """主页模块的桥梁组件"""
    FileInfo = Signal(FileInfoList, name='提取的文件信息类')

    def __init__(self, viewer: HomeViewer, model: HomeModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # 统计变量
        self._task_count:int = 0
        self._task_index:int = 0
        self._password_count:int=0
        self._password_index:int = 0

        # 绑定信号
        self.viewer.Stop.connect(self.stop)
        self.viewer.DropFiles.connect(self.drop_paths)
        self.model.RuntimeTotal.connect(self.viewer.set_runtime_total)
        self.model.RuntimeCurrent.connect(self.viewer.set_runtime_current)

    def drop_paths(self, paths: list):
        """拖入文件"""
        print('接收文件列表，进行后续处理')
        # 启动模型组件的定时器
        self.model.start_timing()
        # 提取路径中包含的所有文件
        files = self.model.get_files(paths)
        # 如果没有提取到文件，则不需要进行后续处理，直接终止
        if not files:
            self.set_info_skip()
            return

        # 如果是解压模式，则检查文件路径同目录中是否存在解压用临时文件夹，如果存在且不为空文件夹，则直接终止
        archive_model = function_setting.get_archive_model()
        if isinstance(archive_model, ModelArchive.Extract):
            # 如果指定了目标解压目录，则只需要检查该目录
            target_path = function_setting.get_extract_output_folder()
            if target_path:
                is_temp_exists = function_extract.is_exists_temp_folder(target_path)
            else:  # 否则检查所有文件所在路径
                is_temp_exists = function_extract.is_exists_temp_folder(files)
            if is_temp_exists:
                self.set_info_exists_temp_folder()
                return

        # 如果勾选了仅处理压缩文件，则进行一次筛选，剔除非压缩文件
        is_try_unknown_filetype = function_setting.get_is_try_unknown_filetype()
        # filetype库无法正确识别分卷压缩包的文件类型，并且通过读取文件头检查文件类型的方法速度较慢
        # 所以最后决定先检查文件名再进行文件头检查
        # 待优化：文件较多时，读取文件头速度较慢，会堵塞UI线程
        if not is_try_unknown_filetype:
            files = [file for file in files
                     if lzytools.archive.is_archive_by_filename(os.path.basename(file))
                     or lzytools.archive.is_archive(file)]

        # 区分普通压缩文件和分卷压缩文件，便于后续处理
        archive_spliter = self.model.split_volume_archive(files)

        # 如果没有需要处理的文件，则直接终止
        if not archive_spliter.is_has_archives():
            self.set_info_skip()
            return

        # 将分类对象转换为文件信息类
        file_info_list = FileInfoList()
        for file in archive_spliter.get_files():
            role = archive_spliter.get_role(file)
            group_files = archive_spliter.get_members(file)
            file_info_list.add_file(file, role, group_files)

        # 发送信号，传递文件信息类
        self.FileInfo.emit(file_info_list)

    def stop(self):
        """终止当前任务"""
        self.stop_timer()




    def set_task_count(self, count: int):
        """设置总进度：任务总数"""
        self._task_count = count


    def set_task_index(self, index: int):
        """设置总进度：当前任务索引"""
        self._task_index = index
        self.viewer.set_progress_total(f'{self._task_index}/{self._task_count}')






    def set_current_file(self, filename: str):
        """设置当前处理的文件名"""
        self.viewer.set_current_file(filename)

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

    def stop_timer(self):
        """停止模型组件的计时器"""
        self.model.stop_timing()
    """各类状态"""

    def set_info_skip(self):
        """设置运行状态 跳过（没有需要处理的文件时）"""
        # 修改图标
        self.set_icon_skip()
        # 修改文本
        self.viewer.set_page_test()
        self.viewer.set_progress_total('-/-')
        self.viewer.set_current_file('没有需要处理的文件')
        self.viewer.set_runtime_current('0:00:00')
        self.viewer.set_progress_test('-/-')
        self.viewer.set_current_password('...')

    def set_info_exists_temp_folder(self):
        """设置运行状态 终止（存在非空的临时解压文件夹）"""
        # 修改图标
        self.set_icon_warning()
        # 修改文本
        self.viewer.set_page_test()
        self.viewer.set_progress_total('-/-')
        self.viewer.set_current_file('存在临时解压文件夹，请检查解压目录')
        self.viewer.set_runtime_current('0:00:00')
        self.viewer.set_progress_test('-/-')
        self.viewer.set_current_password('...')
    def set_info_finished(self,finish_info:str,tooltip:str=''):
        """设置运行状态 完成所有任务，结束"""
        # 修改图标
        self.set_icon_complete()
        # 修改文本
        self.viewer.set_page_test()
        self.viewer.set_progress_total('-/-')
        self.viewer.set_current_file(finish_info, tooltip)
        self.viewer.set_runtime_current('-:-:-')
        self.viewer.set_progress_test('-/-')
        self.viewer.set_current_password('...')

    """icon方法"""

    def set_default_icon_test(self):
        """设置默认图标为测试模式"""
        self.viewer.set_default_icon(ICON_TEST)

    def set_default_icon_extract(self):
        """设置默认图标为解压模式"""
        self.viewer.set_default_icon(ICON_EXTRACT)

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
