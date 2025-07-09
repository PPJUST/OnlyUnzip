# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindowwRGtbR.ui'
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
from PySide6.QtWidgets import (QApplication, QButtonGroup, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(320, 240)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_home = QPushButton(self.centralwidget)
        self.buttonGroup = QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.pushButton_home)
        self.pushButton_home.setObjectName(u"pushButton_home")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_home.sizePolicy().hasHeightForWidth())
        self.pushButton_home.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_home)

        self.pushButton_password = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.pushButton_password)
        self.pushButton_password.setObjectName(u"pushButton_password")
        sizePolicy.setHeightForWidth(self.pushButton_password.sizePolicy().hasHeightForWidth())
        self.pushButton_password.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_password)

        self.pushButton_setting = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.pushButton_setting)
        self.pushButton_setting.setObjectName(u"pushButton_setting")
        sizePolicy.setHeightForWidth(self.pushButton_setting.sizePolicy().hasHeightForWidth())
        self.pushButton_setting.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_setting)

        self.pushButton_history = QPushButton(self.centralwidget)
        self.buttonGroup.addButton(self.pushButton_history)
        self.pushButton_history.setObjectName(u"pushButton_history")
        sizePolicy.setHeightForWidth(self.pushButton_history.sizePolicy().hasHeightForWidth())
        self.pushButton_history.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.pushButton_history)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.verticalLayout_3 = QVBoxLayout(self.page_home)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_home)
        self.page_password = QWidget()
        self.page_password.setObjectName(u"page_password")
        self.verticalLayout_4 = QVBoxLayout(self.page_password)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_password)
        self.page_setting = QWidget()
        self.page_setting.setObjectName(u"page_setting")
        self.verticalLayout_5 = QVBoxLayout(self.page_setting)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_setting)
        self.page_history = QWidget()
        self.page_history.setObjectName(u"page_history")
        self.verticalLayout_2 = QVBoxLayout(self.page_history)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.page_history)

        self.horizontalLayout.addWidget(self.stackedWidget)

        self.horizontalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"OnlyUnzip", None))
        self.pushButton_home.setText(QCoreApplication.translate("MainWindow", u"\u4e3b\u9875", None))
        self.pushButton_password.setText(QCoreApplication.translate("MainWindow", u"\u5bc6\u7801\u672c", None))
        self.pushButton_setting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.pushButton_history.setText(QCoreApplication.translate("MainWindow", u"\u5386\u53f2\u8bb0\u5f55", None))
    # retranslateUi

