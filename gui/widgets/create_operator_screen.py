from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt6.QtCore import Qt
import os, json

class CreateOperatorScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.data_file = "data/operators/operators.json"
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(50, 20, 50, 20)

        title_label = QLabel("Create Operator")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #f0f0f0;")
        layout.addWidget(title_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        layout.addWidget(self.name_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.role_select = QComboBox()
        self.role_select.addItems(["Operator", "Supervisor"])
        layout.addWidget(self.role_select, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.save_btn = QPushButton("💾 Save Operator")
        self.back_btn = QPushButton("⬅️ Back")
        layout.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.save_btn.clicked.connect(self.save_operator)
        self.setLayout(layout)

    def save_operator(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_select.currentText()

        if not name or not username or not password:
            print("Fill all fields!")
            return

        data = []
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)

        data.append({"name": name, "username": username, "password": password, "role": role})

        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Operator '{name}' saved!")
        self.name_input.clear()
        self.username_input.clear()
        self.password_input.clear()
