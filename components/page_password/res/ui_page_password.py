# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_page_passwordOfnyZo.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QPlainTextEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(320, 240)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.plainTextEdit_password = QPlainTextEdit(Form)
        self.plainTextEdit_password.setObjectName(u"plainTextEdit_password")

        self.verticalLayout_2.addWidget(self.plainTextEdit_password)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_clipboard = QPushButton(Form)
        self.pushButton_clipboard.setObjectName(u"pushButton_clipboard")

        self.verticalLayout.addWidget(self.pushButton_clipboard)

        self.pushButton_output = QPushButton(Form)
        self.pushButton_output.setObjectName(u"pushButton_output")

        self.verticalLayout.addWidget(self.pushButton_output)

        self.pushButton_open = QPushButton(Form)
        self.pushButton_open.setObjectName(u"pushButton_open")

        self.verticalLayout.addWidget(self.pushButton_open)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.pushButton_update = QPushButton(Form)
        self.pushButton_update.setObjectName(u"pushButton_update")

        self.horizontalLayout.addWidget(self.pushButton_update)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_clipboard.setText(QCoreApplication.translate("Form", u"\u8bfb\u53d6\u526a\u5207\u677f", None))
        self.pushButton_output.setText(QCoreApplication.translate("Form", u"\u5bfc\u51fa\u5bc6\u7801", None))
        self.pushButton_open.setText(QCoreApplication.translate("Form", u"\u6253\u5f00\u5bfc\u51fa\u6587\u4ef6", None))
        self.pushButton_update.setText(QCoreApplication.translate("Form", u"\u66f4\u65b0\u5bc6\u7801\u672c", None))
    # retranslateUi

