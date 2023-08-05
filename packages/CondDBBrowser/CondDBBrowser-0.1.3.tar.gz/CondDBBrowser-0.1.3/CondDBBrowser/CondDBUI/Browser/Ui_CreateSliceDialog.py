# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt_resources/CreateSliceDialog.ui',
# licensing of 'qt_resources/CreateSliceDialog.ui' applies.
#
# Created: Thu Dec 27 16:24:07 2018
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CreateSliceDialog(object):
    def setupUi(self, CreateSliceDialog):
        CreateSliceDialog.setObjectName("CreateSliceDialog")
        CreateSliceDialog.resize(412, 624)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateSliceDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.destinationGroup = QtWidgets.QGroupBox(CreateSliceDialog)
        self.destinationGroup.setObjectName("destinationGroup")
        self.formLayout = QtWidgets.QFormLayout(self.destinationGroup)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.filenameLabel = QtWidgets.QLabel(self.destinationGroup)
        self.filenameLabel.setObjectName("filenameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.filenameLabel)
        self.filenameWidget = QtWidgets.QWidget(self.destinationGroup)
        self.filenameWidget.setObjectName("filenameWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.filenameWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filename = QtWidgets.QLineEdit(self.filenameWidget)
        self.filename.setObjectName("filename")
        self.horizontalLayout.addWidget(self.filename)
        self.fileDialogButton = QtWidgets.QToolButton(self.filenameWidget)
        self.fileDialogButton.setObjectName("fileDialogButton")
        self.horizontalLayout.addWidget(self.fileDialogButton)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.filenameWidget)
        self.partitionLabel = QtWidgets.QLabel(self.destinationGroup)
        self.partitionLabel.setObjectName("partitionLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.partitionLabel)
        self.partition = QtWidgets.QComboBox(self.destinationGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.partition.sizePolicy().hasHeightForWidth())
        self.partition.setSizePolicy(sizePolicy)
        self.partition.setEditable(True)
        self.partition.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.partition.setObjectName("partition")
        self.partition.addItem("")
        self.partition.addItem("")
        self.partition.addItem("")
        self.partition.addItem("")
        self.partition.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.partition)
        self.append = QtWidgets.QCheckBox(self.destinationGroup)
        self.append.setObjectName("append")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.append)
        self.verticalLayout.addWidget(self.destinationGroup)
        self.selectionGroup = QtWidgets.QGroupBox(CreateSliceDialog)
        self.selectionGroup.setObjectName("selectionGroup")
        self.formLayout_2 = QtWidgets.QFormLayout(self.selectionGroup)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.pathLabel = QtWidgets.QLabel(self.selectionGroup)
        self.pathLabel.setObjectName("pathLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pathLabel)
        self.path = QtWidgets.QComboBox(self.selectionGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.path.sizePolicy().hasHeightForWidth())
        self.path.setSizePolicy(sizePolicy)
        self.path.setObjectName("path")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.path)
        self.sinceLabel = QtWidgets.QLabel(self.selectionGroup)
        self.sinceLabel.setObjectName("sinceLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.sinceLabel)
        self.since = TimePointEdit(self.selectionGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.since.sizePolicy().hasHeightForWidth())
        self.since.setSizePolicy(sizePolicy)
        self.since.setObjectName("since")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.since)
        self.untilLabel = QtWidgets.QLabel(self.selectionGroup)
        self.untilLabel.setObjectName("untilLabel")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.untilLabel)
        self.until = TimePointEdit(self.selectionGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.until.sizePolicy().hasHeightForWidth())
        self.until.setSizePolicy(sizePolicy)
        self.until.setObjectName("until")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.until)
        self.tagsLabel = QtWidgets.QLabel(self.selectionGroup)
        self.tagsLabel.setObjectName("tagsLabel")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.tagsLabel)
        self.tags = QtWidgets.QListView(self.selectionGroup)
        self.tags.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tags.setObjectName("tags")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.tags)
        self.selectionButtons = QtWidgets.QWidget(self.selectionGroup)
        self.selectionButtons.setObjectName("selectionButtons")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.selectionButtons)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.addButton = QtWidgets.QPushButton(self.selectionButtons)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_2.addWidget(self.addButton)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.selectionButtons)
        self.verticalLayout.addWidget(self.selectionGroup)
        self.selectionSetGroup = QtWidgets.QGroupBox(CreateSliceDialog)
        self.selectionSetGroup.setObjectName("selectionSetGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.selectionSetGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.selections = QtWidgets.QTableView(self.selectionSetGroup)
        self.selections.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.selections.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.selections.setObjectName("selections")
        self.verticalLayout_2.addWidget(self.selections)
        self.selectionSetButtons = QtWidgets.QWidget(self.selectionSetGroup)
        self.selectionSetButtons.setObjectName("selectionSetButtons")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.selectionSetButtons)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.utc = QtWidgets.QCheckBox(self.selectionSetButtons)
        self.utc.setObjectName("utc")
        self.horizontalLayout_3.addWidget(self.utc)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.removeButton = QtWidgets.QPushButton(self.selectionSetButtons)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout_3.addWidget(self.removeButton)
        self.verticalLayout_2.addWidget(self.selectionSetButtons)
        self.verticalLayout.addWidget(self.selectionSetGroup)
        self.buttonBox = QtWidgets.QDialogButtonBox(CreateSliceDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.filenameLabel.setBuddy(self.filename)
        self.partitionLabel.setBuddy(self.partition)
        self.pathLabel.setBuddy(self.path)
        self.sinceLabel.setBuddy(self.since)
        self.untilLabel.setBuddy(self.until)
        self.tagsLabel.setBuddy(self.tags)

        self.retranslateUi(CreateSliceDialog)
        self.partition.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), CreateSliceDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), CreateSliceDialog.reject)
        QtCore.QObject.connect(self.fileDialogButton, QtCore.SIGNAL("clicked()"), CreateSliceDialog.openFileDialog)
        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL("clicked()"), CreateSliceDialog.addSelection)
        QtCore.QObject.connect(self.removeButton, QtCore.SIGNAL("clicked()"), CreateSliceDialog.removeSelection)
        QtCore.QObject.connect(self.path, QtCore.SIGNAL("currentIndexChanged(QString)"), CreateSliceDialog.currentPathSelected)
        QtCore.QObject.connect(self.since, QtCore.SIGNAL("dateTimeChanged(QDateTime)"), self.until.setMinimumDateTime)
        QtCore.QObject.connect(self.until, QtCore.SIGNAL("dateTimeChanged(QDateTime)"), self.since.setMaximumDateTime)
        QtCore.QObject.connect(self.filename, QtCore.SIGNAL("textChanged(QString)"), CreateSliceDialog.checkValidData)
        QtCore.QObject.connect(self.partition, QtCore.SIGNAL("textChanged(QString)"), CreateSliceDialog.checkValidData)
        QtCore.QMetaObject.connectSlotsByName(CreateSliceDialog)

    def retranslateUi(self, CreateSliceDialog):
        CreateSliceDialog.setWindowTitle(QtWidgets.QApplication.translate("CreateSliceDialog", "Create slice", None, -1))
        self.destinationGroup.setTitle(QtWidgets.QApplication.translate("CreateSliceDialog", "Destination", None, -1))
        self.filenameLabel.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "Fi&le name", None, -1))
        self.filename.setToolTip(QtWidgets.QApplication.translate("CreateSliceDialog", "Path to the SQLite file", None, -1))
        self.fileDialogButton.setToolTip(QtWidgets.QApplication.translate("CreateSliceDialog", "Open a dialog box to select a file", None, -1))
        self.fileDialogButton.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "...", None, -1))
        self.partitionLabel.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "&Partition", None, -1))
        self.partition.setToolTip(QtWidgets.QApplication.translate("CreateSliceDialog", "Partition name: only uppercase letters or numbers", None, -1))
        self.partition.setItemText(0, QtWidgets.QApplication.translate("CreateSliceDialog", "DDDB", None, -1))
        self.partition.setItemText(1, QtWidgets.QApplication.translate("CreateSliceDialog", "LHCBCOND", None, -1))
        self.partition.setItemText(2, QtWidgets.QApplication.translate("CreateSliceDialog", "SIMCOND", None, -1))
        self.partition.setItemText(3, QtWidgets.QApplication.translate("CreateSliceDialog", "ONLINE", None, -1))
        self.partition.setItemText(4, QtWidgets.QApplication.translate("CreateSliceDialog", "CALIBOFF", None, -1))
        self.append.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "Append", None, -1))
        self.selectionGroup.setTitle(QtWidgets.QApplication.translate("CreateSliceDialog", "Selection", None, -1))
        self.pathLabel.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "&Node", None, -1))
        self.sinceLabel.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "&Since", None, -1))
        self.untilLabel.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "&Until", None, -1))
        self.tagsLabel.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "&Tags", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "&Add", None, -1))
        self.selectionSetGroup.setTitle(QtWidgets.QApplication.translate("CreateSliceDialog", "Selection set", None, -1))
        self.utc.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "UTC", None, -1))
        self.removeButton.setText(QtWidgets.QApplication.translate("CreateSliceDialog", "&Remove", None, -1))

from CondDBBrowser.CondDBUI.Browser.Widgets import TimePointEdit
