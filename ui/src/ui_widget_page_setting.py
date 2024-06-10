# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_widget_page_settingkAifck.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(213, 287)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -54, 194, 339))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.checkBox_mode_extract = QCheckBox(self.scrollAreaWidgetContents)
        self.buttonGroup_mode = QButtonGroup(Form)
        self.buttonGroup_mode.setObjectName(u"buttonGroup_mode")
        self.buttonGroup_mode.addButton(self.checkBox_mode_extract)
        self.checkBox_mode_extract.setObjectName(u"checkBox_mode_extract")

        self.verticalLayout_2.addWidget(self.checkBox_mode_extract)

        self.checkBox_mode_test = QCheckBox(self.scrollAreaWidgetContents)
        self.buttonGroup_mode.addButton(self.checkBox_mode_test)
        self.checkBox_mode_test.setObjectName(u"checkBox_mode_test")

        self.verticalLayout_2.addWidget(self.checkBox_mode_test)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.checkBox_extract_smart = QCheckBox(self.scrollAreaWidgetContents)
        self.buttonGroup_folder = QButtonGroup(Form)
        self.buttonGroup_folder.setObjectName(u"buttonGroup_folder")
        self.buttonGroup_folder.addButton(self.checkBox_extract_smart)
        self.checkBox_extract_smart.setObjectName(u"checkBox_extract_smart")

        self.verticalLayout_2.addWidget(self.checkBox_extract_smart)

        self.checkBox_extract_folder = QCheckBox(self.scrollAreaWidgetContents)
        self.buttonGroup_folder.addButton(self.checkBox_extract_folder)
        self.checkBox_extract_folder.setObjectName(u"checkBox_extract_folder")

        self.verticalLayout_2.addWidget(self.checkBox_extract_folder)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.checkBox_delete_file = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_delete_file.setObjectName(u"checkBox_delete_file")

        self.verticalLayout_2.addWidget(self.checkBox_delete_file)

        self.checkBox_handle_multi_folder = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_handle_multi_folder.setObjectName(u"checkBox_handle_multi_folder")

        self.verticalLayout_2.addWidget(self.checkBox_handle_multi_folder)

        self.line_3 = QFrame(self.scrollAreaWidgetContents)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.checkBox_check_filetype = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_check_filetype.setObjectName(u"checkBox_check_filetype")

        self.verticalLayout_2.addWidget(self.checkBox_check_filetype)

        self.checkBox_handle_multi_archive = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_handle_multi_archive.setObjectName(u"checkBox_handle_multi_archive")

        self.verticalLayout_2.addWidget(self.checkBox_handle_multi_archive)

        self.line_5 = QFrame(self.scrollAreaWidgetContents)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_5)

        self.label_2 = QLabel(self.scrollAreaWidgetContents)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit_output_path = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_output_path.setObjectName(u"lineEdit_output_path")

        self.horizontalLayout.addWidget(self.lineEdit_output_path)

        self.toolButton_ask_path = QToolButton(self.scrollAreaWidgetContents)
        self.toolButton_ask_path.setObjectName(u"toolButton_ask_path")

        self.horizontalLayout.addWidget(self.toolButton_ask_path)

        self.toolButton_clear_path = QToolButton(self.scrollAreaWidgetContents)
        self.toolButton_clear_path.setObjectName(u"toolButton_clear_path")

        self.horizontalLayout.addWidget(self.toolButton_clear_path)

        self.toolButton_open_path = QToolButton(self.scrollAreaWidgetContents)
        self.toolButton_open_path.setObjectName(u"toolButton_open_path")

        self.horizontalLayout.addWidget(self.toolButton_open_path)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_4)

        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.lineEdit_filter_suffix = QLineEdit(self.scrollAreaWidgetContents)
        self.lineEdit_filter_suffix.setObjectName(u"lineEdit_filter_suffix")

        self.verticalLayout_2.addWidget(self.lineEdit_filter_suffix)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.checkBox_mode_extract.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u6a21\u5f0f", None))
        self.checkBox_mode_test.setText(QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u6a21\u5f0f", None))
        self.checkBox_extract_smart.setText(QCoreApplication.translate("Form", u"\u667a\u80fd\u89e3\u538b", None))
        self.checkBox_extract_folder.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u5230\u540c\u540d\u6587\u4ef6\u5939", None))
        self.checkBox_delete_file.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u540e\u5220\u9664\u6e90\u6587\u4ef6", None))
        self.checkBox_handle_multi_folder.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u540e\u89e3\u5957\u591a\u5c42\u6587\u4ef6\u5939", None))
        self.checkBox_check_filetype.setText(QCoreApplication.translate("Form", u"\u4ec5\u5904\u7406\u538b\u7f29\u5305", None))
        self.checkBox_handle_multi_archive.setText(QCoreApplication.translate("Form", u"\u9012\u5f52\u89e3\u538b\u5957\u5a03\u538b\u7f29\u5305", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u81f3\u6307\u5b9a\u76ee\u5f55\uff1a", None))
        self.toolButton_ask_path.setText(QCoreApplication.translate("Form", u"...", None))
        self.toolButton_clear_path.setText(QCoreApplication.translate("Form", u"...", None))
        self.toolButton_open_path.setText(QCoreApplication.translate("Form", u"...", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u8fc7\u6ee4\uff1a", None))
    # retranslateUi

