# src/analysis/fit_manager.py
import os

import numpy as np
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QAbstractItemView, QMenu, QApplication, QTableView, QTableWidgetItem, QMessageBox, \
    QFileDialog

from src.analysis.file_table_model import FileTableModel
from src.analysis.peak_fits_table_model import PeakFitsTableModel
from src.utils.checkbox_lineedit_delegate import CheckboxLineEditDelegate
from ..utils.voigt_profile import VoigtFitter


class FitManager(QObject):
    fit_updated = Signal()

    def __init__(self, ui, project_manager):
        super().__init__()
        self.file_model = None
        self.ui = ui
        self.project_manager = project_manager
        self.project = self.project_manager.project

        self.setup()

        self.setup_connections()

        self.save_status()

    def setup(self):
        self.file_model = FileTableModel()
        self.ui.tableView_files.setModel(self.file_model)

        # Allow multiple selection but keep cells editable
        self.ui.tableView_files.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.tableView_files.setSelectionBehavior(QAbstractItemView.SelectItems)

        # Ensure tables are not editable
        self.ui.tableWidget_pressures.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_crystals.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_velocities.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.peak_fits_model = PeakFitsTableModel(project=self.project)
        self.ui.tableView_peakFits.setModel(self.peak_fits_model)

        self.ui.tableView_files.doubleClicked.connect(self.file_double_clicked)

        self.ui.tableView_files.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableView_files.customContextMenuRequested.connect(self.show_context_menu)

        # Enable copy-paste shortcuts in the tableView_files
        self.ui.tableView_files.keyPressEvent = self.table_keyPressEvent

        # Assign the custom delegate to the default values row, excluding 'calibration' (col 1) and 'elastic_peak_ch' (col 3)
        delegate = CheckboxLineEditDelegate(self.ui.tableView_files)
        for col in range(self.file_model.columnCount()):
            if col not in [1, 3]:  # Exclude calibration and elastic_peak_ch columns in the 0th row
                self.ui.tableView_files.setItemDelegateForRow(0, delegate)

    def set_project(self):
        self.project = self.project_manager.project
        self.peak_fits_model.project = self.project
        self.update_all_ui()
        self.peak_fits_model.update_data()

    def update_all_ui(self):
        return

    def update_peakfits_model_data(self):
        self.peak_fits_model.update_data()

    def save_status(self):
        self.project_manager.save_status()

    def populate_calibration_dropdowns(self):
        """Populate calibration comboboxes with unique values from the project."""
        if self.project:
            calibration_names = self.project.list_calibrations()
            self.ui.comboBox_calibration.clear()
            self.ui.comboBox_calibration.addItems(calibration_names)
            # Update the calibration for all files
            default_calibration = self.ui.comboBox_calibration.currentText()
            self.file_model.setCalibrationForAllFiles(default_calibration)
            # Notify the model that data has changed
            self.file_model.layoutChanged.emit()

    def setup_connections(self):
        self.file_model.data_changed_signal.connect(self.update_metadata)
        self.ui.pushButton_addFiles.clicked.connect(self.add_files_clicked)
        self.ui.pushButton_removeFiles.clicked.connect(self.remove_files_clicked)
        # Connect comboboxes
        self.ui.comboBox_pressure.currentIndexChanged.connect(self.pressure_combobox_changed)
        self.ui.comboBox_crystal.currentIndexChanged.connect(self.crystal_combobox_changed)
        # Connect calibration combobox
        self.ui.comboBox_calibration.currentIndexChanged.connect(self.calibration_combobox_changed)

    def file_double_clicked(self, index):
        # Get the filename from the file model
        if index.isValid():
            row = index.row()
            filename = self.file_model.data(self.file_model.index(row, 0), Qt.DisplayRole)
            if filename:
                self.peak_fits_model.set_current_file(filename)
                self.project_manager.last_action(f'Selected file {filename}')
        else:
            self.peak_fits_model.set_current_file(None)

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
            self.project_manager.last_action('Copied')
        elif action == paste_action:
            self.paste_selection()
            self.project_manager.last_action('Pasted')
        elif action == fill_column_action:
            self.fill_column(index)  # Call fill_column method with the selected index
            self.project_manager.last_action('Fill column')

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

        # Do not allow filling the 'Calibration' column
        if column == 1:
            return

        # Fill the entire column with the selected value
        for row in range(self.file_model.rowCount()):
            current_index = self.file_model.index(row, column)
            self.file_model.setData(current_index, value, Qt.EditRole)

    def copy_selection(self):
        selection = self.ui.tableView_files.selectedIndexes()
        if not selection:
            return

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
                # Do not allow pasting into the 'Calibration' column
                if col == 1:
                    continue
                index = self.file_model.index(row, col)
                self.file_model.setData(index, value, Qt.EditRole)

    def table_keyPressEvent(self, event):
        if event.matches(QKeySequence.Copy):
            self.copy_selection()
        elif event.matches(QKeySequence.Paste):
            self.paste_selection()
        else:
            QTableView.keyPressEvent(self.ui.tableView_files, event)

    def update_metadata(self, row, filename, metadata):
        """
        Slot to receive metadata changes from FileTableModel and update the HDF5 temp file.
        """
        if self.project:
            try:
                # Ensure the file exists in the HDF5 file before updating metadata
                if filename in self.project.h5file['data']:
                    for key, value in metadata.items():
                        if key == 'calibration':
                            # Store the calibration name as metadata
                            self.project.add_metadata_to_dataset(filename, key, value)
                            continue
                        if value is None and key in ['chi_angle', 'elastic_peak_ch', 'pinhole', 'power', 'polarization', 'scans']:
                            value = np.nan  # Use np.nan for missing numeric values
                        self.project.add_metadata_to_dataset(filename, key, value)
                    self.project_manager.last_action('Table modified')
                else:
                    print(f"Warning: Tried to update metadata for non-existent file: {filename}")
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to update metadata in temp file: {e}")
        self.save_status()

    def pressure_combobox_changed(self):
        """Handle pressure combobox change."""
        self.update_table()
        self.project_manager.last_action('Pressure changed')
        self.save_status()

    def calibration_combobox_changed(self):
        """Handle calibration combobox change."""
        default_calibration = self.ui.comboBox_calibration.currentText()
        # Update the calibration for all files
        self.file_model.setCalibrationForAllFiles(default_calibration)
        self.save_status()

    def crystal_combobox_changed(self):
        """Handle crystal combobox change."""
        self.update_table()
        self.project_manager.last_action('Crystal changed')
        self.save_status()

    def update_table(self):
        """Update the file table based on selected pressure and crystal."""
        if not self.project:
            return

        selected_pressure = self.ui.comboBox_pressure.currentText()
        selected_crystal = self.ui.comboBox_crystal.currentText()
        default_calibration = self.ui.comboBox_calibration.currentText()

        if selected_pressure and selected_crystal:
            # Clear the table before adding new data
            self.file_model.clear()

            # Use optimized method to find matching files
            matching_files = self.project.find_files_by_pressure_and_crystal(
                float(selected_pressure), selected_crystal
            )

            # Fetch metadata for all matching files in bulk
            metadata_keys = ['chi_angle', 'elastic_peak_ch', 'pinhole', 'power', 'polarization', 'scans']
            metadata_dict = self.project.get_metadata_for_files(matching_files, keys=metadata_keys)

            # Prepare the data to add to the model
            files_with_metadata = [
                (
                    filename,
                    default_calibration,  # Use current calibration
                    metadata_dict[filename].get('chi_angle'),
                    metadata_dict[filename].get('elastic_peak_ch'),
                    metadata_dict[filename].get('pinhole'),
                    metadata_dict[filename].get('power'),
                    metadata_dict[filename].get('polarization'),
                    metadata_dict[filename].get('scans')
                )
                for filename in matching_files
            ]

            # Add files to the model without emitting unnecessary signals
            self.file_model.addFilesWithMetadata(files_with_metadata, default_calibration)
            self.project_manager.last_action('Table updated')
        else:
            # If pressure or crystal is not selected, clear the table
            self.file_model.clear()

    def group_changed(self, pressures, crystals, velocities):
        self.populate_dropdowns(pressures, crystals, velocities)

    def populate_dropdowns(self, pressures, crystals, velocities):
        """Populate pressure, crystal, and calibration comboboxes with unique values from the project."""
        if self.project:
            print('inside project')
            unique_pressures, unique_crystals, unique_velocities = pressures, crystals, velocities

            self.ui.comboBox_pressure.clear()
            self.ui.comboBox_crystal.clear()

            for pressure in unique_pressures:
                self.ui.comboBox_pressure.addItem(str(pressure))
            for crystal in unique_crystals:
                self.ui.comboBox_crystal.addItem(crystal)

            # Populate calibration combobox
            calibration_names = self.project.list_calibrations()
            self.ui.comboBox_calibration.clear()
            self.ui.comboBox_calibration.addItems(calibration_names)

            self.file_model.calibration_options = calibration_names

            # Populate calibration dropdowns
            self.populate_calibration_dropdowns()
            self.save_status()

    def add_files_clicked(self):
        """Handle the add files button click."""
        pressure = self.ui.comboBox_pressure.currentText()
        crystal_name = self.ui.comboBox_crystal.currentText()
        default_calibration = self.ui.comboBox_calibration.currentText()

        if pressure and crystal_name:
            self.add_files(float(pressure), crystal_name, default_calibration)
            self.project_manager.update_file_count()
            self.project_manager.last_action('Files added')
            self.save_status()

    def add_files(self, pressure, crystal_name, default_calibration):
        """Prompt the user to select files and add them to the project."""
        filepaths, _ = QFileDialog.getOpenFileNames(None, "Add Files", "", "Data Files (*.DAT)")
        if filepaths:
            try:
                self.project.load_all_files_with_metadata(filepaths, pressure, crystal_name)
                self.file_model.addFiles(filepaths, default_calibration=default_calibration)
                # Now, for each file, read the data, fit the elastic peak, and save the result
                for filepath in filepaths:
                    filename = os.path.basename(filepath)
                    # Get the data from the project
                    data = self.project.get_dataset_data(filename)
                    if data is not None:
                        # Fit the elastic peak
                        elastic_peak_ch = self.fit_elastic_peak(data)
                        if elastic_peak_ch is not None:
                            # Save the elastic peak channel in the project metadata
                            self.project.add_metadata_to_dataset(filename, 'elastic_peak_ch', elastic_peak_ch)
                            # Update the file model
                            row = self.file_model.getRowByFilename(filename)
                            if row is not None:
                                index = self.file_model.index(row, 3)  # Column 3 is 'Elastic peak Ch'
                                self.file_model.setData(index, str(elastic_peak_ch), Qt.UserRole)
                        else:
                            print(f"Elastic peak fitting failed for {filename}")
                    else:
                        print(f"Failed to get data for {filename}")
                self.peak_fits_model.update_data()
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to add files: {e}")

    def remove_files_clicked(self):
        """Handle the remove files button click."""
        self.remove_files()
        self.project_manager.update_file_count()
        self.project_manager.last_action('Files removed')
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
        pressure = self.ui.comboBox_pressure.currentText()
        crystal_name = self.ui.comboBox_crystal.currentText()
        if self.project and pressure and crystal_name:
            row_count = self.file_model.rowCount() - 1
            if row_count > 0:
                filenames = []
                metadata_list = []
                for row in range(1, row_count + 1):
                    filename = self.file_model.data(self.file_model.index(row, 0), Qt.DisplayRole)
                    metadata = {
                        'calibration': self.file_model.data(self.file_model.index(row, 1), Qt.DisplayRole),
                        'chi_angle': self.file_model.data(self.file_model.index(row, 2), Qt.DisplayRole),
                        'elastic_peak_ch': self.file_model.data(self.file_model.index(row, 3), Qt.DisplayRole),
                        'pinhole': self.file_model.data(self.file_model.index(row, 4), Qt.DisplayRole),
                        'power': self.file_model.data(self.file_model.index(row, 5), Qt.DisplayRole),
                        'polarization': self.file_model.data(self.file_model.index(row, 6), Qt.DisplayRole),
                        'scans': self.file_model.data(self.file_model.index(row, 7), Qt.DisplayRole)
                    }
                    filenames.append(filename)
                    metadata_list.append(metadata)
                self.project.set_metadata_for_multiple_files(filenames, metadata_list)

    def fit_elastic_peak(self, data):
        """Fit the central elastic peak in the data and return the peak center."""
        num_channels = len(data)
        print('num_channels: ', num_channels)
        # Determine central channel
        central_channel = num_channels // 2
        print('central_channel: ', central_channel)
        # Determine fit range (±8% of total channels)
        delta = int(0.08 * num_channels)
        print('delta: ', delta)
        start = max(0, central_channel - delta)
        print('start: ', start)
        end = min(num_channels, central_channel + delta)
        print('send: ', end)
        x = np.arange(start, end)
        y = data[start:end]
        print('x: ', x)
        print('y: ', y)
        # Decide if we need to invert the data
        inverted=False
        # Initialize the fitter
        fitter = VoigtFitter(inverted=inverted, fit_baseline=True)
        try:
            # Perform the fit
            fitter.fit(x, y)
            # Check goodness of fit
            gof = fitter.goodness_of_fit()
            print('gof: ', gof)
            threshold = 0.8  # Define an acceptable threshold
            if gof >= threshold:
                # Get peak center
                peak_center = fitter.get_parameter('center')
                print('peak_center: ', peak_center)
                return peak_center
            else:
                return None
        except Exception as e:
            print(f"Fit failed: {e}")
            return None