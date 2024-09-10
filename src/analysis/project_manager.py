# src/analysis/project_manager.py
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QAbstractItemView, QTableWidgetItem
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
        self.ui.tableView_files.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.tableView_files.setSelectionBehavior(QAbstractItemView.SelectItems)

        # Ensure tables are not editable
        self.ui.tableWidget_pressures.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_crystals.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Define columns for the pressures and crystals tables
        self.ui.tableWidget_pressures.setColumnCount(1)
        self.ui.tableWidget_pressures.setHorizontalHeaderLabels(["Pressure (GPa)"])

        self.ui.tableWidget_crystals.setColumnCount(1)
        self.ui.tableWidget_crystals.setHorizontalHeaderLabels(["Crystal"])

        # Connect signals to corresponding slots
        self.setup_connections()

    def setup_connections(self):
        """Setup signal-slot connections."""
        # Connect model signal for metadata updates
        self.file_model.data_changed_signal.connect(self.update_metadata)

        # Connect UI buttons to methods
        self.ui.pushButton_newProject.clicked.connect(self.new_project_clicked)
        self.ui.pushButton_loadProject.clicked.connect(self.load_project_clicked)
        self.ui.pushButton_saveProject.clicked.connect(self.save_project_clicked)
        self.ui.pushButton_deleteProject.clicked.connect(self.delete_project_clicked)
        self.ui.pushButton_newPressure.clicked.connect(self.new_pressure_clicked)
        self.ui.pushButton_deletePressure.clicked.connect(self.delete_pressure_clicked)
        self.ui.pushButton_newCrystal.clicked.connect(self.new_crystal_clicked)
        self.ui.pushButton_deleteCrystal.clicked.connect(self.delete_crystal_clicked)
        self.ui.pushButton_addFiles.clicked.connect(self.add_files_clicked)
        self.ui.pushButton_removeFiles.clicked.connect(self.remove_files_clicked)
        self.ui.lineEdit_currentProject.editingFinished.connect(self.rename_project_clicked)

        # Connect comboboxes
        self.ui.comboBox_pressure.currentIndexChanged.connect(self.pressure_combobox_changed)
        self.ui.comboBox_crystal.currentIndexChanged.connect(self.crystal_combobox_changed)

    def populate_table_widgets(self):
        """Populate the pressure and crystal tableWidgets with unique values."""
        if self.project:
            pressures, crystals = self.project.get_unique_pressures_and_crystals()

            # Populate pressure tableWidget
            self.ui.tableWidget_pressures.setRowCount(0)  # Clear previous entries
            for pressure in pressures:
                row_position = self.ui.tableWidget_pressures.rowCount()
                self.ui.tableWidget_pressures.insertRow(row_position)
                self.ui.tableWidget_pressures.setItem(row_position, 0, QTableWidgetItem(str(pressure)))

            # Populate crystal tableWidget
            self.ui.tableWidget_crystals.setRowCount(0)  # Clear previous entries
            for crystal in crystals:
                row_position = self.ui.tableWidget_crystals.rowCount()
                self.ui.tableWidget_crystals.insertRow(row_position)
                self.ui.tableWidget_crystals.setItem(row_position, 0, QTableWidgetItem(crystal))

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

    def pressure_combobox_changed(self):
        """Handle pressure combobox change."""
        self.update_table()

    def crystal_combobox_changed(self):
        """Handle crystal combobox change."""
        self.update_table()

    def update_table(self):
        """Update table based on selected pressure and crystal."""
        if not self.project:
            return

        selected_pressure = self.ui.comboBox_pressure.currentText()
        selected_crystal = self.ui.comboBox_crystal.currentText()

        if selected_pressure and selected_crystal:
            # Clear the table before adding new data
            self.file_model.clear()

            matching_files = self.project.find_files_by_pressure_and_crystal(
                float(selected_pressure), selected_crystal
            )

            files_with_metadata = [
                (
                    filename,
                    self.project.get_metadata_from_dataset(filename, 'chi_angle'),
                    self.project.get_metadata_from_dataset(filename, 'pinhole'),
                    self.project.get_metadata_from_dataset(filename, 'power'),
                    self.project.get_metadata_from_dataset(filename, 'polarization'),
                    self.project.get_metadata_from_dataset(filename, 'scans'),
                )
                for filename in matching_files
            ]

            self.file_model.addFilesWithMetadata(files_with_metadata)

    def new_project_clicked(self):
        """Handle the new project button click."""
        folder_path, project_name = self.get_project_folder_and_name()
        if folder_path and project_name:
            self.create_new_project(folder_path, project_name)

    def get_project_folder_and_name(self):
        """Helper to retrieve folder and project name from user input."""
        folder_path = QFileDialog.getExistingDirectory(None, "Select Project Folder")
        if folder_path:
            project_name, ok = QInputDialog.getText(None, "Project Name", "Enter a project name:")
            if ok and project_name:
                return folder_path, project_name
        return None, None

    def create_new_project(self, folder_path, project_name):
        """Create a new project with the specified folder and name."""
        self.project = BrillouinProject(folder_path, project_name)
        self.project.create_h5file()
        self.ui.lineEdit_currentProject.setText(project_name)

    def load_project_clicked(self):
        """Handle the load project button click."""
        filepath = self.get_project_file()
        if filepath:
            self.load_project(filepath)

    def get_project_file(self):
        """Helper to retrieve project file path from user input."""
        filepath, _ = QFileDialog.getOpenFileName(None, "Load Project", "", "HDF5 Files (*.h5)")
        return filepath

    def load_project(self, filepath):
        """Load the selected project."""
        folder = os.path.dirname(filepath)
        project_name = os.path.basename(filepath).replace('.h5', '')
        self.project = BrillouinProject(folder, project_name)
        self.project.load_h5file()
        self.ui.lineEdit_currentProject.setText(project_name)
        self.populate_dropdowns()
        self.populate_table_widgets()  # Populate tables after loading project

    def populate_dropdowns(self):
        """Populate pressure and crystal comboboxes with unique values from the project."""
        if self.project:
            unique_pressures, unique_crystals = self.project.get_unique_pressures_and_crystals()

            self.ui.comboBox_pressure.clear()
            self.ui.comboBox_crystal.clear()

            for pressure in unique_pressures:
                print(str(pressure))
                print(type(str(pressure)))
                self.ui.comboBox_pressure.addItem(str(pressure))
            for crystal in unique_crystals:
                self.ui.comboBox_crystal.addItem(crystal)

    def save_project_clicked(self):
        """Handle the save project button click."""
        if self.project:
            self.save_project()

    def save_project(self):
        """Save the current project."""
        try:
            self.save_table_data()
            self.project.save_project()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to save project: {e}")

    def delete_project_clicked(self):
        """Handle the delete project button click."""
        if self.project:
            self.delete_project()

    def delete_project(self):
        """Delete the current project after confirmation."""
        confirm = QMessageBox.question(
            None, "Confirm Delete", "Are you sure you want to delete this project?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            try:
                os.remove(self.project.h5file_path)
                self.ui.lineEdit_currentProject.clear()
                self.ui.tableView_files.clearContents()
                self.project = None
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to delete project: {e}")

    def rename_project_clicked(self):
        """Handle the rename project text edit finished."""
        if self.project:
            self.rename_project(self.ui.lineEdit_currentProject.text())

    def rename_project(self, new_name):
        """Rename the current project."""
        confirm = QMessageBox.question(
            None, "Confirm Rename", f"Do you want to rename the project to '{new_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            new_h5file_path = os.path.join(self.project.folder, f"{new_name}.h5")
            try:
                os.rename(self.project.h5file_path, new_h5file_path)
                self.project.h5file_path = new_h5file_path
                self.project.project_name = new_name
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to rename project: {e}")

    def new_pressure_clicked(self):
        """Handle the new pressure button click."""
        pressure, ok = QInputDialog.getDouble(None, "New Pressure", "Enter pressure in GPa:", decimals=2)
        if ok:
            self.project.add_pressure(float(pressure))  # Add to project file
            self.populate_table_widgets()  # Update tableWidget
            self.populate_dropdowns()

    def delete_pressure_clicked(self):
        """Handle the delete pressure button click."""
        selected_rows = self.ui.tableWidget_pressures.selectionModel().selectedRows()
        if selected_rows:
            confirm = QMessageBox.question(None, "Confirm Delete", "Do you want to delete the selected pressure(s)?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                for row in selected_rows:
                    pressure = float(self.ui.tableWidget_pressures.item(row.row(), 0).text())
                    self.project.remove_pressure(pressure)  # Remove from project file
                self.populate_table_widgets()  # Update tableWidget
                self.populate_dropdowns()

    def new_crystal_clicked(self):
        """Handle the new crystal button click."""
        crystal_name, ok = QInputDialog.getText(None, "New Crystal", "Enter crystal name:")
        if ok and crystal_name:
            self.project.add_crystal(crystal_name)  # Add to project file
            self.populate_table_widgets()  # Update tableWidget
            self.populate_dropdowns()

    def delete_crystal_clicked(self):
        """Handle the delete crystal button click."""
        selected_rows = self.ui.tableWidget_crystals.selectionModel().selectedRows()
        if selected_rows:
            confirm = QMessageBox.question(None, "Confirm Delete", "Do you want to delete the selected crystal(s)?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                for row in selected_rows:
                    crystal = self.ui.tableWidget_crystals.item(row.row(), 0).text()
                    self.project.remove_crystal(crystal)  # Remove from project file
                self.populate_table_widgets()  # Update tableWidget
                self.populate_dropdowns()

    def add_files_clicked(self):
        """Handle the add files button click."""
        pressure = self.ui.comboBox_pressure.currentText()
        crystal_name = self.ui.comboBox_crystal.currentText()

        if pressure and crystal_name:
            self.add_files(float(pressure), crystal_name)

    def add_files(self, pressure, crystal_name):
        """Prompt the user to select files and add them to the project."""
        filepaths, _ = QFileDialog.getOpenFileNames(None, "Add Files", "", "Data Files (*.DAT)")
        if filepaths:
            try:
                self.project.load_all_files_with_metadata(filepaths, pressure, crystal_name)
                self.file_model.addFiles(filepaths)
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to add files: {e}")

    def remove_files_clicked(self):
        """Handle the remove files button click."""
        self.remove_files()

    def remove_files(self):
        """Remove selected files from the project and table after confirmation."""
        selected_files = self.get_selected_files()
        if selected_files:
            confirm = self.show_delete_confirmation(selected_files)
            if confirm == QMessageBox.Yes:
                self.delete_selected_files(selected_files)

    def get_selected_files(self):
        """Get the filenames of the selected rows."""
        selected_indexes = self.ui.tableView_files.selectionModel().selectedIndexes()
        selected_rows = list(set(index.row() for index in selected_indexes))
        return [self.file_model.data(self.file_model.index(row, 0), Qt.DisplayRole) for row in selected_rows]

    def show_delete_confirmation(self, selected_files):
        """Show a scrollable confirmation dialog for deleting files."""
        file_list_str = "\n".join(selected_files)
        confirm = QMessageBox()
        confirm.setIcon(QMessageBox.Question)
        confirm.setWindowTitle("Confirm Delete")
        confirm.setText("Are you sure you want to delete the following files?")
        confirm.setDetailedText(file_list_str)
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        return confirm.exec()

    def delete_selected_files(self, selected_files):
        """Delete selected files from the project and table."""
        try:
            for file in selected_files:
                self.project.remove_dataset(file)
                self.file_model.removeFileByName(file)
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to delete files: {e}")

    def save_table_data(self):
        """Save the table data as metadata for each file."""
        pressure = self.ui.comboBox_pressure.currentText()
        crystal_name = self.ui.comboBox_crystal.currentText()
        if self.project and pressure and crystal_name:
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
