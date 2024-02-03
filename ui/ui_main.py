# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainZhRqho.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QFrame,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QPlainTextEdit, QProgressBar, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStackedWidget,
    QToolButton, QVBoxLayout, QWidget)

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
        self.button_page_home = QPushButton(self.centralwidget)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.button_page_home)
        self.button_page_home.setObjectName(u"button_page_home")
        self.button_page_home.setMinimumSize(QSize(0, 40))
        self.button_page_home.setMaximumSize(QSize(16777215, 16777215))
        self.button_page_home.setIconSize(QSize(16, 16))
        self.button_page_home.setAutoRepeat(False)
        self.button_page_home.setAutoDefault(False)
        self.button_page_home.setFlat(False)

        self.verticalLayout_6.addWidget(self.button_page_home)

        self.button_page_password = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.button_page_password)
        self.button_page_password.setObjectName(u"button_page_password")
        self.button_page_password.setMinimumSize(QSize(0, 40))
        self.button_page_password.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_6.addWidget(self.button_page_password)

        self.button_page_setting = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.button_page_setting)
        self.button_page_setting.setObjectName(u"button_page_setting")
        self.button_page_setting.setMinimumSize(QSize(0, 40))
        self.button_page_setting.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_6.addWidget(self.button_page_setting)

        self.button_page_history = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.button_page_history)
        self.button_page_history.setObjectName(u"button_page_history")
        self.button_page_history.setMinimumSize(QSize(0, 40))
        self.button_page_history.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_6.addWidget(self.button_page_history)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.verticalSpacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.stackedWidget_main = QStackedWidget(self.centralwidget)
        self.stackedWidget_main.setObjectName(u"stackedWidget_main")
        self.stackedWidget_main.setAcceptDrops(False)
        self.stackedWidget_main.setFrameShape(QFrame.Box)
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.page_home.setAcceptDrops(False)
        self.verticalLayout_2 = QVBoxLayout(self.page_home)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_dropped_label = QVBoxLayout()
        self.verticalLayout_dropped_label.setSpacing(0)
        self.verticalLayout_dropped_label.setObjectName(u"verticalLayout_dropped_label")
        self.verticalLayout_dropped_label.setSizeConstraint(QLayout.SetDefaultConstraint)

        self.verticalLayout_2.addLayout(self.verticalLayout_dropped_label)

        self.line_3 = QFrame(self.page_home)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_schedule_total = QLabel(self.page_home)
        self.label_schedule_total.setObjectName(u"label_schedule_total")
        self.label_schedule_total.setWordWrap(True)

        self.horizontalLayout_7.addWidget(self.label_schedule_total)

        self.button_stop = QToolButton(self.page_home)
        self.button_stop.setObjectName(u"button_stop")

        self.horizontalLayout_7.addWidget(self.button_stop)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.label_current_file = QLabel(self.page_home)
        self.label_current_file.setObjectName(u"label_current_file")
        self.label_current_file.setMaximumSize(QSize(16777215, 24))
        self.label_current_file.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_current_file)

        self.stackedWidget_schedule = QStackedWidget(self.page_home)
        self.stackedWidget_schedule.setObjectName(u"stackedWidget_schedule")
        self.page_info = QWidget()
        self.page_info.setObjectName(u"page_info")
        self.horizontalLayout_5 = QHBoxLayout(self.page_info)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_schedule_state = QLabel(self.page_info)
        self.label_schedule_state.setObjectName(u"label_schedule_state")

        self.horizontalLayout_5.addWidget(self.label_schedule_state)

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
        self.stackedWidget_main.addWidget(self.page_home)
        self.page_pw = QWidget()
        self.page_pw.setObjectName(u"page_pw")
        self.verticalLayout_3 = QVBoxLayout(self.page_pw)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.text_password = QPlainTextEdit(self.page_pw)
        self.text_password.setObjectName(u"text_password")

        self.verticalLayout_3.addWidget(self.text_password)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.button_read_clipboard = QPushButton(self.page_pw)
        self.button_read_clipboard.setObjectName(u"button_read_clipboard")

        self.verticalLayout.addWidget(self.button_read_clipboard)

        self.button_export_password = QPushButton(self.page_pw)
        self.button_export_password.setObjectName(u"button_export_password")

        self.verticalLayout.addWidget(self.button_export_password)

        self.button_open_password = QPushButton(self.page_pw)
        self.button_open_password.setObjectName(u"button_open_password")
        self.button_open_password.setEnabled(False)

        self.verticalLayout.addWidget(self.button_open_password)


        self.horizontalLayout_8.addLayout(self.verticalLayout)

        self.button_update_password = QPushButton(self.page_pw)
        self.button_update_password.setObjectName(u"button_update_password")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_update_password.sizePolicy().hasHeightForWidth())
        self.button_update_password.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.button_update_password)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 162, 311))
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

        self.checkBox_delete_original_file = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_delete_original_file.setObjectName(u"checkBox_delete_original_file")

        self.verticalLayout_4.addWidget(self.checkBox_delete_original_file)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.checkBox_handling_nested_folder = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_handling_nested_folder.setObjectName(u"checkBox_handling_nested_folder")
        self.checkBox_handling_nested_folder.setChecked(False)

        self.verticalLayout_4.addWidget(self.checkBox_handling_nested_folder)

        self.checkBox_handling_nested_archive = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_handling_nested_archive.setObjectName(u"checkBox_handling_nested_archive")
        self.checkBox_handling_nested_archive.setEnabled(True)

        self.verticalLayout_4.addWidget(self.checkBox_handling_nested_archive)

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

        self.lineEdit_exclude_rules = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_exclude_rules.setObjectName(u"lineEdit_exclude_rules")

        self.verticalLayout_4.addWidget(self.lineEdit_exclude_rules)

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
        self.lineEdit_output_folder = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_output_folder.setObjectName(u"lineEdit_output_folder")

        self.horizontalLayout_6.addWidget(self.lineEdit_output_folder)

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
        self.verticalLayout_history = QVBoxLayout()
        self.verticalLayout_history.setSpacing(0)
        self.verticalLayout_history.setObjectName(u"verticalLayout_history")

        self.horizontalLayout_2.addLayout(self.verticalLayout_history)

        self.stackedWidget_main.addWidget(self.page_history)

        self.horizontalLayout.addWidget(self.stackedWidget_main)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.button_page_home.setDefault(False)
        self.stackedWidget_main.setCurrentIndex(0)
        self.stackedWidget_schedule.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OnlyUnzip", None))
        self.button_page_home.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9875", None))
        self.button_page_password.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801", None))
        self.button_page_setting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.button_page_history.setText(QCoreApplication.translate("MainWindow", u"\u5386\u53f2", None))
        self.label_schedule_total.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u603b\u8fdb\u5ea6", None))
        self.button_stop.setText("")
        self.label_current_file.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5f53\u524d\u6587\u4ef6", None))
        self.label_schedule_state.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u72b6\u6001", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5\u5bc6\u7801\uff1a", None))
        self.label_schedule_test.setText(QCoreApplication.translate("MainWindow", u"0/0", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\uff1a", None))
        self.text_password.setPlainText("")
        self.text_password.setPlaceholderText("")
        self.button_read_clipboard.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6\u526a\u5207\u677f", None))
        self.button_export_password.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u5bc6\u7801", None))
        self.button_open_password.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u5bfc\u51fa\u6587\u4ef6", None))
        self.button_update_password.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u5bc6\u7801", None))
#if QT_CONFIG(tooltip)
        self.checkBox_mode_extract.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u89e3\u538b\u6587\u4ef6</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_mode_extract.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\u6a21\u5f0f", None))
#if QT_CONFIG(tooltip)
        self.checkBox_mode_test.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u4ec5\u641c\u7d22\u6587\u4ef6\u7684\u5bc6\u7801\uff0c\u7ed3\u679c\u663e\u793a\u5728\u5386\u53f2\u8bb0\u5f55\u4e2d</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_mode_test.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5\u6a21\u5f0f", None))
#if QT_CONFIG(tooltip)
        self.checkBox_delete_original_file.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u89e3\u538b\u5b8c\u6210\u540e\uff0c\u5220\u9664\u6587\u4ef6\u81f3\u56de\u6536\u7ad9</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_delete_original_file.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u539f\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.checkBox_handling_nested_folder.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u81ea\u52a8\u89e3\u9664\u5d4c\u5957\u6587\u4ef6\u5939\u7ed3\u6784</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_handling_nested_folder.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u89e3\u5957\u5d4c\u5957\u6587\u4ef6\u5939", None))
#if QT_CONFIG(tooltip)
        self.checkBox_handling_nested_archive.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u5c06\u89e3\u538b\u540e\u7684\u6587\u4ef6\u91cd\u65b0\u8fd0\u884c\u4e00\u6b21\u89e3\u538b</p><p>\u5efa\u8bae\u4e0e\u201c<span style=\" font-weight:600;\">\u4ec5\u89e3\u538b\u538b\u7f29\u5305</span>\u201d\u9009\u9879\u540c\u65f6\u9009\u4e2d</p><p>\u7528\u4e8e\u89e3\u538b\u3010<span style=\" font-weight:600;\">\u6e38\u620f\u7b49\u590d\u6742\u7ed3\u6784\u6587\u4ef6</span>\u3011\u65f6\u4e0d\u5efa\u8bae\u4f7f\u7528</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_handling_nested_archive.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u89e3\u538b\u5957\u5a03\u538b\u7f29\u5305", None))
#if QT_CONFIG(tooltip)
        self.checkBox_check_filetype.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u8bc6\u522b\u538b\u7f29\u6587\u4ef6\uff08EXE\u81ea\u89e3\u538b\u683c\u5f0f\u4e0d\u4f1a\u88ab\u8ba4\u5b9a\u4e3a\u538b\u7f29\u5305\uff09</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_check_filetype.setText(QCoreApplication.translate("MainWindow", u"\u4ec5\u89e3\u538b\u538b\u7f29\u5305", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7\u89e3\u538b\u7684\u540e\u7f00\u540d:\uff08\u4ee5\u7a7a\u683c\u6216\u9017\u53f7\u5206\u9694\uff09", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\u5230\u6307\u5b9a\u6587\u4ef6\u5939", None))
        self.button_ask_folder.setText(QCoreApplication.translate("MainWindow", u"..", None))
    # retranslateUi

