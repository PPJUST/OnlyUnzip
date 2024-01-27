import os
import re
import time

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QMovie, QPalette
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMenu, QFileDialog, QMessageBox

import module.function_file
import module.function_filetype
import module.function_password
from constant import _ICON_TEST_GIF, _ICON_EXTRACT_GIF, _ICON_MAIN, _ICON_DEFAULT, _ICON_DEFAULT_WITH_OUTPUT, \
    _ICON_ERROR, \
    _ICON_FINISH, _PASSWORD_EXPORT
from module import function_config, function_password
from module import function_static
from module.function_config import Config
from qthread_7zip import ExtractQthread
from ui.drop_label import DropLabel
from ui.ui_main import Ui_MainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 添加自定义控件
        self.dropped_label = DropLabel()
        self.ui.verticalLayout_dropped_label.addWidget(self.dropped_label)




        # 初始化
        function_static.init_settings()  # 检查初始文件
        self.load_config()
        self.check_output_folder()
        self.icon_gif_droplabel = None  # 动图对象，显示在拖入控件中

        # 设置ui
        self.ui.stackedWidget_main.setCurrentIndex(0)  # 将主页面设为第1页
        self.ui.stackedWidget_schedule.setCurrentIndex(0)  # 将信息页设为第1页
        self.change_page(self.ui.buttonGroup.id(self.ui.buttonGroup.buttons()[0]))  # 设置第一个按钮的颜色

        # 实例化子线程
        # self.qthread = ExtractQthread()
        # self.qthread.signal_update_ui.connect(self.update_ui)
        # self.qthread.signal_extracted_files.connect(lambda x: self.accept_files(x))

        # 设置槽函数
        # 标签页
        self.ui.buttonGroup.buttonClicked[int].connect(self.change_page)
        # 主页
        self.dropped_label.signal_dropped.connect(self.dropped_files)
        self.ui.button_stop.clicked.connect(self.stop_qthread)
        # 密码
        self.ui.button_update_password.clicked.connect(self.update_password)
        self.ui.button_read_clipboard.clicked.connect(self.read_clipboard)
        self.ui.button_export_password.clicked.connect(lambda: function_password.export_password)
        self.ui.button_export_password.clicked.connect(lambda: self.ui.button_open_password.setEnabled(True))
        self.ui.button_open_password.clicked.connect(lambda: os.startfile(_PASSWORD_EXPORT))




    def load_config(self):
        """读取配置文件，更新选项"""
        # 读取
        config = Config()
        setting_mode = config.mode
        setting_handling_nested_folder = config.handling_nested_folder
        setting_handling_nested_archive = config.handling_nested_archive
        setting_delete_original_file = config.delete_original_file
        setting_check_filetype = config.check_filetype
        setting_exclude_rules = config.exclude_rules
        setting_output_folder = config.output_folder

        # 更新选项
        if setting_mode == 'extract':
            self.ui.checkBox_mode_extract.setChecked(True)
            self.set_checkbox_enable(mode=True)
        elif setting_mode == 'test':
            self.ui.checkBox_mode_test.setChecked(True)
            self.set_checkbox_enable(mode=False)
        self.ui.checkBox_handling_nested_folder.setChecked(setting_handling_nested_folder)
        self.ui.checkBox_handling_nested_archive.setChecked(setting_handling_nested_archive)
        self.ui.checkBox_delete_original_file.setChecked(setting_delete_original_file)
        self.ui.checkBox_check_filetype.setChecked(setting_check_filetype)
        self.ui.lineEdit_exclude_rules.setText(' '.join(setting_exclude_rules))
        self.ui.lineEdit_output_folder.setText(setting_output_folder)

    def set_checkbox_enable(self, mode=True):
        """切换模式后启用/禁用相关设置项"""
        self.ui.checkBox_delete_original_file.setEnabled(mode)
        self.ui.checkBox_check_filetype.setEnabled(mode)
        self.ui.checkBox_handling_nested_folder.setEnabled(mode)
        self.ui.checkBox_handling_nested_archive.setEnabled(mode)
        self.ui.lineEdit_output_folder.setEnabled(mode)
        self.ui.lineEdit_exclude_rules.setEnabled(mode)

    def check_output_folder(self):
        """检查是否指定了解压输出路径，并修改相关ui显示"""
        output_dir = self.ui.lineEdit_output_folder.text()
        if output_dir:
            if not os.path.exists(output_dir) or os.path.isfile(output_dir):
                self.ui.lineEdit_output_folder.setStyleSheet('border: 1px solid red;')
                self.dropped_label.reset_icon(_ICON_DEFAULT)
            else:
                self.ui.lineEdit_output_folder.setStyleSheet('')
                self.dropped_label.reset_icon(_ICON_DEFAULT_WITH_OUTPUT)
        else:
            self.ui.lineEdit_output_folder.setStyleSheet('')
            self.dropped_label.reset_icon(_ICON_DEFAULT)

    def change_page(self, button_id):
        """切换标签页，并高亮被点击的标签页按钮"""
        # 切换标签页
        new_page_number = self.ui.buttonGroup.buttons().index(self.ui.buttonGroup.button(button_id))
        self.ui.stackedWidget_main.setCurrentIndex(new_page_number)

        # 高亮被点击的按钮
        original_style = self.ui.button_update_password.styleSheet()
        for button in self.ui.buttonGroup.buttons():
            button.setStyleSheet(original_style)

        clicked_style = r'background-color: rgb(255, 228, 181);'
        clicked_button = self.ui.buttonGroup.button(button_id)
        clicked_button.setStyleSheet(clicked_style)

    def dropped_files(self, paths: list):
        """拖入文件后进行测试或解压"""
        file_list = []
        for path in paths:
            path = os.path.normpath(path)
            if os.path.exists(path):
                if os.path.isfile(path):
                    file_list.append(path)
                else:
                    walk_files = module.function_file.get_files_list(path)
                    file_list += walk_files
        file_list = list(set(file_list))

        self.start_thread(file_list)

    """
    密码相关
    """
    def update_password(self):
        """更新密码"""
        add_pw = [n for n in self.ui.text_password.toPlainText().split('\n') if n.strip()]
        add_pw_strip = [n.strip() for n in add_pw]
        pw_list = list(set(add_pw + add_pw_strip))  # 考虑到密码两端的空格，需要添加两种形式的密码
        module.function_password.update_password(pw_list)
        self.ui.text_password.clear()

    def read_clipboard(self):
        """读取剪切板"""
        clipboard = QApplication.clipboard()
        self.ui.text_password.setPlainText(clipboard.text())

    def export_password(self, with_count:bool = False):
        """导出明文密码"""
        function_password.export_password(with_count)




def main():
    app = QApplication()
    app.setStyle('Fusion')
    # 设置白色背景色
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    app.setPalette(palette)

    show_ui = Main()
    show_ui.setWindowIcon(QIcon(_ICON_MAIN))
    show_ui.setFixedSize(262, 232)
    show_ui.show()
    app.exec_()


if __name__ == "__main__":
    main()
