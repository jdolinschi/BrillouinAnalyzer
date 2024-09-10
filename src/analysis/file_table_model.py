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
        self._headers = ['Filename', 'CHI Angle', 'Pinhole', 'Power', 'Polarization', 'Scans']
        self._sort_order = Qt.AscendingOrder
        self._sort_column = -1  # No sorting by default

    def rowCount(self, parent=QModelIndex()):
        return len(self._files)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        value = self._files[index.row()][index.column()]

        if role in (Qt.DisplayRole, Qt.EditRole):
            # Convert np.float64 to Python float for display
            if isinstance(value, np.float64):
                value = float(value)
            return "" if value is None else value  # Display empty string for None values

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole and self._is_editable_column(index.column()):
            if not self._validate_and_set_data(index, value):
                return False
            self._emit_data_changed(index)
            return True
        return False

    def flags(self, index):
        if index.column() == 0:  # Filename column is not user-editable
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._headers[section] if orientation == Qt.Horizontal else str(section + 1)
        return None

    def insertRows(self, position, rows, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        self._files[position:position] = [['', None, None, None, None, None] for _ in range(rows)]
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        del self._files[position:position + rows]
        self.endRemoveRows()
        return True

    def addFiles(self, filepaths):
        new_files = [[os.path.basename(filepath), None, None, None, None, None] for filepath in filepaths]
        self._add_files_to_model(new_files)

    def addFilesWithMetadata(self, files_with_metadata):
        self._add_files_to_model([list(metadata) for metadata in files_with_metadata])

    def sort(self, column, order=Qt.AscendingOrder):
        if column == 0: return  # Avoid sorting by Filename
        self._sort_files(column, order)
        self._sort_column, self._sort_order = column, order

    def clear(self):
        self.removeRows(0, self.rowCount())

    def removeFileByName(self, filename):
        self._remove_file_by_condition(lambda row: row[0] == filename)

    def _is_editable_column(self, column):
        return column != 0  # Filename column is not editable

    def _validate_and_set_data(self, index, value):
        try:
            if index.column() > 0:
                value = float(value) if value else None  # Convert to float or None for empty
            self._files[index.row()][index.column()] = value
            return True
        except ValueError:
            return False

    def _emit_data_changed(self, index):
        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        row = index.row()
        filename = self._files[row][0]
        metadata = self._get_metadata(row)
        self.data_changed_signal.emit(row, filename, metadata)

    def _add_files_to_model(self, files):
        self.blockSignals(True)
        self.insertRows(self.rowCount(), len(files))
        self._files[-len(files):] = files
        self.blockSignals(False)
        for i, file in enumerate(files, start=self.rowCount() - len(files)):
            self.data_changed_signal.emit(i, file[0], self._get_metadata(i))
        self.layoutChanged.emit()

    def _sort_files(self, column, order):
        self.layoutAboutToBeChanged.emit()
        try:
            self._files.sort(key=lambda x: (x[column] if x[column] is not None else float('-inf')),
                             reverse=(order == Qt.DescendingOrder))
        except TypeError:
            self._files.sort(key=lambda x: str(x[column]) if x[column] is not None else '',
                             reverse=(order == Qt.DescendingOrder))
        self.layoutChanged.emit()

    def _get_metadata(self, row):
        return {
            'chi_angle': self._files[row][1],
            'pinhole': self._files[row][2],
            'power': self._files[row][3],
            'polarization': self._files[row][4],
            'scans': self._files[row][5]
        }

    def _remove_file_by_condition(self, condition):
        for i, row in enumerate(self._files):
            if condition(row):
                self.removeRows(i, 1)
                break
