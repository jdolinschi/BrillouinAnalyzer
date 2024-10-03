# In peak_fits_table_model.py

from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
import numpy as np

class PeakFitsTableModel(QAbstractTableModel):
    def __init__(self, project=None, parent=None):
        super(PeakFitsTableModel, self).__init__(parent)
        self.project = project
        self._headers = [
            'Name',
            'Left Center (m/s)',
            'Right Center (m/s)',
            'Offset (m/s)',
            'Left Center (ch)',
            'Right Center (ch)',
            'Offset (ch)',
            'Left Goodness of Fit',
            'Left Amplitude',
            'Left Sigma',
            'Left Gamma',
            'Left FWHM',
            'Left Area',
            'Right Goodness of Fit',
            'Right Amplitude',
            'Right Sigma',
            'Right Gamma',
            'Right FWHM',
            'Right Area'
        ]
        self.current_file = None
        self._velocities = []
        self.update_data()

    def set_current_file(self, filename):
        self.current_file = filename
        self.update_data()

    def update_data(self):
        self.beginResetModel()
        if self.project and self.current_file:
            # Get velocities for the current file
            self.project.update_file_velocities(self.current_file)
            velocities_group = self.project.h5file['data'][self.current_file]['velocities']
            self._velocities = list(velocities_group.keys())
        else:
            self._velocities = []
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._velocities)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not self.current_file:
            return None
        row = index.row()
        col = index.column()
        if row >= self.rowCount() or col >= self.columnCount():
            return None
        velocity_name = self._velocities[row]
        column_name = self._headers[col]
        if role == Qt.DisplayRole:
            if col == 0:
                return velocity_name
            else:
                data_key = self.column_to_data_key(column_name)
                data_dict = self.project.get_peak_fit_data(self.current_file, velocity_name)
                value = data_dict.get(data_key, np.nan)
                if value is None or (isinstance(value, float) and np.isnan(value)):
                    return ''  # Return empty string for None or np.nan
                else:
                    return str(value)
        return None

    def column_to_data_key(self, column_name):
        mapping = {
            'Left Center (m/s)': 'left_center_mps',
            'Right Center (m/s)': 'right_center_mps',
            'Offset (m/s)': 'offset_mps',
            'Left Center (ch)': 'left_center_ch',
            'Right Center (ch)': 'right_center_ch',
            'Offset (ch)': 'offset_ch',
            'Left Goodness of Fit': 'left_goodness_of_fit',
            'Left Amplitude': 'left_amplitude',
            'Left Sigma': 'left_sigma',
            'Left Gamma': 'left_gamma',
            'Left FWHM': 'left_fwhm',
            'Left Area': 'left_area',
            'Right Goodness of Fit': 'right_goodness_of_fit',
            'Right Amplitude': 'right_amplitude',
            'Right Sigma': 'right_sigma',
            'Right Gamma': 'right_gamma',
            'Right FWHM': 'right_fwhm',
            'Right Area': 'right_area'
        }
        return mapping.get(column_name)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable  # Not editable

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() or not self.current_file:
            return False
        if role != Qt.EditRole:
            return False
        row = index.row()
        col = index.column()
        if row >= self.rowCount() or col >= self.columnCount():
            return False
        velocity_name = self._velocities[row]
        column_name = self._headers[col]
        if col == 0:
            # Name column is not editable
            return False
        data_key = self.column_to_data_key(column_name)
        if data_key is None:
            return False
        try:
            value = float(value)
        except ValueError:
            value = np.nan
        # Update the data in the HDF5 file
        data_dict = {data_key: value}
        self.project.set_peak_fit_data(self.current_file, velocity_name, data_dict)
        # Notify that data has changed
        self.dataChanged.emit(index, index, [Qt.DisplayRole])
        return True

