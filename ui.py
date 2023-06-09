# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui ԭ�ļ�iDUfPI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class MyLabel(QLabel):
    dropSignal = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)  # 设置可拖入

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            drop_path = [url.toLocalFile() for url in urls]  # 获取多个文件的路径的列表
            self.dropSignal.emit(drop_path)  # 发送文件列表信号


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
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.button_page_main = QPushButton(self.centralwidget)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.button_page_main)
        self.button_page_main.setObjectName(u"button_page_main")
        self.button_page_main.setMinimumSize(QSize(0, 40))
        self.button_page_main.setMaximumSize(QSize(16777215, 16777215))
        self.button_page_main.setAutoRepeat(False)
        self.button_page_main.setAutoDefault(False)
        self.button_page_main.setFlat(False)

        self.verticalLayout_6.addWidget(self.button_page_main)

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

        self.button_page_about = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.button_page_about)
        self.button_page_about.setObjectName(u"button_page_about")
        self.button_page_about.setEnabled(True)
        self.button_page_about.setMinimumSize(QSize(0, 40))
        self.button_page_about.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_6.addWidget(self.button_page_about)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.verticalSpacer = QSpacerItem(20, 21, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_7)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setAcceptDrops(False)
        self.stackedWidget.setFrameShape(QFrame.Box)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setAcceptDrops(False)
        self.verticalLayout_3 = QVBoxLayout(self.page)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 3)
        self.label_icon = MyLabel(self.page)
        self.label_icon.setObjectName(u"label_icon")
        self.label_icon.setAcceptDrops(True)
        self.label_icon.setFrameShape(QFrame.NoFrame)
        self.label_icon.setScaledContents(True)

        self.verticalLayout_3.addWidget(self.label_icon)

        self.line_3 = QFrame(self.page)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_current_file = QLabel(self.page)
        self.label_current_file.setObjectName(u"label_current_file")
        self.label_current_file.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_current_file)

        self.label_schedule = QLabel(self.page)
        self.label_schedule.setObjectName(u"label_schedule")
        self.label_schedule.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label_schedule)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3.setStretch(0, 3)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout = QGridLayout(self.page_2)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.text_password = QPlainTextEdit(self.page_2)
        self.text_password.setObjectName(u"text_password")

        self.gridLayout.addWidget(self.text_password, 0, 0, 1, 2)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.button_read_clipboard = QPushButton(self.page_2)
        self.button_read_clipboard.setObjectName(u"button_read_clipboard")

        self.verticalLayout_8.addWidget(self.button_read_clipboard)

        self.button_update_password = QPushButton(self.page_2)
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
        self.button_export_password = QPushButton(self.page_2)
        self.button_export_password.setObjectName(u"button_export_password")

        self.verticalLayout.addWidget(self.button_export_password)

        self.button_export_password_with_number = QPushButton(self.page_2)
        self.button_export_password_with_number.setObjectName(u"button_export_password_with_number")

        self.verticalLayout.addWidget(self.button_export_password_with_number)

        self.button_open_password = QPushButton(self.page_2)
        self.button_open_password.setObjectName(u"button_open_password")
        self.button_open_password.setEnabled(False)

        self.verticalLayout.addWidget(self.button_open_password)


        self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_9 = QVBoxLayout(self.page_3)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.page_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 162, 229))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.checkBox_model_unzip = QCheckBox(self.scrollAreaWidgetContents)
        self.buttonGroup_check_model = QButtonGroup(MainWindow)
        self.buttonGroup_check_model.setObjectName(u"buttonGroup_check_model")
        self.buttonGroup_check_model.addButton(self.checkBox_model_unzip)
        self.checkBox_model_unzip.setObjectName(u"checkBox_model_unzip")

        self.verticalLayout_4.addWidget(self.checkBox_model_unzip)

        self.checkBox_model_test = QCheckBox(self.scrollAreaWidgetContents)
        self.buttonGroup_check_model.addButton(self.checkBox_model_test)
        self.checkBox_model_test.setObjectName(u"checkBox_model_test")

        self.verticalLayout_4.addWidget(self.checkBox_model_test)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.checkBox_delect_zip = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_delect_zip.setObjectName(u"checkBox_delect_zip")

        self.verticalLayout_4.addWidget(self.checkBox_delect_zip)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.checkBox_nested_folders = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_nested_folders.setObjectName(u"checkBox_nested_folders")
        self.checkBox_nested_folders.setChecked(False)

        self.verticalLayout_4.addWidget(self.checkBox_nested_folders)

        self.checkBox_nested_zip = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_nested_zip.setObjectName(u"checkBox_nested_zip")
        self.checkBox_nested_zip.setEnabled(True)

        self.verticalLayout_4.addWidget(self.checkBox_nested_zip)

        self.checkBox_check_zip = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_check_zip.setObjectName(u"checkBox_check_zip")
        self.checkBox_check_zip.setChecked(False)

        self.verticalLayout_4.addWidget(self.checkBox_check_zip)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_4)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.label)

        self.lineedit_unzip_skip_suffix = QLineEdit(self.scrollAreaWidgetContents)
        self.lineedit_unzip_skip_suffix.setObjectName(u"lineedit_unzip_skip_suffix")

        self.verticalLayout_4.addWidget(self.lineedit_unzip_skip_suffix)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_9.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.horizontalLayout_2 = QHBoxLayout(self.page_4)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.listWidget_history = QListWidget(self.page_4)
        self.listWidget_history.setObjectName(u"listWidget_history")
        self.listWidget_history.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.listWidget_history)

        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_5 = QVBoxLayout(self.page_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.textBrowser = QTextBrowser(self.page_5)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_5.addWidget(self.textBrowser)

        self.stackedWidget.addWidget(self.page_5)

        self.horizontalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.button_page_main.setDefault(False)
        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OnlyUnzip", None))
        self.button_page_main.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9875\u9762", None))
        self.button_page_password.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u5bc6\u7801", None))
        self.button_page_setting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.button_page_history.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\u8bb0\u5f55", None))
        self.button_page_about.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.label_icon.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u6807", None))
        self.label_current_file.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5f53\u524d\u6587\u4ef6", None))
        self.label_schedule.setText(QCoreApplication.translate("MainWindow", u"\u663e\u793a\u5f53\u524d\u8fdb\u5ea6", None))
        self.text_password.setPlainText("")
        self.text_password.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u5bc6\u7801\uff0c\u4e00\u4e2a\u5bc6\u7801\u5360\u4e00\u884c\uff0c\u70b9\u51fb\u201c\u66f4\u65b0\u5bc6\u7801\u201d\u5373\u53ef\u66f4\u65b0", None))
        self.button_read_clipboard.setText(QCoreApplication.translate("MainWindow", u"\u8bfb\u53d6\u526a\u5207\u677f", None))
        self.button_update_password.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u5bc6\u7801", None))
        self.button_export_password.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u5bc6\u7801", None))
        self.button_export_password_with_number.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa(\u542b\u6b21\u6570)", None))
        self.button_open_password.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u5bfc\u51fa\u6587\u4ef6", None))
        self.checkBox_model_unzip.setText(QCoreApplication.translate("MainWindow", u"\u89e3\u538b\u6a21\u5f0f", None))
        self.checkBox_model_test.setText(QCoreApplication.translate("MainWindow", u"\u6d4b\u8bd5\u6a21\u5f0f", None))
        self.checkBox_delect_zip.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u539f\u6587\u4ef6", None))
        self.checkBox_nested_folders.setText(QCoreApplication.translate("MainWindow", u"\u5904\u7406\u5957\u5a03\u6587\u4ef6\u5939", None))
#if QT_CONFIG(tooltip)
        self.checkBox_nested_zip.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u7528\u4e8e\u89e3\u538b\u3010\u6e38\u620f\u3001\u590d\u6742\u7ed3\u6784\u6587\u4ef6\u5939\u3011\u65f6\u4e0d\u5efa\u8bae\u4f7f\u7528\u3002</p><p>\u903b\u8f91\u4e3a\u5c06\u89e3\u538b\u540e\u7684\u6587\u4ef6\u91cd\u65b0\u8fd0\u884c\u4e00\u904d\u89e3\u538b\u3002</p><p>\u5efa\u8bae\u4e0e\u201c\u4ec5\u89e3\u538b\u538b\u7f29\u5305\u201d\u9009\u9879\u540c\u65f6\u9009\u4e2d\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_nested_zip.setText(QCoreApplication.translate("MainWindow", u"\u5904\u7406\u5957\u5a03\u538b\u7f29\u5305**", None))
        self.checkBox_check_zip.setText(QCoreApplication.translate("MainWindow", u"\u4ec5\u89e3\u538b\u538b\u7f29\u5305", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8df3\u8fc7\u89e3\u538b\u7684\u540e\u7f00\u540d\uff1a\uff08\u4ee5,\u6216\u7a7a\u683c\u5206\u9694\uff0c\u5ffd\u7565\u5927\u5c0f\u5199\uff09", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">\u8bbe\u7f6e\u9009\u9879\u8bf4\u660e\uff1a</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u89e3\u538b\u6a21\u5f0f\uff1a\u89e3\u538b\u6587\u4ef6\u5230\u5f53\u524d\u6587\u4ef6\u6240\u5728\u76ee\u5f55</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                        "margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u6d4b\u8bd5\u6a21\u5f0f\uff1a\u6d4b\u8bd5\u6587\u4ef6\u5bc6\u7801\uff0c\u53ef\u5230\u5386\u53f2\u8bb0\u5f55\u67e5\u770b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5220\u9664\u539f\u6587\u4ef6\uff1a\u89e3\u538b\u540e\u5220\u9664\u539f\u6587\u4ef6</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5904\u7406\u5957\u5a03\u6587\u4ef6\u5939\uff1a\u903b\u8f91\u7c7b\u4f3cBandzip</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margi"
                        "n-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u5904\u7406\u5957\u5a03\u538b\u7f29\u5305\uff1a\u903b\u8f91\u662f\u5c06\u89e3\u538b\u540e\u7684\u6587\u4ef6\u518d\u6b21\u8fd0\u884c\u89e3\u538b</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u4ec5\u8bc6\u522b\u538b\u7f29\u5305\uff1a\u538b\u7f29\u5305\u7684\u8bc6\u522b\u57fa\u4e8efiletype\u5e93+\u6307\u5b9a\u7684\u538b\u7f29\u6587\u4ef6\u540e\u7f00\uff08EXE\u6587\u4ef6\u4e0e\u56fe\u79cd\u4e0d\u4f1a\u88ab\u8bc6\u522b\u4e3a\u538b\u7f29\u5305\uff0c\u9700\u8981\u89e3\u538b\u8bf7\u5173\u95ed\u8be5\u9009\u9879\uff09</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0p"
                        "x; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">\u6e90\u7801\uff1a</span>https://github.com/PPJUST/only_unzip</p></body></html>", None))
    # retranslateUi

