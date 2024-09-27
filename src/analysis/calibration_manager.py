# calibration_manager.py
import numpy as np
from PySide6.QtCore import Qt, QItemSelectionModel
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog
from .calibration_file_table_model import CalibrationFileTableModel
from .calibration_plot_widget import CalibrationPlotWidget
from ..utils.brillouin_calibration import BrillouinCalibration

class CalibrationManager:
    def __init__(self, ui, project_manager):
        self.ui = ui
        self.project_manager = project_manager  # Reference to ProjectManager
        self.project = project_manager.project  # Access the project instance

        # Initialize the CalibrationPlotWidget
        self.calibration_plot_widget = CalibrationPlotWidget(self.ui.calib_plotWidget, self.ui, self)

        # Create an instance of the calibration file model
        self.calib_files_model = CalibrationFileTableModel()
        self.ui.tableView_calibFiles.setModel(self.calib_files_model)

        # Connect signals to corresponding slots
        self.setup_connections()

        # Connect model signals to update stats
        self.calib_files_model.dataChanged.connect(self.update_calibration_stats)
        self.calib_files_model.rowsInserted.connect(self.update_calibration_stats)
        self.calib_files_model.rowsRemoved.connect(self.update_calibration_stats)
        self.calib_files_model.modelReset.connect(self.update_calibration_stats)

    def setup_connections(self):
        # Calibration tab connections
        self.ui.pushButton_calibNewCalib.clicked.connect(self.calib_new_calibration_clicked)
        self.ui.pushButton_calibRenameCalib.clicked.connect(self.calib_rename_calibration_clicked)
        self.ui.pushButton_calibRemoveCalib.clicked.connect(self.calib_remove_calibration_clicked)
        self.ui.comboBox_calibSelect.currentIndexChanged.connect(self.calib_select_changed)
        self.ui.lineEdit_calibLaserWavelength.editingFinished.connect(self.calib_laser_wavelength_changed)
        self.ui.lineEdit_calibMirrorSpacing.editingFinished.connect(self.calib_mirror_spacing_changed)
        self.ui.lineEdit_calibScatteringAngle.editingFinished.connect(self.calib_scattering_angle_changed)
        self.ui.pushButton_calibAddFiles.clicked.connect(self.calib_add_files_clicked)
        self.ui.pushButton_calibRemoveFiles.clicked.connect(self.calib_remove_files_clicked)
        self.ui.tableView_calibFiles.doubleClicked.connect(self.calib_file_double_clicked)
        self.ui.pushButton_calibDeleteLeftPeak.clicked.connect(self.calibration_plot_widget.delete_left_peak)
        self.ui.pushButton_calibDeleteRightPeak.clicked.connect(self.calibration_plot_widget.delete_right_peak)
        self.ui.pushButton_calibSaveCalib.clicked.connect(self.save_current_calibration)

    def update_calibration_stats(self):
        nm_values = self.calib_files_model.get_nm_per_channel_values()
        ghz_values = self.calib_files_model.get_ghz_per_channel_values()

        if len(nm_values) >= 2:
            nm_avg = np.mean(nm_values)
            nm_std = np.std(nm_values, ddof=1)
            self.ui.label_calibStatsNM.setText(f"{nm_avg:.6f} ± {nm_std:.6f}")
        else:
            self.ui.label_calibStatsNM.setText("")

        if len(ghz_values) >= 2:
            ghz_avg = np.mean(ghz_values)
            ghz_std = np.std(ghz_values, ddof=1)
            self.ui.label_calibStatsGHz.setText(f"{ghz_avg:.6f} ± {ghz_std:.6f}")
        else:
            self.ui.label_calibStatsGHz.setText("")

    def attempt_calculate_calibration_constants(self, filename):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            # Get left and right peak fits
            left_peak_fit = self.project.get_peak_fit(calibration_name, filename, 'left')
            right_peak_fit = self.project.get_peak_fit(calibration_name, filename, 'right')
            # Check if centers are valid
            if left_peak_fit and 'center' in left_peak_fit and not np.isnan(left_peak_fit['center']) and \
               right_peak_fit and 'center' in right_peak_fit and not np.isnan(right_peak_fit['center']):
                # Get calibration parameters
                laser_wavelength_text = self.ui.lineEdit_calibLaserWavelength.text()
                mirror_spacing_text = self.ui.lineEdit_calibMirrorSpacing.text()
                scattering_angle_text = self.ui.lineEdit_calibScatteringAngle.text()
                if laser_wavelength_text and mirror_spacing_text and scattering_angle_text:
                    try:
                        laser_wavelength = float(laser_wavelength_text)
                        mirror_spacing = float(mirror_spacing_text)
                        scattering_angle = float(scattering_angle_text)
                        # Perform calculation
                        calibration = BrillouinCalibration()
                        calibration.set_parameters(laser_wavelength, mirror_spacing, scattering_angle)
                        x1 = left_peak_fit['center']
                        x2 = right_peak_fit['center']
                        calibration.set_peak_positions(x1, x2)
                        calibration.calculate()
                        results = calibration.get_results()
                        nm_per_channel = results['nm_per_channel']
                        ghz_per_channel = results['ghz_per_channel']
                        # Update the table model
                        self.calib_files_model.update_calibration_constants(filename, nm_per_channel, ghz_per_channel)
                        # Update the calibration file data in the project
                        self.project.update_calibration_file_data(
                            calibration_name,
                            filename,
                            nm_per_channel=nm_per_channel,
                            ghz_per_channel=ghz_per_channel
                        )
                    except ValueError as e:
                        print(f"Error in calibration calculation: {e}")
                else:
                    print("Calibration parameters not set")
            else:
                print("Both peaks are not fitted")


    def save_current_calibration(self):
        if not self.project:
            QMessageBox.warning(None, "No Project", "Please create or load a project first.")
            return

        calibration_name = self.ui.comboBox_calibSelect.currentText()
        if not calibration_name:
            QMessageBox.warning(None, "No Calibration Selected", "Please select a calibration.")
            return

        # Get calibration parameters
        laser_wavelength_text = self.ui.lineEdit_calibLaserWavelength.text()
        mirror_spacing_text = self.ui.lineEdit_calibMirrorSpacing.text()
        scattering_angle_text = self.ui.lineEdit_calibScatteringAngle.text()

        # Convert to floats, or np.nan if empty
        laser_wavelength = float(laser_wavelength_text) if laser_wavelength_text else np.nan
        mirror_spacing = float(mirror_spacing_text) if mirror_spacing_text else np.nan
        scattering_angle = float(scattering_angle_text) if scattering_angle_text else np.nan

        # Update calibration attributes
        self.project.update_calibration_attributes(
            calibration_name,
            laser_wavelength=laser_wavelength,
            mirror_spacing=mirror_spacing,
            scattering_angle=scattering_angle
        )

        # Iterate over files in the calibration
        for row in range(self.calib_files_model.rowCount()):
            filename_index = self.calib_files_model.index(row, 0)
            channels_index = self.calib_files_model.index(row, 1)
            nm_per_channel_index = self.calib_files_model.index(row, 2)
            ghz_per_channel_index = self.calib_files_model.index(row, 3)

            filename = self.calib_files_model.data(filename_index, Qt.DisplayRole)

            channels_text = self.calib_files_model.data(channels_index, Qt.DisplayRole)
            nm_per_channel_text = self.calib_files_model.data(nm_per_channel_index, Qt.DisplayRole)
            ghz_per_channel_text = self.calib_files_model.data(ghz_per_channel_index, Qt.DisplayRole)

            # Convert to float, or np.nan if empty
            channels = float(channels_text) if channels_text else np.nan
            nm_per_channel = float(nm_per_channel_text) if nm_per_channel_text else np.nan
            ghz_per_channel = float(ghz_per_channel_text) if ghz_per_channel_text else np.nan

            # Retrieve peak fits if they have been fitted
            left_peak_fit = self.project.get_peak_fit(calibration_name, filename, 'left')
            right_peak_fit = self.project.get_peak_fit(calibration_name, filename, 'right')

            # Update calibration file data
            self.project.update_calibration_file_data(
                calibration_name,
                filename,
                channels=channels,
                nm_per_channel=nm_per_channel,
                ghz_per_channel=ghz_per_channel,
                left_peak_fit=left_peak_fit,
                right_peak_fit=right_peak_fit
            )

        # Indicate success
        QMessageBox.information(None, "Calibration Saved", f"Calibration '{calibration_name}' has been saved.")
        self.last_action('Calibration saved')
        self.save_status()

    def update_project(self):
        """Update the project instance when it changes in ProjectManager."""
        self.project = self.project_manager.project
        if self.project:
            self.populate_calibration_dropdown()

    def calib_new_calibration_clicked(self):
        if self.project is None:
            QMessageBox.warning(None, "No Project", "Please create or load a project first.")
            return

        calibration_name, ok = QInputDialog.getText(None, "New Calibration", "Enter a calibration name:")
        if ok and calibration_name:
            try:
                # Add the new calibration to the project
                self.project.add_calibration(calibration_name)

                # Populate the dropdown and select the new calibration
                self.populate_calibration_dropdown()
                index = self.ui.comboBox_calibSelect.findText(calibration_name)
                if index >= 0:
                    self.ui.comboBox_calibSelect.setCurrentIndex(index)

                # Clear input fields for calibration parameters
                self.ui.lineEdit_calibLaserWavelength.clear()
                self.ui.lineEdit_calibMirrorSpacing.clear()
                self.ui.lineEdit_calibScatteringAngle.clear()

                # Clear the calibration files table
                self.calib_files_model.clear()
                self.update_calibration_stats()

                # Clear the plot and reset the peak lists
                self.calibration_plot_widget.reset_fits()  # Reset the plot and fit curves
                self.clear_left_peak_list()  # Clear the left peak list widget
                self.clear_right_peak_list()  # Clear the right peak list widget

                # Update status and last action
                self.last_action('Calibration added')
                self.save_status()
            except ValueError as e:
                QMessageBox.warning(None, "Error", str(e))

    def save_peak_fit(self, peak_type, fitter):
        # Get the current calibration and file
        calibration_name = self.ui.comboBox_calibSelect.currentText()
        filename = self.current_calibration_file

        # Prepare the fit parameters, including x_min and x_max
        peak_fit = {
            'center': fitter.get_parameter('center'),
            'amplitude': fitter.get_parameter('amplitude'),
            'sigma': fitter.get_parameter('sigma'),
            'gamma': fitter.get_parameter('gamma'),
            'fwhm': fitter.get_parameter('fwhm'),
            'area': fitter.get_parameter('area'),
            'goodness_of_fit': fitter.goodness_of_fit(),
            'x_min': fitter.x_min,
            'x_max': fitter.x_max,
            'x_fit': fitter.x_fit.tolist(),
            'y_fit': fitter.y_fit.tolist()
            # Note: 'inverted' is saved as a file attribute below
        }

        # Save to the project
        if peak_type == 'left':
            self.project.update_peak_fit(calibration_name, filename, left_peak_fit=peak_fit)
        elif peak_type == 'right':
            self.project.update_peak_fit(calibration_name, filename, right_peak_fit=peak_fit)
        self.last_action(f'{peak_type.capitalize()} peak fitted')
        self.save_status()

        # Save inverted parameter as file attribute
        inverted = fitter.inverted
        self.project.update_calibration_file_data(
            calibration_name,
            filename,
            inverted=inverted
        )

        # Attempt to calculate calibration constants
        self.attempt_calculate_calibration_constants(filename)

    def delete_left_peak_fit(self):
        if self.project and hasattr(self, 'current_calibration_name') and hasattr(self, 'current_calibration_file'):
            self.project.update_peak_fit(self.current_calibration_name, self.current_calibration_file, left_peak_fit={})
            self.ui.listWidget_calibLeftPeak.clear()
            self.last_action('Left peak fit deleted')
            self.save_status()
            self.clear_calibration_constants(self.current_calibration_file)
        else:
            QMessageBox.warning(None, "No File Selected", "Please select a calibration file first.")

    def delete_right_peak_fit(self):
        if self.project and hasattr(self, 'current_calibration_name') and hasattr(self, 'current_calibration_file'):
            self.project.update_peak_fit(self.current_calibration_name, self.current_calibration_file, right_peak_fit={})
            self.ui.listWidget_calibRightPeak.clear()
            self.last_action('Right peak fit deleted')
            self.save_status()
            self.clear_calibration_constants(self.current_calibration_file)
        else:
            QMessageBox.warning(None, "No File Selected", "Please select a calibration file first.")

    def update_left_peak_list(self, fitter):
        self.ui.listWidget_calibLeftPeak.clear()
        params = ['center', 'amplitude', 'sigma', 'gamma', 'fwhm', 'area']
        for param in params:
            value = fitter.get_parameter(param)
            self.ui.listWidget_calibLeftPeak.addItem(f"{param.capitalize()}: {value}")

    def update_right_peak_list(self, fitter):
        self.ui.listWidget_calibRightPeak.clear()
        params = ['center', 'amplitude', 'sigma', 'gamma', 'fwhm', 'area']
        for param in params:
            value = fitter.get_parameter(param)
            self.ui.listWidget_calibRightPeak.addItem(f"{param.capitalize()}: {value}")

    def clear_calibration_constants(self, filename):
        # Update the table model
        self.calib_files_model.clear_calibration_constants(filename)
        # Update the calibration file data in the project
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            self.project.update_calibration_file_data(
                calibration_name,
                filename,
                nm_per_channel=np.nan,
                ghz_per_channel=np.nan
            )

    def clear_left_peak_list(self):
        self.ui.listWidget_calibLeftPeak.clear()

    def clear_right_peak_list(self):
        self.ui.listWidget_calibRightPeak.clear()

    def populate_calibration_dropdown(self):
        if self.project:
            calibrations = self.project.list_calibrations()
            self.ui.comboBox_calibSelect.clear()
            self.ui.comboBox_calibSelect.addItems(calibrations)

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

    def calib_select_changed(self):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            if calibration_name:
                # Get calibration attributes
                attributes = self.project.get_calibration_attributes(calibration_name)
                self.ui.lineEdit_calibLaserWavelength.setText(str(attributes.get('laser_wavelength', '')))
                self.ui.lineEdit_calibMirrorSpacing.setText(str(attributes.get('mirror_spacing', '')))
                self.ui.lineEdit_calibScatteringAngle.setText(str(attributes.get('scattering_angle', '')))

                # Get files in calibration
                files = self.project.list_files_in_calibration(calibration_name)

                # Clear and populate calib_files_model
                self.calib_files_model.clear()
                self.calib_files_model.addFiles(files)

                # Update file data in the model
                for filename in files:
                    data = self.project.get_calibration_file_data(calibration_name, filename)
                    channels = len(data) if data is not None else None

                    # Get attributes from the project
                    file_attributes = self.project.get_calibration_file_attributes(calibration_name, filename)
                    nm_per_channel = file_attributes.get('nm_per_channel', None)
                    ghz_per_channel = file_attributes.get('ghz_per_channel', None)

                    # Update the model
                    self.calib_files_model.update_file_data(filename, channels, nm_per_channel, ghz_per_channel)

                self.last_action('Calibration selected')
                self.save_status()

                # Update stats after loading the calibration
                self.update_calibration_stats()

    def calib_laser_wavelength_changed(self):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            if calibration_name:
                value = self.ui.lineEdit_calibLaserWavelength.text()
                try:
                    laser_wavelength = float(value)
                    self.project.update_calibration_attributes(calibration_name, laser_wavelength=laser_wavelength)
                    self.last_action('Laser wavelength updated')
                    self.save_status()
                    # Recalculate calibration constants for all files
                    files = self.project.list_files_in_calibration(calibration_name)
                    for filename in files:
                        self.attempt_calculate_calibration_constants(filename)
                except ValueError:
                    QMessageBox.warning(None, "Invalid Input", "Please enter a valid number for laser wavelength.")

    def calib_mirror_spacing_changed(self):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            if calibration_name:
                value = self.ui.lineEdit_calibMirrorSpacing.text()
                try:
                    mirror_spacing = float(value)
                    self.project.update_calibration_attributes(calibration_name, mirror_spacing=mirror_spacing)
                    self.last_action('Mirror spacing updated')
                    self.save_status()
                    # Recalculate calibration constants for all files
                    files = self.project.list_files_in_calibration(calibration_name)
                    for filename in files:
                        self.attempt_calculate_calibration_constants(filename)
                except ValueError:
                    QMessageBox.warning(None, "Invalid Input", "Please enter a valid number for mirror spacing.")

    def calib_scattering_angle_changed(self):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            if calibration_name:
                value = self.ui.lineEdit_calibScatteringAngle.text()
                try:
                    scattering_angle = float(value)
                    self.project.update_calibration_attributes(calibration_name, scattering_angle=scattering_angle)
                    self.last_action('Scattering angle updated')
                    self.save_status()
                    # Recalculate calibration constants for all files
                    files = self.project.list_files_in_calibration(calibration_name)
                    for filename in files:
                        self.attempt_calculate_calibration_constants(filename)
                except ValueError:
                    QMessageBox.warning(None, "Invalid Input", "Please enter a valid number for scattering angle.")

    def calib_add_files_clicked(self):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            if calibration_name:
                filepaths, _ = QFileDialog.getOpenFileNames(None, "Add Calibration Files", "", "Data Files (*.DAT)")
                if filepaths:
                    for filepath in filepaths:
                        self.project.add_file_to_calibration(calibration_name, filepath)
                    self.calib_select_changed()  # Refresh the files in the calibration
                    self.last_action('Files added to calibration')
                    self.save_status()

    def calib_remove_files_clicked(self):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            if calibration_name:
                # Get selected files from the table view
                selected_indexes = self.ui.tableView_calibFiles.selectionModel().selectedRows()
                selected_files = [self.calib_files_model.data(index, Qt.DisplayRole) for index in selected_indexes]
                if selected_files:
                    confirm = QMessageBox.question(
                        None, "Confirm Remove", "Are you sure you want to remove the selected files from calibration?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if confirm == QMessageBox.Yes:
                        for filename in selected_files:
                            self.project.remove_file_from_calibration(calibration_name, filename)
                        self.calib_select_changed()  # Refresh the files in the calibration
                        self.last_action('Files removed from calibration')
                        self.save_status()

    def calib_file_double_clicked(self, index):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            if calibration_name:
                filename = self.calib_files_model.data(index, Qt.DisplayRole)
                # Store the current calibration and file
                self.current_calibration_name = calibration_name
                self.current_calibration_file = filename
                # Get the data from the project
                data = self.project.get_calibration_file_data(calibration_name, filename)
                if data is not None:
                    self.current_calibration_data = data

                    # Get inverted parameter
                    inverted = self.project.get_calibration_file_attribute(calibration_name, filename, 'inverted')
                    if not np.isnan(inverted):
                        self.ui.checkBox_calibInvertedPeaks.setChecked(bool(inverted))
                    else:
                        self.ui.checkBox_calibInvertedPeaks.setChecked(False)

                    self.plot_calibration_data(data)
                    self.last_action('Calibration file plotted')

                    # Load saved fits
                    left_peak_fit = self.project.get_peak_fit(calibration_name, filename, 'left')
                    if left_peak_fit and not any(np.any(np.isnan(val)) if isinstance(val, np.ndarray) else np.isnan(val)
                                                 for val in left_peak_fit.values()):
                        self.calibration_plot_widget.load_saved_fit('left', left_peak_fit)
                        self.update_left_peak_list_from_saved_fit(left_peak_fit)
                    else:
                        self.ui.listWidget_calibLeftPeak.clear()

                    right_peak_fit = self.project.get_peak_fit(calibration_name, filename, 'right')
                    if right_peak_fit and not any(
                            np.any(np.isnan(val)) if isinstance(val, np.ndarray) else np.isnan(val)
                            for val in right_peak_fit.values()):
                        self.calibration_plot_widget.load_saved_fit('right', right_peak_fit)
                        self.update_right_peak_list_from_saved_fit(right_peak_fit)
                    else:
                        self.ui.listWidget_calibRightPeak.clear()

    def update_left_peak_list_from_saved_fit(self, peak_fit):
        self.ui.listWidget_calibLeftPeak.clear()
        params = ['center', 'amplitude', 'sigma', 'gamma', 'fwhm', 'area']
        for param in params:
            value = peak_fit.get(param)
            self.ui.listWidget_calibLeftPeak.addItem(f"{param.capitalize()}: {value}")

    def update_right_peak_list_from_saved_fit(self, peak_fit):
        self.ui.listWidget_calibRightPeak.clear()
        params = ['center', 'amplitude', 'sigma', 'gamma', 'fwhm', 'area']
        for param in params:
            value = peak_fit.get(param)
            self.ui.listWidget_calibRightPeak.addItem(f"{param.capitalize()}: {value}")

    def plot_calibration_data(self, data):
        # Store the x and y data for fitting
        self.calib_x_data = np.arange(len(data))
        self.calib_y_data = data
        self.calibration_plot_widget.plot_data(self.calib_x_data, self.calib_y_data)

    def calib_rename_calibration_clicked(self):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            if calibration_name:
                new_name, ok = QInputDialog.getText(None, "Rename Calibration", "Enter new calibration name:")
                if ok and new_name:
                    try:
                        self.project.rename_calibration(calibration_name, new_name)
                        self.populate_calibration_dropdown()
                        index = self.ui.comboBox_calibSelect.findText(new_name)
                        if index >= 0:
                            self.ui.comboBox_calibSelect.setCurrentIndex(index)
                        self.last_action('Calibration renamed')
                        self.save_status()
                    except ValueError as e:
                        QMessageBox.warning(None, "Error", str(e))

    def calib_remove_calibration_clicked(self):
        if self.project:
            calibration_name = self.ui.comboBox_calibSelect.currentText()
            if calibration_name:
                confirm = QMessageBox.question(
                    None, "Confirm Remove", f"Are you sure you want to remove calibration '{calibration_name}'?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if confirm == QMessageBox.Yes:
                    try:
                        self.project.remove_calibration(calibration_name)
                        self.populate_calibration_dropdown()
                        self.ui.lineEdit_calibLaserWavelength.clear()
                        self.ui.lineEdit_calibMirrorSpacing.clear()
                        self.ui.lineEdit_calibScatteringAngle.clear()
                        self.calib_files_model.clear()
                        self.update_calibration_stats()
                        self.last_action('Calibration removed')
                        self.save_status()
                    except ValueError as e:
                        QMessageBox.warning(None, "Error", str(e))
