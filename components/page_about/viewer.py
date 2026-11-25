# 关于模块的界面组件
from PySide6.QtWidgets import QApplication, QWidget

from components.page_about.res.ui_about import Ui_Form

# 版本信息，与 更新日志.txt 中的最后一条保持一致
VERSION = 'v2.2.1'
BUILD_DATE = '2026.10.29'

# 项目主页和各下载地址
PROJECT_URL = 'https://github.com/PPJUST/OnlyUnzip'
DOWNLOAD_URL_GITHUB = 'https://github.com/PPJUST/OnlyUnzip/releases'
DOWNLOAD_URL_LANZOU = 'https://wwvb.lanzout.com/b01fna1qh'
FEEDBACK_URL = 'https://wj.qq.com/s2/23570318/20f3/'


def make_link(url, text):
    """生成可点击的链接文本"""
    return f'<a href="{url}">{text}</a>'


class AboutViewer(QWidget):
    """关于模块的界面组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._enable_external_links()
        self._hide_unused_labels()
        self.set_info()

    def _enable_external_links(self):
        """让链接标签可以在浏览器中打开"""
        labels = [
            self.ui.label_project,
            self.ui.label_download_link_1,
            self.ui.label_download_link_2,
            self.ui.label_feedback,
        ]
        for label in labels:
            label.setOpenExternalLinks(True)

    def _hide_unused_labels(self):
        """隐藏暂不展示的信息行"""
        labels = [
            self.ui.label_3,
            self.ui.label_10,
            self.ui.label_feedback,
            self.ui.label_other,
        ]
        for label in labels:
            label.setVisible(False)

    def set_info(self):
        """写入版本号、日期和各链接的显示文本"""
        # 版本号
        self.ui.label_version.setText(VERSION)
        # 编译日期
        self.ui.label_date.setText(BUILD_DATE)
        # 项目主页
        self.ui.label_project.setText(make_link(PROJECT_URL, 'Github'))
        # 下载地址
        self.ui.label_download_link_1.setText(make_link(DOWNLOAD_URL_GITHUB, 'Github'))
        self.ui.label_download_link_2.setText(make_link(DOWNLOAD_URL_LANZOU, '蓝奏云 密码1234'))
        # 反馈入口与说明（当前隐藏，保留文本以便以后启用）
        self.ui.label_feedback.setText(make_link(FEEDBACK_URL, '点击直达'))
        self.ui.label_other.setText('<a>有问题推荐在<br>Github反馈</a>')


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = AboutViewer()
    program_ui.show()
    app_.exec()
