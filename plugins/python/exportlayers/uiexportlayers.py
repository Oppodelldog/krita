# This script is licensed CC 0 1.0, so that you can learn from it.

# ------ CC 0 1.0 ---------------

# The person who associated a work with this deed has dedicated the
# work to the public domain by waiving all of his or her rights to the
# work worldwide under copyright law, including all related and
# neighboring rights, to the extent allowed by law.

# You can copy, modify, distribute and perform the work, even for
# commercial purposes, all without asking permission.

# https://creativecommons.org/publicdomain/zero/1.0/legalcode
from . import exportlayers_defaults
from . import exportlayersdialog
from PyQt5.QtCore import (Qt, QRect)
from PyQt5.QtWidgets import (QFormLayout, QListWidget, QHBoxLayout,
                             QDialogButtonBox, QVBoxLayout, QFrame,
                             QPushButton, QAbstractScrollArea, QLineEdit,
                             QMessageBox, QFileDialog, QCheckBox, QSpinBox,
                             QComboBox)
import os
import krita


class UIExportLayers(object):

    def __init__(self):
        self.mainDialog = exportlayersdialog.ExportLayersDialog()
        self.mainLayout = QVBoxLayout(self.mainDialog)
        self.formLayout = QFormLayout()
        self.resSpinBoxLayout = QFormLayout()
        self.documentLayout = QVBoxLayout()
        self.directorySelectorLayout = QHBoxLayout()
        self.optionsLayout = QVBoxLayout()
        self.rectSizeLayout = QHBoxLayout()
        self.saveSettingsLayout = QHBoxLayout()

        self.refreshButton = QPushButton(i18n("Refresh"))
        self.widgetDocuments = QListWidget()
        self.directoryTextField = QLineEdit()
        self.directoryDialogButton = QPushButton(i18n("..."))
        self.exportFilterLayersCheckBox = QCheckBox(i18n("Export filter layers"))
        self.batchmodeCheckBox = QCheckBox(i18n("Export in batchmode"))
        self.ignoreInvisibleLayersCheckBox = QCheckBox(i18n("Ignore invisible layers"))
        self.cropToImageBounds = QCheckBox(i18n("Adjust export size to layer content"))
        self.saveSettingsCheckBox = QCheckBox(i18n("Remember Settings"))
        self.saveSettingsResetButton = QPushButton(i18n("Reset to defaults"))
        self.rectWidthSpinBox = QSpinBox()
        self.rectHeightSpinBox = QSpinBox()
        self.formatsComboBox = QComboBox()
        self.resSpinBox = QSpinBox()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.kritaInstance = krita.Krita.instance()
        self.documentsList = []

        self.directoryTextField.setReadOnly(True)
        self.batchmodeCheckBox.setChecked(True)
        self.directoryDialogButton.clicked.connect(self._selectDir)
        self.widgetDocuments.currentRowChanged.connect(self._selectedDocumentChanged)
        self.refreshButton.clicked.connect(self.refreshButtonClicked)
        self.buttonBox.accepted.connect(self.confirmButton)
        self.buttonBox.rejected.connect(self.mainDialog.close)
        self.cropToImageBounds.stateChanged.connect(self._toggleCropSize)
        self.saveSettingsResetButton.clicked.connect(self._resetSettings)

        self.mainDialog.setWindowModality(Qt.NonModal)
        self.widgetDocuments.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.defaultValues = exportlayers_defaults.ExportLayersDefaultValuesFactory.create(self.kritaInstance)

    def initialize(self):
        self.loadDocuments()
        if self.widgetDocuments.count() == 0:
            messageBox = QMessageBox(self.mainDialog)
            messageBox.setText(i18n("To export Layers open a document first"))
            messageBox.exec_()
            self.mainDialog.destroy()
            return

        self.rectWidthSpinBox.setRange(1, 10000)
        self.rectHeightSpinBox.setRange(1, 10000)
        self.resSpinBox.setRange(20, 1200)

        self.formatsComboBox.addItem(i18n("JPEG"))
        self.formatsComboBox.addItem(i18n("PNG"))

        self.documentLayout.addWidget(self.widgetDocuments)
        self.documentLayout.addWidget(self.refreshButton)

        self.directorySelectorLayout.addWidget(self.directoryTextField)
        self.directorySelectorLayout.addWidget(self.directoryDialogButton)

        self.optionsLayout.addWidget(self.exportFilterLayersCheckBox)
        self.optionsLayout.addWidget(self.batchmodeCheckBox)
        self.optionsLayout.addWidget(self.ignoreInvisibleLayersCheckBox)
        self.optionsLayout.addWidget(self.cropToImageBounds)

        self.resSpinBoxLayout.addRow(i18n("dpi:"), self.resSpinBox)

        self.rectSizeLayout.addWidget(self.rectWidthSpinBox)
        self.rectSizeLayout.addWidget(self.rectHeightSpinBox)
        self.rectSizeLayout.addLayout(self.resSpinBoxLayout)

        self.saveSettingsLayout.addWidget(self.saveSettingsCheckBox)
        self.saveSettingsLayout.addWidget(self.saveSettingsResetButton)

        self.formLayout.addRow(i18n("Documents:"), self.documentLayout)
        self.formLayout.addRow(i18n("Initial directory:"), self.directorySelectorLayout)
        self.formLayout.addRow(i18n("Export options:"), self.optionsLayout)
        self.formLayout.addRow(i18n("Export size:"), self.rectSizeLayout)
        self.formLayout.addRow(i18n("Images extensions:"), self.formatsComboBox)
        self.formLayout.addRow(i18n("Save Settings:"), self.saveSettingsLayout)

        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.line)
        self.mainLayout.addWidget(self.buttonBox)

        self.defaultValues.bind_output_format(self.formatsComboBox)
        self.defaultValues.bind_output_directory(self.directoryTextField)
        self.defaultValues.bind_crop_to_image_bounds(self.cropToImageBounds)
        self.defaultValues.bind_export_filter_layers_check_box(self.exportFilterLayersCheckBox)
        self.defaultValues.bind_batch_mode_check_box(self.batchmodeCheckBox)
        self.defaultValues.bind_ignore_invisible_layers_check_box(self.ignoreInvisibleLayersCheckBox)
        self.defaultValues.bind_rect_width_spin_box(self.rectWidthSpinBox)
        self.defaultValues.bind_rect_height_spin_box(self.rectHeightSpinBox)
        self.defaultValues.bind_dpi_spin_box(self.resSpinBox)
        self.defaultValues.bind_dpi_spin_box(self.resSpinBox)

        self.mainDialog.resize(500, 300)
        self.mainDialog.setWindowTitle(i18n("Export Layers"))
        self.mainDialog.setSizeGripEnabled(True)
        self.mainDialog.show()
        self.mainDialog.activateWindow()

    def selectedDocumentFilePath(self):
        return self.widgetDocuments.currentItem().text()

    @staticmethod
    def selectListWidgetRow(listWidget, value):
        for i in range(listWidget.count()):
            item = listWidget.item(i)
            if item.text() == value:
                listWidget.setCurrentRow(i)

    def loadDocuments(self):
        self.widgetDocuments.clear()

        self.documentsList = [
            document for document in self.kritaInstance.documents()
            if document.fileName()
        ]

        for document in self.documentsList:
            self.widgetDocuments.addItem(document.fileName())

        if self.canSelectActiveDocument():
            self.selectActiveDocument()

    def canSelectActiveDocument(self):
        return self.widgetDocuments.count() > 0 and self.widgetDocuments.currentItem() is None and self.kritaInstance.activeDocument() is not None

    def selectActiveDocument(self):
        self.selectListWidgetRow(self.widgetDocuments, self.kritaInstance.activeDocument().fileName())

    def refreshButtonClicked(self):
        self.loadDocuments()

    def confirmButton(self):
        selectedPaths = [
            item.text() for item in self.widgetDocuments.selectedItems()]
        selectedDocuments = [
            document for document in self.documentsList
            for path in selectedPaths if path == document.fileName()
        ]

        self.msgBox = QMessageBox(self.mainDialog)
        if not selectedDocuments:
            self.msgBox.setText(i18n("Select one document."))
        elif not self.directoryTextField.text():
            self.msgBox.setText(i18n("Select the initial directory."))
        else:
            self.export(selectedDocuments[0])
            self.msgBox.setText(i18n("All layers has been exported."))
        self.msgBox.exec_()

        self.saveSettings()

    def mkdir(self, directory):
        target_directory = self.directoryTextField.text() + directory
        if (os.path.exists(target_directory)
                and os.path.isdir(target_directory)):
            return

        try:
            os.makedirs(target_directory)
        except OSError as e:
            raise e

    def export(self, document):
        self.kritaInstance.setBatchmode(self.batchmodeCheckBox.isChecked())

        documentName = document.fileName() if document.fileName() else 'Untitled'  # noqa: E501
        fileName, extension = os.path.splitext(os.path.basename(documentName))
        self.mkdir('/' + fileName)

        self._exportLayers(
            document.rootNode(),
            self.formatsComboBox.currentText(),
            '/' + fileName)
        self.kritaInstance.setBatchmode(True)

    def _exportLayers(self, parentNode, fileFormat, parentDir):
        """ This method get all sub-nodes from the current node and export then in
            the defined format."""

        for node in parentNode.childNodes():
            newDir = ''
            if node.type() == 'grouplayer':
                newDir = os.path.join(parentDir, node.name())
                self.mkdir(newDir)
            elif (not self.exportFilterLayersCheckBox.isChecked()
                  and 'filter' in node.type()):
                continue
            elif (self.ignoreInvisibleLayersCheckBox.isChecked()
                  and not node.visible()):
                continue
            else:
                nodeName = node.name()
                _fileFormat = self.formatsComboBox.currentText()
                if '[jpeg]' in nodeName:
                    _fileFormat = 'jpeg'
                elif '[png]' in nodeName:
                    _fileFormat = 'png'

                if self.cropToImageBounds.isChecked():
                    bounds = QRect()
                else:
                    bounds = QRect(0, 0, self.rectWidthSpinBox.value(), self.rectHeightSpinBox.value())

                layerFileName = '{0}{1}/{2}.{3}'.format(
                    self.directoryTextField.text(),
                    parentDir, node.name(), _fileFormat)
                node.save(layerFileName, self.resSpinBox.value() / 72.,
                          self.resSpinBox.value() / 72., krita.InfoObject(), bounds)

            if node.childNodes():
                self._exportLayers(node, fileFormat, newDir)

    def _selectDir(self):
        directory = QFileDialog.getExistingDirectory(
            self.mainDialog,
            i18n("Select a Folder"),
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly)
        self.directoryTextField.setText(directory)

    def _selectedDocumentChanged(self, index):
        document = self.documentsList[index]
        self.rectWidthSpinBox.setValue(document.width())
        self.rectHeightSpinBox.setValue(document.height())
        self.resSpinBox.setValue(document.resolution())

    def _toggleCropSize(self):
        cropToLayer = self.cropToImageBounds.isChecked()
        self.rectWidthSpinBox.setDisabled(cropToLayer)
        self.rectHeightSpinBox.setDisabled(cropToLayer)

    def load_settings(self, document):
        self.saveSettingsCheckBox.setChecked(False)
        is_saved_setting = self.defaultValues.load(document.fileName())
        self.saveSettingsResetButton.setDisabled(not is_saved_setting)

    def saveSettings(self):
        if self.saveSettingsCheckBox.isChecked():
            self.defaultValues.save(self.selectedDocumentFilePath())
            self.saveSettingsCheckBox.setChecked(False)
            self.saveSettingsResetButton.setDisabled(False)

    def _resetSettings(self):
        self.defaultValues.remove(self.selectedDocumentFilePath())
        self.saveSettingsResetButton.setDisabled(True)
