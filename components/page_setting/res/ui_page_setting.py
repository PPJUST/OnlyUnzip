# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_settinggAfybw.ui'
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
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(Form)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -372, 301, 610))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
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

        self.checkBox_read_password_from_filename = QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_read_password_from_filename.setObjectName(u"checkBox_read_password_from_filename")

        self.verticalLayout.addWidget(self.checkBox_read_password_from_filename)

        self.line_4 = QFrame(self.scrollAreaWidgetContents)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.widget_test = QWidget(self.scrollAreaWidgetContents)
        self.widget_test.setObjectName(u"widget_test")
        self.verticalLayout_3 = QVBoxLayout(self.widget_test)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.checkBox_write_filename = QCheckBox(self.widget_test)
        self.checkBox_write_filename.setObjectName(u"checkBox_write_filename")

        self.verticalLayout_3.addWidget(self.checkBox_write_filename)

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
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
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
        self.comboBox_cover_file.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
        self.comboBox_cover_file.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.comboBox_cover_file.setDuplicatesEnabled(False)

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
        self.comboBox_break_folder.setFocusPolicy(Qt.FocusPolicy.WheelFocus)

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
#if QT_CONFIG(tooltip)
        self.radioButton_mode1_test.setToolTip(QCoreApplication.translate("Form", u"\u9010\u4e2a\u6d4b\u8bd5\u5bc6\u7801\u672c\u4e2d\u7684\u5bc6\u7801\uff0c\u76f4\u5230\u68c0\u7d22\u5230\u6b63\u786e\u7684\u5bc6\u7801", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_mode1_test.setText(QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u5bc6\u7801", None))
#if QT_CONFIG(tooltip)
        self.radioButton_mode1_extract.setToolTip(QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u5bc6\u7801\u5e76\u89e3\u538b\u5230\u672c\u5730", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_mode1_extract.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.checkBox_try_unknown_filetype.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u5ffd\u7565\u6587\u4ef6\u7c7b\u578b\uff0c\u5bf9\u6240\u6709\u7c7b\u578b\u7684\u6587\u4ef6\u8fdb\u884c\u6d4b\u8bd5\u6216\u89e3\u538b</p><p>\u6ce8\u610f\uff1a</p><p>1. \u542f\u7528\u8be5\u9009\u9879\u8fdb\u884c\u89e3\u538b\u65f6\uff0c\u4f1a\u5bfc\u81f4 exe/doc/xls \u7b49\u7c7b\u578b\u7684\u6587\u4ef6\u88ab\u89e3\u538b\u3002</p><p>2. \u5224\u65ad\u6587\u4ef6\u7c7b\u578b\u7684\u65b9\u6cd5\u4e3a\u8bfb\u53d6\u6587\u4ef6\u5934\uff0c\u53ef\u80fd\u5b58\u5728\u90e8\u5206\u6587\u4ef6\u7c7b\u578b\u88ab\u8bef\u5224/\u65e0\u6cd5\u5224\u65ad\u7684\u60c5\u51b5\u3002</p><p>3. \u5bf9\u4e8e\u4f2a\u88c5\u4e3a\u5a92\u4f53\u683c\u5f0f\u7684\u538b\u7f29\u6587\u4ef6\uff0c\u53ef\u4ee5\u542f\u7528\u8be5\u9009\u9879\u8fdb\u884c\u5c1d\u8bd5\uff08\u90e8\u5206\u6587\u4ef6\u53ef\u4ee5\u6b63\u5e38\u8fdb\u884c\u6d4b\u8bd5/\u89e3\u538b\uff09\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_try_unknown_filetype.setText(QCoreApplication.translate("Form", u"\u5c1d\u8bd5\u5904\u7406\u672a\u77e5\u683c\u5f0f\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.checkBox_read_password_from_filename.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u4ece\u6587\u4ef6\u540d\u4e2d\u8bfb\u53d6\u53ef\u80fd\u5b58\u5728\u7684\u5bc6\u7801\u3002</p><p>\u652f\u6301\u7684\u683c\u5f0f\uff08\u4ee5xxx\u6307\u4ee3\u5bc6\u7801\uff09\uff1a</p><p>1. \u4ee5\u7a7a\u683c\u4e3a\u95f4\u9694\u7684\u4e24\u7aef\u5b57\u7b26\uff1axxx \u6587\u4ef6\u540d/\u6587\u4ef6\u540d xxx</p><p>2. \u4ee5#\u5f00\u5934\uff0c\u7a7a\u683c\u7ed3\u5c3e\u7684\u5b57\u7b26\uff1a#xxx \u6587\u4ef6\u540d</p><p>3. \u4ee5@\u5f00\u5934\uff0c\u7a7a\u683c\u7ed3\u5c3e\u7684\u5b57\u7b26\uff1a@xxx \u6587\u4ef6\u540d</p><p>4. \u5728\u3010\u3011\u3001[]\u3001()\u4e2d\u7684\u5b57\u7b26\uff1a\u3010xxx\u3011\u6587\u4ef6\u540d</p><p>5. \u4ee5&quot;\u5bc6\u7801&quot;\u3001&quot;\u89e3\u538b\u7801&quot;\u3001&quot;\u89e3\u538b\u5bc6\u7801&quot;\u3001&quot;pw&quot;\u3001&quot;PW&quot;\u4ee5\u53ca\u4e0a\u8ff0\u5b57\u7b26\u540e\u5e26&quot;:&quot;\u3001&quot;\uff1a&quot;\u5f00\u5934\uff0c\u7a7a\u683c\u7ed3\u5c3e\u7684\u5b57\u7b26\uff1a\u5bc6\u7801xxx \u6587\u4ef6\u540d/\u89e3\u538b\u5bc6\u7801:xxx \u6587"
                        "\u4ef6\u540d</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_read_password_from_filename.setText(QCoreApplication.translate("Form", u"\u5c1d\u8bd5\u4ece\u6587\u4ef6\u540d\u4e2d\u8bfb\u53d6\u5bc6\u7801", None))
#if QT_CONFIG(tooltip)
        self.checkBox_write_filename.setToolTip(QCoreApplication.translate("Form", u"\u5982\u679c\u68c0\u7d22\u5230\u6b63\u786e\u7684\u5bc6\u7801\uff0c\u5219\u5c06\u6539\u5bc6\u7801\u5199\u5165\u6587\u4ef6\u540d\u4e2d", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_write_filename.setText(QCoreApplication.translate("Form", u"\u5c06\u5bc6\u7801\u5199\u5165\u6587\u4ef6\u540d", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\u6587\u672c\u683c\u5f0f:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\u5de6\u4fa7\u5b57\u7b26:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_left_word.setToolTip(QCoreApplication.translate("Form", u"\u5199\u5165\u6587\u4ef6\u540d\u65f6\u6dfb\u52a0\u5728\u5de6\u4fa7\u7684\u5b57\u7b26", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\u53f3\u4fa7\u5b57\u7b26:", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_right_word.setToolTip(QCoreApplication.translate("Form", u"\u5199\u5165\u6587\u4ef6\u540d\u65f6\u6dfb\u52a0\u5728\u53f3\u4fa7\u7684\u5b57\u7b26", None))
#endif // QT_CONFIG(tooltip)
        self.label_5.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\u4f4d\u7f6e:", None))
        self.comboBox_pw_position.setItemText(0, QCoreApplication.translate("Form", u"\u6700\u5de6\u7aef", None))
        self.comboBox_pw_position.setItemText(1, QCoreApplication.translate("Form", u"\u6700\u53f3\u7aef", None))

#if QT_CONFIG(tooltip)
        self.comboBox_pw_position.setToolTip(QCoreApplication.translate("Form", u"\u5199\u5165\u7684\u4f4d\u7f6e\uff0c\u5199\u5165\u5728\u6700\u5de6\u7aef\u6216\u8005\u6700\u53f3\u7aef", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u540d\u9884\u89c8:", None))
        self.label_preview_filename.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u540d\u793a\u4f8b", None))
#if QT_CONFIG(tooltip)
        self.radioButton_mode2_smart_extract.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u81ea\u52a8\u5224\u65ad\u6587\u4ef6\u5c42\u7ea7\u7ed3\u6784\u8fdb\u884c\u89e3\u538b\uff0c\u7c7b\u4f3c\u4e8eBandizip\u3002</p><p>\u5982\u679c\u4ec5\u5b58\u5728\u5355\u4e2a\u6587\u4ef6/\u6587\u4ef6\u5939\uff0c\u5219\u76f4\u63a5\u89e3\u538b\uff0c\u5982\u679c\u5b58\u5728\u591a\u4e2a\u6587\u4ef6\u4e14\u65e0\u4e0a\u7ea7\u6587\u4ef6\u5939\uff0c\u5219\u81ea\u52a8\u521b\u5efa\u6587\u4ef6\u5939\u5e76\u89e3\u538b\u5230\u8be5\u6587\u4ef6\u5939\u4e0b\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_mode2_smart_extract.setText(QCoreApplication.translate("Form", u"\u667a\u80fd\u89e3\u538b", None))
#if QT_CONFIG(tooltip)
        self.radioButton_mode2_direct_extract.setToolTip(QCoreApplication.translate("Form", u"\u4e0d\u5bf9\u6587\u4ef6\u5c42\u7ea7\u7ed3\u6784\u8fdb\u884c\u68c0\u67e5\uff0c\u4e0d\u8fdb\u884c\u5904\u7406\u76f4\u63a5\u89e3\u538b", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_mode2_direct_extract.setText(QCoreApplication.translate("Form", u"\u76f4\u63a5\u89e3\u538b", None))
#if QT_CONFIG(tooltip)
        self.radioButton_mode2_extract_same_folder.setToolTip(QCoreApplication.translate("Form", u"\u89e3\u538b\u5230\u4ee5\u538b\u7f29\u6587\u4ef6\u540d\u547d\u540d\u7684\u6587\u4ef6\u5939\u4e2d", None))
#endif // QT_CONFIG(tooltip)
        self.radioButton_mode2_extract_same_folder.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u5230\u540c\u540d\u76ee\u5f55", None))
#if QT_CONFIG(tooltip)
        self.checkBox_delete_origin.setToolTip(QCoreApplication.translate("Form", u"\u6210\u529f\u89e3\u538b\u540e\u5220\u9664\u6e90\u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_delete_origin.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u540e\u5220\u9664\u539f\u6587\u4ef6", None))
#if QT_CONFIG(tooltip)
        self.checkBox_recursive_extract.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u89e3\u538b\u5d4c\u5957\u7684\u538b\u7f29\u6587\u4ef6\uff0c\u76f4\u5230\u89e3\u538b\u7ed3\u679c\u4e2d\u4e0d\u5b58\u5728\u538b\u7f29\u6587\u4ef6\u3002</p><p>\u5b9e\u73b0\u65b9\u6cd5\uff1a\u5bf9\u89e3\u538b\u7684\u7ed3\u679c\u8fdb\u884c\u518d\u4e00\u6b21\u7684\u89e3\u538b\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_recursive_extract.setText(QCoreApplication.translate("Form", u"\u9012\u5f52\u89e3\u538b\u5d4c\u5957\u538b\u7f29\u5305", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8986\u76d6\u6a21\u5f0f", None))
        self.comboBox_cover_file.setItemText(0, QCoreApplication.translate("Form", u"\u8986\u76d6\u91cd\u590d\u6587\u4ef6", None))
        self.comboBox_cover_file.setItemText(1, QCoreApplication.translate("Form", u"\u8df3\u8fc7\u91cd\u590d\u6587\u4ef6", None))
        self.comboBox_cover_file.setItemText(2, QCoreApplication.translate("Form", u"\u91cd\u547d\u540d\u65b0\u6587\u4ef6", None))
        self.comboBox_cover_file.setItemText(3, QCoreApplication.translate("Form", u"\u91cd\u547d\u540d\u65e7\u6587\u4ef6", None))

#if QT_CONFIG(tooltip)
        self.comboBox_cover_file.setToolTip(QCoreApplication.translate("Form", u"\u89e3\u538b\u6587\u4ef6\u5b58\u5728\u51b2\u7a81\u65f6\u7684\u5904\u7406\u65b9\u6cd5", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_break_folder.setText(QCoreApplication.translate("Form", u"\u89e3\u6563\u6587\u4ef6\u5939", None))
        self.comboBox_break_folder.setItemText(0, QCoreApplication.translate("Form", u"\u79fb\u52a8\u5230\u9876\u5c42\u76ee\u5f55", None))
        self.comboBox_break_folder.setItemText(1, QCoreApplication.translate("Form", u"\u79fb\u52a8\u5e95\u5c42\u6587\u4ef6\u5939", None))
        self.comboBox_break_folder.setItemText(2, QCoreApplication.translate("Form", u"\u4ec5\u79fb\u52a8\u6587\u4ef6", None))

#if QT_CONFIG(tooltip)
        self.comboBox_break_folder.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u5904\u7406\u591a\u5c42\u7ea7\u7684\u6587\u4ef6\u5939\u7ed3\u6784\uff0c\u7528\u4e8e\u6e05\u7406\u7a7a\u6587\u4ef6\u5939\u3002</p><p>\u79fb\u52a8\u5230\u9876\u5c42\u76ee\u5f55\uff1a\u79fb\u52a8\u6700\u5e95\u5c42\u7684\u9996\u4e2a\u975e\u7a7a\u6587\u4ef6\u5939\u4e0b\u7684\u6587\u4ef6\u5230\u9876\u5c42\u76ee\u5f55\u4e4b\u4e0b\uff08\u4fdd\u6301\u6587\u4ef6\u5c42\u7ea7\u7ed3\u6784\uff0c\u5e76\u5220\u9664\u7a7a\u7684\u8be5\u5e95\u5c42\u6587\u4ef6\u5939\uff09\u3002</p><p>\u79fb\u52a8\u5e95\u5c42\u6587\u4ef6\u5939\uff1a\u79fb\u52a8\u6700\u5e95\u5c42\u7684\u9996\u4e2a\u975e\u7a7a\u6587\u4ef6\u5939\u5230\u9876\u5c42\u76ee\u5f55\u4e4b\u5916\uff08\u5e76\u5220\u9664\u7a7a\u7684\u9876\u5c42\u76ee\u5f55\uff09\u3002</p><p>\u4ec5\u79fb\u52a8\u6587\u4ef6\uff1a\u79fb\u52a8\u6240\u6709\u6587\u4ef6\u5230\u9876\u5c42\u76ee\u5f55\u4e4b\u4e0b\uff08\u5e76\u5220\u9664\u7a7a\u7684\u5b50\u6587\u4ef6\u5939\uff09\u3002</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkBox_extract_output_folder.setToolTip(QCoreApplication.translate("Form", u"\u89e3\u538b\u5230\u8be5\u6307\u5b9a\u7684\u6587\u4ef6\u5939\uff0c\u800c\u4e0d\u662f\u6e90\u6587\u4ef6\u7684\u540c\u7ea7\u6587\u4ef6\u5939\u4e2d", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_extract_output_folder.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u81f3\u6307\u5b9a\u76ee\u5f55", None))
        self.toolButton_choose.setText(QCoreApplication.translate("Form", u"c", None))
        self.toolButton_open.setText(QCoreApplication.translate("Form", u"o", None))
#if QT_CONFIG(tooltip)
        self.checkBox_extract_filter.setToolTip(QCoreApplication.translate("Form", u"\u89e3\u538b\u65f6\u8fc7\u6ee4\u7b26\u5408\u6761\u4ef6\u7684\u6587\u4ef6\uff08\u4e0d\u89e3\u538b\u8be5\u90e8\u5206\u6587\u4ef6\uff09", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_extract_filter.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u8fc7\u6ee4\u89c4\u5219", None))
#if QT_CONFIG(tooltip)
        self.plainTextEdit_extract_filter_rule.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>\u89e3\u538b\u65f6\u8fc7\u6ee4\u6389\u7b26\u5408\u89c4\u5219\u7684\u6587\u4ef6\uff0c\u901a\u914d\u7b26\u4e3a*\uff0c\u5982\u65e0\u7279\u6b8a\u9700\u6c42\u5efa\u8bae\u4e0d\u4f7f\u7528\u8be5\u529f\u80fd\u3002</p><p>\u793a\u4f8b\uff1a</p><p>1. \u8fc7\u6ee4\u6307\u5b9a\u6587\u4ef6\u540d\uff1a\u5e7f\u544a.*</p><p>2. \u8fc7\u6ee4\u90e8\u5206\u6587\u4ef6\u540d\uff1a*\u6c49\u5316\u7ec4*.*</p><p>3. \u8fc7\u6ee4\u6307\u5b9a\u6587\u4ef6\u6269\u5c55\u540d\uff1a*.html</p><p>3. \u8fc7\u6ee4\u4e0d\u7a33\u6587\u4ef6\u6269\u5c55\uff1a*.*xls*</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.checkBox_top_window.setToolTip(QCoreApplication.translate("Form", u"\u4fdd\u6301\u7a97\u53e3\u5728\u524d\u53f0", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_top_window.setText(QCoreApplication.translate("Form", u"\u7f6e\u9876\u7a0b\u5e8f\u7a97\u53e3", None))
#if QT_CONFIG(tooltip)
        self.checkBox_lock_size.setToolTip(QCoreApplication.translate("Form", u"\u9501\u5b9a\u7a97\u53e3\u5c3a\u5bf8\uff0c\u7981\u6b62\u4fee\u6539", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_lock_size.setText(QCoreApplication.translate("Form", u"\u9501\u5b9a\u7a97\u53e3\u5927\u5c0f", None))
    # retranslateUi

