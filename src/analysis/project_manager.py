# src/analysis/project_manager.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QInputDialog
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

    def new_project(self):
        # Open a file dialog to select a folder
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_path = folder_dialog.getExistingDirectory(None, "Select Project Folder")

        if folder_path:
            # Ask for the project name
            project_name, ok = QInputDialog.getText(None, "Project Name", "Enter a project name:")
            if ok and project_name:
                # Define the HDF5 file path
                hdf5_file_path = os.path.join(folder_path, f"{project_name}.h5")
                self.project = BrillouinProject()
                self.project.create_project(hdf5_file_path, project_name)
                self.ui.lineEdit_currentProject.setText(project_name)

    def load_project(self):
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        file_dialog.setNameFilter("HDF5 Files (*.h5)")
        filepath, _ = file_dialog.getOpenFileName(None, "Load Project", "", "HDF5 Files (*.h5)")

        if filepath:
            self.project = BrillouinProject()
            self.project.load_project(filepath)
            self.ui.lineEdit_currentProject.setText(self.project.project_name)

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
                    self.project.delete_project()
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
                    self.project.rename_project(new_name)

    def new_pressure(self):
        if self.project:
            pressure, ok = QInputDialog.getDouble(None, "New Pressure", "Enter pressure in GPa:", decimals=2)
            if ok:
                try:
                    self.project.add_pressure(pressure)
                    self.ui.comboBox_pressure.addItem(f"{pressure} GPa")
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"Failed to add pressure: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

    def delete_pressure(self):
        if self.project:
            pressure = self.ui.comboBox_pressure.currentText()
            if pressure:
                pressure_value = float(pressure.split()[0])
                confirm = QMessageBox.question(None, "Confirm Delete", f"Do you want to delete pressure '{pressure}'?",
                                               QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    try:
                        self.project.delete_pressure(pressure_value)
                        self.ui.comboBox_pressure.removeItem(self.ui.comboBox_pressure.currentIndex())
                    except Exception as e:
                        QMessageBox.critical(None, "Error", f"Failed to delete pressure: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

    def new_crystal(self):
        if self.project:
            pressure = self.ui.comboBox_pressure.currentText()
            if pressure:
                pressure_value = float(pressure.split()[0])
                crystal_name, ok = QInputDialog.getText(None, "New Crystal", "Enter crystal name:")
                if ok and crystal_name:
                    try:
                        self.project.add_crystal(pressure_value, crystal_name)
                        self.ui.comboBox_crystal.addItem(crystal_name)
                    except Exception as e:
                        QMessageBox.critical(None, "Error", f"Failed to add crystal: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

    def delete_crystal(self):
        if self.project:
            pressure = self.ui.comboBox_pressure.currentText()
            if pressure:
                pressure_value = float(pressure.split()[0])
                crystal_name = self.ui.comboBox_crystal.currentText()
                if crystal_name:
                    confirm = QMessageBox.question(None, "Confirm Delete",
                                                   f"Do you want to delete crystal '{crystal_name}'?",
                                                   QMessageBox.Yes | QMessageBox.No)
                    if confirm == QMessageBox.Yes:
                        try:
                            self.project.delete_crystal(pressure_value, crystal_name)
                            self.ui.comboBox_crystal.removeItem(self.ui.comboBox_crystal.currentIndex())
                        except Exception as e:
                            QMessageBox.critical(None, "Error", f"Failed to delete crystal: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

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
                        # This line correctly populates the filename in the FileTableModel
                        self.file_model.addFiles(filepaths)

                        try:
                            self.project.add_files(float(pressure.split()[0]), crystal_name, filepaths, metadata={})
                        except Exception as e:
                            QMessageBox.critical(None, "Error", f"Failed to add files: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

    def remove_files(self):
        if self.project:
            pressure = self.ui.comboBox_pressure.currentText()
            if pressure:
                crystal_name = self.ui.comboBox_crystal.currentText()
                if crystal_name:
                    selected_row = self.ui.tableView_files.currentIndex().row()
                    if selected_row >= 0:
                        selected_file = self.file_model.data(self.file_model.index(selected_row, 0), Qt.DisplayRole)
                        confirm = QMessageBox.question(None, "Confirm Delete", f"Do you want to delete file '{selected_file}'?",
                                                       QMessageBox.Yes | QMessageBox.No)
                        if confirm == QMessageBox.Yes:
                            try:
                                self.project.remove_file(float(pressure.split()[0]), crystal_name, selected_file)
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
                        self.project.add_files(float(pressure.split()[0]), crystal_name, [filename], metadata)
