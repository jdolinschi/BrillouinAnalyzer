# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QStatusBar, QTabWidget, QTableView, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1097)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_calib = QWidget()
        self.tab_calib.setObjectName(u"tab_calib")
        self.tabWidget.addTab(self.tab_calib, "")
        self.tab_fit = QWidget()
        self.tab_fit.setObjectName(u"tab_fit")
        self.verticalLayout_3 = QVBoxLayout(self.tab_fit)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter_3 = QSplitter(self.tab_fit)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.splitter = QSplitter(self.splitter_3)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Plain)
        self.verticalLayout_15 = QVBoxLayout(self.frame)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.frame_topPlotToolbar = QFrame(self.frame)
        self.frame_topPlotToolbar.setObjectName(u"frame_topPlotToolbar")
        self.frame_topPlotToolbar.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_topPlotToolbar.sizePolicy().hasHeightForWidth())
        self.frame_topPlotToolbar.setSizePolicy(sizePolicy)
        self.frame_topPlotToolbar.setFrameShape(QFrame.NoFrame)
        self.frame_topPlotToolbar.setFrameShadow(QFrame.Plain)
        self.verticalLayout_8 = QVBoxLayout(self.frame_topPlotToolbar)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.pushButton_2 = QPushButton(self.frame_topPlotToolbar)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_6.addWidget(self.pushButton_2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)


        self.verticalLayout_9.addWidget(self.frame_topPlotToolbar)

        self.main_plotwidget = PlotWidget(self.frame)
        self.main_plotwidget.setObjectName(u"main_plotwidget")

        self.verticalLayout_9.addWidget(self.main_plotwidget)


        self.verticalLayout_15.addLayout(self.verticalLayout_9)

        self.splitter.addWidget(self.frame)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.layoutWidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Plain)
        self.verticalLayout_6 = QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame_leftPlotToolbar = QFrame(self.frame_2)
        self.frame_leftPlotToolbar.setObjectName(u"frame_leftPlotToolbar")
        self.frame_leftPlotToolbar.setFrameShape(QFrame.NoFrame)
        self.frame_leftPlotToolbar.setFrameShadow(QFrame.Plain)
        self.verticalLayout_17 = QVBoxLayout(self.frame_leftPlotToolbar)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_4 = QPushButton(self.frame_leftPlotToolbar)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_7.addWidget(self.pushButton_4)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayout_17.addLayout(self.horizontalLayout_7)


        self.verticalLayout_4.addWidget(self.frame_leftPlotToolbar)

        self.left_plotwidget = PlotWidget(self.frame_2)
        self.left_plotwidget.setObjectName(u"left_plotwidget")

        self.verticalLayout_4.addWidget(self.left_plotwidget)


        self.verticalLayout_6.addLayout(self.verticalLayout_4)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.layoutWidget)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Plain)
        self.verticalLayout_7 = QVBoxLayout(self.frame_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_rightPlotToolbar = QFrame(self.frame_3)
        self.frame_rightPlotToolbar.setObjectName(u"frame_rightPlotToolbar")
        self.frame_rightPlotToolbar.setFrameShape(QFrame.NoFrame)
        self.frame_rightPlotToolbar.setFrameShadow(QFrame.Plain)
        self.verticalLayout_16 = QVBoxLayout(self.frame_rightPlotToolbar)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.pushButton_3 = QPushButton(self.frame_rightPlotToolbar)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_8.addWidget(self.pushButton_3)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)


        self.verticalLayout_16.addLayout(self.horizontalLayout_8)


        self.verticalLayout_5.addWidget(self.frame_rightPlotToolbar)

        self.right_plotwidget = PlotWidget(self.frame_3)
        self.right_plotwidget.setObjectName(u"right_plotwidget")

        self.verticalLayout_5.addWidget(self.right_plotwidget)


        self.verticalLayout_7.addLayout(self.verticalLayout_5)


        self.horizontalLayout_2.addWidget(self.frame_3)

        self.splitter.addWidget(self.layoutWidget)
        self.splitter_3.addWidget(self.splitter)
        self.frame_4 = QFrame(self.splitter_3)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Plain)
        self.verticalLayout = QVBoxLayout(self.frame_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget_sideBar = QTabWidget(self.frame_4)
        self.tabWidget_sideBar.setObjectName(u"tabWidget_sideBar")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter_2 = QSplitter(self.tab)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.frame_filesBrowser = QFrame(self.splitter_2)
        self.frame_filesBrowser.setObjectName(u"frame_filesBrowser")
        self.frame_filesBrowser.setFrameShape(QFrame.NoFrame)
        self.frame_filesBrowser.setFrameShadow(QFrame.Plain)
        self.verticalLayout_23 = QVBoxLayout(self.frame_filesBrowser)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.frame_filesBrowserToolbar = QFrame(self.frame_filesBrowser)
        self.frame_filesBrowserToolbar.setObjectName(u"frame_filesBrowserToolbar")
        self.frame_filesBrowserToolbar.setMinimumSize(QSize(0, 30))
        self.frame_filesBrowserToolbar.setFrameShape(QFrame.NoFrame)
        self.frame_filesBrowserToolbar.setFrameShadow(QFrame.Plain)
        self.verticalLayout_11 = QVBoxLayout(self.frame_filesBrowserToolbar)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetMaximumSize)
        self.label_2 = QLabel(self.frame_filesBrowserToolbar)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.comboBox_pressure = QComboBox(self.frame_filesBrowserToolbar)
        self.comboBox_pressure.setObjectName(u"comboBox_pressure")

        self.horizontalLayout_5.addWidget(self.comboBox_pressure)

        self.label_3 = QLabel(self.frame_filesBrowserToolbar)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.comboBox_crystal = QComboBox(self.frame_filesBrowserToolbar)
        self.comboBox_crystal.setObjectName(u"comboBox_crystal")

        self.horizontalLayout_5.addWidget(self.comboBox_crystal)


        self.verticalLayout_10.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setSizeConstraint(QLayout.SetMaximumSize)
        self.pushButton_addFiles = QPushButton(self.frame_filesBrowserToolbar)
        self.pushButton_addFiles.setObjectName(u"pushButton_addFiles")

        self.horizontalLayout_9.addWidget(self.pushButton_addFiles)

        self.pushButton_removeFiles = QPushButton(self.frame_filesBrowserToolbar)
        self.pushButton_removeFiles.setObjectName(u"pushButton_removeFiles")

        self.horizontalLayout_9.addWidget(self.pushButton_removeFiles)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)


        self.verticalLayout_10.addLayout(self.horizontalLayout_9)


        self.verticalLayout_11.addLayout(self.verticalLayout_10)


        self.verticalLayout_14.addWidget(self.frame_filesBrowserToolbar)

        self.tableView_files = QTableView(self.frame_filesBrowser)
        self.tableView_files.setObjectName(u"tableView_files")
        self.tableView_files.setSortingEnabled(True)

        self.verticalLayout_14.addWidget(self.tableView_files)


        self.verticalLayout_23.addLayout(self.verticalLayout_14)

        self.splitter_2.addWidget(self.frame_filesBrowser)
        self.frame_7 = QFrame(self.splitter_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Plain)
        self.verticalLayout_13 = QVBoxLayout(self.frame_7)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.frame_peakToolbar = QFrame(self.frame_7)
        self.frame_peakToolbar.setObjectName(u"frame_peakToolbar")
        self.frame_peakToolbar.setMinimumSize(QSize(0, 30))
        self.frame_peakToolbar.setFrameShape(QFrame.NoFrame)
        self.frame_peakToolbar.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_peakToolbar)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton = QPushButton(self.frame_peakToolbar)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_3.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_12.addWidget(self.frame_peakToolbar)

        self.tableView_peakFits = QTableView(self.frame_7)
        self.tableView_peakFits.setObjectName(u"tableView_peakFits")
        self.tableView_peakFits.setSortingEnabled(True)

        self.verticalLayout_12.addWidget(self.tableView_peakFits)


        self.verticalLayout_13.addLayout(self.verticalLayout_12)

        self.splitter_2.addWidget(self.frame_7)

        self.verticalLayout_2.addWidget(self.splitter_2)

        self.tabWidget_sideBar.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_21 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.verticalLayout_22 = QVBoxLayout()
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.groupBox_project = QGroupBox(self.tab_2)
        self.groupBox_project.setObjectName(u"groupBox_project")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_project.sizePolicy().hasHeightForWidth())
        self.groupBox_project.setSizePolicy(sizePolicy2)
        self.groupBox_project.setFlat(True)
        self.groupBox_project.setCheckable(False)
        self.verticalLayout_27 = QVBoxLayout(self.groupBox_project)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.frame_8 = QFrame(self.groupBox_project)
        self.frame_8.setObjectName(u"frame_8")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy3)
        self.frame_8.setFrameShape(QFrame.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Plain)
        self.verticalLayout_18 = QVBoxLayout(self.frame_8)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.pushButton_newProject = QPushButton(self.frame_8)
        self.pushButton_newProject.setObjectName(u"pushButton_newProject")

        self.horizontalLayout_10.addWidget(self.pushButton_newProject)

        self.pushButton_loadProject = QPushButton(self.frame_8)
        self.pushButton_loadProject.setObjectName(u"pushButton_loadProject")

        self.horizontalLayout_10.addWidget(self.pushButton_loadProject)

        self.pushButton_saveProject = QPushButton(self.frame_8)
        self.pushButton_saveProject.setObjectName(u"pushButton_saveProject")

        self.horizontalLayout_10.addWidget(self.pushButton_saveProject)

        self.pushButton_saveProjectAs = QPushButton(self.frame_8)
        self.pushButton_saveProjectAs.setObjectName(u"pushButton_saveProjectAs")

        self.horizontalLayout_10.addWidget(self.pushButton_saveProjectAs)

        self.pushButton_deleteProject = QPushButton(self.frame_8)
        self.pushButton_deleteProject.setObjectName(u"pushButton_deleteProject")

        self.horizontalLayout_10.addWidget(self.pushButton_deleteProject)


        self.verticalLayout_18.addLayout(self.horizontalLayout_10)


        self.verticalLayout_26.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.groupBox_project)
        self.frame_9.setObjectName(u"frame_9")
        sizePolicy3.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy3)
        self.frame_9.setFrameShape(QFrame.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Plain)
        self.verticalLayout_24 = QVBoxLayout(self.frame_9)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.pushButton_renameProject = QPushButton(self.frame_9)
        self.pushButton_renameProject.setObjectName(u"pushButton_renameProject")

        self.horizontalLayout_11.addWidget(self.pushButton_renameProject)

        self.lineEdit_currentProject = QLineEdit(self.frame_9)
        self.lineEdit_currentProject.setObjectName(u"lineEdit_currentProject")

        self.horizontalLayout_11.addWidget(self.lineEdit_currentProject)


        self.verticalLayout_24.addLayout(self.horizontalLayout_11)


        self.verticalLayout_26.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.groupBox_project)
        self.frame_10.setObjectName(u"frame_10")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy4)
        self.frame_10.setFrameShape(QFrame.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Plain)
        self.verticalLayout_25 = QVBoxLayout(self.frame_10)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_projectPath = QLabel(self.frame_10)
        self.label_projectPath.setObjectName(u"label_projectPath")
        sizePolicy3.setHeightForWidth(self.label_projectPath.sizePolicy().hasHeightForWidth())
        self.label_projectPath.setSizePolicy(sizePolicy3)
        font = QFont()
        font.setPointSize(12)
        self.label_projectPath.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_projectPath)

        self.label_modDate = QLabel(self.frame_10)
        self.label_modDate.setObjectName(u"label_modDate")
        sizePolicy3.setHeightForWidth(self.label_modDate.sizePolicy().hasHeightForWidth())
        self.label_modDate.setSizePolicy(sizePolicy3)
        self.label_modDate.setFont(font)

        self.horizontalLayout_12.addWidget(self.label_modDate)


        self.verticalLayout_25.addLayout(self.horizontalLayout_12)


        self.verticalLayout_26.addWidget(self.frame_10)


        self.verticalLayout_27.addLayout(self.verticalLayout_26)


        self.verticalLayout_22.addWidget(self.groupBox_project)

        self.groupBox_conditions = QGroupBox(self.tab_2)
        self.groupBox_conditions.setObjectName(u"groupBox_conditions")
        self.groupBox_conditions.setFlat(True)
        self.horizontalLayout_20 = QHBoxLayout(self.groupBox_conditions)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.splitter_4 = QSplitter(self.groupBox_conditions)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Horizontal)
        self.frame_5 = QFrame(self.splitter_4)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Plain)
        self.verticalLayout_21 = QVBoxLayout(self.frame_5)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.label_6 = QLabel(self.frame_5)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_19.addWidget(self.label_6)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.pushButton_newPressure = QPushButton(self.frame_5)
        self.pushButton_newPressure.setObjectName(u"pushButton_newPressure")

        self.horizontalLayout_17.addWidget(self.pushButton_newPressure)

        self.pushButton_deletePressure = QPushButton(self.frame_5)
        self.pushButton_deletePressure.setObjectName(u"pushButton_deletePressure")

        self.horizontalLayout_17.addWidget(self.pushButton_deletePressure)


        self.verticalLayout_19.addLayout(self.horizontalLayout_17)

        self.tableWidget_pressures = QTableWidget(self.frame_5)
        self.tableWidget_pressures.setObjectName(u"tableWidget_pressures")

        self.verticalLayout_19.addWidget(self.tableWidget_pressures)


        self.verticalLayout_21.addLayout(self.verticalLayout_19)

        self.splitter_4.addWidget(self.frame_5)
        self.frame_6 = QFrame(self.splitter_4)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.label_7 = QLabel(self.frame_6)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_20.addWidget(self.label_7)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.pushButton_newCrystal = QPushButton(self.frame_6)
        self.pushButton_newCrystal.setObjectName(u"pushButton_newCrystal")

        self.horizontalLayout_18.addWidget(self.pushButton_newCrystal)

        self.pushButton_deleteCrystal = QPushButton(self.frame_6)
        self.pushButton_deleteCrystal.setObjectName(u"pushButton_deleteCrystal")

        self.horizontalLayout_18.addWidget(self.pushButton_deleteCrystal)


        self.verticalLayout_20.addLayout(self.horizontalLayout_18)

        self.tableWidget_crystals = QTableWidget(self.frame_6)
        self.tableWidget_crystals.setObjectName(u"tableWidget_crystals")

        self.verticalLayout_20.addWidget(self.tableWidget_crystals)


        self.horizontalLayout_19.addLayout(self.verticalLayout_20)

        self.splitter_4.addWidget(self.frame_6)

        self.horizontalLayout_20.addWidget(self.splitter_4)


        self.verticalLayout_22.addWidget(self.groupBox_conditions)

        self.groupBox_settings = QGroupBox(self.tab_2)
        self.groupBox_settings.setObjectName(u"groupBox_settings")

        self.verticalLayout_22.addWidget(self.groupBox_settings)

        self.verticalLayout_22.setStretch(1, 1)

        self.horizontalLayout_21.addLayout(self.verticalLayout_22)

        self.tabWidget_sideBar.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget_sideBar)

        self.splitter_3.addWidget(self.frame_4)

        self.verticalLayout_3.addWidget(self.splitter_3)

        self.tabWidget.addTab(self.tab_fit, "")

        self.horizontalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_sideBar.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_calib), QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Pressure (GPa): ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Crystal: ", None))
        self.pushButton_addFiles.setText(QCoreApplication.translate("MainWindow", u"Add files", None))
        self.pushButton_removeFiles.setText(QCoreApplication.translate("MainWindow", u"Remove files", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidget_sideBar.setTabText(self.tabWidget_sideBar.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Main", None))
        self.groupBox_project.setTitle(QCoreApplication.translate("MainWindow", u"Project", None))
        self.pushButton_newProject.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.pushButton_loadProject.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.pushButton_saveProject.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pushButton_saveProjectAs.setText(QCoreApplication.translate("MainWindow", u"Save as...", None))
        self.pushButton_deleteProject.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.pushButton_renameProject.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.label_projectPath.setText("")
        self.label_modDate.setText("")
        self.groupBox_conditions.setTitle(QCoreApplication.translate("MainWindow", u"Conditions", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Pressures (GPa)", None))
        self.pushButton_newPressure.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.pushButton_deletePressure.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Crystals", None))
        self.pushButton_newCrystal.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.pushButton_deleteCrystal.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.groupBox_settings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.tabWidget_sideBar.setTabText(self.tabWidget_sideBar.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Setup", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_fit), QCoreApplication.translate("MainWindow", u"Fit", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

