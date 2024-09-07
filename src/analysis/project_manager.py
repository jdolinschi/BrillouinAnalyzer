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
        self.ui.tableView_files.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.tableView_files.setSelectionBehavior(QAbstractItemView.SelectItems)

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

        selected_pressure = self.ui.comboBox_pressure.currentText().replace(" GPa", "")
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

    def populate_dropdowns(self):
        """Populate pressure and crystal comboboxes with unique values from the project."""
        if self.project:
            unique_pressures, unique_crystals = self.project.get_unique_pressures_and_crystals()

            self.ui.comboBox_pressure.clear()
            self.ui.comboBox_crystal.clear()

            for pressure in unique_pressures:
                self.ui.comboBox_pressure.addItem(f"{pressure} GPa")
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
        self.add_new_pressure()

    def add_new_pressure(self):
        """Prompt the user for a new pressure and add it to the combobox."""
        pressure, ok = QInputDialog.getDouble(None, "New Pressure", "Enter pressure in GPa:", decimals=2)
        if ok:
            self.ui.comboBox_pressure.addItem(f"{pressure} GPa")

    def delete_pressure_clicked(self):
        """Handle the delete pressure button click."""
        self.delete_pressure()

    def delete_pressure(self):
        """Delete the selected pressure after confirmation."""
        pressure = self.ui.comboBox_pressure.currentText()
        if pressure:
            confirm = QMessageBox.question(
                None, "Confirm Delete", f"Do you want to delete pressure '{pressure}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.ui.comboBox_pressure.removeItem(self.ui.comboBox_pressure.currentIndex())

    def new_crystal_clicked(self):
        """Handle the new crystal button click."""
        self.add_new_crystal()

    def add_new_crystal(self):
        """Prompt the user for a new crystal and add it to the combobox."""
        crystal_name, ok = QInputDialog.getText(None, "New Crystal", "Enter crystal name:")
        if ok and crystal_name:
            self.ui.comboBox_crystal.addItem(crystal_name)

    def delete_crystal_clicked(self):
        """Handle the delete crystal button click."""
        self.delete_crystal()

    def delete_crystal(self):
        """Delete the selected crystal after confirmation."""
        crystal_name = self.ui.comboBox_crystal.currentText()
        if crystal_name:
            confirm = QMessageBox.question(
                None, "Confirm Delete", f"Do you want to delete crystal '{crystal_name}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.ui.comboBox_crystal.removeItem(self.ui.comboBox_crystal.currentIndex())

    def add_files_clicked(self):
        """Handle the add files button click."""
        pressure = self.ui.comboBox_pressure.currentText().replace(" GPa", "")
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
