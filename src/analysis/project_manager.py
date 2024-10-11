# src/analysis/project_manager.py
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QTableWidgetItem, QPlainTextEdit, QVBoxLayout, QWidget

from .brillouin_project import BrillouinProject
import os


class ProjectManager(QObject):
    project_changed = Signal()  # Emit the BrillouinProject instance
    group_changed = Signal(list, list, list)

    def __init__(self, ui):
        super().__init__()
        self.fits_manager = None
        self.calibration_manager = None
        self.ui = ui
        self.project = None
        self.unsaved_changes = False

        # Define columns for the pressures, crystals, and velocities tables
        self.ui.tableWidget_pressures.setColumnCount(1)
        self.ui.tableWidget_pressures.setHorizontalHeaderLabels(["Pressure (GPa)"])

        self.ui.tableWidget_crystals.setColumnCount(1)
        self.ui.tableWidget_crystals.setHorizontalHeaderLabels(["Crystal"])

        self.ui.tableWidget_velocities.setColumnCount(1)
        self.ui.tableWidget_velocities.setHorizontalHeaderLabels(["Velocity"])

        # Connect signals to corresponding slots
        self.setup_connections()

        self.save_status()

    def set_fits_manager(self, calibration_manager):
        self.fits_manager = calibration_manager

    def set_calibration_manager(self, calibration_manager):
        self.calibration_manager = calibration_manager
        # Connect to the calibrations_updated signal
        self.calibration_manager.calibrations_updated.connect(self.update_calibrations)

    def last_action(self, text):
        """Update the last action label."""
        self.ui.label_lastAction.setText(f"| Last action: {text} ")

    def update_calibrations(self):
        # Re-populate the calibration dropdowns
        self.fits_manager.populate_calibration_dropdowns()

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

        # Connect UI buttons to methods
        self.ui.pushButton_newProject.clicked.connect(self.new_project_clicked)
        self.ui.pushButton_loadProject.clicked.connect(self.load_project_clicked)
        self.ui.pushButton_saveProject.clicked.connect(self.save_project_clicked)
        self.ui.pushButton_deleteProject.clicked.connect(self.delete_project_clicked)
        self.ui.pushButton_newPressure.clicked.connect(self.new_pressure_clicked)
        self.ui.pushButton_deletePressure.clicked.connect(self.delete_pressure_clicked)
        self.ui.pushButton_newCrystal.clicked.connect(self.new_crystal_clicked)
        self.ui.pushButton_deleteCrystal.clicked.connect(self.delete_crystal_clicked)
        self.ui.pushButton_newVelocity.clicked.connect(self.new_velocity_clicked)
        self.ui.pushButton_deleteVelocity.clicked.connect(self.delete_velocity_clicked)
        self.ui.pushButton_renameVelocity.clicked.connect(self.rename_velocity_clicked)
        self.ui.lineEdit_currentProject.editingFinished.connect(self.rename_project_clicked)

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

        # Create a scrollable text area for the changes
        text_area = QPlainTextEdit()
        text_area.setPlainText(change_message)
        text_area.setReadOnly(True)
        text_area.setFixedHeight(200)  # Adjust the height as necessary

        # Create a custom layout to include the text area within the QMessageBox
        custom_layout = QVBoxLayout()
        custom_layout.addWidget(text_area)

        # Create a custom widget to contain the layout
        custom_widget = QWidget()
        custom_widget.setLayout(custom_layout)

        msg_box.layout().addWidget(custom_widget, 0, 1, 1, -1)

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
            self.project_changed.emit()

    def populate_table_widgets(self):
        """Populate the pressure, crystal, and velocity tableWidgets with unique values."""
        if self.project:
            pressures, crystals, velocities = self.project.get_unique_pressures_crystals_velocities()

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

            # Populate velocity tableWidget
            self.ui.tableWidget_velocities.setRowCount(0)  # Clear previous entries
            for velocity in velocities:
                row_position = self.ui.tableWidget_velocities.rowCount()
                self.ui.tableWidget_velocities.insertRow(row_position)
                self.ui.tableWidget_velocities.setItem(row_position, 0, QTableWidgetItem(velocity))

            # Emit the signal with the pressures, crystals, and velocities
            self.group_changed.emit(pressures, crystals, velocities)

            self.save_status()

    def new_project_clicked(self):
        """Handle the new project button click."""
        folder_path, project_name = self.get_project_folder_and_name()
        if folder_path and project_name:
            self.create_new_project(folder_path, project_name)
            self.last_action('New project created')
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
        self.project_changed.emit()
        self.populate_table_widgets()  # Populate tables after loading project

    def load_project_clicked(self):
        """Handle the load project button click."""
        filepath = self.get_project_file()
        if filepath:
            self.load_project(filepath)
            self.last_action('Project loaded')
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
        self.project_changed.emit()
        self.populate_table_widgets()  # Populate tables after loading project
        self.update_file_count()

    def save_project_clicked(self):
        """Handle the save project button click."""
        if self.project:
            self.save_project()
            self.last_action('Project saved')
            self.save_status()

    def save_project(self):
        """Save the current project."""
        try:
            self.fits_manager.save_table_data()
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
                self.project_changed.emit()
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
                self.project_changed.emit()
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to rename project: {e}")

    def new_pressure_clicked(self):
        """Handle the new pressure button click."""
        pressure, ok = QInputDialog.getDouble(None, "New Pressure", "Enter pressure in GPa:", decimals=2)
        if ok:
            self.project.add_pressure(float(pressure))  # Add to project file
            self.populate_table_widgets()  # Update tableWidget
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
                self.last_action('Pressure deleted')
                self.save_status()

    def rename_velocity_clicked(self):
        """Handle the rename velocity button click."""
        selected_rows = self.ui.tableWidget_velocities.selectionModel().selectedRows()
        if selected_rows and len(selected_rows) == 1:
            row = selected_rows[0].row()
            old_velocity = self.ui.tableWidget_velocities.item(row, 0).text()
            new_velocity, ok = QInputDialog.getText(None, "Rename Velocity", "Enter new velocity name:",
                                                    text=old_velocity)
            if ok and new_velocity:
                self.rename_velocity(old_velocity, new_velocity)  # Use self.rename_velocity
                self.populate_table_widgets()  # Update tableWidget
                self.last_action('Velocity renamed')
                self.fits_manager.update_peakfits_model_data()
                self.save_status()

    def new_crystal_clicked(self):
        """Handle the new crystal button click."""
        crystal_name, ok = QInputDialog.getText(None, "New Crystal", "Enter crystal name:")
        if ok and crystal_name:
            self.project.add_crystal(crystal_name)  # Add to project file
            self.populate_table_widgets()  # Update tableWidget
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
                self.last_action('Crystal deleted')
                self.save_status()

    def new_velocity_clicked(self):
        """Handle the new velocity button click."""
        velocity_name, ok = QInputDialog.getText(None, "New Velocity", "Enter velocity name:")
        if ok and velocity_name:
            self.add_velocity(velocity_name)
            self.populate_table_widgets()
            self.last_action('Velocity added')
            self.fits_manager.update_peakfits_model_data()
            self.save_status()

    def delete_velocity_clicked(self):
        """Handle the delete velocity button click."""
        selected_rows = self.ui.tableWidget_velocities.selectionModel().selectedRows()
        if selected_rows:
            confirm = QMessageBox.question(None, "Confirm Delete", "Do you want to delete the selected velocity(s)?",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                for row in selected_rows:
                    velocity = self.ui.tableWidget_velocities.item(row.row(), 0).text()
                    self.delete_velocity(velocity)  # Use self.delete_velocity
                self.populate_table_widgets()  # Update tableWidget
                self.last_action('Velocity deleted')
                self.fits_manager.update_peakfits_model_data()
                self.save_status()

    def add_velocity(self, velocity_name):
        self.project.add_velocity(velocity_name)
        # Update velocities under each file
        for filename in self.project.list_datasets():
            self.project.update_file_velocities(filename)
        self.populate_table_widgets()
        self.fits_manager.update_peakfits_model_data()

    def delete_velocity(self, velocity_name):
        self.project.remove_velocity(velocity_name)
        # Update velocities under each file
        for filename in self.project.list_datasets():
            self.project.update_file_velocities(filename)
        self.populate_table_widgets()
        self.fits_manager.update_peakfits_model_data()

    def rename_velocity(self, old_velocity, new_velocity):
        self.project.rename_velocity(old_velocity, new_velocity)
        # Update velocities under each file
        for filename in self.project.list_datasets():
            self.project.update_file_velocities(filename)
        self.populate_table_widgets()
        self.fits_manager.update_peakfits_model_data()
