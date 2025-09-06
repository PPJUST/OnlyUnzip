# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_dialognwXfbF.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QPlainTextEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 240)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.plainTextEdit_password = QPlainTextEdit(Dialog)
        self.plainTextEdit_password.setObjectName(u"plainTextEdit_password")

        self.verticalLayout_2.addWidget(self.plainTextEdit_password)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_read_clipboard = QPushButton(Dialog)
        self.pushButton_read_clipboard.setObjectName(u"pushButton_read_clipboard")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_read_clipboard.sizePolicy().hasHeightForWidth())
        self.pushButton_read_clipboard.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_read_clipboard)

        self.pushButton_clear_password = QPushButton(Dialog)
        self.pushButton_clear_password.setObjectName(u"pushButton_clear_password")
        sizePolicy.setHeightForWidth(self.pushButton_clear_password.sizePolicy().hasHeightForWidth())
        self.pushButton_clear_password.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_clear_password)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.pushButton_write_to_db = QPushButton(Dialog)
        self.pushButton_write_to_db.setObjectName(u"pushButton_write_to_db")
        sizePolicy.setHeightForWidth(self.pushButton_write_to_db.sizePolicy().hasHeightForWidth())
        self.pushButton_write_to_db.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButton_write_to_db)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(0, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u4e34\u65f6\u5bc6\u7801", None))
        self.pushButton_read_clipboard.setText(QCoreApplication.translate("Dialog", u"\u8bfb\u53d6\u526a\u5207\u677f", None))
        self.pushButton_clear_password.setText(QCoreApplication.translate("Dialog", u"\u6e05\u7a7a", None))
        self.pushButton_write_to_db.setText(QCoreApplication.translate("Dialog", u"\u5b58\u50a8\u5230\u5bc6\u7801\u672c", None))
    # retranslateUi

