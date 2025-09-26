# gui/widgets/icon_button.py
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

class IconButton(QPushButton):
    def __init__(self, text, icon_path=None, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(220, 60)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3c3f41;
                color: #f0f0f0;
                border: 1px solid #555;
                border-radius: 8px;
                font-size: 14px;
                text-align: left;
                padding-left: 12px;
            }
            QPushButton:hover {
                background-color: #505357;
            }
        """)
        if icon_path:
            icon = QIcon(icon_path)
            self.setIcon(icon)
            self.setIconSize(QSize(32, 32))
