# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_homebkUIcq.ui'
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
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_label_drop = QVBoxLayout()
        self.verticalLayout_label_drop.setObjectName(u"verticalLayout_label_drop")

        self.verticalLayout_3.addLayout(self.verticalLayout_label_drop)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.label_progress_total = QLabel(Form)
        self.label_progress_total.setObjectName(u"label_progress_total")

        self.horizontalLayout_2.addWidget(self.label_progress_total)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.label_runtime_total = QLabel(Form)
        self.label_runtime_total.setObjectName(u"label_runtime_total")

        self.horizontalLayout.addWidget(self.label_runtime_total)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_4.addWidget(self.label_5)

        self.label_runtime_current = QLabel(Form)
        self.label_runtime_current.setObjectName(u"label_runtime_current")

        self.horizontalLayout_4.addWidget(self.label_runtime_current)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.toolButton_stop = QToolButton(Form)
        self.toolButton_stop.setObjectName(u"toolButton_stop")

        self.horizontalLayout_7.addWidget(self.toolButton_stop)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)


        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.label_current_file = QLabel(Form)
        self.label_current_file.setObjectName(u"label_current_file")

        self.verticalLayout_3.addWidget(self.label_current_file)

        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_9 = QLabel(self.page)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_5.addWidget(self.label_9)

        self.label_progress_test = QLabel(self.page)
        self.label_progress_test.setObjectName(u"label_progress_test")

        self.horizontalLayout_5.addWidget(self.label_progress_test)

        self.horizontalLayout_5.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_11 = QLabel(self.page)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_6.addWidget(self.label_11)

        self.label_current_password = QLabel(self.page)
        self.label_current_password.setObjectName(u"label_current_password")

        self.horizontalLayout_6.addWidget(self.label_current_password)

        self.horizontalLayout_6.setStretch(1, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout = QVBoxLayout(self.page_2)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_13 = QLabel(self.page_2)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_3.addWidget(self.label_13)

        self.label_right_password = QLabel(self.page_2)
        self.label_right_password.setObjectName(u"label_right_password")

        self.horizontalLayout_3.addWidget(self.label_right_password)

        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.progressBar_progress_extract = QProgressBar(self.page_2)
        self.progressBar_progress_extract.setObjectName(u"progressBar_progress_extract")
        self.progressBar_progress_extract.setValue(24)

        self.verticalLayout.addWidget(self.progressBar_progress_extract)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout_3.addWidget(self.stackedWidget)

        self.verticalLayout_3.setStretch(0, 1)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u603b\u8fdb\u5ea6", None))
        self.label_progress_total.setText(QCoreApplication.translate("Form", u"-/-", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u603b\u8017\u65f6:", None))
        self.label_runtime_total.setText(QCoreApplication.translate("Form", u"0:00:00", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u8017\u65f6:", None))
        self.label_runtime_current.setText(QCoreApplication.translate("Form", u"0:00:00", None))
        self.toolButton_stop.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u6587\u4ef6:", None))
        self.label_current_file.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u5bc6\u7801:", None))
        self.label_progress_test.setText(QCoreApplication.translate("Form", u"-/-", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u5bc6\u7801:", None))
        self.label_current_password.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u8fdb\u5ea6:", None))
        self.label_right_password.setText(QCoreApplication.translate("Form", u"\u6b63\u786e\u5bc6\u7801", None))
    # retranslateUi

