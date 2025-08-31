# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'managerjSYeNs.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(344, 290)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label_pw_count_100 = QLabel(Form)
        self.label_pw_count_100.setObjectName(u"label_pw_count_100")

        self.gridLayout.addWidget(self.label_pw_count_100, 0, 1, 1, 1)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_pw_count_10 = QLabel(Form)
        self.label_pw_count_10.setObjectName(u"label_pw_count_10")

        self.gridLayout.addWidget(self.label_pw_count_10, 1, 1, 1, 1)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_pw_count_1 = QLabel(Form)
        self.label_pw_count_1.setObjectName(u"label_pw_count_1")

        self.gridLayout.addWidget(self.label_pw_count_1, 2, 1, 1, 1)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_pw_count_0 = QLabel(Form)
        self.label_pw_count_0.setObjectName(u"label_pw_count_0")

        self.gridLayout.addWidget(self.label_pw_count_0, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_2.addWidget(self.label_10)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBox_delete_use_count = QCheckBox(Form)
        self.checkBox_delete_use_count.setObjectName(u"checkBox_delete_use_count")

        self.horizontalLayout.addWidget(self.checkBox_delete_use_count)

        self.lineEdit_use_count = QLineEdit(Form)
        self.lineEdit_use_count.setObjectName(u"lineEdit_use_count")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_use_count.sizePolicy().hasHeightForWidth())
        self.lineEdit_use_count.setSizePolicy(sizePolicy)
        self.lineEdit_use_count.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.lineEdit_use_count)

        self.label_11 = QLabel(Form)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout.addWidget(self.label_11)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.checkBox_delete_add_data = QCheckBox(Form)
        self.checkBox_delete_add_data.setObjectName(u"checkBox_delete_add_data")

        self.horizontalLayout_2.addWidget(self.checkBox_delete_add_data)

        self.lineEdit_add_data = QLineEdit(Form)
        self.lineEdit_add_data.setObjectName(u"lineEdit_add_data")
        self.lineEdit_add_data.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_2.addWidget(self.lineEdit_add_data)

        self.label_12 = QLabel(Form)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_2.addWidget(self.label_12)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkBox_delete_use_data = QCheckBox(Form)
        self.checkBox_delete_use_data.setObjectName(u"checkBox_delete_use_data")

        self.horizontalLayout_3.addWidget(self.checkBox_delete_use_data)

        self.lineEdit_use_data = QLineEdit(Form)
        self.lineEdit_use_data.setObjectName(u"lineEdit_use_data")
        self.lineEdit_use_data.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEdit_use_data)

        self.label_13 = QLabel(Form)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_3.addWidget(self.label_13)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_14 = QLabel(Form)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_4.addWidget(self.label_14)

        self.label_count_delete = QLabel(Form)
        self.label_count_delete.setObjectName(u"label_count_delete")

        self.horizontalLayout_4.addWidget(self.label_count_delete)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_6)

        self.pushButton_preview = QPushButton(Form)
        self.pushButton_preview.setObjectName(u"pushButton_preview")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_preview.sizePolicy().hasHeightForWidth())
        self.pushButton_preview.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.pushButton_preview)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.pushButton_delete = QPushButton(Form)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        sizePolicy1.setHeightForWidth(self.pushButton_delete.sizePolicy().hasHeightForWidth())
        self.pushButton_delete.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.pushButton_delete)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u5bc6\u7801\u4f7f\u7528\u60c5\u51b5", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4f7f\u7528100\u6b21\u4ee5\u4e0a\u7684\u5bc6\u7801\u6570\uff1a", None))
        self.label_pw_count_100.setText(QCoreApplication.translate("Form", u"count100", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u4f7f\u752810~100\u6b21\u4ee5\u4e0a\u7684\u5bc6\u7801\u6570\uff1a", None))
        self.label_pw_count_10.setText(QCoreApplication.translate("Form", u"count10", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u4f7f\u75281~10\u6b21\u4ee5\u4e0a\u7684\u5bc6\u7801\u6570\uff1a", None))
        self.label_pw_count_1.setText(QCoreApplication.translate("Form", u"count1", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u672a\u4f7f\u7528\u8fc7\u7684\u5bc6\u7801\u6570\uff1a", None))
        self.label_pw_count_0.setText(QCoreApplication.translate("Form", u"count0", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u5bc6\u7801", None))
        self.checkBox_delete_use_count.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u4f7f\u7528\u6b21\u6570\u4e3a", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u6b21\u53ca\u4ee5\u4e0b\u7684\u5bc6\u7801", None))
        self.checkBox_delete_add_data.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u6dfb\u52a0\u65f6\u95f4\u5728", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u65e5\u4e4b\u524d\u7684\u5bc6\u7801", None))
        self.checkBox_delete_use_data.setText(QCoreApplication.translate("Form", u"\u5220\u9664\u6700\u540e\u4e00\u6b21\u4f7f\u7528\u65f6\u95f4\u5728", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"\u65e5\u4e4b\u524d\u7684\u5bc6\u7801", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"\u7b26\u5408\u6761\u4ef6\u7684\u5bc6\u7801\u6570\uff1a", None))
        self.label_count_delete.setText(QCoreApplication.translate("Form", u"0", None))
        self.pushButton_preview.setText(QCoreApplication.translate("Form", u"\u663e\u793a\u9884\u89c8", None))
        self.pushButton_delete.setText(QCoreApplication.translate("Form", u"\u5220\u9664", None))
    # retranslateUi

