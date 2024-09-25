# src/analysis/project_manager.py
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QClipboard
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QAbstractItemView, QTableWidgetItem, QMenu, \
    QApplication, QTableView
from scipy.optimize import curve_fit
from scipy.special import wofz

from .brillouin_project import BrillouinProject
from .file_table_model import FileTableModel  # Import the custom model
from .calibration_file_table_model import CalibrationFileTableModel
from ..utils.custom_delegate import CheckboxLineEditDelegate
import os


class ProjectManager:
    def __init__(self, ui):
        self.ui = ui
        self.project = None
        self.unsaved_changes = False

        # Create an instance of the custom model
        self.file_model = FileTableModel()
        self.ui.tableView_files.setModel(self.file_model)

        self.calib_files_model = CalibrationFileTableModel()
        self.ui.tableView_calibFiles.setModel(self.calib_files_model)

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

        self.ui.tableView_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView_files.customContextMenuRequested.connect(self.show_context_menu)

        # Enable copy-paste shortcuts in the tableView_files
        self.ui.tableView_files.keyPressEvent = self.table_keyPressEvent

        # Assign the custom delegate to the top row
        delegate = CheckboxLineEditDelegate(self.ui.tableView_files)
        self.ui.tableView_files.setItemDelegateForRow(0, delegate)

        # Connect signals to corresponding slots
        self.setup_connections()

        self.save_status()

    def set_calibration_manager(self, calibration_manager):
        self.calibration_manager = calibration_manager

    def last_action(self, text):
        """Update the last action label."""
        self.ui.label_lastAction.setText(f"| Last action: {text} ")

    def update_file_count(self):
        """Update the file count label."""
        if self.project is None:
            self.ui.label_fileCount.setText("| File count: 0 ")
        else:
            file_count = self.project.get_file_count()
            self.ui.label_fileCount.setText(f"| File count: {file_count} ")

    def save_status(self):
        """Update project status based on whether there are unsaved changes."""
        if self.project is None:
            self.ui.label_projectStatus.setText("| No project loaded")
        else:
            unsaved_changes = self.project.check_unsaved_changes()
            if unsaved_changes:
                self.ui.label_projectStatus.setText("| Unsaved Changes")
            else:
                self.ui.label_projectStatus.setText("| Project Saved")

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


    # Add a new method for context menu:
    def show_context_menu(self, pos):
        index = self.ui.tableView_files.indexAt(pos)
        if not index.isValid():
            return

        menu = QMenu()
        copy_action = menu.addAction("Copy")
        paste_action = menu.addAction("Paste")
        fill_column_action = menu.addAction("Fill column")

        action = menu.exec_(self.ui.tableView_files.viewport().mapToGlobal(pos))

        if action == copy_action:
            self.copy_selection()
            self.last_action('Copied')
        elif action == paste_action:
            self.paste_selection()
            self.last_action('Pasted')
        elif action == fill_column_action:
            self.fill_column(index)  # Call fill_column method with the selected index
            self.last_action('Fill column')

        self.save_status()

    def fill_column(self, index):
        """
        Fill the entire column with the value from the selected cell.
        """
        if not index.isValid():
            return

        value = self.file_model.data(index, Qt.DisplayRole)  # Get the value from the selected cell

        if value is None or value == '':
            return  # If the cell is empty, don't fill the column

        column = index.column()

        # Fill the entire column with the selected value
        for row in range(self.file_model.rowCount()):
            current_index = self.file_model.index(row, column)
            self.file_model.setData(current_index, value, Qt.EditRole)

    # Add copy and paste functions:
    def copy_selection(self):
        selection = self.ui.tableView_files.selectedIndexes()
        if not selection:
            return

        data = []
        rows = max(index.row() for index in selection) - min(index.row() for index in selection) + 1
        cols = max(index.column() for index in selection) - min(index.column() for index in selection) + 1
        data = [['' for _ in range(cols)] for _ in range(rows)]

        for index in selection:
            data[index.row() - min(i.row() for i in selection)][
                index.column() - min(i.column() for i in selection)] = self.file_model.data(index, Qt.DisplayRole)

        clipboard = QApplication.clipboard()
        clipboard.setText('\n'.join('\t'.join(map(str, row)) for row in data))

    def paste_selection(self):
        clipboard = QApplication.clipboard()
        data = [line.split('\t') for line in clipboard.text().split('\n')]

        selected_indexes = self.ui.tableView_files.selectedIndexes()
        if not selected_indexes:
            return

        row_offset = min(index.row() for index in selected_indexes)
        col_offset = min(index.column() for index in selected_indexes)

        for i, row_data in enumerate(data):
            for j, value in enumerate(row_data):
                row = row_offset + i
                col = col_offset + j
                index = self.file_model.index(row, col)
                self.file_model.setData(index, value, Qt.EditRole)

    # Handle keyboard shortcuts for copy-paste
    def table_keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy_selection()
        elif event.matches(QKeySequence.Paste):
            self.paste_selection()
        else:
            QTableView.keyPressEvent(self.ui.tableView_files, event)

    def check_unsaved_changes(self):
        """Check if there are unsaved changes and show a popup with the changes."""
        if self.project is None:
            return True  # No project open, safe to close

        # Get the unsaved changes
        changes = self.project.check_unsaved_changes(detailed=True)

        if not changes["added"] and not changes["removed"] and not changes["altered"]:
            return True  # No unsaved changes, safe to close

        # Build the list of changes
        change_text = []
        if changes["added"]:
            change_text.append("ADDED:\n" + "\n".join(changes["added"]))
        if changes["removed"]:
            change_text.append("REMOVED:\n" + "\n".join(changes["removed"]))
        if changes["altered"]:
            change_text.append("ALTERED:\n" + "\n".join(changes["altered"]))

        change_message = "\n\n".join(change_text)

        # Display a popup with options to cancel, save and exit, or exit without saving
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Unsaved Changes")
        msg_box.setText("There are unsaved changes in the project:")
        msg_box.setInformativeText(change_message)
        msg_box.setStandardButtons(QMessageBox.Cancel | QMessageBox.Save | QMessageBox.Discard)
        msg_box.setDefaultButton(QMessageBox.Save)

        ret = msg_box.exec()

        if ret == QMessageBox.Save:
            self.save_project()  # Save the project
            self.cleanup_project()
            return True
        elif ret == QMessageBox.Discard:
            self.cleanup_project()
            return True  # Exit without saving
        else:
            return False  # Cancel the close event

    def cleanup_project(self):
        if self.project:
            self.project.cleanup_temp_file()
            self.project = None
            self.last_action('Cleaned up project')
            self.save_status()

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
            self.save_status()

    def update_metadata(self, row, filename, metadata):
        """
        Slot to receive metadata changes from FileTableModel and update the HDF5 temp file.
        """
        if self.project:
            try:
                # Ensure the file exists in the HDF5 file before updating metadata
                if filename in self.project.h5file:
                    for key, value in metadata.items():
                        if value is None and key in ['chi_angle', 'pinhole', 'power', 'polarization', 'scans',
                                                     'laser_wavelength', 'mirror_spacing', 'scattering_angle']:
                            value = np.nan  # Use np.nan for missing numeric values
                        self.project.add_metadata_to_dataset(filename, key, value)
                    self.last_action('Table modified')
                else:
                    print(f"Warning: Tried to update metadata for non-existent file: {filename}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to update metadata in temp file: {e}")
        self.save_status()

    def pressure_combobox_changed(self):
        """Handle pressure combobox change."""
        self.update_table()
        self.last_action('Pressure changed')
        self.save_status()

    def crystal_combobox_changed(self):
        """Handle crystal combobox change."""
        self.update_table()
        self.last_action('Crystal changed')
        self.save_status()

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
                    self.project.get_metadata_from_dataset(filename, 'laser_wavelength'),
                    self.project.get_metadata_from_dataset(filename, 'mirror_spacing'),
                    self.project.get_metadata_from_dataset(filename, 'scattering_angle'),
                )
                for filename in matching_files
            ]

            self.file_model.addFilesWithMetadata(files_with_metadata)

    def new_project_clicked(self):
        """Handle the new project button click."""
        folder_path, project_name = self.get_project_folder_and_name()
        if folder_path and project_name:
            self.create_new_project(folder_path, project_name)
            self.last_action('New project created')
            if hasattr(self, 'calibration_manager'):
                self.calibration_manager.update_project()
            self.save_status()

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
        self.update_file_count()

    def load_project_clicked(self):
        """Handle the load project button click."""
        filepath = self.get_project_file()
        if filepath:
            self.load_project(filepath)
            self.last_action('Project loaded')
            if hasattr(self, 'calibration_manager'):
                self.calibration_manager.update_project()
            self.save_status()

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
        self.update_file_count()

    def populate_dropdowns(self):
        """Populate pressure and crystal comboboxes with unique values from the project."""
        if self.project:
            unique_pressures, unique_crystals = self.project.get_unique_pressures_and_crystals()

            self.ui.comboBox_pressure.clear()
            self.ui.comboBox_crystal.clear()

            for pressure in unique_pressures:
                self.ui.comboBox_pressure.addItem(str(pressure))
            for crystal in unique_crystals:
                self.ui.comboBox_crystal.addItem(crystal)
            self.save_status()

    def save_project_clicked(self):
        """Handle the save project button click."""
        if self.project:
            self.save_project()
            self.last_action('Project saved')
            self.save_status()

    def save_project(self):
        """Save the current project."""
        try:
            self.save_table_data()
            self.project.save_project()
            self.update_file_count()
            self.save_status()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to save project: {e}")

    def delete_project_clicked(self):
        """Handle the delete project button click."""
        if self.project:
            self.delete_project()
            self.last_action('Project deleted')
            self.save_status()

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
                self.update_file_count()
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to delete project: {e}")

    def rename_project_clicked(self):
        """Handle the rename project text edit finished."""
        if self.project:
            self.rename_project(self.ui.lineEdit_currentProject.text())
            self.last_action('Project renamed')
            self.save_status()

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
                self.save_status()
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to rename project: {e}")

    def new_pressure_clicked(self):
        """Handle the new pressure button click."""
        pressure, ok = QInputDialog.getDouble(None, "New Pressure", "Enter pressure in GPa:", decimals=2)
        if ok:
            self.project.add_pressure(float(pressure))  # Add to project file
            self.populate_table_widgets()  # Update tableWidget
            self.populate_dropdowns()
            self.last_action('Pressure added')
            self.save_status()

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
                self.last_action('Pressure deleted')
                self.save_status()

    def new_crystal_clicked(self):
        """Handle the new crystal button click."""
        crystal_name, ok = QInputDialog.getText(None, "New Crystal", "Enter crystal name:")
        if ok and crystal_name:
            self.project.add_crystal(crystal_name)  # Add to project file
            self.populate_table_widgets()  # Update tableWidget
            self.populate_dropdowns()
            self.last_action('Crystal added')
            self.save_status()

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
                self.last_action('Crystal deleted')
                self.save_status()

    def add_files_clicked(self):
        """Handle the add files button click."""
        pressure = self.ui.comboBox_pressure.currentText()
        crystal_name = self.ui.comboBox_crystal.currentText()

        if pressure and crystal_name:
            self.add_files(float(pressure), crystal_name)
            self.update_file_count()
            self.last_action('Files added')
            self.save_status()

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
        self.update_file_count()
        self.last_action('Files removed')
        self.save_status()

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
            row_count = self.file_model.rowCount() - 1  # Exclude default values row
            if row_count > 0:  # Ensure there are rows to process
                for row in range(1, row_count+1):
                    filename = self.file_model.data(self.file_model.index(row, 0), Qt.DisplayRole)
                    metadata = {
                        'chi_angle': self.file_model.data(self.file_model.index(row, 1), Qt.DisplayRole),
                        'pinhole': self.file_model.data(self.file_model.index(row, 2), Qt.DisplayRole),
                        'power': self.file_model.data(self.file_model.index(row, 3), Qt.DisplayRole),
                        'polarization': self.file_model.data(self.file_model.index(row, 4), Qt.DisplayRole),
                        'scans': self.file_model.data(self.file_model.index(row, 5), Qt.DisplayRole),
                        'laser_wavelength': self.file_model.data(self.file_model.index(row, 6), Qt.DisplayRole),
                        'mirror_spacing': self.file_model.data(self.file_model.index(row, 7), Qt.DisplayRole),
                        'scattering_angle': self.file_model.data(self.file_model.index(row, 8), Qt.DisplayRole),
                    }
                    for key, value in metadata.items():
                        if value is not None:
                            self.project.add_metadata_to_dataset(filename, key, value)


