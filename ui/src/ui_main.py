# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainsqxZjG.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(272, 238)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_page_homepage = QPushButton(self.centralwidget)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.pushButton_page_homepage)
        self.pushButton_page_homepage.setObjectName(u"pushButton_page_homepage")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_page_homepage.sizePolicy().hasHeightForWidth())
        self.pushButton_page_homepage.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_page_homepage)

        self.pushButton_page_password = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.pushButton_page_password)
        self.pushButton_page_password.setObjectName(u"pushButton_page_password")
        sizePolicy.setHeightForWidth(self.pushButton_page_password.sizePolicy().hasHeightForWidth())
        self.pushButton_page_password.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_page_password)

        self.pushButton_page_setting = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.pushButton_page_setting)
        self.pushButton_page_setting.setObjectName(u"pushButton_page_setting")
        sizePolicy.setHeightForWidth(self.pushButton_page_setting.sizePolicy().hasHeightForWidth())
        self.pushButton_page_setting.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_page_setting)

        self.pushButton_page_history = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.pushButton_page_history)
        self.pushButton_page_history.setObjectName(u"pushButton_page_history")
        sizePolicy.setHeightForWidth(self.pushButton_page_history.sizePolicy().hasHeightForWidth())
        self.pushButton_page_history.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_page_history)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_homepage = QWidget()
        self.page_homepage.setObjectName(u"page_homepage")
        self.verticalLayout_2 = QVBoxLayout(self.page_homepage)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_homepage)
        self.page_password = QWidget()
        self.page_password.setObjectName(u"page_password")
        self.verticalLayout_3 = QVBoxLayout(self.page_password)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_password)
        self.page_setting = QWidget()
        self.page_setting.setObjectName(u"page_setting")
        self.verticalLayout_4 = QVBoxLayout(self.page_setting)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_setting)
        self.page_history = QWidget()
        self.page_history.setObjectName(u"page_history")
        self.verticalLayout_5 = QVBoxLayout(self.page_history)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_history)

        self.horizontalLayout.addWidget(self.stackedWidget)

        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OnlyUnzip", None))
        self.pushButton_page_homepage.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9875", None))
        self.pushButton_page_password.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801\u9875", None))
        self.pushButton_page_setting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u9875", None))
        self.pushButton_page_history.setText(QCoreApplication.translate("MainWindow", u"\u5386\u53f2\u9875", None))
    # retranslateUi

