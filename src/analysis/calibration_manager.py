import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog, QAbstractItemView
from scipy.optimize import curve_fit
from scipy.special import wofz
from .brillouin_project import BrillouinProject
from .calibration_file_table_model import CalibrationFileTableModel
from .calibration_plot_widget import CalibrationPlotWidget

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
        self.ui.pushButton_calibFitLeftPeak.clicked.connect(self.calib_fit_left_peak_clicked)
        self.ui.pushButton_calibFitRightPeak.clicked.connect(self.calib_fit_right_peak_clicked)
        self.ui.pushButton_calibDeleteLeftPeak.clicked.connect(self.calib_delete_left_peak_clicked)
        self.ui.pushButton_calibDeleteRightPeak.clicked.connect(self.calib_delete_right_peak_clicked)

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
                self.project.add_calibration(calibration_name)
                self.populate_calibration_dropdown()
                index = self.ui.comboBox_calibSelect.findText(calibration_name)
                if index >= 0:
                    self.ui.comboBox_calibSelect.setCurrentIndex(index)
                self.ui.lineEdit_calibLaserWavelength.clear()
                self.ui.lineEdit_calibMirrorSpacing.clear()
                self.ui.lineEdit_calibScatteringAngle.clear()
                self.calib_files_model.clear()
                self.last_action('Calibration added')
                self.save_status()
            except ValueError as e:
                QMessageBox.warning(None, "Error", str(e))

    def save_peak_fit(self, peak_type, fitter):
        # Get the current calibration and file
        calibration_name = self.ui.comboBox_calibSelect.currentText()
        filename = self.current_calibration_file

        # Prepare the fit parameters
        peak_fit = {
            'center': fitter.get_parameter('center'),
            'amplitude': fitter.get_parameter('amplitude'),
            'sigma': fitter.get_parameter('sigma'),
            'gamma': fitter.get_parameter('gamma'),
            'fwhm': fitter.get_parameter('fwhm'),
            'area': fitter.get_parameter('area'),
            'goodness_of_fit': fitter.goodness_of_fit()
        }

        # Save to the project
        if peak_type == 'left':
            self.project.update_peak_fit(calibration_name, filename, left_peak_fit=peak_fit)
        elif peak_type == 'right':
            self.project.update_peak_fit(calibration_name, filename, right_peak_fit=peak_fit)

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
                self.last_action('Calibration selected')
                self.save_status()

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
                    self.plot_calibration_data(data)
                    self.last_action('Calibration file plotted')

    def plot_calibration_data(self, data):
        # Optionally, store the x and y data for fitting
        self.calib_x_data = np.arange(len(data))
        self.calib_y_data = data
        self.calibration_plot_widget.plot_data(self.calib_x_data, self.calib_y_data)

    def calib_fit_left_peak_clicked(self):
        if not hasattr(self, 'current_calibration_data'):
            QMessageBox.warning(None, "No Data", "Please select a calibration file and plot it first.")
            return

        data = self.current_calibration_data
        x = np.arange(len(data))
        y = data

        # Assume left peak is in the first half
        x_left = x[:len(x) // 2]
        y_left = y[:len(y) // 2]

        # Implement peak fitting on x_left, y_left
        def voigt(x, amplitude, center, sigma, gamma):
            sigma = max(sigma, 1e-10)
            return amplitude * np.real(wofz(((x - center) + 1j * gamma) / (sigma * np.sqrt(2)))) / (
                        sigma * np.sqrt(2 * np.pi))

        initial_params = [max(y_left), x_left[np.argmax(y_left)], 1.0, 1.0]
        bounds = ([0, x_left[0], 0, 0], [np.inf, x_left[-1], np.inf, np.inf])

        try:
            popt, pcov = curve_fit(voigt, x_left, y_left, p0=initial_params, bounds=bounds)
            amplitude, center, sigma, gamma = popt
            fwhm = 0.5346 * 2 * gamma + np.sqrt(0.2166 * (2 * gamma) ** 2 + (2.355 * sigma) ** 2)
            area = amplitude * fwhm

            # Display fit parameters
            self.ui.listWidget_calibLeftPeak.clear()
            self.ui.listWidget_calibLeftPeak.addItem(f"Center: {center}")
            self.ui.listWidget_calibLeftPeak.addItem(f"Amplitude: {amplitude}")
            self.ui.listWidget_calibLeftPeak.addItem(f"Sigma: {sigma}")
            self.ui.listWidget_calibLeftPeak.addItem(f"Gamma: {gamma}")
            self.ui.listWidget_calibLeftPeak.addItem(f"FWHM: {fwhm}")
            self.ui.listWidget_calibLeftPeak.addItem(f"Area: {area}")

            # Save the fit parameters to the project
            left_peak_fit = {
                'center': center,
                'amplitude': amplitude,
                'sigma': sigma,
                'gamma': gamma,
                'fwhm': fwhm,
                'area': area,
                'goodness_of_fit': np.nan  # Optionally compute this
            }
            self.project.update_peak_fit(self.current_calibration_name, self.current_calibration_file,
                                         left_peak_fit=left_peak_fit)
            self.last_action('Left peak fitted')
            self.save_status()

        except Exception as e:
            QMessageBox.critical(None, "Fitting Error", f"Error fitting left peak: {e}")

    def calib_fit_right_peak_clicked(self):
        if not hasattr(self, 'current_calibration_data'):
            QMessageBox.warning(None, "No Data", "Please select a calibration file and plot it first.")
            return

        data = self.current_calibration_data
        x = np.arange(len(data))
        y = data

        # Assume right peak is in the second half
        x_right = x[len(x) // 2:]
        y_right = y[len(y) // 2:]

        # Implement peak fitting on x_right, y_right
        def voigt(x, amplitude, center, sigma, gamma):
            sigma = max(sigma, 1e-10)
            return amplitude * np.real(wofz(((x - center) + 1j * gamma) / (sigma * np.sqrt(2)))) / (
                        sigma * np.sqrt(2 * np.pi))

        initial_params = [max(y_right), x_right[np.argmax(y_right)], 1.0, 1.0]
        bounds = ([0, x_right[0], 0, 0], [np.inf, x_right[-1], np.inf, np.inf])

        try:
            popt, pcov = curve_fit(voigt, x_right, y_right, p0=initial_params, bounds=bounds)
            amplitude, center, sigma, gamma = popt
            fwhm = 0.5346 * 2 * gamma + np.sqrt(0.2166 * (2 * gamma) ** 2 + (2.355 * sigma) ** 2)
            area = amplitude * fwhm

            # Display fit parameters
            self.ui.listWidget_calibRightPeak.clear()
            self.ui.listWidget_calibRightPeak.addItem(f"Center: {center}")
            self.ui.listWidget_calibRightPeak.addItem(f"Amplitude: {amplitude}")
            self.ui.listWidget_calibRightPeak.addItem(f"Sigma: {sigma}")
            self.ui.listWidget_calibRightPeak.addItem(f"Gamma: {gamma}")
            self.ui.listWidget_calibRightPeak.addItem(f"FWHM: {fwhm}")
            self.ui.listWidget_calibRightPeak.addItem(f"Area: {area}")

            # Save the fit parameters to the project
            right_peak_fit = {
                'center': center,
                'amplitude': amplitude,
                'sigma': sigma,
                'gamma': gamma,
                'fwhm': fwhm,
                'area': area,
                'goodness_of_fit': np.nan  # Optionally compute this
            }
            self.project.update_peak_fit(self.current_calibration_name, self.current_calibration_file,
                                         right_peak_fit=right_peak_fit)
            self.last_action('Right peak fitted')
            self.save_status()

        except Exception as e:
            QMessageBox.critical(None, "Fitting Error", f"Error fitting right peak: {e}")

    def calib_delete_left_peak_clicked(self):
        if self.project:
            if not hasattr(self, 'current_calibration_name') or not hasattr(self, 'current_calibration_file'):
                QMessageBox.warning(None, "No File Selected", "Please select a calibration file first.")
                return
            self.project.update_peak_fit(self.current_calibration_name, self.current_calibration_file, left_peak_fit={})
            self.ui.listWidget_calibLeftPeak.clear()
            self.last_action('Left peak fit deleted')
            self.save_status()

    def calib_delete_right_peak_clicked(self):
        if self.project:
            if not hasattr(self, 'current_calibration_name') or not hasattr(self, 'current_calibration_file'):
                QMessageBox.warning(None, "No File Selected", "Please select a calibration file first.")
                return
            self.project.update_peak_fit(self.current_calibration_name, self.current_calibration_file,
                                         right_peak_fit={})
            self.ui.listWidget_calibRightPeak.clear()
            self.last_action('Right peak fit deleted')
            self.save_status()

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
                        self.last_action('Calibration removed')
                        self.save_status()
                    except ValueError as e:
                        QMessageBox.warning(None, "Error", str(e))