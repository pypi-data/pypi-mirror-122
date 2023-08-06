# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
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
        MainWindow.resize(900, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"font-family:Candara;\n"
"color:#627176;")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setFamilies([u"Candara"])
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.tabWidget.setFont(font)
        self.tabWidget.setStyleSheet(u"\n"
"\n"
"QTabWidget>QWidget {\n"
"color: #49687A;\n"
"}")
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(True)
        self.tab_facebook = QWidget()
        self.tab_facebook.setObjectName(u"tab_facebook")
        self.tab_facebook.setStyleSheet(u"background-color:#F0F1F1;\n"
"")
        self.verticalLayout_7 = QVBoxLayout(self.tab_facebook)
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.tab_facebook)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.widget)
        self.header_frame.setObjectName(u"header_frame")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header_frame.sizePolicy().hasHeightForWidth())
        self.header_frame.setSizePolicy(sizePolicy)
        self.header_frame.setStyleSheet(u"QPushButton {\n"
"	box-shadow:inset 0px 1px 0px 0px #ffffff;\n"
"	background:linear-gradient(to bottom, #f9f9f9 5%, #e9e9e9 100%);\n"
"	background-color:#f9f9f9;\n"
"	border-radius:8px;\n"
"	border:1px solid #dcdcdc;\n"
"	display:inline-block;\n"
"	cursor:pointer;\n"
"	color:#627176;\n"
"	font-family:Candara;\n"
"	font-size:12px;\n"
"	font-weight:600;\n"
"	padding:6px 20px;\n"
"	text-decoration:none;\n"
"	text-shadow:0px 1px 0px #ffffff;\n"
"	border-bottom:1px solid #86C8E0;\n"
"}\n"
"QPushButton::hover {\n"
"	background:linear-gradient(to bottom, #DFE7EA 5%, #8DB3C3 100%);\n"
"	background-color:#F0F1F1;\n"
"	border-radius:8px;\n"
"	border:1px solid #86C8E0;\n"
"	border-bottom:2px solid #86C8E0;\n"
"\n"
"}\n"
"QPushButton::pressed {\n"
"	background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f6f7fa, stop: 1 #86C8E0);\n"
"    \n"
"}\n"
"")
        self.header_frame.setFrameShape(QFrame.NoFrame)
        self.header_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.header_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.device_frame = QFrame(self.header_frame)
        self.device_frame.setObjectName(u"device_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(5)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.device_frame.sizePolicy().hasHeightForWidth())
        self.device_frame.setSizePolicy(sizePolicy1)
        self.device_frame.setFrameShape(QFrame.NoFrame)
        self.device_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.device_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 3)
        self.device_table = QTableWidget(self.device_frame)
        self.device_table.setObjectName(u"device_table")
        self.device_table.viewport().setProperty("cursor", QCursor(Qt.PointingHandCursor))
        self.device_table.setStyleSheet(u"background-color:#E6E8E8;\n"
"border-bottom-right-radius:12px;\n"
"border:1px solid #FFFFFF;")
        self.device_table.setFrameShape(QFrame.NoFrame)
        self.device_table.setLineWidth(0)

        self.verticalLayout_5.addWidget(self.device_table)


        self.horizontalLayout.addWidget(self.device_frame)

        self.btn_frame = QFrame(self.header_frame)
        self.btn_frame.setObjectName(u"btn_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_frame.sizePolicy().hasHeightForWidth())
        self.btn_frame.setSizePolicy(sizePolicy2)
        self.btn_frame.setStyleSheet(u"")
        self.btn_frame.setFrameShape(QFrame.NoFrame)
        self.btn_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.btn_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 8, 5, 5)
        self.btn_stop = QPushButton(self.btn_frame)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_stop.setToolTipDuration(7)
        self.btn_stop.setAutoFillBackground(False)
        self.btn_stop.setStyleSheet(u"")
        self.btn_stop.setCheckable(False)
        self.btn_stop.setChecked(False)
        self.btn_stop.setFlat(False)

        self.verticalLayout_2.addWidget(self.btn_stop)

        self.btn_start = QPushButton(self.btn_frame)
        self.btn_start.setObjectName(u"btn_start")
        self.btn_start.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.btn_start)

        self.btn_restart = QPushButton(self.btn_frame)
        self.btn_restart.setObjectName(u"btn_restart")
        self.btn_restart.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.btn_restart)

        self.btn_disable = QPushButton(self.btn_frame)
        self.btn_disable.setObjectName(u"btn_disable")
        self.btn_disable.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.btn_disable)

        self.btn_reboot = QPushButton(self.btn_frame)
        self.btn_reboot.setObjectName(u"btn_reboot")
        font1 = QFont()
        font1.setFamilies([u"Candara"])
        font1.setBold(True)
        font1.setUnderline(False)
        font1.setStrikeOut(False)
        self.btn_reboot.setFont(font1)
        self.btn_reboot.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.btn_reboot)

        self.btn_cast = QPushButton(self.btn_frame)
        self.btn_cast.setObjectName(u"btn_cast")
        self.btn_cast.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_cast.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.btn_cast)

        self.btn_dump = QPushButton(self.btn_frame)
        self.btn_dump.setObjectName(u"btn_dump")
        self.btn_dump.setCursor(QCursor(Qt.PointingHandCursor))

        self.verticalLayout_2.addWidget(self.btn_dump)


        self.horizontalLayout.addWidget(self.btn_frame)

        self.stat_frame = QFrame(self.header_frame)
        self.stat_frame.setObjectName(u"stat_frame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.stat_frame.sizePolicy().hasHeightForWidth())
        self.stat_frame.setSizePolicy(sizePolicy3)
        self.stat_frame.setFrameShape(QFrame.NoFrame)
        self.stat_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.stat_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 4)
        self.stat_list = QListView(self.stat_frame)
        self.stat_list.setObjectName(u"stat_list")
        self.stat_list.setStyleSheet(u"background-color:#E6E8E8;\n"
"border-bottom-left-radius:12px;\n"
"border:1px solid #FFFFFF;\n"
"")
        self.stat_list.setFrameShape(QFrame.NoFrame)
        self.stat_list.setAutoScrollMargin(16)
        self.stat_list.setResizeMode(QListView.Adjust)

        self.verticalLayout_3.addWidget(self.stat_list)


        self.horizontalLayout.addWidget(self.stat_frame)


        self.verticalLayout_6.addWidget(self.header_frame)

        self.log_frame = QFrame(self.widget)
        self.log_frame.setObjectName(u"log_frame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.log_frame.sizePolicy().hasHeightForWidth())
        self.log_frame.setSizePolicy(sizePolicy4)
        self.log_frame.setFrameShape(QFrame.NoFrame)
        self.log_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.log_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 1, 0, 0)
        self.log_text = QTextBrowser(self.log_frame)
        self.log_text.setObjectName(u"log_text")
        self.log_text.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.log_text.setStyleSheet(u"background-color:#E6E8E8;\n"
"border:1px solid #FFFFFF;")
        self.log_text.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_4.addWidget(self.log_text)


        self.verticalLayout_6.addWidget(self.log_frame)


        self.verticalLayout_7.addWidget(self.widget)

        self.tabWidget.addTab(self.tab_facebook, "")
        self.tab_snapchat = QWidget()
        self.tab_snapchat.setObjectName(u"tab_snapchat")
        self.tabWidget.addTab(self.tab_snapchat, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(tooltip)
        self.btn_stop.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.btn_start.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.btn_restart.setText(QCoreApplication.translate("MainWindow", u"RESTART", None))
        self.btn_disable.setText(QCoreApplication.translate("MainWindow", u"DISABLE", None))
#if QT_CONFIG(tooltip)
        self.btn_reboot.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_reboot.setText(QCoreApplication.translate("MainWindow", u"REBOOT", None))
        self.btn_cast.setText(QCoreApplication.translate("MainWindow", u"CAST", None))
        self.btn_dump.setText(QCoreApplication.translate("MainWindow", u"DUMP", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_facebook), QCoreApplication.translate("MainWindow", u"Facebook", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_snapchat), QCoreApplication.translate("MainWindow", u"Snapchat", None))
    # retranslateUi

