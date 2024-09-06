# src/analysis/project_manager.py
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QAbstractItemView
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

        # Allow multiple selection but keep cells editable
        self.ui.tableView_files.setSelectionMode(QAbstractItemView.ExtendedSelection)  # Enable multi-selection
        self.ui.tableView_files.setSelectionBehavior(QAbstractItemView.SelectItems)  # Allow selecting individual cells

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

        # Add logic to repopulate table when dropdowns change
        self.ui.comboBox_pressure.currentIndexChanged.connect(self.update_table_based_on_dropdown)
        self.ui.comboBox_crystal.currentIndexChanged.connect(self.update_table_based_on_dropdown)

    def update_metadata(self, row, filename, metadata):
        """
        Slot to receive metadata changes from FileTableModel and update the HDF5 temp file.
        """
        if self.project:
            try:
                # Ensure the file exists in the HDF5 file before updating metadata
                if filename in self.project.h5file:
                    for key, value in metadata.items():
                        if value is None and key in ['chi_angle', 'pinhole', 'power', 'polarization', 'scans']:
                            value = np.nan  # Use np.nan for missing numeric values
                        self.project.add_metadata_to_dataset(filename, key, value)
                else:
                    print(f"Warning: Tried to update metadata for non-existent file: {filename}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to update metadata in temp file: {e}")

    def new_project(self):
        folder_dialog = QFileDialog()
        folder_dialog.setFileMode(QFileDialog.Directory)
        folder_path = folder_dialog.getExistingDirectory(None, "Select Project Folder")

        if folder_path:
            project_name, ok = QInputDialog.getText(None, "Project Name", "Enter a project name:")
            if ok and project_name:
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

            # Populate the dropdowns with all unique pressures and crystals from the project
            self.populate_dropdowns()

            QMessageBox.information(None, "Project Loaded",
                                    "Project loaded successfully. Please select a pressure and crystal to view the files.")

    def update_table_based_on_dropdown(self):
        """
        Update the table view to show only the files that match the selected pressure and crystal,
        and populate the metadata columns (chi_angle, pinhole, etc.).
        """

        if self.project:
            selected_pressure = self.ui.comboBox_pressure.currentText().replace(" GPa", "")
            selected_crystal = self.ui.comboBox_crystal.currentText()

            if selected_pressure and selected_crystal:
                # Clear the table before adding new data
                self.file_model.clear()

                # Find files that match the selected pressure and crystal
                matching_files = self.project.find_files_by_pressure_and_crystal(float(selected_pressure),
                                                                                 selected_crystal)

                # Retrieve metadata for each file and populate the table
                files_with_metadata = []
                for filename in matching_files:
                    chi_angle = self.project.get_metadata_from_dataset(filename, 'chi_angle')
                    pinhole = self.project.get_metadata_from_dataset(filename, 'pinhole')
                    power = self.project.get_metadata_from_dataset(filename, 'power')
                    polarization = self.project.get_metadata_from_dataset(filename, 'polarization')
                    scans = self.project.get_metadata_from_dataset(filename, 'scans')
                    files_with_metadata.append((filename, chi_angle, pinhole, power, polarization, scans))

                # Add matching files with metadata to the table
                self.file_model.addFilesWithMetadata(files_with_metadata)

    def populate_dropdowns(self):
        """
        Populate the pressure and crystal dropdowns with all unique values in the project.
        """
        unique_pressures, unique_crystals = self.project.get_unique_pressures_and_crystals()

        # Clear the current items in dropdowns
        self.ui.comboBox_pressure.clear()
        self.ui.comboBox_crystal.clear()

        # Add unique pressures and crystals to the dropdowns
        for pressure in unique_pressures:
            self.ui.comboBox_pressure.addItem(f"{pressure} GPa")
        for crystal in unique_crystals:
            self.ui.comboBox_crystal.addItem(crystal)

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
            pressure = self.ui.comboBox_pressure.currentText().replace(" GPa", "")
            crystal_name = self.ui.comboBox_crystal.currentText()

            if pressure and crystal_name:
                file_dialog = QFileDialog()
                file_dialog.setFileMode(QFileDialog.ExistingFiles)
                filepaths, _ = file_dialog.getOpenFileNames(None, "Add Files", "", "Data Files (*.DAT)")

                if filepaths:
                    try:
                        # Add files to the HDF5 file with the current pressure and crystal
                        self.project.load_all_files_with_metadata(filepaths, float(pressure), crystal_name)

                        # Refresh the table
                        self.file_model.addFiles(filepaths)

                    except Exception as e:
                        QMessageBox.critical(None, "Error", f"Failed to add files: {e}")
        else:
            QMessageBox.warning(None, "Warning", "No project loaded.")

    def remove_files(self):
        if self.project:
            # Get the selected rows by checking which rows contain selected cells
            selected_indexes = self.ui.tableView_files.selectionModel().selectedIndexes()
            selected_rows = list(set(index.row() for index in selected_indexes))  # Get unique rows

            if selected_rows:
                # Get the filenames of the selected rows
                selected_files = [self.file_model.data(self.file_model.index(row, 0), Qt.DisplayRole) for row in
                                  selected_rows]

                # Prepare the list of files for confirmation
                file_list_str = "\n".join(selected_files)

                # Show a scrollable confirmation dialog
                confirm = QMessageBox()
                confirm.setIcon(QMessageBox.Question)
                confirm.setWindowTitle("Confirm Delete")
                confirm.setText("Are you sure you want to delete the following files?")
                confirm.setDetailedText(file_list_str)  # Scrollable list
                confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                confirm.setDefaultButton(QMessageBox.No)

                if confirm.exec() == QMessageBox.Yes:
                    try:
                        # Remove the files from the project and the table model
                        for file in selected_files:
                            self.project.remove_dataset(file)
                            self.file_model.removeFileByName(file)
                    except Exception as e:
                        QMessageBox.critical(None, "Error", f"Failed to delete files: {e}")
            else:
                QMessageBox.warning(None, "Warning", "No files selected.")
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
