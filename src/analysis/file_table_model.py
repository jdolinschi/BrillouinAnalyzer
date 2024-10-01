import numpy as np
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QKeySequence, QClipboard
from PySide6.QtWidgets import QApplication, QTableView, QMenu
import os

class FileTableModel(QAbstractTableModel):
    data_changed_signal = Signal(int, str, dict)  # Signal to notify ProjectManager (row index, filename, metadata)

    def __init__(self, files=None, parent=None):
        super(FileTableModel, self).__init__(parent)
        self._files = files if files else []
        self._headers = [
            'Filename',
            'Calibration',  # New column added here
            'Chi angle (degrees)',
            'Pinhole',
            'Power',
            'Polarization',
            'Scans',
            'Laser wavelength (nm)',
            'Mirror spacing (mm)',
            'Scattering angle (degrees)'
        ]
        self._sort_order = Qt.AscendingOrder
        self._sort_column = -1  # No sorting by default

        # Initialize default values for each column (starting from column 1)
        self._default_values = {col: {'value': None, 'use_default': False} for col in range(1, len(self._headers))}

        self.calibration_options = []  # This will be populated from the ProjectManager

    def rowCount(self, parent=QModelIndex()):
        # Include an extra row for default values (row 0)
        return len(self._files) + 1

    @property
    def calibration_options(self):
        return self._calibration_options

    @calibration_options.setter
    def calibration_options(self, calibrations):
        self._calibration_options = calibrations
        # Notify the view that data has changed
        self.layoutChanged.emit()

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        if row == 0:
            # Default values row
            if col == 0:
                return '' if role in (Qt.DisplayRole, Qt.EditRole) else None
            elif role == Qt.DisplayRole or role == Qt.EditRole:
                default_value = self._default_values[col]['value']
                return "" if default_value is None else default_value
        else:
            # Regular file rows
            value = self._files[row - 1][col]  # Adjust for default row
            if role in (Qt.DisplayRole, Qt.EditRole):
                if isinstance(value, np.float64):
                    value = float(value)
                return "" if value is None else value
            elif role == Qt.EditRole and col == 1:
                # Return the calibration name for the combo box editor
                return value
            elif role == Qt.DisplayRole and col == 1:
                # Display the calibration name
                return value
            elif role == Qt.ToolTipRole and col == 1:
                return value
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        row = index.row()
        col = index.column()

        if row == 0:
            # Default values row
            if col == 0:
                # Filename column is not editable
                return False
            if role == Qt.EditRole:
                # Update default value and use_default flag
                if isinstance(value, dict):
                    self._default_values[col]['value'] = value['value'] if value['value'] != '' else None
                    self._default_values[col]['use_default'] = value['use_default']
                else:
                    self._default_values[col]['value'] = value if value != '' else None
                self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
                return True
            return False
        else:
            # Regular file rows
            if role == Qt.EditRole and self._is_editable_column(col):
                if not self._validate_and_set_data(index, value):
                    return False
                self._emit_data_changed(index)
                return True
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled

        row = index.row()
        col = index.column()

        if row == 0:
            # Default values row
            if col == 0:
                return Qt.ItemIsEnabled  # Filename column is not editable
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable  # No checkable flag for default row
        else:
            # Regular file rows
            if col == 0:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
            elif col == 1:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable  # Enable editing for Calibration column
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._headers[section] if orientation == Qt.Horizontal else str(section + 1)
        return None

    def insertRows(self, position, rows, parent=QModelIndex()):
        self.beginInsertRows(parent, position + 1, position + rows)  # Skip the default row
        for _ in range(rows):
            # Initialize the row with default values, including the default calibration
            row_data = ['']
            for col in range(1, self.columnCount()):
                if self._default_values[col]['use_default']:
                    value = self._default_values[col]['value']
                else:
                    value = None
                row_data.append(value)
            self._files.insert(position, row_data)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position + 1, position + rows)  # Skip the default row
        del self._files[position:position + rows]
        self.endRemoveRows()
        return True

    def removeFileByName(self, filename):
        self._remove_file_by_condition(lambda row: row[0] == filename)

    def addFiles(self, filepaths, default_calibration=None):
        new_files = []
        for filepath in filepaths:
            file_data = [os.path.basename(filepath)]
            for col in range(1, self.columnCount()):
                if self._default_values[col]['use_default']:
                    value = self._default_values[col]['value']
                else:
                    value = None
                file_data.append(value)
            # Set the default calibration
            if default_calibration is not None:
                file_data[1] = default_calibration  # Calibration column is at index 1
            new_files.append(file_data)
        self._add_files_to_model(new_files)

    def addFilesWithMetadata(self, files_with_metadata):
        self._add_files_to_model([list(metadata) for metadata in files_with_metadata])

    def sort(self, column, order=Qt.AscendingOrder):
        if column == 0:
            return  # Avoid sorting by Filename

        self.layoutAboutToBeChanged.emit()

        # Sort only the file rows (ignore the default row at index 0)
        try:
            self._files.sort(key=lambda x: (x[column] if x[column] is not None else float('-inf')),
                             reverse=(order == Qt.DescendingOrder))
        except TypeError:
            # Handle mixed data types by converting to string for comparison
            self._files.sort(key=lambda x: (str(x[column]) if x[column] is not None else ''),
                             reverse=(order == Qt.DescendingOrder))

        self.layoutChanged.emit()

    def _is_editable_column(self, column):
        return column != 0  # Filename column is not editable

    def _validate_and_set_data(self, index, value):
        try:
            if index.column() == 1:
                # Calibration column
                self._files[index.row() - 1][index.column()] = value  # Store the calibration name
            elif index.column() > 1:
                value = float(value) if value else None  # Convert to float or None for empty
                self._files[index.row() - 1][index.column()] = value  # Adjust for default row
            return True
        except ValueError:
            return False

    def clear(self):
        self.removeRows(0, self.rowCount())

    def _emit_data_changed(self, index):
        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        row = index.row() - 1  # Adjust for default row
        filename = self._files[row][0]
        metadata = self._get_metadata(row)
        self.data_changed_signal.emit(row, filename, metadata)

    def _add_files_to_model(self, files):
        self.blockSignals(True)
        self.insertRows(self.rowCount() - 1, len(files))  # Insert before the last row (default values row)
        self._files[-len(files):] = files
        self.blockSignals(False)
        for i, file in enumerate(files, start=self.rowCount() - len(files) - 1):
            self.data_changed_signal.emit(i, file[0], self._get_metadata(i))
        self.layoutChanged.emit()

    def _get_metadata(self, row):
        return {
            'calibration': self._files[row][1],  # Calibration column
            'chi_angle': self._files[row][2],
            'pinhole': self._files[row][3],
            'power': self._files[row][4],
            'polarization': self._files[row][5],
            'scans': self._files[row][6],
            'laser_wavelength': self._files[row][7],
            'mirror_spacing': self._files[row][8],
            'scattering_angle': self._files[row][9]
        }

    def _remove_file_by_condition(self, condition):
        for i, row in enumerate(self._files):
            if condition(row):
                self.removeRows(i, 1)
                break



