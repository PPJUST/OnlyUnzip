# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_page_settingJRsall.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QComboBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPlainTextEdit, QRadioButton, QScrollArea, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(320, 240)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 283, 712))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.radioButton_mode1_test = QRadioButton(self.scrollAreaWidgetContents)
        self.buttonGroup = QButtonGroup(Form)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.radioButton_mode1_test)
        self.radioButton_mode1_test.setObjectName(u"radioButton_mode1_test")

        self.verticalLayout.addWidget(self.radioButton_mode1_test)

        self.radioButton_mode1_extract = QRadioButton(self.scrollAreaWidgetContents)
        self.buttonGroup.addButton(self.radioButton_mode1_extract)
        self.radioButton_mode1_extract.setObjectName(u"radioButton_mode1_extract")

        self.verticalLayout.addWidget(self.radioButton_mode1_extract)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.checkBox_try_unknown_filetype = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_try_unknown_filetype.setObjectName(u"checkBox_try_unknown_filetype")

        self.verticalLayout.addWidget(self.checkBox_try_unknown_filetype)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.widget_test = QWidget(self.scrollAreaWidgetContents)
        self.widget_test.setObjectName(u"widget_test")
        self.verticalLayout_3 = QVBoxLayout(self.widget_test)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBox_write_filename = QCheckBox(self.widget_test)
        self.checkBox_write_filename.setObjectName(u"checkBox_write_filename")

        self.verticalLayout_3.addWidget(self.checkBox_write_filename)

        self.line_3 = QFrame(self.widget_test)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.label_4 = QLabel(self.widget_test)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.widget_test)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.lineEdit_left_word = QLineEdit(self.widget_test)
        self.lineEdit_left_word.setObjectName(u"lineEdit_left_word")

        self.horizontalLayout_4.addWidget(self.lineEdit_left_word)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.widget_test)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.lineEdit_right_word = QLineEdit(self.widget_test)
        self.lineEdit_right_word.setObjectName(u"lineEdit_right_word")

        self.horizontalLayout_5.addWidget(self.lineEdit_right_word)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_5 = QLabel(self.widget_test)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_6.addWidget(self.label_5)

        self.comboBox_pw_position = QComboBox(self.widget_test)
        self.comboBox_pw_position.addItem("")
        self.comboBox_pw_position.addItem("")
        self.comboBox_pw_position.setObjectName(u"comboBox_pw_position")

        self.horizontalLayout_6.addWidget(self.comboBox_pw_position)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_6 = QLabel(self.widget_test)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_5.addWidget(self.label_6)

        self.label_preview_filename = QLabel(self.widget_test)
        self.label_preview_filename.setObjectName(u"label_preview_filename")

        self.verticalLayout_5.addWidget(self.label_preview_filename)


        self.verticalLayout_3.addLayout(self.verticalLayout_5)


        self.verticalLayout.addWidget(self.widget_test)

        self.widget_extract = QWidget(self.scrollAreaWidgetContents)
        self.widget_extract.setObjectName(u"widget_extract")
        self.verticalLayout_4 = QVBoxLayout(self.widget_extract)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.radioButton_mode2_smart_extract = QRadioButton(self.widget_extract)
        self.radioButton_mode2_smart_extract.setObjectName(u"radioButton_mode2_smart_extract")

        self.verticalLayout_4.addWidget(self.radioButton_mode2_smart_extract)

        self.radioButton_mode2_direct_extract = QRadioButton(self.widget_extract)
        self.radioButton_mode2_direct_extract.setObjectName(u"radioButton_mode2_direct_extract")

        self.verticalLayout_4.addWidget(self.radioButton_mode2_direct_extract)

        self.radioButton_mode2_extract_same_folder = QRadioButton(self.widget_extract)
        self.radioButton_mode2_extract_same_folder.setObjectName(u"radioButton_mode2_extract_same_folder")

        self.verticalLayout_4.addWidget(self.radioButton_mode2_extract_same_folder)

        self.line_5 = QFrame(self.widget_extract)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line_5)

        self.checkBox_delete_origin = QCheckBox(self.widget_extract)
        self.checkBox_delete_origin.setObjectName(u"checkBox_delete_origin")

        self.verticalLayout_4.addWidget(self.checkBox_delete_origin)

        self.checkBox_recursive_extract = QCheckBox(self.widget_extract)
        self.checkBox_recursive_extract.setObjectName(u"checkBox_recursive_extract")

        self.verticalLayout_4.addWidget(self.checkBox_recursive_extract)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget_extract)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBox_cover_file = QComboBox(self.widget_extract)
        self.comboBox_cover_file.addItem("")
        self.comboBox_cover_file.addItem("")
        self.comboBox_cover_file.addItem("")
        self.comboBox_cover_file.addItem("")
        self.comboBox_cover_file.setObjectName(u"comboBox_cover_file")

        self.horizontalLayout.addWidget(self.comboBox_cover_file)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_break_folder = QCheckBox(self.widget_extract)
        self.checkBox_break_folder.setObjectName(u"checkBox_break_folder")

        self.horizontalLayout_2.addWidget(self.checkBox_break_folder)

        self.comboBox_break_folder = QComboBox(self.widget_extract)
        self.comboBox_break_folder.addItem("")
        self.comboBox_break_folder.addItem("")
        self.comboBox_break_folder.addItem("")
        self.comboBox_break_folder.setObjectName(u"comboBox_break_folder")

        self.horizontalLayout_2.addWidget(self.comboBox_break_folder)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.checkBox_extract_output_folder = QCheckBox(self.widget_extract)
        self.checkBox_extract_output_folder.setObjectName(u"checkBox_extract_output_folder")

        self.verticalLayout_4.addWidget(self.checkBox_extract_output_folder)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_extract_output_folder = QLineEdit(self.widget_extract)
        self.lineEdit_extract_output_folder.setObjectName(u"lineEdit_extract_output_folder")

        self.horizontalLayout_3.addWidget(self.lineEdit_extract_output_folder)

        self.toolButton_choose = QToolButton(self.widget_extract)
        self.toolButton_choose.setObjectName(u"toolButton_choose")

        self.horizontalLayout_3.addWidget(self.toolButton_choose)

        self.toolButton_open = QToolButton(self.widget_extract)
        self.toolButton_open.setObjectName(u"toolButton_open")

        self.horizontalLayout_3.addWidget(self.toolButton_open)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.checkBox_extract_filter = QCheckBox(self.widget_extract)
        self.checkBox_extract_filter.setObjectName(u"checkBox_extract_filter")

        self.verticalLayout_4.addWidget(self.checkBox_extract_filter)

        self.plainTextEdit_extract_filter_rule = QPlainTextEdit(self.widget_extract)
        self.plainTextEdit_extract_filter_rule.setObjectName(u"plainTextEdit_extract_filter_rule")

        self.verticalLayout_4.addWidget(self.plainTextEdit_extract_filter_rule)


        self.verticalLayout.addWidget(self.widget_extract)

        self.line_2 = QFrame(self.scrollAreaWidgetContents)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.checkBox_top_window = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_top_window.setObjectName(u"checkBox_top_window")

        self.verticalLayout.addWidget(self.checkBox_top_window)

        self.checkBox_lock_size = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_lock_size.setObjectName(u"checkBox_lock_size")

        self.verticalLayout.addWidget(self.checkBox_lock_size)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.radioButton_mode1_test.setText(QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u5bc6\u7801", None))
        self.radioButton_mode1_extract.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u6587\u4ef6", None))
        self.checkBox_try_unknown_filetype.setText(QCoreApplication.translate("Form", u"\u5c1d\u8bd5\u5904\u7406\u672a\u77e5\u683c\u5f0f\u6587\u4ef6", None))
        self.checkBox_write_filename.setText(QCoreApplication.translate("Form", u"\u5c06\u5bc6\u7801\u5199\u5165\u6587\u4ef6\u540d", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\u6587\u672c\u683c\u5f0f:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\u5de6\u4fa7\u5b57\u7b26:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\u53f3\u4fa7\u5b57\u7b26:", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\u4f4d\u7f6e:", None))
        self.comboBox_pw_position.setItemText(0, QCoreApplication.translate("Form", u"\u6700\u5de6\u7aef", None))
        self.comboBox_pw_position.setItemText(1, QCoreApplication.translate("Form", u"\u6700\u53f3\u7aef", None))

        self.label_6.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u540d\u9884\u89c8:", None))
        self.label_preview_filename.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u540d\u793a\u4f8b", None))
        self.radioButton_mode2_smart_extract.setText(QCoreApplication.translate("Form", u"\u667a\u80fd\u89e3\u538b", None))
        self.radioButton_mode2_direct_extract.setText(QCoreApplication.translate("Form", u"\u76f4\u63a5\u89e3\u538b", None))
        self.radioButton_mode2_extract_same_folder.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u5230\u540c\u540d\u76ee\u5f55", None))
        self.checkBox_delete_origin.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u540e\u5220\u9664\u539f\u6587\u4ef6", None))
        self.checkBox_recursive_extract.setText(QCoreApplication.translate("Form", u"\u9012\u5f52\u89e3\u538b\u5d4c\u5957\u538b\u7f29\u5305", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8986\u76d6\u6a21\u5f0f", None))
        self.comboBox_cover_file.setItemText(0, QCoreApplication.translate("Form", u"\u8986\u76d6\u91cd\u590d\u6587\u4ef6", None))
        self.comboBox_cover_file.setItemText(1, QCoreApplication.translate("Form", u"\u8df3\u8fc7\u91cd\u590d\u6587\u4ef6", None))
        self.comboBox_cover_file.setItemText(2, QCoreApplication.translate("Form", u"\u91cd\u547d\u540d\u65b0\u6587\u4ef6", None))
        self.comboBox_cover_file.setItemText(3, QCoreApplication.translate("Form", u"\u91cd\u547d\u540d\u65e7\u6587\u4ef6", None))

        self.checkBox_break_folder.setText(QCoreApplication.translate("Form", u"\u89e3\u6563\u6587\u4ef6\u5939", None))
        self.comboBox_break_folder.setItemText(0, QCoreApplication.translate("Form", u"\u79fb\u52a8\u5230\u9876\u5c42\u76ee\u5f55", None))
        self.comboBox_break_folder.setItemText(1, QCoreApplication.translate("Form", u"\u79fb\u52a8\u5e95\u5c42\u6587\u4ef6\u5939", None))
        self.comboBox_break_folder.setItemText(2, QCoreApplication.translate("Form", u"\u4ec5\u79fb\u52a8\u6587\u4ef6", None))

        self.checkBox_extract_output_folder.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u81f3\u6307\u5b9a\u76ee\u5f55", None))
        self.toolButton_choose.setText(QCoreApplication.translate("Form", u"c", None))
        self.toolButton_open.setText(QCoreApplication.translate("Form", u"o", None))
        self.checkBox_extract_filter.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u8fc7\u6ee4\u89c4\u5219", None))
        self.checkBox_top_window.setText(QCoreApplication.translate("Form", u"\u7f6e\u9876\u7a0b\u5e8f\u7a97\u53e3", None))
        self.checkBox_lock_size.setText(QCoreApplication.translate("Form", u"\u9501\u5b9a\u7a97\u53e3\u5927\u5c0f", None))
    # retranslateUi

