# main.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from src.gui.main_window import Ui_MainWindow
from src.analysis.project_manager import ProjectManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create an instance of Ui_MainWindow and set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create an instance of ProjectManager and pass the UI to it
        self.project_manager = ProjectManager(self.ui)

    def closeEvent(self, event):
        # Call a method in ProjectManager to handle unsaved changes, etc.
        if not self.project_manager.check_unsaved_changes():
            event.ignore()  # Ignore the close event if there are unsaved changes
        else:
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
