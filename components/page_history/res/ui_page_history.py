# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_historyaEjmJb.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QSizePolicy,
    QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(320, 240)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBox_result_state = QComboBox(Form)
        self.comboBox_result_state.setObjectName(u"comboBox_result_state")

        self.horizontalLayout.addWidget(self.comboBox_result_state)

        self.lineEdit_search = QLineEdit(Form)
        self.lineEdit_search.setObjectName(u"lineEdit_search")

        self.horizontalLayout.addWidget(self.lineEdit_search)

        self.toolButton_filter = QToolButton(Form)
        self.toolButton_filter.setObjectName(u"toolButton_filter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_filter.sizePolicy().hasHeightForWidth())
        self.toolButton_filter.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.toolButton_filter)

        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget_records = QListWidget(Form)
        self.listWidget_records.setObjectName(u"listWidget_records")

        self.verticalLayout.addWidget(self.listWidget_records)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u7b5b\u9009\u5668\uff1a", None))
        self.toolButton_filter.setText(QCoreApplication.translate("Form", u"\u67e5\u8be2", None))
    # retranslateUi

