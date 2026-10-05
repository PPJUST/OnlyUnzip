# ?????????

from PySide6.QtWidgets import QApplication, QWidget

from components.page_about.res.ui_about import Ui_Form


class AboutViewer(QWidget):
    """?????????"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.label_project.setOpenExternalLinks(True)
        self.ui.label_download_link_1.setOpenExternalLinks(True)
        self.ui.label_download_link_2.setOpenExternalLinks(True)
        self.ui.label_feedback.setOpenExternalLinks(True)

        self.set_info()

        # ??????
        self.ui.label_3.setVisible(False)
        self.ui.label_10.setVisible(False)
        self.ui.label_feedback.setVisible(False)
        self.ui.label_other.setVisible(False)

    def set_info(self):
        # ???
        self.ui.label_version.setText('v2.2.0')
        # ????
        self.ui.label_date.setText('2026.09.22')
        # ????
        self.ui.label_project.setText('<a href="https://github.com/PPJUST/OnlyUnzip">Github</a>')
        # ????
        self.ui.label_download_link_1.setText('<a href="https://github.com/PPJUST/OnlyUnzip/releases">Github</a>')
        self.ui.label_download_link_2.setText('<a href="https://wwvb.lanzout.com/b01fna1qh">??? ??1234</a>')
        # ????
        self.ui.label_feedback.setText('<a href="https://wj.qq.com/s2/23570318/20f3/">????</a>')
        # ????
        self.ui.label_other.setText('<a>??????<br>Github??</a>')


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = AboutViewer()
    program_ui.show()
    app_.exec()
