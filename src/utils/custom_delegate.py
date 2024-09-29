# custom_delegate.py
from PySide6.QtWidgets import QStyledItemDelegate, QWidget, QLineEdit, QCheckBox, QHBoxLayout, QApplication, QStyle, QStyleOptionButton
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter

class CheckboxLineEditDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(CheckboxLineEditDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QWidget(parent)
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)

        self.checkbox = QCheckBox(editor)
        self.line_edit = QLineEdit(editor)

        layout.addWidget(self.checkbox)
        layout.addWidget(self.line_edit)

        return editor

    def setEditorData(self, editor, index):
        model = index.model()
        value = model.data(index, Qt.EditRole)
        # Since CheckStateRole is no longer handled, retrieve 'use_default' from the model's internal state
        # Assuming you have a method or property to get 'use_default' for the column
        use_default = model._default_values[index.column()]['use_default']

        editor.findChild(QLineEdit).setText(str(value) if value is not None else '')
        editor.findChild(QCheckBox).setChecked(use_default)

    def setModelData(self, editor, model, index):
        text = editor.findChild(QLineEdit).text()
        checked = editor.findChild(QCheckBox).isChecked()
        data = {'value': text, 'use_default': checked}
        model.setData(index, data, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        # Get the model
        model = index.model()

        # Ensure the index column exists in _default_values
        if index.column() not in model._default_values:
            super(CheckboxLineEditDelegate, self).paint(painter, option, index)
            return

        # Get the value and use_default flag for the current column
        value = model.data(index, Qt.DisplayRole)
        use_default = model._default_values[index.column()]['use_default']

        # Draw the background
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        # Calculate the checkbox rectangle
        checkbox_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, QStyleOptionButton(), None)
        checkbox_rect.moveTopLeft(option.rect.topLeft())

        # Draw the checkbox
        checkbox_style_option = QStyleOptionButton()
        checkbox_style_option.rect = checkbox_rect
        checkbox_style_option.state = QStyle.State_On if use_default else QStyle.State_Off
        QApplication.style().drawControl(QStyle.CE_CheckBox, checkbox_style_option, painter)

        # Draw the text next to the checkbox
        text_rect = option.rect
        text_rect.setLeft(checkbox_rect.right() + 5)  # Adjust the position to the right of the checkbox
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, str(value) if value else '')
