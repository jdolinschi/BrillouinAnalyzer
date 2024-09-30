import h5py
import os
import time
import shutil

import numpy as np


class BrillouinProject:
    """
    A class to manage Brillouin spectroscopy data stored in an HDF5 file.

    Attributes:
        folder (str): The directory where the HDF5 file will be stored.
        project_name (str): The name of the project, used to create the HDF5 file.
        h5file_path (str): The full path to the HDF5 file.
        temp_h5file_path (str): The full path to the temporary HDF5 file.
        h5file (h5py.File or None): The handle to the open temporary HDF5 file.

    Methods:
        create_h5file(): Creates a new HDF5 file in the specified folder.
        load_h5file(): Loads an existing HDF5 file for reading and writing.
        add_calibration(): Adds a new calibration to the project.
        remove_calibration(): Removes an existing calibration from the project.
        update_calibration_attributes(): Updates attributes of a calibration.
        add_file_to_calibration(): Adds a file to a calibration.
        remove_file_from_calibration(): Removes a file from a calibration.
        update_calibration_file_data(): Updates file-level data within a calibration.
        update_peak_fit(): Updates peak fit data for a file within a calibration.
        get_peak_fit(): Retrieves peak fit data for a file within a calibration.
        get_calibration_attributes(): Retrieves attributes of a calibration.
        get_calibration_file_data(): Retrieves data from a file within a calibration.
        list_calibrations(): Lists all calibrations in the project.
        list_files_in_calibration(): Lists all files in a calibration.
        save_project(): Saves the temporary HDF5 file to the main project file.
        check_unsaved_changes(): Checks if there are unsaved changes.
        cleanup_temp_file(): Cleans up the temporary HDF5 file.
        Other methods for managing pressures, crystals, and datasets.
    """

    def __init__(self, folder, project_name):
        """
        Initializes the BrillouinProject object with the folder path and project name.

        Parameters:
            folder (str): The directory where the HDF5 file will be stored.
            project_name (str): The name of the project, used to create the HDF5 file.
        """
        self.folder = folder
        self.project_name = project_name
        self.h5file_path = os.path.join(folder, f"{project_name}.h5")

        # Create a /temp/ directory within the folder if it doesn't exist
        temp_folder = os.path.join(folder, "temp")
        os.makedirs(temp_folder, exist_ok=True)

        self.temp_h5file_path = os.path.join(temp_folder, f"{project_name}_temp.h5")
        self.h5file = None  # Handle to the temporary HDF5 file object, initially set to None

    def _update_modification_date(self):
        """
        Internal method to update the modification date attribute of the temporary HDF5 file.
        """
        if self.h5file is not None:
            self.h5file.attrs['modification_date'] = time.ctime()
            self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def create_h5file(self):
        """
        Creates a new HDF5 file in the specified folder with the project name and initializes a temporary HDF5 file.
        """
        # Create the original HDF5 file
        with h5py.File(self.h5file_path, 'w') as h5file:
            h5file.attrs['creation_date'] = time.ctime()
            h5file.attrs['modification_date'] = time.ctime()
            h5file.attrs['project_name'] = self.project_name
            h5file.create_group('data')  # Create 'data' group

        # Initialize the temporary HDF5 file
        self.h5file = h5py.File(self.temp_h5file_path, 'w')
        self.h5file.attrs['creation_date'] = time.ctime()
        self._update_modification_date()
        self.h5file.attrs['project_name'] = self.project_name
        self.h5file.create_group('data')  # Create 'data' group

    def load_all_files_with_metadata(self, file_paths, pressure, crystal):
        for file_path in file_paths:
            self.add_file_to_h5(file_path, pressure, crystal)

    def load_all_files(self, file_paths):
        """
        Adds all provided .DAT file paths to the temporary HDF5 file.

        Parameters:
            file_paths (list of str): A list of file paths to .DAT files to be added.
        """
        for file_path in file_paths:
            self.add_file_to_h5(file_path)

    def load_h5file(self):
        """
        Loads an existing HDF5 file for reading and writing by copying it to a temporary file.

        Raises:
            FileNotFoundError: If the HDF5 file does not exist at the specified path.
        """
        if not os.path.exists(self.h5file_path):
            raise FileNotFoundError(f"The file {self.h5file_path} does not exist.")

        # Copy the original file to the temporary file
        shutil.copyfile(self.h5file_path, self.temp_h5file_path)
        self.h5file = h5py.File(self.temp_h5file_path, 'a')

        # Ensure 'data' group exists
        if 'data' not in self.h5file:
            self.h5file.create_group('data')

    def add_metadata_to_dataset(self, dataset_name, key, value):
        """
        Adds a key-value pair as metadata to a specific dataset within the temporary HDF5 file.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        data_group = self.h5file['data']

        if dataset_name not in data_group:
            print('Error in add_metadata_to_dataset')
            raise ValueError(f"Dataset {dataset_name} does not exist in the HDF5 file.")

        group = data_group[dataset_name]
        group.attrs[key] = value

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def add_array_to_dataset(self, dataset_name, array_name, array_data):
        """
        Adds a new array to the specified dataset within the temporary HDF5 file.

        Parameters:
            dataset_name (str): The name of the dataset to which the array will be added.
            array_name (str): The name to be given to the new array.
            array_data (array-like): The data to be stored in the new array.

        Raises:
            ValueError: If the temporary HDF5 file is not open or the dataset does not exist.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        data_group = self.h5file['data']

        if dataset_name not in data_group:
            print('Error in add_array_to_dataset')
            raise ValueError(f"Dataset {dataset_name} does not exist in the HDF5 file.")

        group = data_group[dataset_name]
        group.create_dataset(array_name, data=array_data)

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def add_pressure(self, pressure):
        """Add a new pressure to the project."""
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")

        if 'pressures' not in self.h5file.attrs:
            self.h5file.attrs['pressures'] = []

        pressures = list(self.h5file.attrs['pressures'])
        if pressure not in pressures:
            pressures.append(pressure)
            self.h5file.attrs['pressures'] = pressures

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def add_crystal(self, crystal):
        """Add a new crystal to the project."""
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")

        if 'crystals' not in self.h5file.attrs:
            self.h5file.attrs['crystals'] = []

        crystals = list(self.h5file.attrs['crystals'])
        if crystal not in crystals:
            crystals.append(crystal)
            self.h5file.attrs['crystals'] = crystals

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def remove_crystal(self, crystal):
        """Remove an existing crystal from the project."""
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")

        crystals = list(self.h5file.attrs['crystals'])
        if crystal in crystals:
            crystals.remove(crystal)
            self.h5file.attrs['crystals'] = crystals

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def remove_dataset(self, dataset_name):
        """
        Removes a dataset (group) from the temporary HDF5 file.

        Parameters:
            dataset_name (str): The name of the dataset to remove.

        Raises:
            ValueError: If the temporary HDF5 file is not open or the dataset does not exist.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        data_group = self.h5file['data']

        if dataset_name not in data_group:
            print('Error in remove_dataset')
            raise ValueError(f"Dataset {dataset_name} does not exist in the HDF5 file.")

        del data_group[dataset_name]
        print(f"Dataset {dataset_name} has been removed from the HDF5 file.")

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def add_calibration(self, calibration_name, mirror_spacing=np.nan, laser_wavelength=np.nan, scattering_angle=np.nan):
        """
        Adds a new calibration to the project.

        Parameters:
            calibration_name (str): The name of the calibration.
            mirror_spacing (float): The mirror spacing in mm.
            laser_wavelength (float): The laser wavelength in nm.
            scattering_angle (float): The scattering angle in degrees.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")

        if 'calibrations' not in self.h5file:
            self.h5file.create_group('calibrations')

        if calibration_name in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' already exists.")

        calibration_group = self.h5file['calibrations'].create_group(calibration_name)
        calibration_group.attrs['mirror_spacing'] = mirror_spacing
        calibration_group.attrs['laser_wavelength'] = laser_wavelength
        calibration_group.attrs['scattering_angle'] = scattering_angle

        self.h5file.flush()

    def remove_pressure(self, pressure):
        """Remove an existing pressure from the project."""
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")

        pressures = list(self.h5file.attrs['pressures'])
        if pressure in pressures:
            pressures.remove(pressure)
            self.h5file.attrs['pressures'] = pressures

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def remove_calibration(self, calibration_name):
        """
        Removes an existing calibration from the project.

        Parameters:
            calibration_name (str): The name of the calibration to remove.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")

        del self.h5file['calibrations'][calibration_name]
        self.h5file.flush()

    def add_file_to_h5(self, file_path, pressure=np.nan, crystal=''):
        """
        Adds the contents of a single .dat file to the temporary HDF5 file.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        dataset_name = os.path.basename(file_path)

        data_group = self.h5file['data']

        if dataset_name in data_group:
            print(f"Dataset {dataset_name} already exists in the HDF5 file. Skipping.")
            return

        # Create the dataset under 'data' group
        group = data_group.create_group(dataset_name)

        # Use np.nan for numeric fields instead of None
        group.attrs['pressure'] = pressure
        group.attrs['crystal'] = crystal
        group.attrs['chi_angle'] = np.nan
        group.attrs['pinhole'] = np.nan
        group.attrs['power'] = np.nan
        group.attrs['polarization'] = np.nan
        group.attrs['scans'] = np.nan
        group.attrs['laser_wavelength'] = np.nan
        group.attrs['mirror_spacing'] = np.nan
        group.attrs['scattering_angle'] = np.nan

        # Optionally, add the file content
        with open(file_path, 'rb') as file:
            raw_data = file.read()
        group.create_dataset('raw_content', data=raw_data)

        with open(file_path, 'r') as file:
            lines = file.readlines()
            numeric_data = [int(line.strip()) for line in lines[12:] if line.strip().isdigit()]
        group.create_dataset('original_data', data=numeric_data)

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def add_file_to_calibration(self, calibration_name, file_path):
        """
        Adds a file to a calibration.

        Parameters:
            calibration_name (str): The name of the calibration.
            file_path (str): The path to the file to add.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")

        calibration_group = self.h5file['calibrations'][calibration_name]
        dataset_name = os.path.basename(file_path)

        if dataset_name in calibration_group:
            print(f"File {dataset_name} already exists in the calibration. Skipping.")
            return

        with open(file_path, 'rb') as file:
            raw_data = file.read()

        group = calibration_group.create_group(dataset_name)
        group.create_dataset('raw_content', data=raw_data)

        with open(file_path, 'r') as file:
            lines = file.readlines()
            numeric_data = [int(line.strip()) for line in lines[12:] if line.strip().isdigit()]
        group.create_dataset('original_data', data=numeric_data)

        # Initialize empty attributes for the peak fits
        for peak in ['left_peak', 'right_peak']:
            group.attrs[f'{peak}_center'] = np.nan
            group.attrs[f'{peak}_amplitude'] = np.nan
            group.attrs[f'{peak}_sigma'] = np.nan
            group.attrs[f'{peak}_gamma'] = np.nan
            group.attrs[f'{peak}_fwhm'] = np.nan
            group.attrs[f'{peak}_area'] = np.nan
            group.attrs[f'{peak}_goodness_of_fit'] = np.nan
            group.attrs[f'{peak}_x_min'] = np.nan
            group.attrs[f'{peak}_x_max'] = np.nan
            # Initialize empty datasets for x_fit and y_fit
            group.create_dataset(f'{peak}_x_fit', data=np.array([]), maxshape=(None,))
            group.create_dataset(f'{peak}_y_fit', data=np.array([]), maxshape=(None,))

        # Initialize empty calibration ratios
        group.attrs['channels'] = np.nan
        group.attrs['nm_per_channel'] = np.nan
        group.attrs['ghz_per_channel'] = np.nan

        # Initialize inverted attribute
        group.attrs['inverted'] = 1  # Default to 1 (True)

        self.h5file.flush()

    def remove_file_from_calibration(self, calibration_name, file_name):
        """
        Removes a file from a calibration.

        Parameters:
            calibration_name (str): The name of the calibration.
            file_name (str): The name of the file to remove.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")

        calibration_group = self.h5file['calibrations'][calibration_name]

        if file_name in calibration_group:
            del calibration_group[file_name]
            self.h5file.flush()
        else:
            raise ValueError(f"File '{file_name}' does not exist in the calibration.")

    def update_calibration_attributes(self, calibration_name, mirror_spacing=None, laser_wavelength=None, scattering_angle=None):
        """
        Updates attributes of a calibration.

        Parameters:
            calibration_name (str): The name of the calibration.
            mirror_spacing (float): The mirror spacing in mm.
            laser_wavelength (float): The laser wavelength in nm.
            scattering_angle (float): The scattering angle in degrees.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")

        calibration_group = self.h5file['calibrations'][calibration_name]

        if mirror_spacing is not None:
            calibration_group.attrs['mirror_spacing'] = mirror_spacing
        if laser_wavelength is not None:
            calibration_group.attrs['laser_wavelength'] = laser_wavelength
        if scattering_angle is not None:
            calibration_group.attrs['scattering_angle'] = scattering_angle

        self.h5file.flush()

    def update_calibration_file_data(self, calibration_name, file_name, **attributes):
        """
        Updates file-level data within a calibration, including calibration ratios and peak fits.

        Parameters:
            calibration_name (str): The name of the calibration.
            file_name (str): The name of the file within the calibration.
            **attributes: Arbitrary keyword arguments representing attributes to update.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")
        calibration_group = self.h5file['calibrations'][calibration_name]
        if file_name not in calibration_group:
            raise ValueError(f"File '{file_name}' does not exist in calibration '{calibration_name}'.")

        group = calibration_group[file_name]

        # Update attributes
        for attr_name, attr_value in attributes.items():
            if attr_name in ['left_peak_fit', 'right_peak_fit']:
                continue  # Handle peak fits separately
            group.attrs[attr_name] = attr_value

        # Update peak fits if provided
        if 'left_peak_fit' in attributes:
            left_peak_fit = attributes['left_peak_fit']
            if left_peak_fit is not None:
                self.update_peak_fit(calibration_name, file_name, left_peak_fit=left_peak_fit)

        if 'right_peak_fit' in attributes:
            right_peak_fit = attributes['right_peak_fit']
            if right_peak_fit is not None:
                self.update_peak_fit(calibration_name, file_name, right_peak_fit=right_peak_fit)

        self.h5file.flush()

    def update_peak_fit(self, calibration_name, file_name, left_peak_fit=None, right_peak_fit=None):
        """
        Updates peak fit data for a file within a calibration.

        Parameters:
            calibration_name (str): The name of the calibration.
            file_name (str): The name of the file within the calibration.
            left_peak_fit (dict): The left peak fit parameters.
            right_peak_fit (dict): The right peak fit parameters.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")

        calibration_group = self.h5file['calibrations'][calibration_name]

        if file_name not in calibration_group:
            raise ValueError(f"File '{file_name}' does not exist in the calibration.")

        group = calibration_group[file_name]

        if left_peak_fit is not None:
            for key, value in left_peak_fit.items():
                if key in ['x_fit', 'y_fit']:
                    # Save x_fit and y_fit as datasets
                    dataset_name = f'left_peak_{key}'
                    if dataset_name in group:
                        del group[dataset_name]  # Delete existing dataset if it exists
                    group.create_dataset(dataset_name, data=np.array(value))  # Save as numpy array
                else:
                    group.attrs[f'left_peak_{key}'] = value  # Scalar attributes

        if right_peak_fit is not None:
            for key, value in right_peak_fit.items():
                if key in ['x_fit', 'y_fit']:
                    # Save x_fit and y_fit as datasets
                    dataset_name = f'right_peak_{key}'
                    if dataset_name in group:
                        del group[dataset_name]  # Delete existing dataset if it exists
                    group.create_dataset(dataset_name, data=np.array(value))  # Save as numpy array
                else:
                    group.attrs[f'right_peak_{key}'] = value  # Scalar attributes

        self.h5file.flush()

    def get_metadata_from_dataset(self, dataset_name, key):
        """
        Retrieves the value of a specific metadata key from a given dataset in the temporary HDF5 file.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        data_group = self.h5file['data']

        if dataset_name not in data_group:
            print('Error in get_metadata_from_dataset')
            raise ValueError(f"Dataset {dataset_name} does not exist in the HDF5 file.")

        group = data_group[dataset_name]

        value = group.attrs[key]

        # Replace np.nan with None for display purposes
        if isinstance(value, float) and np.isnan(value):
            return None
        return value

    def get_file_count(self):
        """Return the number of files in the project."""
        data_group = self.h5file['data']
        return len(data_group.keys())

    def get_unique_pressures_and_crystals(self):
        """Return the unique pressures and crystals."""
        pressures = self.h5file.attrs.get('pressures', [])
        crystals = self.h5file.attrs.get('crystals', [])
        return sorted(pressures), sorted(crystals)

    def get_peak_fit(self, calibration_name, file_name, peak_type):
        """
        Retrieves peak fit data for a file within a calibration.

        Parameters:
            calibration_name (str): The name of the calibration.
            file_name (str): The name of the file within the calibration.
            peak_type (str): 'left' or 'right' indicating which peak fit to retrieve.

        Returns:
            dict: A dictionary containing the peak fit parameters.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")

        calibration_group = self.h5file['calibrations'][calibration_name]

        if file_name not in calibration_group:
            raise ValueError(f"File '{file_name}' does not exist in the calibration.")

        group = calibration_group[file_name]

        # Initialize an empty dictionary to store peak fit parameters
        peak_fit = {}

        # Retrieve attributes (center, amplitude, sigma, gamma, fwhm, area, goodness_of_fit, etc.)
        params = ['center', 'amplitude', 'sigma', 'gamma', 'fwhm', 'area', 'goodness_of_fit', 'x_min', 'x_max']
        for param in params:
            attr_name = f'{peak_type}_peak_{param}'
            if attr_name in group.attrs:
                peak_fit[param] = group.attrs[attr_name]
            else:
                peak_fit[param] = np.nan  # Default to NaN if the attribute does not exist

        # Retrieve x_fit and y_fit datasets if they exist
        x_fit_name = f'{peak_type}_peak_x_fit'
        y_fit_name = f'{peak_type}_peak_y_fit'

        if x_fit_name in group:
            peak_fit['x_fit'] = group[x_fit_name][()]  # Load as a numpy array
        else:
            peak_fit['x_fit'] = np.array([])  # Default to empty array if dataset does not exist

        if y_fit_name in group:
            peak_fit['y_fit'] = group[y_fit_name][()]  # Load as a numpy array
        else:
            peak_fit['y_fit'] = np.array([])  # Default to empty array if dataset does not exist

        return peak_fit

    def add_velocity(self, velocity):
        """Add a new velocity to the project."""
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")

        if 'velocities' not in self.h5file.attrs:
            self.h5file.attrs['velocities'] = []

        velocities = list(self.h5file.attrs['velocities'])
        if velocity not in velocities:
            velocities.append(velocity)
            self.h5file.attrs['velocities'] = velocities

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def remove_velocity(self, velocity):
        """Remove an existing velocity from the project."""
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")

        velocities = list(self.h5file.attrs['velocities'])
        if velocity in velocities:
            velocities.remove(velocity)
            self.h5file.attrs['velocities'] = velocities

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def rename_velocity(self, old_velocity, new_velocity):
        """Rename an existing velocity in the project."""
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")

        velocities = list(self.h5file.attrs['velocities'])
        if old_velocity in velocities:
            velocities[velocities.index(old_velocity)] = new_velocity
            self.h5file.attrs['velocities'] = velocities

        self.h5file.flush()  # Ensure that the temporary file is immediately updated.

    def get_unique_pressures_crystals_velocities(self):
        """Return the unique pressures, crystals, and velocities."""
        pressures = self.h5file.attrs.get('pressures', [])
        crystals = self.h5file.attrs.get('crystals', [])
        velocities = self.h5file.attrs.get('velocities', [])
        return sorted(pressures), sorted(crystals), sorted(velocities)

    def get_calibration_attributes(self, calibration_name):
        """
        Retrieves attributes of a calibration.

        Parameters:
            calibration_name (str): The name of the calibration.

        Returns:
            dict: A dictionary containing the calibration attributes.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")

        calibration_group = self.h5file['calibrations'][calibration_name]
        attributes = {
            'mirror_spacing': calibration_group.attrs.get('mirror_spacing', np.nan),
            'laser_wavelength': calibration_group.attrs.get('laser_wavelength', np.nan),
            'scattering_angle': calibration_group.attrs.get('scattering_angle', np.nan)
        }
        return attributes

    def get_calibration_file_data(self, calibration_name, file_name):
        """
        Retrieves the original data from a file within a calibration.

        Parameters:
            calibration_name (str): The name of the calibration.
            file_name (str): The name of the file within the calibration.

        Returns:
            numpy.ndarray: The original data from the file.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")
        calibration_group = self.h5file['calibrations'][calibration_name]
        if file_name not in calibration_group:
            raise ValueError(f"File '{file_name}' does not exist in the calibration.")
        group = calibration_group[file_name]
        data = group['original_data'][()]
        return data

    def get_calibration_file_attributes(self, calibration_name, file_name):
        """
        Retrieves attributes of a calibration file.

        Parameters:
            calibration_name (str): The name of the calibration.
            file_name (str): The name of the file within the calibration.

        Returns:
            dict: A dictionary containing the file attributes.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")
        calibration_group = self.h5file['calibrations'][calibration_name]
        if file_name not in calibration_group:
            raise ValueError(f"File '{file_name}' does not exist in the calibration.")
        group = calibration_group[file_name]
        attributes = {
            'channels': group.attrs.get('channels', np.nan),
            'nm_per_channel': group.attrs.get('nm_per_channel', np.nan),
            'ghz_per_channel': group.attrs.get('ghz_per_channel', np.nan)
        }
        return attributes

    def get_calibration_file_attribute(self, calibration_name, file_name, attribute_name):
        """
        Retrieves a specific attribute of a calibration file.

        Parameters:
            calibration_name (str): The name of the calibration.
            file_name (str): The name of the file within the calibration.
            attribute_name (str): The name of the attribute to retrieve.

        Returns:
            The value of the attribute, or np.nan if it does not exist.
        """
        if self.h5file is None:
            raise ValueError("Temporary HDF5 file not created or opened.")
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            raise ValueError(f"Calibration '{calibration_name}' does not exist.")
        calibration_group = self.h5file['calibrations'][calibration_name]
        if file_name not in calibration_group:
            raise ValueError(f"File '{file_name}' does not exist in the calibration.")
        group = calibration_group[file_name]
        return group.attrs.get(attribute_name, np.nan)


    def list_calibrations(self):
        """
        Lists all calibrations in the project.

        Returns:
            list: A list of calibration names.
        """
        if self.h5file is None or 'calibrations' not in self.h5file:
            return []
        return list(self.h5file['calibrations'].keys())

    def list_files_in_calibration(self, calibration_name):
        """
        Lists all files within a calibration.

        Parameters:
            calibration_name (str): The name of the calibration.

        Returns:
            list: A list of file names within the calibration.
        """
        if 'calibrations' not in self.h5file or calibration_name not in self.h5file['calibrations']:
            return []
        return list(self.h5file['calibrations'][calibration_name].keys())

    def cleanup_temp_file(self):
        """
        Closes the temporary HDF5 file if it is open and then deletes it.
        """
        try:
            # Close the file if it is open
            if self.h5file is not None and self.h5file.id:
                self.h5file.close()
                self.h5file = None
                print(f"Temporary file {self.temp_h5file_path} has been closed.")

            # Delete the temporary file
            if os.path.exists(self.temp_h5file_path):
                os.remove(self.temp_h5file_path)
                print(f"Temporary file {self.temp_h5file_path} has been deleted.")
            else:
                print(f"Temporary file {self.temp_h5file_path} does not exist.")
        except Exception as e:
            print(f"Error deleting temporary file: {e}")

    def find_datasets_by_metadata_dict(self, metadata_dict):
        """
        Finds and returns the names of all datasets in the temporary HDF5 file that match all the key-value pairs in the provided dictionary.

        Parameters:
            metadata_dict (dict): A dictionary of key-value pairs to match.

        Returns:
            List[str]: A list of dataset names that match all key-value pairs.

        Raises:
            ValueError: If the temporary HDF5 file is not open.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        matching_datasets = []
        data_group = self.h5file['data']
        for dataset_name in data_group.keys():
            group = data_group[dataset_name]
            match = all(group.attrs.get(key) == value for key, value in metadata_dict.items())
            if match:
                matching_datasets.append(dataset_name)

        return matching_datasets

    def find_datasets_by_metadata(self, key, value):
        """
        Finds and returns the names of all datasets in the temporary HDF5 file that have a specific key-value pair in their metadata.

        Parameters:
            key (str): The metadata key to search for.
            value (Any): The metadata value to match.

        Returns:
            List[str]: A list of dataset names that match the key-value pair.

        Raises:
            ValueError: If the temporary HDF5 file is not open.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        matching_datasets = []
        data_group = self.h5file['data']
        for dataset_name in data_group.keys():
            group = data_group[dataset_name]
            if key in group.attrs and group.attrs[key] == value:
                matching_datasets.append(dataset_name)

        return matching_datasets

    def find_files_by_pressure_and_crystal(self, pressure, crystal):
        matching_files = []
        data_group = self.h5file['data']
        for dataset_name in data_group.keys():
            group = data_group[dataset_name]
            if group.attrs['pressure'] == pressure and group.attrs['crystal'] == crystal:
                matching_files.append(dataset_name)
        return matching_files

    def save_project(self):
        """
        Saves and closes the temporary HDF5 file, updating the modification date,
        and then copies the contents of the temporary file to the original HDF5 file.
        """
        self._update_modification_date()

        if self.h5file is not None:
            self.h5file.flush()  # Ensure everything in memory is written to the temporary file

            # Copy the temporary file contents to the original HDF5 file
            with h5py.File(self.temp_h5file_path, 'r') as temp_file, h5py.File(self.h5file_path, 'w') as orig_file:

                # Copy attributes of the root
                for key, value in temp_file.attrs.items():
                    orig_file.attrs[key] = value

                # Copy datasets, groups, and their attributes
                def copy_items(source, target):
                    for key in source.keys():
                        item = source[key]
                        if isinstance(item, h5py.Group):
                            # Create the group and copy its attributes
                            new_group = target.create_group(key)
                            for attr_key, attr_value in item.attrs.items():
                                new_group.attrs[attr_key] = attr_value
                            copy_items(item, new_group)
                        elif isinstance(item, h5py.Dataset):
                            # Create the dataset and copy its data
                            target.create_dataset(key, data=item[()])
                            # Copy dataset attributes
                            for attr_key, attr_value in item.attrs.items():
                                target[key].attrs[attr_key] = attr_value

                copy_items(temp_file, orig_file)

        else:
            print("No open temporary HDF5 file to save.")

    def check_unsaved_changes(self, detailed=False):
        """
        Checks if there are unsaved changes in the temporary HDF5 file and returns them.

        Parameters:
            detailed (bool): If True, returns a dictionary with details of differences;
                             if False, returns a boolean indicating whether there are unsaved changes.

        Returns:
            bool or dict: If detailed is False, returns a boolean indicating whether there are unsaved changes.
                          If detailed is True, returns a dictionary with keys "added", "removed", "altered" showing the differences.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        # Save the current in-memory version to ensure it is up-to-date
        self.h5file.flush()

        # Compare the temporary file with the on-disk version
        differences = self._compare_h5_files(self.temp_h5file_path, self.h5file_path)

        if detailed:
            return differences
        else:
            return bool(differences["added"] or differences["removed"] or differences["altered"])

    def _compare_h5_files(self, file1_path, file2_path):
        """
        Compares two HDF5 files and returns the differences.

        Parameters:
            file1_path (str): Path to the first HDF5 file (temporary file).
            file2_path (str): Path to the second HDF5 file (original file on disk).

        Returns:
            dict: A dictionary with keys "added", "removed", "altered", each containing lists of differences.
        """
        differences = {"added": [], "removed": [], "altered": []}

        with h5py.File(file1_path, 'r') as file1, h5py.File(file2_path, 'r') as file2:
            def compare_items(name, obj):
                if name not in file2:
                    differences["added"].append(name)
                else:
                    if isinstance(obj, h5py.Group):
                        for attr_key in obj.attrs:
                            if attr_key not in file2[name].attrs or obj.attrs[attr_key] != file2[name].attrs[attr_key]:
                                differences["altered"].append(name + " attribute " + attr_key)
                        for sub_name in obj:
                            compare_items(name + '/' + sub_name, obj[sub_name])
                    elif isinstance(obj, h5py.Dataset):
                        if not np.array_equal(obj[()], file2[name][()]):
                            differences["altered"].append(name)

            def compare_removed(name, obj):
                if name not in file1:
                    differences["removed"].append(name)
                else:
                    if isinstance(obj, h5py.Group):
                        for sub_name in obj:
                            compare_removed(name + '/' + sub_name, obj[sub_name])

            for item in file1:
                compare_items(item, file1[item])

            for item in file2:
                compare_removed(item, file2[item])

        return differences

    def list_datasets(self):
        """
        Lists all datasets in the 'data' group of the project.

        Returns:
            list: A list of dataset names.
        """
        if self.h5file is None or 'data' not in self.h5file:
            return []
        return list(self.h5file['data'].keys())