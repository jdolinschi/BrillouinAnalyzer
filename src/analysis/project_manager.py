# src/analysis/project_manager.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog
from .brillouin_project import BrillouinProject
from .file_table_model import FileTableModel  # Import the custom model
import os


class ProjectManager:
    def __init__(self, ui):
        self.ui = ui
        self.project = None

        # Create an instance of the custom model
        self.file_model = FileTableModel()
        self.ui.tableView_files.setModel(self.file_model)

        # Connect the signal to the slot
        self.file_model.data_changed_signal.connect(self.update_metadata)

        # Connect buttons to their corresponding methods
        self.ui.pushButton_newProject.clicked.connect(self.new_project)
        self.ui.pushButton_loadProject.clicked.connect(self.load_project)
        self.ui.pushButton_saveProject.clicked.connect(self.save_project)
        self.ui.pushButton_deleteProject.clicked.connect(self.delete_project)
        self.ui.pushButton_newPressure.clicked.connect(self.new_pressure)
        self.ui.pushButton_deletePressure.clicked.connect(self.delete_pressure)
        self.ui.pushButton_newCrystal.clicked.connect(self.new_crystal)
        self.ui.pushButton_deleteCrystal.clicked.connect(self.delete_crystal)
        self.ui.pushButton_addFiles.clicked.connect(self.add_files)
        self.ui.pushButton_removeFiles.clicked.connect(self.remove_files)
        self.ui.lineEdit_currentProject.editingFinished.connect(self.rename_project)

    def update_metadata(self, row, filename, metadata):
        """
        Slot to receive metadata changes from FileTableModel and update the HDF5 temp file.
        """
        if self.project:
            try:
                # Ensure the file exists in the HDF5 file before updating metadata
                if filename in self.project.h5file:
                    for key, value in metadata.items():
                        self.project.add_metadata_to_dataset(filename, key, value)
                else:
                    print(f"Warning: Tried to update metadata for non-existent file: {filename}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to update metadata in temp file: {e}")

    def new_project(self):
        # Open a file dialog to select a folder
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_path = folder_dialog.getExistingDirectory(None, "Select Project Folder")

        if folder_path:
            # Ask for the project name
            project_name, ok = QInputDialog.getText(None, "Project Name", "Enter a project name:")
            if ok and project_name:
                # Create the BrillouinProject instance
                self.project = BrillouinProject(folder_path, project_name)
                self.project.create_h5file()
                self.ui.lineEdit_currentProject.setText(project_name)

    def load_project(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setNameFilter("HDF5 Files (*.h5)")
        filepath, _ = file_dialog.getOpenFileName(None, "Load Project", "", "HDF5 Files (*.h5)")

        if filepath:
            folder = os.path.dirname(filepath)
            project_name = os.path.basename(filepath).replace('.h5', '')
            self.project = BrillouinProject(folder, project_name)
            self.project.load_h5file()
            self.ui.lineEdit_currentProject.setText(project_name)

    def save_project(self):
        if self.project:
            try:
                self.save_table_data()
                self.project.save_project()
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to save project: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

    def delete_project(self):
        if self.project:
            confirm = QMessageBox.question(None, "Confirm Delete", "Are you sure you want to delete this project?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                try:
                    os.remove(self.project.h5file_path)
                    self.ui.lineEdit_currentProject.clear()
                    self.ui.tableView_files.clearContents()
                    self.project = None
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Failed to delete project: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

    def rename_project(self):
        if self.project:
            new_name = self.ui.lineEdit_currentProject.text()
            if new_name:
                confirm = QMessageBox.question(None, "Confirm Rename",
                                               f"Do you want to rename the project to '{new_name}'?",
                                               QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    # Rename the project file and update the project name
                    new_h5file_path = os.path.join(self.project.folder, f"{new_name}.h5")
                    try:
                        os.rename(self.project.h5file_path, new_h5file_path)
                        self.project.h5file_path = new_h5file_path
                        self.project.project_name = new_name
                    except Exception as e:
                        QMessageBox.critical(None, "Error", f"Failed to rename project: {e}")

    def new_pressure(self):
        if self.project:
            pressure, ok = QInputDialog.getDouble(None, "New Pressure", "Enter pressure in GPa:", decimals=2)
            if ok:
                self.ui.comboBox_pressure.addItem(f"{pressure} GPa")

    def delete_pressure(self):
        if self.project:
            pressure = self.ui.comboBox_pressure.currentText()
            if pressure:
                confirm = QMessageBox.question(None, "Confirm Delete", f"Do you want to delete pressure '{pressure}'?",
                                               QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    self.ui.comboBox_pressure.removeItem(self.ui.comboBox_pressure.currentIndex())

    def new_crystal(self):
        if self.project:
            pressure = self.ui.comboBox_pressure.currentText()
            if pressure:
                crystal_name, ok = QInputDialog.getText(None, "New Crystal", "Enter crystal name:")
                if ok and crystal_name:
                    self.ui.comboBox_crystal.addItem(crystal_name)

    def delete_crystal(self):
        if self.project:
            crystal_name = self.ui.comboBox_crystal.currentText()
            if crystal_name:
                confirm = QMessageBox.question(None, "Confirm Delete",
                                               f"Do you want to delete crystal '{crystal_name}'?",
                                               QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    self.ui.comboBox_crystal.removeItem(self.ui.comboBox_crystal.currentIndex())

    def add_files(self):
        if self.project:
            pressure = self.ui.comboBox_pressure.currentText()
            if pressure:
                crystal_name = self.ui.comboBox_crystal.currentText()
                if crystal_name:
                    file_dialog = QFileDialog()
                    file_dialog.setFileMode(QFileDialog.ExistingFiles)
                    filepaths, _ = file_dialog.getOpenFileNames(None, "Add Files", "", "Data Files (*.DAT)")

                    if filepaths:
                        # Add filenames to the table view
                        print('inside "add_files". filepaths:')
                        print(filepaths)
                        self.file_model.addFiles(filepaths)

                        try:
                            # First, load all files into the HDF5 file
                            self.project.load_all_files(filepaths)

                            # No need to add metadata here; it will be added when the user edits the table

                        except Exception as e:
                            QMessageBox.critical(None, "Error", f"Failed to add files: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

    def remove_files(self):
        if self.project:
            selected_row = self.ui.tableView_files.currentIndex().row()
            if selected_row >= 0:
                selected_file = self.file_model.data(self.file_model.index(selected_row, 0), Qt.DisplayRole)
                confirm = QMessageBox.question(None, "Confirm Delete", f"Do you want to delete file '{selected_file}'?",
                                               QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    try:
                        self.project.remove_dataset(selected_file)
                        self.file_model.removeRows(selected_row, 1)
                    except Exception as e:
                        QMessageBox.critical(None, "Error", f"Failed to delete file: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

    def save_table_data(self):
        """Save the table data as metadata for each file."""
        if self.project:
            pressure = self.ui.comboBox_pressure.currentText()
            if pressure:
                crystal_name = self.ui.comboBox_crystal.currentText()
                if crystal_name:
                    for row in range(self.file_model.rowCount()):
                        filename = self.file_model.data(self.file_model.index(row, 0), Qt.DisplayRole)
                        metadata = {
                            'chi_angle': self.file_model.data(self.file_model.index(row, 1), Qt.DisplayRole),
                            'pinhole': self.file_model.data(self.file_model.index(row, 2), Qt.DisplayRole),
                            'power': self.file_model.data(self.file_model.index(row, 3), Qt.DisplayRole),
                            'polarization': self.file_model.data(self.file_model.index(row, 4), Qt.DisplayRole),
                            'scans': self.file_model.data(self.file_model.index(row, 5), Qt.DisplayRole),
                        }
                        for key, value in metadata.items():
                            if value is not None:
                                self.project.add_metadata_to_dataset(filename, key, value)
