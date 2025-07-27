# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_homeFNBYKZ.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QProgressBar, QSizePolicy, QStackedWidget,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(289, 314)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_label_drop = QVBoxLayout()
        self.verticalLayout_label_drop.setObjectName(u"verticalLayout_label_drop")

        self.verticalLayout.addLayout(self.verticalLayout_label_drop)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_welcome = QWidget()
        self.page_welcome.setObjectName(u"page_welcome")
        self.horizontalLayout = QHBoxLayout(self.page_welcome)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.page_welcome)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.stackedWidget.addWidget(self.page_welcome)
        self.page_step_notice = QWidget()
        self.page_step_notice.setObjectName(u"page_step_notice")
        self.horizontalLayout_2 = QHBoxLayout(self.page_step_notice)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_step_notice = QLabel(self.page_step_notice)
        self.label_step_notice.setObjectName(u"label_step_notice")

        self.horizontalLayout_2.addWidget(self.label_step_notice)

        self.stackedWidget.addWidget(self.page_step_notice)
        self.page_test_and_extract = QWidget()
        self.page_test_and_extract.setObjectName(u"page_test_and_extract")
        self.verticalLayout_5 = QVBoxLayout(self.page_test_and_extract)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_6 = QLabel(self.page_test_and_extract)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_10.addWidget(self.label_6)

        self.label_progress_total = QLabel(self.page_test_and_extract)
        self.label_progress_total.setObjectName(u"label_progress_total")

        self.horizontalLayout_10.addWidget(self.label_progress_total)


        self.gridLayout.addLayout(self.horizontalLayout_10, 0, 0, 1, 1)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_8 = QLabel(self.page_test_and_extract)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_11.addWidget(self.label_8)

        self.label_runtime_total = QLabel(self.page_test_and_extract)
        self.label_runtime_total.setObjectName(u"label_runtime_total")

        self.horizontalLayout_11.addWidget(self.label_runtime_total)


        self.gridLayout.addLayout(self.horizontalLayout_11, 0, 1, 1, 1)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.page_test_and_extract)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_12.addWidget(self.label_10)

        self.label_runtime_current = QLabel(self.page_test_and_extract)
        self.label_runtime_current.setObjectName(u"label_runtime_current")

        self.horizontalLayout_12.addWidget(self.label_runtime_current)


        self.gridLayout.addLayout(self.horizontalLayout_12, 1, 1, 1, 1)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.toolButton_stop = QToolButton(self.page_test_and_extract)
        self.toolButton_stop.setObjectName(u"toolButton_stop")

        self.horizontalLayout_13.addWidget(self.toolButton_stop)

        self.label_12 = QLabel(self.page_test_and_extract)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_13.addWidget(self.label_12)


        self.gridLayout.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout)

        self.label_current_file = QLabel(self.page_test_and_extract)
        self.label_current_file.setObjectName(u"label_current_file")

        self.verticalLayout_5.addWidget(self.label_current_file)

        self.stackedWidget_2 = QStackedWidget(self.page_test_and_extract)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_4 = QVBoxLayout(self.page_3)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_14 = QLabel(self.page_3)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_14.addWidget(self.label_14)

        self.label_progress_test = QLabel(self.page_3)
        self.label_progress_test.setObjectName(u"label_progress_test")

        self.horizontalLayout_14.addWidget(self.label_progress_test)

        self.horizontalLayout_14.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_15 = QLabel(self.page_3)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_15.addWidget(self.label_15)

        self.label_current_password = QLabel(self.page_3)
        self.label_current_password.setObjectName(u"label_current_password")

        self.horizontalLayout_15.addWidget(self.label_current_password)

        self.horizontalLayout_15.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_15)

        self.stackedWidget_2.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_6 = QVBoxLayout(self.page_4)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_16 = QLabel(self.page_4)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_16.addWidget(self.label_16)

        self.label_right_password = QLabel(self.page_4)
        self.label_right_password.setObjectName(u"label_right_password")

        self.horizontalLayout_16.addWidget(self.label_right_password)

        self.horizontalLayout_16.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_16)

        self.progressBar_progress_extract = QProgressBar(self.page_4)
        self.progressBar_progress_extract.setObjectName(u"progressBar_progress_extract")
        self.progressBar_progress_extract.setValue(24)

        self.verticalLayout_6.addWidget(self.progressBar_progress_extract)

        self.stackedWidget_2.addWidget(self.page_4)

        self.verticalLayout_5.addWidget(self.stackedWidget_2)

        self.stackedWidget.addWidget(self.page_test_and_extract)
        self.page_result = QWidget()
        self.page_result.setObjectName(u"page_result")
        self.gridLayout_3 = QGridLayout(self.page_result)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_17 = QLabel(self.page_result)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_3.addWidget(self.label_17, 0, 0, 1, 1)

        self.label_time_final = QLabel(self.page_result)
        self.label_time_final.setObjectName(u"label_time_final")

        self.gridLayout_3.addWidget(self.label_time_final, 0, 1, 1, 1)

        self.label_18 = QLabel(self.page_result)
        self.label_18.setObjectName(u"label_18")

        self.gridLayout_3.addWidget(self.label_18, 1, 0, 1, 1)

        self.label_process_file_count = QLabel(self.page_result)
        self.label_process_file_count.setObjectName(u"label_process_file_count")

        self.gridLayout_3.addWidget(self.label_process_file_count, 1, 1, 1, 1)

        self.label_19 = QLabel(self.page_result)
        self.label_19.setObjectName(u"label_19")

        self.gridLayout_3.addWidget(self.label_19, 2, 0, 1, 1)

        self.label_result_count = QLabel(self.page_result)
        self.label_result_count.setObjectName(u"label_result_count")

        self.gridLayout_3.addWidget(self.label_result_count, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.page_result)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(3)
        self.stackedWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u62d6\u5165\u6587\u4ef6\u5230\u53f3\u4fa7\u533a\u57df\u5373\u53ef\u5904\u7406\u6587\u4ef6", None))
        self.label_step_notice.setText(QCoreApplication.translate("Form", u"\u6b65\u9aa4\u63d0\u793a", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u603b\u8fdb\u5ea6", None))
        self.label_progress_total.setText(QCoreApplication.translate("Form", u"-/-", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u603b\u8017\u65f6:", None))
        self.label_runtime_total.setText(QCoreApplication.translate("Form", u"0:00:00", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u8017\u65f6:", None))
        self.label_runtime_current.setText(QCoreApplication.translate("Form", u"0:00:00", None))
        self.toolButton_stop.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u6587\u4ef6:", None))
        self.label_current_file.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u5bc6\u7801:", None))
        self.label_progress_test.setText(QCoreApplication.translate("Form", u"-/-", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u5bc6\u7801:", None))
        self.label_current_password.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_16.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u8fdb\u5ea6:", None))
        self.label_right_password.setText(QCoreApplication.translate("Form", u"\u6b63\u786e\u5bc6\u7801", None))
        self.label_17.setText(QCoreApplication.translate("Form", u"\u8017\u65f6:", None))
        self.label_time_final.setText(QCoreApplication.translate("Form", u"0:00:00", None))
        self.label_18.setText(QCoreApplication.translate("Form", u"\u5904\u7406\u6587\u4ef6\u6570\u91cf:", None))
        self.label_process_file_count.setText(QCoreApplication.translate("Form", u"5", None))
        self.label_19.setText(QCoreApplication.translate("Form", u"\u5904\u7406\u7ed3\u679c\u7edf\u8ba1:", None))
        self.label_result_count.setText(QCoreApplication.translate("Form", u"\u6210\u529f:5, \u5931\u8d25:0", None))
    # retranslateUi

