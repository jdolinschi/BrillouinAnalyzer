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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTabWidget, QTableView, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_29 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_28 = QVBoxLayout()
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.tabWidget_project = QTabWidget(self.centralwidget)
        self.tabWidget_project.setObjectName(u"tabWidget_project")
        self.Project = QWidget()
        self.Project.setObjectName(u"Project")
        self.verticalLayout_37 = QVBoxLayout(self.Project)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.splitter_7 = QSplitter(self.Project)
        self.splitter_7.setObjectName(u"splitter_7")
        self.splitter_7.setOrientation(Qt.Horizontal)
        self.groupBox = QGroupBox(self.splitter_7)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_35 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.verticalLayout_42 = QVBoxLayout()
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.verticalLayout_41 = QVBoxLayout()
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.pushButton_newProject = QPushButton(self.groupBox)
        self.pushButton_newProject.setObjectName(u"pushButton_newProject")

        self.horizontalLayout_27.addWidget(self.pushButton_newProject)

        self.pushButton_loadProject = QPushButton(self.groupBox)
        self.pushButton_loadProject.setObjectName(u"pushButton_loadProject")

        self.horizontalLayout_27.addWidget(self.pushButton_loadProject)

        self.pushButton_saveProject = QPushButton(self.groupBox)
        self.pushButton_saveProject.setObjectName(u"pushButton_saveProject")

        self.horizontalLayout_27.addWidget(self.pushButton_saveProject)

        self.pushButton_saveProjectAs = QPushButton(self.groupBox)
        self.pushButton_saveProjectAs.setObjectName(u"pushButton_saveProjectAs")

        self.horizontalLayout_27.addWidget(self.pushButton_saveProjectAs)

        self.pushButton_deleteProject = QPushButton(self.groupBox)
        self.pushButton_deleteProject.setObjectName(u"pushButton_deleteProject")

        self.horizontalLayout_27.addWidget(self.pushButton_deleteProject)


        self.verticalLayout_41.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_28.addWidget(self.label_5)

        self.lineEdit_currentProject = QLineEdit(self.groupBox)
        self.lineEdit_currentProject.setObjectName(u"lineEdit_currentProject")

        self.horizontalLayout_28.addWidget(self.lineEdit_currentProject)

        self.pushButton_renameProject = QPushButton(self.groupBox)
        self.pushButton_renameProject.setObjectName(u"pushButton_renameProject")

        self.horizontalLayout_28.addWidget(self.pushButton_renameProject)


        self.verticalLayout_41.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.label_projectPath = QLabel(self.groupBox)
        self.label_projectPath.setObjectName(u"label_projectPath")

        self.horizontalLayout_29.addWidget(self.label_projectPath)

        self.label_modDate = QLabel(self.groupBox)
        self.label_modDate.setObjectName(u"label_modDate")

        self.horizontalLayout_29.addWidget(self.label_modDate)


        self.verticalLayout_41.addLayout(self.horizontalLayout_29)


        self.verticalLayout_42.addLayout(self.verticalLayout_41)

        self.groupBox_3 = QGroupBox(self.groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_40 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.verticalLayout_38 = QVBoxLayout()
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_10)

        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_30.addWidget(self.label_10)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_11)


        self.verticalLayout_38.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.pushButton_newPressure = QPushButton(self.groupBox_3)
        self.pushButton_newPressure.setObjectName(u"pushButton_newPressure")

        self.horizontalLayout_31.addWidget(self.pushButton_newPressure)

        self.pushButton_deletePressure = QPushButton(self.groupBox_3)
        self.pushButton_deletePressure.setObjectName(u"pushButton_deletePressure")

        self.horizontalLayout_31.addWidget(self.pushButton_deletePressure)

        self.pushButton_renamePressure = QPushButton(self.groupBox_3)
        self.pushButton_renamePressure.setObjectName(u"pushButton_renamePressure")

        self.horizontalLayout_31.addWidget(self.pushButton_renamePressure)


        self.verticalLayout_38.addLayout(self.horizontalLayout_31)

        self.tableWidget_pressures = QTableWidget(self.groupBox_3)
        self.tableWidget_pressures.setObjectName(u"tableWidget_pressures")

        self.verticalLayout_38.addWidget(self.tableWidget_pressures)


        self.horizontalLayout_34.addLayout(self.verticalLayout_38)

        self.verticalLayout_39 = QVBoxLayout()
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_12)

        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_32.addWidget(self.label_11)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_13)


        self.verticalLayout_39.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.pushButton_newCrystal = QPushButton(self.groupBox_3)
        self.pushButton_newCrystal.setObjectName(u"pushButton_newCrystal")

        self.horizontalLayout_33.addWidget(self.pushButton_newCrystal)

        self.pushButton_deleteCrystal = QPushButton(self.groupBox_3)
        self.pushButton_deleteCrystal.setObjectName(u"pushButton_deleteCrystal")

        self.horizontalLayout_33.addWidget(self.pushButton_deleteCrystal)

        self.pushButton_renameCrystal = QPushButton(self.groupBox_3)
        self.pushButton_renameCrystal.setObjectName(u"pushButton_renameCrystal")

        self.horizontalLayout_33.addWidget(self.pushButton_renameCrystal)


        self.verticalLayout_39.addLayout(self.horizontalLayout_33)

        self.tableWidget_crystals = QTableWidget(self.groupBox_3)
        self.tableWidget_crystals.setObjectName(u"tableWidget_crystals")

        self.verticalLayout_39.addWidget(self.tableWidget_crystals)


        self.horizontalLayout_34.addLayout(self.verticalLayout_39)


        self.verticalLayout_40.addLayout(self.horizontalLayout_34)


        self.verticalLayout_42.addWidget(self.groupBox_3)


        self.horizontalLayout_35.addLayout(self.verticalLayout_42)

        self.splitter_7.addWidget(self.groupBox)
        self.groupBox_2 = QGroupBox(self.splitter_7)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.splitter_7.addWidget(self.groupBox_2)

        self.verticalLayout_37.addWidget(self.splitter_7)

        self.tabWidget_project.addTab(self.Project, "")
        self.tab_calib = QWidget()
        self.tab_calib.setObjectName(u"tab_calib")
        self.verticalLayout_30 = QVBoxLayout(self.tab_calib)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.splitter_5 = QSplitter(self.tab_calib)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setOrientation(Qt.Horizontal)
        self.frame_12 = QFrame(self.splitter_5)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Plain)
        self.verticalLayout_31 = QVBoxLayout(self.frame_12)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.frame_14 = QFrame(self.frame_12)
        self.frame_14.setObjectName(u"frame_14")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_14.sizePolicy().hasHeightForWidth())
        self.frame_14.setSizePolicy(sizePolicy)
        self.frame_14.setFrameShape(QFrame.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.pushButton_calibResetView = QPushButton(self.frame_14)
        self.pushButton_calibResetView.setObjectName(u"pushButton_calibResetView")

        self.horizontalLayout_14.addWidget(self.pushButton_calibResetView)

        self.pushButton_calibZoom = QPushButton(self.frame_14)
        self.pushButton_calibZoom.setObjectName(u"pushButton_calibZoom")
        self.pushButton_calibZoom.setCheckable(True)

        self.horizontalLayout_14.addWidget(self.pushButton_calibZoom)

        self.pushButton_calibPan = QPushButton(self.frame_14)
        self.pushButton_calibPan.setObjectName(u"pushButton_calibPan")
        self.pushButton_calibPan.setCheckable(True)

        self.horizontalLayout_14.addWidget(self.pushButton_calibPan)

        self.horizontalSpacer_7 = QSpacerItem(654, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_7)


        self.verticalLayout_31.addWidget(self.frame_14)

        self.calib_plotWidget = PlotWidget(self.frame_12)
        self.calib_plotWidget.setObjectName(u"calib_plotWidget")

        self.verticalLayout_31.addWidget(self.calib_plotWidget)

        self.frame_15 = QFrame(self.frame_12)
        self.frame_15.setObjectName(u"frame_15")
        sizePolicy.setHeightForWidth(self.frame_15.sizePolicy().hasHeightForWidth())
        self.frame_15.setSizePolicy(sizePolicy)
        self.frame_15.setFrameShape(QFrame.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalSpacer_8 = QSpacerItem(622, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_8)

        self.label_calibText1 = QLabel(self.frame_15)
        self.label_calibText1.setObjectName(u"label_calibText1")

        self.horizontalLayout_15.addWidget(self.label_calibText1)

        self.label_calibText2 = QLabel(self.frame_15)
        self.label_calibText2.setObjectName(u"label_calibText2")

        self.horizontalLayout_15.addWidget(self.label_calibText2)

        self.label_calibText3 = QLabel(self.frame_15)
        self.label_calibText3.setObjectName(u"label_calibText3")

        self.horizontalLayout_15.addWidget(self.label_calibText3)

        self.label_calibText4 = QLabel(self.frame_15)
        self.label_calibText4.setObjectName(u"label_calibText4")

        self.horizontalLayout_15.addWidget(self.label_calibText4)

        self.label_calibText5 = QLabel(self.frame_15)
        self.label_calibText5.setObjectName(u"label_calibText5")

        self.horizontalLayout_15.addWidget(self.label_calibText5)


        self.verticalLayout_31.addWidget(self.frame_15)

        self.splitter_5.addWidget(self.frame_12)
        self.frame_13 = QFrame(self.splitter_5)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Plain)
        self.verticalLayout_32 = QVBoxLayout(self.frame_13)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.tabWidget_calib = QTabWidget(self.frame_13)
        self.tabWidget_calib.setObjectName(u"tabWidget_calib")
        self.tab_calibMain = QWidget()
        self.tab_calibMain.setObjectName(u"tab_calibMain")
        self.verticalLayout_35 = QVBoxLayout(self.tab_calibMain)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.frame_16 = QFrame(self.tab_calibMain)
        self.frame_16.setObjectName(u"frame_16")
        sizePolicy.setHeightForWidth(self.frame_16.sizePolicy().hasHeightForWidth())
        self.frame_16.setSizePolicy(sizePolicy)
        self.frame_16.setFrameShape(QFrame.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.pushButton_calibNewCalib = QPushButton(self.frame_16)
        self.pushButton_calibNewCalib.setObjectName(u"pushButton_calibNewCalib")

        self.horizontalLayout_16.addWidget(self.pushButton_calibNewCalib)

        self.pushButton_calibRenameCalib = QPushButton(self.frame_16)
        self.pushButton_calibRenameCalib.setObjectName(u"pushButton_calibRenameCalib")

        self.horizontalLayout_16.addWidget(self.pushButton_calibRenameCalib)

        self.pushButton_calibRemoveCalib = QPushButton(self.frame_16)
        self.pushButton_calibRemoveCalib.setObjectName(u"pushButton_calibRemoveCalib")

        self.horizontalLayout_16.addWidget(self.pushButton_calibRemoveCalib)


        self.verticalLayout_35.addWidget(self.frame_16)

        self.comboBox_calibSelect = QComboBox(self.tab_calibMain)
        self.comboBox_calibSelect.setObjectName(u"comboBox_calibSelect")

        self.verticalLayout_35.addWidget(self.comboBox_calibSelect)

        self.frame_17 = QFrame(self.tab_calibMain)
        self.frame_17.setObjectName(u"frame_17")
        sizePolicy.setHeightForWidth(self.frame_17.sizePolicy().hasHeightForWidth())
        self.frame_17.setSizePolicy(sizePolicy)
        self.frame_17.setFrameShape(QFrame.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Plain)
        self.gridLayout = QGridLayout(self.frame_17)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit_calibLaserWavelength = QLineEdit(self.frame_17)
        self.lineEdit_calibLaserWavelength.setObjectName(u"lineEdit_calibLaserWavelength")

        self.gridLayout.addWidget(self.lineEdit_calibLaserWavelength, 0, 1, 1, 1)

        self.label = QLabel(self.frame_17)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_laserWavelengthText = QLabel(self.frame_17)
        self.label_laserWavelengthText.setObjectName(u"label_laserWavelengthText")

        self.gridLayout.addWidget(self.label_laserWavelengthText, 0, 0, 1, 1)

        self.lineEdit_calibMirrorSpacing = QLineEdit(self.frame_17)
        self.lineEdit_calibMirrorSpacing.setObjectName(u"lineEdit_calibMirrorSpacing")

        self.gridLayout.addWidget(self.lineEdit_calibMirrorSpacing, 1, 1, 1, 1)

        self.lineEdit_calibScatteringAngle = QLineEdit(self.frame_17)
        self.lineEdit_calibScatteringAngle.setObjectName(u"lineEdit_calibScatteringAngle")

        self.gridLayout.addWidget(self.lineEdit_calibScatteringAngle, 2, 1, 1, 1)

        self.label_4 = QLabel(self.frame_17)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)


        self.verticalLayout_35.addWidget(self.frame_17)

        self.splitter_6 = QSplitter(self.tab_calibMain)
        self.splitter_6.setObjectName(u"splitter_6")
        self.splitter_6.setOrientation(Qt.Vertical)
        self.frame_19 = QFrame(self.splitter_6)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Plain)
        self.verticalLayout_33 = QVBoxLayout(self.frame_19)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.frame_18 = QFrame(self.frame_19)
        self.frame_18.setObjectName(u"frame_18")
        sizePolicy.setHeightForWidth(self.frame_18.sizePolicy().hasHeightForWidth())
        self.frame_18.setSizePolicy(sizePolicy)
        self.frame_18.setFrameShape(QFrame.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_23 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.pushButton_calibAddFiles = QPushButton(self.frame_18)
        self.pushButton_calibAddFiles.setObjectName(u"pushButton_calibAddFiles")

        self.horizontalLayout_23.addWidget(self.pushButton_calibAddFiles)

        self.pushButton_calibRemoveFiles = QPushButton(self.frame_18)
        self.pushButton_calibRemoveFiles.setObjectName(u"pushButton_calibRemoveFiles")

        self.horizontalLayout_23.addWidget(self.pushButton_calibRemoveFiles)

        self.pushButton_calibResetFits = QPushButton(self.frame_18)
        self.pushButton_calibResetFits.setObjectName(u"pushButton_calibResetFits")
        self.pushButton_calibResetFits.setContextMenuPolicy(Qt.DefaultContextMenu)

        self.horizontalLayout_23.addWidget(self.pushButton_calibResetFits)

        self.horizontalSpacer_9 = QSpacerItem(591, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_9)


        self.verticalLayout_33.addWidget(self.frame_18)

        self.tableView_calibFiles = QTableView(self.frame_19)
        self.tableView_calibFiles.setObjectName(u"tableView_calibFiles")

        self.verticalLayout_33.addWidget(self.tableView_calibFiles)

        self.splitter_6.addWidget(self.frame_19)
        self.frame_20 = QFrame(self.splitter_6)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setFrameShape(QFrame.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_26 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.verticalLayout_34 = QVBoxLayout()
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.pushButton_calibFitLeftPeak = QPushButton(self.frame_20)
        self.pushButton_calibFitLeftPeak.setObjectName(u"pushButton_calibFitLeftPeak")
        self.pushButton_calibFitLeftPeak.setCheckable(True)

        self.horizontalLayout_22.addWidget(self.pushButton_calibFitLeftPeak)

        self.pushButton_calibDeleteLeftPeak = QPushButton(self.frame_20)
        self.pushButton_calibDeleteLeftPeak.setObjectName(u"pushButton_calibDeleteLeftPeak")

        self.horizontalLayout_22.addWidget(self.pushButton_calibDeleteLeftPeak)


        self.verticalLayout_34.addLayout(self.horizontalLayout_22)

        self.listWidget_calibLeftPeak = QListWidget(self.frame_20)
        self.listWidget_calibLeftPeak.setObjectName(u"listWidget_calibLeftPeak")

        self.verticalLayout_34.addWidget(self.listWidget_calibLeftPeak)


        self.horizontalLayout_25.addLayout(self.verticalLayout_34)

        self.verticalLayout_36 = QVBoxLayout()
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.pushButton_calibFitRightPeak = QPushButton(self.frame_20)
        self.pushButton_calibFitRightPeak.setObjectName(u"pushButton_calibFitRightPeak")
        self.pushButton_calibFitRightPeak.setCheckable(True)

        self.horizontalLayout_24.addWidget(self.pushButton_calibFitRightPeak)

        self.pushButton_calibDeleteRightPeak = QPushButton(self.frame_20)
        self.pushButton_calibDeleteRightPeak.setObjectName(u"pushButton_calibDeleteRightPeak")

        self.horizontalLayout_24.addWidget(self.pushButton_calibDeleteRightPeak)


        self.verticalLayout_36.addLayout(self.horizontalLayout_24)

        self.listWidget_calibRightPeak = QListWidget(self.frame_20)
        self.listWidget_calibRightPeak.setObjectName(u"listWidget_calibRightPeak")

        self.verticalLayout_36.addWidget(self.listWidget_calibRightPeak)


        self.horizontalLayout_25.addLayout(self.verticalLayout_36)


        self.horizontalLayout_26.addLayout(self.horizontalLayout_25)

        self.splitter_6.addWidget(self.frame_20)

        self.verticalLayout_35.addWidget(self.splitter_6)

        self.tabWidget_calib.addTab(self.tab_calibMain, "")
        self.tab_calibSetup = QWidget()
        self.tab_calibSetup.setObjectName(u"tab_calibSetup")
        self.tabWidget_calib.addTab(self.tab_calibSetup, "")

        self.verticalLayout_32.addWidget(self.tabWidget_calib)

        self.splitter_5.addWidget(self.frame_13)

        self.verticalLayout_30.addWidget(self.splitter_5)

        self.tabWidget_project.addTab(self.tab_calib, "")
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
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_topPlotToolbar.sizePolicy().hasHeightForWidth())
        self.frame_topPlotToolbar.setSizePolicy(sizePolicy1)
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
        sizePolicy1.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy1)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.label_2)

        self.comboBox_pressure = QComboBox(self.frame_filesBrowserToolbar)
        self.comboBox_pressure.setObjectName(u"comboBox_pressure")

        self.horizontalLayout_5.addWidget(self.comboBox_pressure)

        self.label_3 = QLabel(self.frame_filesBrowserToolbar)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)

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
        self.tabWidget_sideBar.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget_sideBar)

        self.splitter_3.addWidget(self.frame_4)

        self.verticalLayout_3.addWidget(self.splitter_3)

        self.tabWidget_project.addTab(self.tab_fit, "")

        self.verticalLayout_28.addWidget(self.tabWidget_project)

        self.frame_11 = QFrame(self.centralwidget)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy)
        self.frame_11.setFrameShape(QFrame.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.label_lastAction = QLabel(self.frame_11)
        self.label_lastAction.setObjectName(u"label_lastAction")

        self.horizontalLayout.addWidget(self.label_lastAction)

        self.label_processStatus = QLabel(self.frame_11)
        self.label_processStatus.setObjectName(u"label_processStatus")

        self.horizontalLayout.addWidget(self.label_processStatus)

        self.label_fileCount = QLabel(self.frame_11)
        self.label_fileCount.setObjectName(u"label_fileCount")

        self.horizontalLayout.addWidget(self.label_fileCount)

        self.label_projectStatus = QLabel(self.frame_11)
        self.label_projectStatus.setObjectName(u"label_projectStatus")

        self.horizontalLayout.addWidget(self.label_projectStatus)


        self.horizontalLayout_13.addLayout(self.horizontalLayout)


        self.verticalLayout_28.addWidget(self.frame_11)


        self.verticalLayout_29.addLayout(self.verticalLayout_28)

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

        self.tabWidget_project.setCurrentIndex(0)
        self.tabWidget_calib.setCurrentIndex(0)
        self.tabWidget_sideBar.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Project management", None))
        self.pushButton_newProject.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.pushButton_loadProject.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.pushButton_saveProject.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pushButton_saveProjectAs.setText(QCoreApplication.translate("MainWindow", u"Save as...", None))
        self.pushButton_deleteProject.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Loaded project:", None))
        self.pushButton_renameProject.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.label_projectPath.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_modDate.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Sample conditions", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Pressures (GPa)", None))
        self.pushButton_newPressure.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.pushButton_deletePressure.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.pushButton_renamePressure.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Crystals", None))
        self.pushButton_newCrystal.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.pushButton_deleteCrystal.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.pushButton_renameCrystal.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.tabWidget_project.setTabText(self.tabWidget_project.indexOf(self.Project), QCoreApplication.translate("MainWindow", u"Project", None))
        self.pushButton_calibResetView.setText(QCoreApplication.translate("MainWindow", u"Reset zom", None))
        self.pushButton_calibZoom.setText(QCoreApplication.translate("MainWindow", u"Zoom", None))
        self.pushButton_calibPan.setText(QCoreApplication.translate("MainWindow", u"Pan", None))
        self.label_calibText1.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_calibText2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_calibText3.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_calibText4.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_calibText5.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.pushButton_calibNewCalib.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.pushButton_calibRenameCalib.setText(QCoreApplication.translate("MainWindow", u"Rename", None))
        self.pushButton_calibRemoveCalib.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Mirror spacing (mm):", None))
        self.label_laserWavelengthText.setText(QCoreApplication.translate("MainWindow", u"Laser wavelength (nm):", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Scattering angle (degrees):", None))
        self.pushButton_calibAddFiles.setText(QCoreApplication.translate("MainWindow", u"Add files", None))
        self.pushButton_calibRemoveFiles.setText(QCoreApplication.translate("MainWindow", u"Remove files", None))
        self.pushButton_calibResetFits.setText(QCoreApplication.translate("MainWindow", u"Reset calibration", None))
        self.pushButton_calibFitLeftPeak.setText(QCoreApplication.translate("MainWindow", u"Fit left peak", None))
        self.pushButton_calibDeleteLeftPeak.setText(QCoreApplication.translate("MainWindow", u"Delete left peak", None))
        self.pushButton_calibFitRightPeak.setText(QCoreApplication.translate("MainWindow", u"Fit right peak", None))
        self.pushButton_calibDeleteRightPeak.setText(QCoreApplication.translate("MainWindow", u"Delete right peak", None))
        self.tabWidget_calib.setTabText(self.tabWidget_calib.indexOf(self.tab_calibMain), QCoreApplication.translate("MainWindow", u"Main", None))
        self.tabWidget_calib.setTabText(self.tabWidget_calib.indexOf(self.tab_calibSetup), QCoreApplication.translate("MainWindow", u"Setup", None))
        self.tabWidget_project.setTabText(self.tabWidget_project.indexOf(self.tab_calib), QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Pressure (GPa): ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Crystal: ", None))
        self.pushButton_addFiles.setText(QCoreApplication.translate("MainWindow", u"Add files", None))
        self.pushButton_removeFiles.setText(QCoreApplication.translate("MainWindow", u"Remove files", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.tabWidget_sideBar.setTabText(self.tabWidget_sideBar.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Main", None))
        self.tabWidget_sideBar.setTabText(self.tabWidget_sideBar.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Setup", None))
        self.tabWidget_project.setTabText(self.tabWidget_project.indexOf(self.tab_fit), QCoreApplication.translate("MainWindow", u"Fit", None))
        self.label_lastAction.setText("")
        self.label_processStatus.setText("")
        self.label_fileCount.setText("")
        self.label_projectStatus.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

