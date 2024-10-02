# src/analysis/calibration_file_table_model.py
import numpy as np
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QBrush, QColor


class CalibrationFileTableModel(QAbstractTableModel):
    data_changed_signal = Signal(int, str, dict)

    def __init__(self, files=None, parent=None):
        super(CalibrationFileTableModel, self).__init__(parent)
        self._files = files if files else []
        self._headers = ['Filename', 'Channels', 'nm/Channel', 'GHz/Channel']
        self._plotted_file = None  # Add this line

    def get_nm_per_channel_values(self):
        values = []
        for file_data in self._files:
            nm_per_channel = file_data[2]
            if nm_per_channel is not None and not np.isnan(nm_per_channel):
                values.append(nm_per_channel)
        return values

    def get_ghz_per_channel_values(self):
        values = []
        for file_data in self._files:
            ghz_per_channel = file_data[3]
            if ghz_per_channel is not None and not np.isnan(ghz_per_channel):
                values.append(ghz_per_channel)
        return values

    def rowCount(self, parent=QModelIndex()):
        return len(self._files)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        value = self._files[row][col]

        if role in (Qt.DisplayRole, Qt.EditRole):
            if isinstance(value, (np.float64, float)):
                value = float(value)
                return "" if np.isnan(value) else f"{value:.6f}"
            return "" if value is None else value
        elif role == Qt.BackgroundRole:
            if self._plotted_file is not None and self._files[row][0] == self._plotted_file:
                # Return a special background color
                return QBrush(QColor(255, 255, 0, 127))  # Semi-transparent yellow
        return None

    def setPlottedFile(self, filename):
        # Find the index of the previous plotted file
        prev_row = None
        if self._plotted_file is not None:
            for row, file_data in enumerate(self._files):
                if file_data[0] == self._plotted_file:
                    prev_row = row
                    break
        # Update the plotted file
        self._plotted_file = filename
        # Find the index of the new plotted file
        new_row = None
        if self._plotted_file is not None:
            for row, file_data in enumerate(self._files):
                if file_data[0] == self._plotted_file:
                    new_row = row
                    break
        # Emit dataChanged for the previous and new rows
        if prev_row is not None:
            top_left = self.index(prev_row, 0)
            bottom_right = self.index(prev_row, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right, [Qt.BackgroundRole])
        if new_row is not None:
            top_left = self.index(new_row, 0)
            bottom_right = self.index(new_row, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right, [Qt.BackgroundRole])

    def setData(self, index, value, role=Qt.EditRole):
        # Implement if needed
        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled

        # All columns should be selectable but not editable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._headers[section] if orientation == Qt.Horizontal else str(section + 1)
        return None

    def clear(self):
        self.beginResetModel()
        self._files.clear()
        self.endResetModel()

    def addFiles(self, files):
        new_files = []
        for filename in files:
            file_data = [filename, None, None, None]
            new_files.append(file_data)
        self._add_files_to_model(new_files)

    def _add_files_to_model(self, files):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + len(files) - 1)
        self._files.extend(files)
        self.endInsertRows()

    def dataChangedSignal(self, index):
        row = index.row()
        filename = self._files[row][0]
        metadata = self._get_metadata(row)
        self.data_changed_signal.emit(row, filename, metadata)

    def _get_metadata(self, row):
        return {
            'channels': self._files[row][1],
            'nm_per_channel': self._files[row][2],
            'ghz_per_channel': self._files[row][3]
        }

    def update_calibration_constants(self, filename, nm_per_channel, ghz_per_channel):
        for row, file_data in enumerate(self._files):
            if file_data[0] == filename:
                file_data[2] = nm_per_channel  # nm_per_channel column
                file_data[3] = ghz_per_channel  # ghz_per_channel column
                index_nm = self.index(row, 2)
                index_ghz = self.index(row, 3)
                self.dataChanged.emit(index_nm, index_nm, [Qt.DisplayRole])
                self.dataChanged.emit(index_ghz, index_ghz, [Qt.DisplayRole])
                break

    def clear_calibration_constants(self, filename):
        for row, file_data in enumerate(self._files):
            if file_data[0] == filename:
                file_data[2] = None
                file_data[3] = None
                index_nm = self.index(row, 2)
                index_ghz = self.index(row, 3)
                self.dataChanged.emit(index_nm, index_nm, [Qt.DisplayRole])
                self.dataChanged.emit(index_ghz, index_ghz, [Qt.DisplayRole])
                break

    def update_file_data(self, filename, channels, nm_per_channel, ghz_per_channel):
        for row, file_data in enumerate(self._files):
            if file_data[0] == filename:
                file_data[1] = channels
                file_data[2] = nm_per_channel
                file_data[3] = ghz_per_channel
                index_channels = self.index(row, 1)
                index_nm = self.index(row, 2)
                index_ghz = self.index(row, 3)
                self.dataChanged.emit(index_channels, index_channels, [Qt.DisplayRole])
                self.dataChanged.emit(index_nm, index_nm, [Qt.DisplayRole])
                self.dataChanged.emit(index_ghz, index_ghz, [Qt.DisplayRole])
                break