# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_widget_page_homepageejiMfL.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QProgressBar, QSizePolicy, QStackedWidget, QToolButton,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(247, 245)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.layout_label_drop = QVBoxLayout()
        self.layout_label_drop.setSpacing(0)
        self.layout_label_drop.setObjectName(u"layout_label_drop")

        self.verticalLayout.addLayout(self.layout_label_drop)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_schedule_file = QLabel(Form)
        self.label_schedule_file.setObjectName(u"label_schedule_file")

        self.horizontalLayout_4.addWidget(self.label_schedule_file)

        self.toolButton_stop = QToolButton(Form)
        self.toolButton_stop.setObjectName(u"toolButton_stop")

        self.horizontalLayout_4.addWidget(self.toolButton_stop)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.label_current_file = QLabel(Form)
        self.label_current_file.setObjectName(u"label_current_file")

        self.verticalLayout.addWidget(self.label_current_file)

        self.stackedWidget = QStackedWidget(Form)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout = QHBoxLayout(self.page)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_state = QLabel(self.page)
        self.label_state.setObjectName(u"label_state")

        self.horizontalLayout.addWidget(self.label_state)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.horizontalLayout_2 = QHBoxLayout(self.page_2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.page_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.label_schedule_test = QLabel(self.page_2)
        self.label_schedule_test.setObjectName(u"label_schedule_test")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_schedule_test.sizePolicy().hasHeightForWidth())
        self.label_schedule_test.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_schedule_test)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_3 = QHBoxLayout(self.page_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.page_3)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_3.addWidget(self.label_6)

        self.progressBar_schedule_extract = QProgressBar(self.page_3)
        self.progressBar_schedule_extract.setObjectName(u"progressBar_schedule_extract")
        self.progressBar_schedule_extract.setMaximumSize(QSize(16777215, 14))
        font = QFont()
        font.setKerning(True)
        self.progressBar_schedule_extract.setFont(font)
        self.progressBar_schedule_extract.setValue(0)
        self.progressBar_schedule_extract.setTextVisible(False)

        self.horizontalLayout_3.addWidget(self.progressBar_schedule_extract)

        self.stackedWidget.addWidget(self.page_3)

        self.verticalLayout.addWidget(self.stackedWidget)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Form)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_schedule_file.setText(QCoreApplication.translate("Form", u"\u603b\u8fdb\u5ea6", None))
        self.toolButton_stop.setText(QCoreApplication.translate("Form", u"...", None))
        self.label_current_file.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u6587\u4ef6", None))
        self.label_state.setText(QCoreApplication.translate("Form", u"\u5f53\u524d\u8fdb\u5ea6", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u6d4b\u8bd5\u5bc6\u7801\uff1a", None))
        self.label_schedule_test.setText(QCoreApplication.translate("Form", u"0/0", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u89e3\u538b\u8fdb\u5ea6\uff1a", None))
    # retranslateUi

