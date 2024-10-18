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

    def get_nm_per_channel_values_and_uncertainties(self):
        values = []
        uncertainties = []
        for file_data in self._files:
            nm_per_channel = file_data['nm_per_channel']
            nm_per_channel_uncertainty = file_data['nm_per_channel_uncertainty']
            if nm_per_channel is not None and not np.isnan(nm_per_channel):
                values.append(nm_per_channel)
                uncertainties.append(nm_per_channel_uncertainty if nm_per_channel_uncertainty is not None else np.nan)
        return values, uncertainties

    def get_ghz_per_channel_values(self):
        values = []
        for file_data in self._files:
            ghz_per_channel = file_data[3]
            if ghz_per_channel is not None and not np.isnan(ghz_per_channel):
                values.append(ghz_per_channel)
        return values

    def get_ghz_per_channel_values_and_uncertainties(self):
        values = []
        uncertainties = []
        for file_data in self._files:
            ghz_per_channel = file_data['ghz_per_channel']
            ghz_per_channel_uncertainty = file_data['ghz_per_channel_uncertainty']
            if ghz_per_channel is not None and not np.isnan(ghz_per_channel):
                values.append(ghz_per_channel)
                uncertainties.append(ghz_per_channel_uncertainty if ghz_per_channel_uncertainty is not None else np.nan)
        return values, uncertainties

    def rowCount(self, parent=QModelIndex()):
        return len(self._files)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        file_data = self._files[row]

        if role in (Qt.DisplayRole, Qt.EditRole):
            if col == 0:  # Filename
                return file_data['filename']
            elif col == 1:  # Channels
                return file_data['channels'] if file_data['channels'] is not None else ""
            elif col == 2:  # nm/Channel
                value = file_data['nm_per_channel']
                uncertainty = file_data['nm_per_channel_uncertainty']
                if value is not None and not np.isnan(value):
                    if uncertainty is not None and not np.isnan(uncertainty):
                        return f"{value:.6f} ± {uncertainty:.6f}"
                    else:
                        return f"{value:.6f}"
                else:
                    return ""
            elif col == 3:  # GHz/Channel
                value = file_data['ghz_per_channel']
                uncertainty = file_data['ghz_per_channel_uncertainty']
                if value is not None and not np.isnan(value):
                    if uncertainty is not None and not np.isnan(uncertainty):
                        return f"{value:.6f} ± {uncertainty:.6f}"
                    else:
                        return f"{value:.6f}"
                else:
                    return ""
        elif role == Qt.BackgroundRole:
            if self._plotted_file is not None and file_data['filename'] == self._plotted_file:
                return QBrush(QColor(255, 255, 0, 127))  # Semi-transparent yellow
        return None

    def setPlottedFile(self, filename):
        # Find the index of the previous plotted file
        prev_row = None
        if self._plotted_file is not None:
            for row, file_data in enumerate(self._files):
                if file_data['filename'] == self._plotted_file:
                    prev_row = row
                    break
        # Update the plotted file
        self._plotted_file = filename
        # Find the index of the new plotted file
        new_row = None
        if self._plotted_file is not None:
            for row, file_data in enumerate(self._files):
                if file_data['filename'] == self._plotted_file:
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
            file_data = {
                'filename': filename,
                'channels': None,
                'nm_per_channel': None,
                'nm_per_channel_uncertainty': None,
                'ghz_per_channel': None,
                'ghz_per_channel_uncertainty': None,
            }
            new_files.append(file_data)
        self._add_files_to_model(new_files)

    def _add_files_to_model(self, files):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount() + len(files) - 1)
        self._files.extend(files)
        self.endInsertRows()

    def dataChangedSignal(self, index):
        row = index.row()
        filename = self._files[row]['filename']
        metadata = self._get_metadata(row)
        self.data_changed_signal.emit(row, filename, metadata)

    def _get_metadata(self, row):
        return {
            'channels': self._files[row]['channels'],
            'nm_per_channel': self._files[row]['nm_per_channel'],
            'ghz_per_channel': self._files[row]['ghz_per_channel']
        }

    def update_calibration_constants(self, filename, nm_per_channel, nm_per_channel_uncertainty, ghz_per_channel,
                                     ghz_per_channel_uncertainty):
        for row, file_data in enumerate(self._files):
            if file_data['filename'] == filename:
                file_data['nm_per_channel'] = nm_per_channel
                file_data['nm_per_channel_uncertainty'] = nm_per_channel_uncertainty
                file_data['ghz_per_channel'] = ghz_per_channel
                file_data['ghz_per_channel_uncertainty'] = ghz_per_channel
                index_nm = self.index(row, 2)
                index_ghz = self.index(row, 3)
                self.dataChanged.emit(index_nm, index_nm, [Qt.DisplayRole])
                self.dataChanged.emit(index_ghz, index_ghz, [Qt.DisplayRole])
                break

    def clear_calibration_constants(self, filename):
        for row, file_data in enumerate(self._files):
            if file_data['filename'] == filename:
                file_data['nm_per_channel'] = None
                file_data['nm_per_channel_uncertainty'] = None
                file_data['ghz_per_channel'] = None
                file_data['ghz_per_channel_uncertainty'] = None
                index_nm = self.index(row, 2)
                index_ghz = self.index(row, 3)
                self.dataChanged.emit(index_nm, index_nm, [Qt.DisplayRole])
                self.dataChanged.emit(index_ghz, index_ghz, [Qt.DisplayRole])
                break

    def update_file_data(self, filename, channels, nm_per_channel, nm_per_channel_uncertainty, ghz_per_channel,
                         ghz_per_channel_uncertainty):
        for row, file_data in enumerate(self._files):
            if file_data['filename'] == filename:
                file_data['channels'] = channels
                file_data['nm_per_channel'] = nm_per_channel
                file_data['nm_per_channel_uncertainty'] = nm_per_channel_uncertainty
                file_data['ghz_per_channel'] = ghz_per_channel
                file_data['ghz_per_channel_uncertainty'] = ghz_per_channel_uncertainty
                index_channels = self.index(row, 1)
                index_nm = self.index(row, 2)
                index_ghz = self.index(row, 3)
                self.dataChanged.emit(index_channels, index_channels, [Qt.DisplayRole])
                self.dataChanged.emit(index_nm, index_nm, [Qt.DisplayRole])
                self.dataChanged.emit(index_ghz, index_ghz, [Qt.DisplayRole])
                break