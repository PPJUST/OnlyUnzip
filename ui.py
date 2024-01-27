# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uibniaIm.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from constant import _ICON_TEST, _ICON_DEFAULT, _ICON_DROP


class DropLabel(QLabel):
    signal_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.icon = _ICON_DEFAULT
        self.last_icon = None
        self.reset_icon(self.icon)

    def reset_icon(self, icon:str):
        self.icon = icon
        self.setPixmap(icon)


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.last_icon = self.pixmap()
            self.setPixmap(_ICON_DROP)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setPixmap(self.last_icon)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            drop_path = [url.toLocalFile() for url in urls]  # 获取多个文件的路径的列表
            self.signal_dropped.emit(drop_path)  # 发送文件列表信号

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(262, 232)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.button_page_main = QPushButton(self.centralwidget)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.button_page_main)
        self.button_page_main.setObjectName(u"button_page_main")
        self.button_page_main.setMinimumSize(QSize(0, 40))
        self.button_page_main.setMaximumSize(QSize(16777215, 16777215))
        icon = QIcon()
        icon.addFile(u"icon/\u4e3b\u9875.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_page_main.setIcon(icon)
        self.button_page_main.setIconSize(QSize(16, 16))
        self.button_page_main.setAutoRepeat(False)
        self.button_page_main.setAutoDefault(False)
        self.button_page_main.setFlat(False)

        self.verticalLayout_6.addWidget(self.button_page_main)

        self.button_page_password = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.button_page_password)
        self.button_page_password.setObjectName(u"button_page_password")
        self.button_page_password.setMinimumSize(QSize(0, 40))
        self.button_page_password.setMaximumSize(QSize(16777215, 16777215))
        icon1 = QIcon()
        icon1.addFile(u"icon/\u5bc6\u7801\u9875.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_page_password.setIcon(icon1)

        self.verticalLayout_6.addWidget(self.button_page_password)

        self.button_page_setting = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.button_page_setting)
        self.button_page_setting.setObjectName(u"button_page_setting")
        self.button_page_setting.setMinimumSize(QSize(0, 40))
        self.button_page_setting.setMaximumSize(QSize(16777215, 16777215))
        icon2 = QIcon()
        icon2.addFile(u"icon/\u8bbe\u7f6e\u9875.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_page_setting.setIcon(icon2)

        self.verticalLayout_6.addWidget(self.button_page_setting)

        self.button_page_history = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.button_page_history)
        self.button_page_history.setObjectName(u"button_page_history")
        self.button_page_history.setMinimumSize(QSize(0, 40))
        self.button_page_history.setMaximumSize(QSize(16777215, 16777215))
        icon3 = QIcon()
        icon3.addFile(u"icon/\u5386\u53f2\u8bb0\u5f55\u9875.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_page_history.setIcon(icon3)

        self.verticalLayout_6.addWidget(self.button_page_history)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.stackedWidget_main = QStackedWidget(self.centralwidget)
        self.stackedWidget_main.setObjectName(u"stackedWidget_main")
        self.stackedWidget_main.setAcceptDrops(False)
        self.stackedWidget_main.setFrameShape(QFrame.Box)
        self.page_main = QWidget()
        self.page_main.setObjectName(u"page_main")
        self.page_main.setAcceptDrops(False)
        self.verticalLayout_2 = QVBoxLayout(self.page_main)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 0, 3, 3)
        self.label_drop_file = DropLabel(self.page_main)
        self.label_drop_file.setObjectName(u"label_drop_file")
        self.label_drop_file.setAcceptDrops(True)
        self.label_drop_file.setFrameShape(QFrame.NoFrame)
        self.label_drop_file.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.label_drop_file)

        self.line_3 = QFrame(self.page_main)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_schedule_file = QLabel(self.page_main)
        self.label_schedule_file.setObjectName(u"label_schedule_file")
        self.label_schedule_file.setWordWrap(True)

        self.horizontalLayout_7.addWidget(self.label_schedule_file)

        self.button_stop = QToolButton(self.page_main)
        self.button_stop.setObjectName(u"button_stop")
        icon4 = QIcon()
        icon4.addFile(u"icon/\u4e2d\u6b62.png", QSize(), QIcon.Normal, QIcon.Off)
        self.button_stop.setIcon(icon4)

        self.horizontalLayout_7.addWidget(self.button_stop)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.label_current_file = QLabel(self.page_main)
        self.label_current_file.setObjectName(u"label_current_file")
        self.label_current_file.setMaximumSize(QSize(16777215, 24))
        self.label_current_file.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_current_file)

        self.stackedWidget_schedule = QStackedWidget(self.page_main)
        self.stackedWidget_schedule.setObjectName(u"stackedWidget_schedule")
        self.page_info = QWidget()
        self.page_info.setObjectName(u"page_info")
        self.horizontalLayout_5 = QHBoxLayout(self.page_info)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_schedule_finish = QLabel(self.page_info)
        self.label_schedule_finish.setObjectName(u"label_schedule_finish")

        self.horizontalLayout_5.addWidget(self.label_schedule_finish)

        self.stackedWidget_schedule.addWidget(self.page_info)
        self.page_test = QWidget()
        self.page_test.setObjectName(u"page_test")
        self.horizontalLayout_3 = QHBoxLayout(self.page_test)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.page_test)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_schedule_test = QLabel(self.page_test)
        self.label_schedule_test.setObjectName(u"label_schedule_test")

        self.horizontalLayout_3.addWidget(self.label_schedule_test)

        self.horizontalLayout_3.setStretch(1, 1)
        self.stackedWidget_schedule.addWidget(self.page_test)
        self.page_unzip = QWidget()
        self.page_unzip.setObjectName(u"page_unzip")
        self.horizontalLayout_4 = QHBoxLayout(self.page_unzip)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.page_unzip)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.progressBar_extract = QProgressBar(self.page_unzip)
        self.progressBar_extract.setObjectName(u"progressBar_extract")
        self.progressBar_extract.setMaximumSize(QSize(16777215, 12))
        self.progressBar_extract.setStyleSheet(u"")
        self.progressBar_extract.setValue(0)
        self.progressBar_extract.setTextVisible(False)

        self.horizontalLayout_4.addWidget(self.progressBar_extract)

        self.horizontalLayout_4.setStretch(1, 1)
        self.stackedWidget_schedule.addWidget(self.page_unzip)

        self.verticalLayout_2.addWidget(self.stackedWidget_schedule)

        self.verticalLayout_2.setStretch(0, 1)
        self.stackedWidget_main.addWidget(self.page_main)
        self.page_pw = QWidget()
        self.page_pw.setObjectName(u"page_pw")
        self.gridLayout = QGridLayout(self.page_pw)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.text_password = QPlainTextEdit(self.page_pw)
        self.text_password.setObjectName(u"text_password")

        self.gridLayout.addWidget(self.text_password, 0, 0, 1, 2)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.button_read_clipboard = QPushButton(self.page_pw)
        self.button_read_clipboard.setObjectName(u"button_read_clipboard")

        self.verticalLayout_8.addWidget(self.button_read_clipboard)

        self.button_update_password = QPushButton(self.page_pw)
        self.button_update_password.setObjectName(u"button_update_password")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_update_password.sizePolicy().hasHeightForWidth())
        self.button_update_password.setSizePolicy(sizePolicy)

        self.verticalLayout_8.addWidget(self.button_update_password)

        self.verticalLayout_8.setStretch(0, 1)
        self.verticalLayout_8.setStretch(1, 2)

        self.gridLayout.addLayout(self.verticalLayout_8, 1, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.button_export_password = QPushButton(self.page_pw)
        self.button_export_password.setObjectName(u"button_export_password")

        self.verticalLayout.addWidget(self.button_export_password)

        self.button_export_password_with_number = QPushButton(self.page_pw)
        self.button_export_password_with_number.setObjectName(u"button_export_password_with_number")

        self.verticalLayout.addWidget(self.button_export_password_with_number)

        self.button_open_password = QPushButton(self.page_pw)
        self.button_open_password.setObjectName(u"button_open_password")
        self.button_open_password.setEnabled(False)

        self.verticalLayout.addWidget(self.button_open_password)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.stackedWidget_main.addWidget(self.page_pw)
        self.page_setting = QWidget()
        self.page_setting.setObjectName(u"page_setting")
        self.verticalLayout_9 = QVBoxLayout(self.page_setting)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.page_setting)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 135, 338))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.checkBox_mode_extract = QCheckBox(self.scrollAreaWidgetContents)
        self.buttonGroup_check_mode = QButtonGroup(MainWindow)
        self.buttonGroup_check_mode.setObjectName(u"buttonGroup_check_mode")
        self.buttonGroup_check_mode.addButton(self.checkBox_mode_extract)
        self.checkBox_mode_extract.setObjectName(u"checkBox_mode_extract")

        self.verticalLayout_4.addWidget(self.checkBox_mode_extract)

        self.checkBox_mode_test = QCheckBox(self.scrollAreaWidgetContents)
        self.buttonGroup_check_mode.addButton(self.checkBox_mode_test)
        self.checkBox_mode_test.setObjectName(u"checkBox_mode_test")

        self.verticalLayout_4.addWidget(self.checkBox_mode_test)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.checkBox_delete_archive = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_delete_archive.setObjectName(u"checkBox_delete_archive")

        self.verticalLayout_4.addWidget(self.checkBox_delete_archive)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.checkBox_un_nest_dir = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_un_nest_dir.setObjectName(u"checkBox_un_nest_dir")
        self.checkBox_un_nest_dir.setChecked(False)

        self.verticalLayout_4.addWidget(self.checkBox_un_nest_dir)

        self.checkBox_un_nest_archive = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_un_nest_archive.setObjectName(u"checkBox_un_nest_archive")
        self.checkBox_un_nest_archive.setEnabled(True)

        self.verticalLayout_4.addWidget(self.checkBox_un_nest_archive)

        self.checkBox_check_filetype = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_check_filetype.setObjectName(u"checkBox_check_filetype")
        self.checkBox_check_filetype.setChecked(False)

        self.verticalLayout_4.addWidget(self.checkBox_check_filetype)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_4)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label)

        self.lineedit_exclude_rule = QLineEdit(self.scrollAreaWidgetContents)
        self.lineedit_exclude_rule.setObjectName(u"lineedit_exclude_rule")

        self.verticalLayout_4.addWidget(self.lineedit_exclude_rule)

        self.line_5 = QFrame(self.scrollAreaWidgetContents)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_5)

        self.label_4 = QLabel(self.scrollAreaWidgetContents)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_4.addWidget(self.label_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lineedit_output_dir = QLineEdit(self.scrollAreaWidgetContents)
        self.lineedit_output_dir.setObjectName(u"lineedit_output_dir")

        self.horizontalLayout_6.addWidget(self.lineedit_output_dir)

        self.button_ask_folder = QToolButton(self.scrollAreaWidgetContents)
        self.button_ask_folder.setObjectName(u"button_ask_folder")

        self.horizontalLayout_6.addWidget(self.button_ask_folder)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_9.addWidget(self.scrollArea)

        self.stackedWidget_main.addWidget(self.page_setting)
        self.page_history = QWidget()
        self.page_history.setObjectName(u"page_history")
        self.horizontalLayout_2 = QHBoxLayout(self.page_history)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listWidget_history = QListWidget(self.page_history)
        self.listWidget_history.setObjectName(u"listWidget_history")
        self.listWidget_history.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.listWidget_history)

        self.stackedWidget_main.addWidget(self.page_history)

        self.horizontalLayout.addWidget(self.stackedWidget_main)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.button_page_main.setDefault(False)
        self.stackedWidget_main.setCurrentIndex(0)
        self.stackedWidget_schedule.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OnlyUnzip", None))
        self.button_page_main.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9875", None))
        self.button_page_password.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801", None))
        self.button_page_setting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.button_page_history.setText(QCoreApplication.translate("MainWindow", u"\u5386\u53f2", None))
        self.label_drop_file.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u6807", None))
        self.label_schedule_file.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u603b\u8fdb\u5ea6", None))
        self.button_stop.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_current_file.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5f53\u524d\u6587\u4ef6", None))
        self.label_schedule_finish.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u72b6\u6001", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5\u5bc6\u7801\uff1a", None))
        self.label_schedule_test.setText(QCoreApplication.translate("MainWindow", u"0/0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\uff1a", None))
        self.text_password.setPlainText("")
        self.text_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u5bc6\u7801\uff0c\u4e00\u4e2a\u5bc6\u7801\u5360\u4e00\u884c\uff0c\u70b9\u51fb\u201c\u66f4\u65b0\u5bc6\u7801\u201d\u5373\u53ef\u66f4\u65b0", None))
        self.button_read_clipboard.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6\u526a\u5207\u677f", None))
        self.button_update_password.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u5bc6\u7801", None))
        self.button_export_password.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u5bc6\u7801", None))
        self.button_export_password_with_number.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa(\u542b\u6b21\u6570)", None))
        self.button_open_password.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u5bfc\u51fa\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.checkBox_mode_extract.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u89e3\u538b\u538b\u7f29\u5305\u5230\u5f53\u524d\u6587\u4ef6\u6240\u5728\u76ee\u5f55</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_mode_extract.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\u6a21\u5f0f", None))
