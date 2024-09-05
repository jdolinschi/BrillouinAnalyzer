import unittest
import os
import shutil
import numpy as np
from tempfile import TemporaryDirectory
import sys
import h5py

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/analysis')))

# Now import the BrillouinProject class
from brillouin_project import BrillouinProject

class TestBrillouinProject(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for the test files
        self.test_dir = TemporaryDirectory()
        self.project_name = "test_project"
        self.project = BrillouinProject(folder=self.test_dir.name, project_name=self.project_name)
        self.project.create_h5file()

    def tearDown(self):
        # Clean up the temporary directory after tests
        self.project.h5file.close() if self.project.h5file else None
        self.test_dir.cleanup()

    def test_create_h5file(self):
        # Test the creation of the HDF5 file
        self.assertTrue(os.path.exists(self.project.h5file_path))
        self.assertTrue(os.path.exists(self.project.temp_h5file_path))

    def test_add_file_to_h5(self):
        # Create a mock .dat file to add to the project
        dat_file_path = os.path.join(self.test_dir.name, "test_data.dat")
        with open(dat_file_path, "w") as f:
            f.write("Header line\n" * 12)
            f.write("1\n2\n3\n4\n5\n")

        # Add the file to the HDF5 project
        self.project.add_file_to_h5(dat_file_path)

        # Verify that the dataset was added
        dataset_name = "test_data.dat"
        self.assertIn(dataset_name, self.project.h5file)

        # Verify the data is correctly stored
        group = self.project.h5file[dataset_name]
        original_data = group['original_data'][:]
        self.assertTrue(np.array_equal(original_data, np.array([1, 2, 3, 4, 5])))

    def test_add_metadata_to_dataset(self):
        # Add metadata to a dataset
        dat_file_path = os.path.join(self.test_dir.name, "test_data.dat")
        with open(dat_file_path, "w") as f:
            f.write("Header line\n" * 12)
            f.write("1\n2\n3\n4\n5\n")
        self.project.add_file_to_h5(dat_file_path)
        self.project.add_metadata_to_dataset("test_data.dat", "test_key", "test_value")

        # Verify the metadata was added
        group = self.project.h5file["test_data.dat"]
        self.assertEqual(group.attrs["test_key"], "test_value")

    def test_find_datasets_by_metadata(self):
        # Add multiple datasets with metadata
        dat_file_path_1 = os.path.join(self.test_dir.name, "test_data_1.dat")
        dat_file_path_2 = os.path.join(self.test_dir.name, "test_data_2.dat")

        with open(dat_file_path_1, "w") as f:
            f.write("Header line\n" * 12)
            f.write("1\n2\n3\n4\n5\n")

        with open(dat_file_path_2, "w") as f:
            f.write("Header line\n" * 12)
            f.write("6\n7\n8\n9\n10\n")

        self.project.add_file_to_h5(dat_file_path_1)
        self.project.add_file_to_h5(dat_file_path_2)

        self.project.add_metadata_to_dataset("test_data_1.dat", "type", "calibration")
        self.project.add_metadata_to_dataset("test_data_2.dat", "type", "measurement")

        # Find datasets by metadata
        result = self.project.find_datasets_by_metadata("type", "calibration")
        self.assertIn("test_data_1.dat", result)
        self.assertNotIn("test_data_2.dat", result)

    def test_save_project(self):
        # Add a dataset and save the project
        dat_file_path = os.path.join(self.test_dir.name, "test_data.dat")
        with open(dat_file_path, "w") as f:
            f.write("Header line\n" * 12)
            f.write("1\n2\n3\n4\n5\n")

        self.project.add_file_to_h5(dat_file_path)
        self.project.save_project()

        # Verify the original HDF5 file was updated
        with h5py.File(self.project.h5file_path, 'r') as h5file:
            self.assertIn("test_data.dat", h5file)

    def test_check_unsaved_changes(self):
        # Initialize the HDF5 file properly by creating it first
        self.project.create_h5file()

        # Initially there should be no unsaved changes
        self.assertFalse(self.project.check_unsaved_changes())

        # Add a file and check for unsaved changes
        dat_file_path = os.path.join(self.test_dir.name, "test_data.dat")
        with open(dat_file_path, "w") as f:
            f.write("Header line\n" * 12)
            f.write("1\n2\n3\n4\n5\n")
        self.project.add_file_to_h5(dat_file_path)

        # Now there should be unsaved changes
        self.assertTrue(self.project.check_unsaved_changes())

        # Save the project and check again
        self.project.save_project()
        self.assertFalse(self.project.check_unsaved_changes())


if __name__ == '__main__':
    unittest.main()
