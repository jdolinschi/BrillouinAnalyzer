import sys

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow
from src.gui.main_window import Ui_MainWindow
from src.analysis.project_manager import ProjectManager
from src.analysis.calibration_manager import CalibrationManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of Ui_MainWindow and set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create an instance of ProjectManager and pass the UI to it
        self.project_manager = ProjectManager(self.ui)

        # Create an instance of CalibrationManager and pass the UI and ProjectManager to it
        self.calibration_manager = CalibrationManager(self.ui, self.project_manager)

        # Let ProjectManager know about CalibrationManager
        self.project_manager.set_calibration_manager(self.calibration_manager)

        # Add the 'Save Project' shortcut (Ctrl+S)
        self.add_save_shortcut()

    def add_save_shortcut(self):
        # Create a QAction for save
        save_action = QAction("Save Project", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))  # Assign the Ctrl+S shortcut
        save_action.triggered.connect(self.project_manager.save_project_clicked)  # Connect to save_project_clicked

        # Add the action to the main window so that the shortcut is active
        self.addAction(save_action)

    def closeEvent(self, event):
        # Call a method in ProjectManager to handle unsaved changes, etc.
        if not self.project_manager.check_unsaved_changes():
            event.ignore()  # Ignore the close event if there are unsaved changes
        else:
            self.project_manager.cleanup_project()
            event.accept()  # Accept the close event to close the window

def main():
    app = QApplication(sys.argv)

    # Create an instance of MainWindow (our subclassed QMainWindow)
    main_window = MainWindow()

    # Show the main window
    main_window.show()

    # Execute the application's main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
