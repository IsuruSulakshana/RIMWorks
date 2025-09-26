from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt

class HomeScreenUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 20, 50, 20)

        # Title container
        title_label = QLabel("RIMWorks")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #f0f0f0;")
        layout.addWidget(title_label)

        # Buttons
        self.engineer_btn = QPushButton("👨‍💼 Engineer")
        self.operator_btn = QPushButton("👷 Operator")

        button_style = """
            QPushButton {
                font-size: 16px;
                padding: 12px 20px;
                min-width: 220px;
                max-width: 280px;
                background-color: #3c3f41;
                color: #f0f0f0;
                border: 1px solid #555;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #505357;
            }
        """

        for btn in [self.engineer_btn, self.operator_btn]:
            btn.setStyleSheet(button_style)
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)
