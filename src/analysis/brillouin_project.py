import h5py
import os
import time
import shutil

class BrillouinProject:
    def __init__(self, filename=None):
        self.filename = filename
        self.project_name = None
        self.h5file = None

    def create_project(self, filepath, project_name):
        """Create a new HDF5 project file."""
        self.filename = filepath
        self.project_name = project_name
        with h5py.File(self.filename, 'w') as f:
            f.attrs['creation_date'] = time.ctime()
            f.attrs['modification_date'] = time.ctime()
            f.attrs['project_name'] = project_name
        self.h5file = h5py.File(self.filename, 'a')

    def load_project(self, filepath):
        """Load an existing HDF5 project file."""
        if os.path.exists(filepath):
            self.filename = filepath
            self.h5file = h5py.File(self.filename, 'a')
            self.project_name = self.h5file.attrs.get('project_name', 'Unnamed Project')
        else:
            raise FileNotFoundError(f"No such file: '{filepath}'")

    def save_project(self):
        """Save changes to the current HDF5 project file."""
        if self.h5file:
            self.h5file.attrs['modification_date'] = time.ctime()
            self.h5file.close()
            self.h5file = h5py.File(self.filename, 'a')

    def delete_project(self):
        """Delete the current project file."""
        if self.h5file:
            self.h5file.close()
        if os.path.exists(self.filename):
            os.remove(self.filename)
            self.filename = None
            self.h5file = None
            self.project_name = None

    def rename_project(self, new_name):
        """Rename the project within the HDF5 file."""
        if self.h5file:
            self.h5file.attrs['project_name'] = new_name
            self.project_name = new_name
            self.save_project()

    def add_pressure(self, pressure_value):
        """Add a new pressure group."""
        pressure_group = f'pressure_{pressure_value}GPa'
        if pressure_group not in self.h5file:
            self.h5file.create_group(pressure_group)
        else:
            raise ValueError(f"Pressure group '{pressure_group}' already exists.")

    def delete_pressure(self, pressure_value):
        """Delete a pressure group."""
        pressure_group = f'pressure_{pressure_value}GPa'
        if pressure_group in self.h5file:
            del self.h5file[pressure_group]
        else:
            raise ValueError(f"Pressure group '{pressure_group}' does not exist.")

    def add_crystal(self, pressure_value, crystal_name):
        """Add a new crystal group under a specific pressure."""
        pressure_group = f'pressure_{pressure_value}GPa'
        if pressure_group in self.h5file:
            crystal_group = f'{pressure_group}/{crystal_name}'
            if crystal_group not in self.h5file:
                self.h5file.create_group(crystal_group)
            else:
                raise ValueError(f"Crystal group '{crystal_group}' already exists.")
        else:
            raise ValueError(f"Pressure group '{pressure_group}' does not exist.")

    def delete_crystal(self, pressure_value, crystal_name):
        """Delete a crystal group."""
        pressure_group = f'pressure_{pressure_value}GPa'
        crystal_group = f'{pressure_group}/{crystal_name}'
        if crystal_group in self.h5file:
            del self.h5file[crystal_group]
        else:
            raise ValueError(f"Crystal group '{crystal_group}' does not exist.")

    def add_files(self, pressure_value, crystal_name, filepaths, metadata):
        """Add .DAT files to a crystal group."""
        pressure_group = f'pressure_{pressure_value}GPa'
        crystal_group = f'{pressure_group}/{crystal_name}'

        if crystal_group in self.h5file:
            for filepath in filepaths:
                filename = os.path.basename(filepath)
                file_group = f'{crystal_group}/{filename}'
                if file_group not in self.h5file:
                    with open(filepath, 'r') as file:
                        data = file.read()
                    data_encoded = data.encode('utf-8')
                    self.h5file.create_dataset(file_group, data=data_encoded)
                    file_metadata_group = f'{file_group}/metadata'
                    for key, value in metadata.items():
                        self.h5file[file_group].attrs[key] = value
                else:
                    raise ValueError(f"File '{filename}' already exists in the project.")
        else:
            raise ValueError(f"Crystal group '{crystal_group}' does not exist.")

    def remove_file(self, pressure_value, crystal_name, filename):
        """Remove a .DAT file from a crystal group."""
        pressure_group = f'pressure_{pressure_value}GPa'
        crystal_group = f'{pressure_group}/{crystal_name}'
        file_group = f'{crystal_group}/{filename}'
        if file_group in self.h5file:
            del self.h5file[file_group]
        else:
            raise ValueError(f"File '{filename}' does not exist in the project.")

    def list_files(self, pressure_value, crystal_name):
        """List all files for a specific pressure and crystal."""
        pressure_group = f'pressure_{pressure_value}GPa'
        crystal_group = f'{pressure_group}/{crystal_name}'
        if crystal_group in self.h5file:
            return list(self.h5file[crystal_group].keys())
        else:
            raise ValueError(f"Crystal group '{crystal_group}' does not exist.")

    def get_file_metadata(self, pressure_value, crystal_name, filename):
        """Get metadata for a specific file."""
        pressure_group = f'pressure_{pressure_value}GPa'
        crystal_group = f'{pressure_group}/{crystal_name}'
        file_group = f'{crystal_group}/{filename}'
        if file_group in self.h5file:
            return dict(self.h5file[file_group].attrs)
        else:
            raise ValueError(f"File '{filename}' does not exist in the project.")

    def rename_file(self, pressure_value, crystal_name, old_filename, new_filename):
        """Rename a file within a crystal group."""
        pressure_group = f'pressure_{pressure_value}GPa'
        crystal_group = f'{pressure_group}/{crystal_name}'
        old_file_group = f'{crystal_group}/{old_filename}'
        new_file_group = f'{crystal_group}/{new_filename}'
        if old_file_group in self.h5file:
            self.h5file.move(old_file_group, new_file_group)
        else:
            raise ValueError(f"File '{old_filename}' does not exist in the project.")

    def close_project(self):
        """Close the HDF5 file."""
        if self.h5file:
            self.h5file.close()
            self.h5file = None
            self.filename = None
            self.project_name = None
