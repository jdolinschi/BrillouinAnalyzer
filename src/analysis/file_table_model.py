from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
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
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self._files[index.row()][index.column()]
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            column = index.column()
            if column == 0:  # Filename column is not editable
                return False
            else:
                # Ensure metadata fields are float values (except Filename)
                if column in [1, 2, 3, 4, 5]:
                    try:
                        value = float(value) if value else None  # Allow empty values
                    except ValueError:
                        return False  # Reject non-numeric input
                self._files[index.row()][column] = value
                self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])

                # Emit signal to update the HDF5 file with the new value
                filename = self._files[index.row()][0]
                metadata = {
                    'chi_angle': self._files[index.row()][1],
                    'pinhole': self._files[index.row()][2],
                    'power': self._files[index.row()][3],
                    'polarization': self._files[index.row()][4],
                    'scans': self._files[index.row()][5]
                }
                self.data_changed_signal.emit(index.row(), filename, metadata)

                return True
        return False

    def flags(self, index):
        if index.column() == 0:  # Filename column is not user-editable
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return None

    def insertRows(self, position, rows, parent=QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            self._files.insert(position, ['', None, None, None, None, None])  # None for numeric fields
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            del self._files[position]
        self.endRemoveRows()
        return True

    def addFiles(self, filepaths):
        for filepath in filepaths:
            filename = os.path.basename(filepath)

            # Add a new row with filename and empty metadata columns
            self.blockSignals(True)  # Temporarily block signals
            self.insertRows(self.rowCount(), 1)
            self._files[-1] = [filename, None, None, None, None, None]  # Set filename, others empty (None)
            self.blockSignals(False)  # Re-enable signals

            # Emit signal to notify ProjectManager about the new file with empty metadata
            self.data_changed_signal.emit(self.rowCount() - 1, filename, {
                'chi_angle': None,
                'pinhole': None,
                'power': None,
                'polarization': None,
                'scans': None
            })

        self.layoutChanged.emit()  # Refresh the view

    def sort(self, column, order=Qt.AscendingOrder):
        if column == 0:
            return  # Do not sort by Filename
        self.layoutAboutToBeChanged.emit()
        try:
            self._files.sort(key=lambda x: (x[column] if x[column] is not None else float('-inf')),
                             reverse=(order == Qt.DescendingOrder))
        except TypeError:
            self._files.sort(key=lambda x: str(x[column]) if x[column] is not None else '',
                             reverse=(order == Qt.DescendingOrder))
        self._sort_column = column
        self._sort_order = order
        self.layoutChanged.emit()

    def clear(self):
        self.removeRows(0, self.rowCount())

    def removeFileByName(self, filename):
        for i, row in enumerate(self._files):
            if row[0] == filename:
                self.removeRows(i, 1)
                break

