import h5py
import os
import time
import shutil


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
        add_file_to_h5(file_path): Adds the contents of a .dat file to the HDF5 file.
        add_metadata_to_dataset(dataset_name, key, value): Adds metadata to a specific dataset.
        add_array_to_dataset(dataset_name, array_name, array_data): Adds a new array to a specific dataset.
        get_metadata_from_dataset(dataset_name, key): Retrieves metadata from a specific dataset.
        find_datasets_by_metadata(key, value): Finds datasets matching a specific metadata key-value pair.
        find_datasets_by_metadata_dict(metadata_dict): Finds datasets matching multiple metadata key-value pairs.
        remove_dataset(dataset_name): Removes a dataset and all its subgroups from the HDF5 file.
        load_all_files(file_paths): Adds multiple .DAT files to the HDF5 file.
        save_project(): Saves the HDF5 file and updates the modification date.
        check_unsaved_changes(detailed=False): Checks if there are unsaved changes in the HDF5 file.
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

    def create_h5file(self):
        """
        Creates a new HDF5 file in the specified folder with the project name and initializes a temporary HDF5 file.
        """
        # Create the original HDF5 file
        with h5py.File(self.h5file_path, 'w') as h5file:
            h5file.attrs['creation_date'] = time.ctime()
            h5file.attrs['modification_date'] = time.ctime()
            h5file.attrs['project_name'] = self.project_name

        # Initialize the temporary HDF5 file
        self.h5file = h5py.File(self.temp_h5file_path, 'w')
        self.h5file.attrs['creation_date'] = time.ctime()
        self._update_modification_date()
        self.h5file.attrs['project_name'] = self.project_name

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

    def add_file_to_h5(self, file_path):
        """
        Adds the contents of a single .dat file to the temporary HDF5 file.

        Parameters:
            file_path (str): The full path to the .dat file to be added.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        dataset_name = os.path.basename(file_path)

        if dataset_name in self.h5file:
            print(f"Dataset {dataset_name} already exists in the HDF5 file. Skipping.")
            return

        with open(file_path, 'rb') as file:
            raw_data = file.read()

        group = self.h5file.create_group(dataset_name)
        group.create_dataset('raw_content', data=raw_data)

        with open(file_path, 'r') as file:
            lines = file.readlines()
            numeric_data = [int(line.strip()) for line in lines[12:] if line.strip().isdigit()]

        group.create_dataset('original_data', data=numeric_data)

    def add_metadata_to_dataset(self, dataset_name, key, value):
        """
        Adds a key-value pair as metadata to a specific dataset within the temporary HDF5 file.

        Parameters:
            dataset_name (str): The name of the dataset to which the metadata will be added.
            key (str): The metadata key.
            value (Any): The metadata value.

        Raises:
            ValueError: If the temporary HDF5 file is not open or the dataset does not exist.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        if dataset_name not in self.h5file:
            raise ValueError(f"Dataset {dataset_name} does not exist in the HDF5 file.")

        group = self.h5file[dataset_name]
        group.attrs[key] = value

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

        if dataset_name not in self.h5file:
            raise ValueError(f"Dataset {dataset_name} does not exist in the HDF5 file.")

        group = self.h5file[dataset_name]
        group.create_dataset(array_name, data=array_data)

    def get_metadata_from_dataset(self, dataset_name, key):
        """
        Retrieves the value of a specific metadata key from a given dataset in the temporary HDF5 file.

        Parameters:
            dataset_name (str): The name of the dataset from which to retrieve the metadata.
            key (str): The metadata key to retrieve.

        Returns:
            The value associated with the metadata key.

        Raises:
            ValueError: If the temporary HDF5 file is not open or the dataset does not exist.
            KeyError: If the specified key does not exist in the dataset's metadata.
        """
        if self.h5file is None:
            raise ValueError(
                "Temporary HDF5 file not created or opened. Please call create_h5file or load_h5file first.")

        if dataset_name not in self.h5file:
            raise ValueError(f"Dataset {dataset_name} does not exist in the HDF5 file.")

        group = self.h5file[dataset_name]

        if key not in group.attrs:
            raise KeyError(f"Key '{key}' not found in dataset '{dataset_name}'.")

        return group.attrs[key]

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
        for dataset_name in self.h5file.keys():
            group = self.h5file[dataset_name]
            if key in group.attrs and group.attrs[key] == value:
                matching_datasets.append(dataset_name)

        return matching_datasets

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
        for dataset_name in self.h5file.keys():
            group = self.h5file[dataset_name]
            match = all(group.attrs.get(key) == value for key, value in metadata_dict.items())
            if match:
                matching_datasets.append(dataset_name)

        return matching_datasets

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

        if dataset_name not in self.h5file:
            raise ValueError(f"Dataset {dataset_name} does not exist in the HDF5 file.")

        del self.h5file[dataset_name]
        print(f"Dataset {dataset_name} has been removed from the HDF5 file.")

    def load_all_files(self, file_paths):
        """
        Adds all provided .DAT file paths to the temporary HDF5 file.

        Parameters:
            file_paths (list of str): A list of file paths to .DAT files to be added.
        """
        for file_path in file_paths:
            self.add_file_to_h5(file_path)

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
                # Copy attributes
                for key, value in temp_file.attrs.items():
                    orig_file.attrs[key] = value

                # Copy datasets and groups
                def copy_items(source, target):
                    for key in source.keys():
                        if isinstance(source[key], h5py.Group):
                            new_group = target.create_group(key)
                            copy_items(source[key], new_group)
                        else:
                            target.create_dataset(key, data=source[key])

                copy_items(temp_file, orig_file)

        else:
            print("No open temporary HDF5 file to save.")

    def check_unsaved_changes(self, detailed=False):
        """
        Checks if there are unsaved changes in the temporary HDF5 file.

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
            # Compare group and dataset keys
            file1_keys = set(file1.keys())
            file2_keys = set(file2.keys())

            differences["added"] = list(file1_keys - file2_keys)
            differences["removed"] = list(file2_keys - file1_keys)

            common_keys = file1_keys & file2_keys

            for key in common_keys:
                group1 = file1[key]
                group2 = file2[key]

                # Compare attributes
                if group1.attrs.items() != group2.attrs.items():
                    differences["altered"].append(key)

                # Compare datasets (by shape and content)
                if isinstance(group1, h5py.Dataset) and isinstance(group2, h5py.Dataset):
                    if group1.shape != group2.shape or not (group1[()] == group2[()]).all():
                        differences["altered"].append(key)

        return differences

if __name__ == '__main__':
    # Usage
    folder = r"E:\BrillouinAnalyzer\BrillouinAnalyzer\my_data\project"
    project_name = "CTGS_Project"

    brillouin_project = BrillouinProject(folder, project_name)
    brillouin_project.create_h5file()

    # Add files individually or in bulk
    single_file = r"E:\BrillouinAnalyzer\BrillouinAnalyzer\my_data\CTGS_P0\CTGS_X1_0deg_ph200_pw100_pol0_3997.DAT"
    brillouin_project.add_file_to_h5(single_file)

    single_file = r"E:\BrillouinAnalyzer\BrillouinAnalyzer\my_data\CTGS_P0\CTGS_X1_0deg_ph200_pw100_pol0_77978.DAT"
    brillouin_project.add_file_to_h5(single_file)

    # Add metadata to a specific dataset
    brillouin_project.add_metadata_to_dataset("CTGS_X1_0deg_ph200_pw100_pol0_3997.DAT", "pressure", 1.1)
    brillouin_project.add_metadata_to_dataset("CTGS_X1_0deg_ph200_pw100_pol0_3997.DAT", "crystal", 'X1')

    brillouin_project.add_metadata_to_dataset("CTGS_X1_0deg_ph200_pw100_pol0_77978.DAT", "pressure", 1.1)
    brillouin_project.add_metadata_to_dataset("CTGS_X1_0deg_ph200_pw100_pol0_77978.DAT", "crystal", 'X1')

    # Search for datasets that match multiple key-value pairs
    search_criteria = {"pressure": 1.1, "crystal": 'X1'}
    matching_datasets = brillouin_project.find_datasets_by_metadata_dict(search_criteria)
    print(f"Datasets matching {search_criteria}: {matching_datasets}")

    # Save the project (close the HDF5 file)
    brillouin_project.save_project()
