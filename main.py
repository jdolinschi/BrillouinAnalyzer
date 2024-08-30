# main.py

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from src.gui.main_window import Ui_MainWindow
from src.analysis.project_manager import ProjectManager  # Import the ProjectManager

def main():
    app = QApplication(sys.argv)

    # Create an instance of QMainWindow
    main_window = QMainWindow()

    # Create an instance of Ui_MainWindow and set up the UI
    ui = Ui_MainWindow()
    ui.setupUi(main_window)

    # Create an instance of ProjectManager and pass the UI to it
    project_manager = ProjectManager(ui)

    # Show the main window
    main_window.show()

    # Execute the application's main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
