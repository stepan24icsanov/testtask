# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\stepa\PycharmProjects\testtask\ui\testtask.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.signal_button = QtWidgets.QPushButton(self.centralwidget)
        self.signal_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.signal_button.sizePolicy().hasHeightForWidth())
        self.signal_button.setSizePolicy(sizePolicy)
        self.signal_button.setMinimumSize(QtCore.QSize(10, 10))
        self.signal_button.setMaximumSize(QtCore.QSize(40, 40))
        self.signal_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("images/sinus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.signal_button.setIcon(icon)
        self.signal_button.setIconSize(QtCore.QSize(32, 32))
        self.signal_button.setObjectName("signal_button")
        self.verticalLayout.addWidget(self.signal_button)
        self.spectrum_button = QtWidgets.QPushButton(self.centralwidget)
        self.spectrum_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spectrum_button.sizePolicy().hasHeightForWidth())
        self.spectrum_button.setSizePolicy(sizePolicy)
        self.spectrum_button.setMinimumSize(QtCore.QSize(10, 10))
        self.spectrum_button.setMaximumSize(QtCore.QSize(40, 40))
        self.spectrum_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("images/spectrum.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.spectrum_button.setIcon(icon1)
        self.spectrum_button.setIconSize(QtCore.QSize(32, 32))
        self.spectrum_button.setObjectName("spectrum_button")
        self.verticalLayout.addWidget(self.spectrum_button)
        self.envelope_button = QtWidgets.QPushButton(self.centralwidget)
        self.envelope_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.envelope_button.sizePolicy().hasHeightForWidth())
        self.envelope_button.setSizePolicy(sizePolicy)
        self.envelope_button.setMinimumSize(QtCore.QSize(10, 10))
        self.envelope_button.setMaximumSize(QtCore.QSize(40, 40))
        self.envelope_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("images/envelope_w_trans.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.envelope_button.setIcon(icon2)
        self.envelope_button.setIconSize(QtCore.QSize(32, 32))
        self.envelope_button.setObjectName("envelope_button")
        self.verticalLayout.addWidget(self.envelope_button)
        self.envelope_spectrum_button = QtWidgets.QPushButton(self.centralwidget)
        self.envelope_spectrum_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.envelope_spectrum_button.sizePolicy().hasHeightForWidth())
        self.envelope_spectrum_button.setSizePolicy(sizePolicy)
        self.envelope_spectrum_button.setMinimumSize(QtCore.QSize(10, 10))
        self.envelope_spectrum_button.setMaximumSize(QtCore.QSize(40, 40))
        self.envelope_spectrum_button.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("images/env spectrum.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.envelope_spectrum_button.setIcon(icon3)
        self.envelope_spectrum_button.setIconSize(QtCore.QSize(32, 32))
        self.envelope_spectrum_button.setObjectName("envelope_spectrum_button")
        self.verticalLayout.addWidget(self.envelope_spectrum_button)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.graph_widget = PlotWidget(self.centralwidget)
        self.graph_widget.setMinimumSize(QtCore.QSize(650, 530))
        self.graph_widget.setObjectName("graph_widget")
        self.horizontalLayout.addWidget(self.graph_widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setObjectName("menu_file")
        self.menu_tools = QtWidgets.QMenu(self.menubar)
        self.menu_tools.setEnabled(False)
        self.menu_tools.setTearOffEnabled(False)
        self.menu_tools.setObjectName("menu_tools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.open_file = QtWidgets.QAction(MainWindow)
        self.open_file.setObjectName("open_file")
        self.signal = QtWidgets.QAction(MainWindow)
        self.signal.setEnabled(False)
        self.signal.setObjectName("signal")
        self.signal_spectrum = QtWidgets.QAction(MainWindow)
        self.signal_spectrum.setEnabled(False)
        self.signal_spectrum.setObjectName("signal_spectrum")
        self.signal_envelope = QtWidgets.QAction(MainWindow)
        self.signal_envelope.setEnabled(False)
        self.signal_envelope.setObjectName("signal_envelope")
        self.envelope_spectrum = QtWidgets.QAction(MainWindow)
        self.envelope_spectrum.setEnabled(False)
        self.envelope_spectrum.setObjectName("envelope_spectrum")
        self.menu_file.addAction(self.open_file)
        self.menu_tools.addAction(self.signal)
        self.menu_tools.addAction(self.signal_spectrum)
        self.menu_tools.addAction(self.signal_envelope)
        self.menu_tools.addAction(self.envelope_spectrum)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_tools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.signal_button.setToolTip(_translate("MainWindow", "Сигнал"))
        self.spectrum_button.setToolTip(_translate("MainWindow", "Спектр сигнала"))
        self.envelope_button.setToolTip(_translate("MainWindow", "Огибающая сигнала"))
        self.envelope_spectrum_button.setToolTip(_translate("MainWindow", "Спектр огибающей"))
        self.menu_file.setTitle(_translate("MainWindow", "Файл"))
        self.menu_tools.setTitle(_translate("MainWindow", "Инструменты"))
        self.open_file.setText(_translate("MainWindow", "Открыть"))
        self.signal.setText(_translate("MainWindow", "Сигнал"))
        self.signal_spectrum.setText(_translate("MainWindow", "Спектр"))
        self.signal_envelope.setText(_translate("MainWindow", "Огибающая"))
        self.envelope_spectrum.setText(_translate("MainWindow", "Спектр огибающей"))
from pyqtgraph import PlotWidget
