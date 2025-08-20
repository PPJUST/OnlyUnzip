# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aboutmRSUad.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(244, 188)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.label_version = QLabel(Form)
        self.label_version.setObjectName(u"label_version")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_version)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.label_data = QLabel(Form)
        self.label_data.setObjectName(u"label_data")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_data)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.label_project = QLabel(Form)
        self.label_project.setObjectName(u"label_project")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.label_project)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.label_download_link_1 = QLabel(Form)
        self.label_download_link_1.setObjectName(u"label_download_link_1")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.label_download_link_1)

        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_9)

        self.label_download_link_2 = QLabel(Form)
        self.label_download_link_2.setObjectName(u"label_download_link_2")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.label_download_link_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u7248\u672c\u53f7\uff1a", None))
        self.label_version.setText(QCoreApplication.translate("Form", u"version", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u7f16\u8bd1\u65e5\u671f\uff1a", None))
        self.label_data.setText(QCoreApplication.translate("Form", u"data", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u9879\u76ee\u4e3b\u9875\uff1a", None))
        self.label_project.setText(QCoreApplication.translate("Form", u"project", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d\u5730\u57401\uff1a", None))
        self.label_download_link_1.setText(QCoreApplication.translate("Form", u"download link", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u4e0b\u8f7d\u5730\u57402\uff1a", None))
        self.label_download_link_2.setText(QCoreApplication.translate("Form", u"download link", None))
    # retranslateUi

