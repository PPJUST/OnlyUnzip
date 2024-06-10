# 主程序
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow

from constant import _ICON_HOMEPAGE, _ICON_PASSWORD, _ICON_SETTING, _ICON_HISTORY
from ui.src.ui_main import Ui_MainWindow
from ui.widget_page_history import ListWidgetHistory
from ui.widget_page_homepage import WidgetPageHomepage
from ui.widget_page_password import WidgetPagePassword
from ui.widget_page_setting import WidgetPageSetting


class OnlyUnzip(QMainWindow):
    def __init__(self, paths: list, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ui设置
        self.ui.pushButton_page_homepage.setProperty('id', 0)
        self.ui.pushButton_page_homepage.setIcon(QIcon(_ICON_HOMEPAGE))
        self.ui.pushButton_page_password.setProperty('id', 1)
        self.ui.pushButton_page_password.setIcon(QIcon(_ICON_PASSWORD))
        self.ui.pushButton_page_setting.setProperty('id', 2)
        self.ui.pushButton_page_setting.setIcon(QIcon(_ICON_SETTING))
        self.ui.pushButton_page_history.setProperty('id', 3)
        self.ui.pushButton_page_history.setIcon(QIcon(_ICON_HISTORY))
        self.change_page(0)

        # 添加控件
        # 主页
        self.widget_homepage = WidgetPageHomepage()
        self.ui.page_homepage.layout().addWidget(self.widget_homepage)
        self.widget_homepage.signal_start_7zip.connect(lambda: self.set_widget_state(False))
        self.widget_homepage.signal_finished_7zip.connect(lambda: self.set_widget_state(True))
        self.widget_homepage.signal_7zip_result.connect(self.add_history)
        # 密码页
        self.widget_password = WidgetPagePassword()
        self.ui.page_password.layout().addWidget(self.widget_password)
        # 设置页
        self.widget_setting = WidgetPageSetting()
        self.ui.page_setting.layout().addWidget(self.widget_setting)
        self.widget_setting.signal_output_path.connect(self.set_default_drop_icon)
        # ；历史记录页
        self.widget_history = ListWidgetHistory()
        self.ui.page_history.layout().addWidget(self.widget_history)

        # 绑定槽函数
        self.ui.buttonGroup.buttonClicked.connect(self.change_page)

        # 响应初始传参
        if paths:
            self.widget_homepage.drop_paths(paths)

    def change_page(self, id_button):
        """切换页面"""
        # 转为int索引
        if isinstance(id_button, int):
            index = id_button
        else:
            index = id_button.property('id')
        # 切换页面
        self.ui.stackedWidget.setCurrentIndex(index)
        # 高亮被点击的按钮
        clicked_style = r'background-color: rgb(255, 228, 181);'
        for button in self.ui.buttonGroup.buttons():
            id_c = button.property('id')
            if id_c == index:
                button.setStyleSheet(clicked_style)
            else:
                button.setStyleSheet('')

    def set_widget_state(self, enable: bool):
        """开始/结束解压和测试时禁用/启用部分控件"""
        self.widget_password.set_button_state(enable)
        self.widget_setting.set_widgets_state(enable)
        self.widget_history.reset_class()

    def add_history(self, state_class):
        """添加历史记录"""
        self.widget_history.insert_item(state_class)

    def set_default_drop_icon(self):
        self.widget_homepage.set_default_drop_icon()
