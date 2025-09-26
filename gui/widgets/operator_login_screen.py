# gui/widgets/operator_login_screen.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
import json
import os

class OperatorLoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.data_file = "data/operators.json"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(50, 20, 50, 20)

        title_label = QLabel("Operator Login")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #f0f0f0;")
        layout.addWidget(title_label)

        # Username and password inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedWidth(280)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(280)

        layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Login button
        self.login_btn = QPushButton("🔑 Login")
        self.login_btn.setFixedWidth(200)
        layout.addWidget(self.login_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def validate_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not os.path.exists(self.data_file):
            print("No operators registered yet!")
            return False

        with open(self.data_file, "r") as f:
            operators = json.load(f)

        match = next((op for op in operators if op["username"] == username and op["password"] == password), None)
        if match:
            print(f"Login successful! Welcome, {match['name']}")
            return True
        else:
            print("Invalid username or password!")
            return False
