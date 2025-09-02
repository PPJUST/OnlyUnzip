# 关于模块的界面组件

from PySide6.QtWidgets import QApplication, QWidget

from components.page_about.res.ui_about import Ui_Form


class AboutViewer(QWidget):
    """关于模块的界面组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.label_project.setOpenExternalLinks(True)
        self.ui.label_download_link_1.setOpenExternalLinks(True)
        self.ui.label_download_link_2.setOpenExternalLinks(True)
        self.ui.label_feedback.setOpenExternalLinks(True)

        self.set_info()

    def set_info(self):
        # 版本号
        self.ui.label_version.setText('v2.0.0')
        # 编译日期
        self.ui.label_date.setText('2025.08.31')
        # 项目主页
        self.ui.label_project.setText('<a href="https://github.com/PPJUST/OnlyUnzip">Github</a>')
        # 下载地址
        self.ui.label_download_link_1.setText('<a href="https://github.com/PPJUST/OnlyUnzip/releases">Github</a>')
        self.ui.label_download_link_2.setText('<a href="https://wwvb.lanzout.com/b01fna1qh">蓝奏云\n密码1234</a>')
        # 反馈地址
        self.ui.label_feedback.setText('<a href="https://wj.qq.com/s2/23570318/20f3/">点击直达</a>')


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = AboutViewer()
    program_ui.show()
    app_.exec()
