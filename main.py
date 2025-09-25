import sys
from PyQt6.QtWidgets import QApplication
from gui.home import HomeScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeScreen()
    window.show()
    sys.exit(app.exec())