#if QT_CONFIG(tooltip)
        self.checkBox_mode_test.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4ec5\u641c\u7d22\u538b\u7f29\u5305\u7684\u5bc6\u7801\u800c\u4e0d\u8fdb\u884c\u89e3\u538b\uff0c\u7ed3\u679c\u663e\u793a\u5728\u201c\u5386\u53f2\u8bb0\u5f55\u201d\u9875</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_mode_test.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5\u6a21\u5f0f", None))
#if QT_CONFIG(tooltip)
        self.checkBox_delete_archive.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u89e3\u538b\u5b8c\u6210\u540e\u5220\u9664\u539f\u6587\u4ef6\uff08\u5230\u56de\u6536\u7ad9\uff09</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_delete_archive.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u539f\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.checkBox_un_nest_dir.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u903b\u8f91\u7c7b\u4f3c\u4e8eBandzip</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_un_nest_dir.setText(QCoreApplication.translate("MainWindow", u"\u5904\u7406\u5957\u5a03\u6587\u4ef6\u5939", None))
#if QT_CONFIG(tooltip)
        self.checkBox_un_nest_archive.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u903b\u8f91\u4e3a\uff1a\u5c06\u89e3\u538b\u540e\u7684\u6587\u4ef6\u91cd\u65b0\u8fd0\u884c\u4e00\u6b21\u89e3\u538b</p><p><br/></p><p>\u5efa\u8bae\u4e0e\u201c<span style=\" font-weight:600;\">\u4ec5\u89e3\u538b\u538b\u7f29\u5305</span>\u201d\u9009\u9879\u540c\u65f6\u9009\u4e2d</p><p><br/></p><p>\u7528\u4e8e\u89e3\u538b\u3010<span style=\" font-weight:600;\">\u6e38\u620f\u3001\u590d\u6742\u7ed3\u6784\u6587\u4ef6</span>\u3011\u65f6\u4e0d\u5efa\u8bae\u4f7f\u7528</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_un_nest_archive.setText(QCoreApplication.translate("MainWindow", u"\u5904\u7406\u5957\u5a03\u538b\u7f29\u5305**", None))
#if QT_CONFIG(tooltip)
        self.checkBox_check_filetype.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u538b\u7f29\u5305\u7684\u8bc6\u522b\u65b9\u6cd5\uff1a\u4f7f\u7528filetype\u5e93+\u6307\u5b9a\u6587\u4ef6\u540d\u540e\u7f00\uff08EXE\u4e0d\u4f1a\u88ab\u8ba4\u5b9a\u4e3a\u538b\u7f29\u5305\uff09</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_check_filetype.setText(QCoreApplication.translate("MainWindow", u"\u4ec5\u89e3\u538b\u538b\u7f29\u5305", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7\u89e3\u538b\u7684\u540e\u7f00\u540d\uff1a\uff08\u4ee5,\u6216\u7a7a\u683c\u5206\u9694\uff0c\u5ffd\u7565\u5927\u5c0f\u5199\uff09", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\u5230\u6307\u5b9a\u6587\u4ef6\u5939", None))
        self.button_ask_folder.setText(QCoreApplication.translate("MainWindow", u"..", None))
    # retranslateUi

