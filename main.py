# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui.home import HomeScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply dark mode stylesheet
    with open("resources/style.qss", "r") as f:
        app.setStyleSheet(f.read())

    # Launch HomeScreen (navigation controller)
    window = HomeScreen()
    window.show()

    sys.exit(app.exec())
