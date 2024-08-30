from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
import os

class FileTableModel(QAbstractTableModel):
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
            # Set data regardless of the column being editable by the user
            if column >= 0:
                if column > 0:  # Only allow numeric edits on columns after Filename
                    try:
                        value = float(value)
                    except ValueError:
                        return False  # Reject non-numeric input
                self._files[index.row()][column] = value
                self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
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
            self.insertRows(self.rowCount(), 1)
            self.setData(self.index(self.rowCount() - 1, 0), filename, Qt.EditRole)

    def sort(self, column, order=Qt.AscendingOrder):
        """Sort the table by the given column."""
        if column == 0:
            return  # Do not allow sorting by Filename
        self.layoutAboutToBeChanged.emit()
        self._files.sort(key=lambda x: x[column] if x[column] is not None else float('-inf'), reverse=(order == Qt.DescendingOrder))
        self._sort_column = column
        self._sort_order = order
        self.layoutChanged.emit()
