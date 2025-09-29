# gui/widgets/create_operator_screen.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QMessageBox
from PyQt6.QtCore import Qt
import os, json

class CreateOperatorScreen(QWidget):
    def __init__(self, on_back=None):
        super().__init__()
        self.on_back = on_back
        self.data_file = "data/operators/operators.json"
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        # --- Title ---
        title_label = QLabel("Create Operator")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title_label)

        # --- Name ---
        name_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Full Name")
        name_layout.addWidget(QLabel("Name:"))
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # --- Username ---
        username_layout = QHBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        username_layout.addWidget(QLabel("Username:"))
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)

        # --- Password ---
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(QLabel("Password:"))
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)

        # --- EPF Number ---
        epf_layout = QHBoxLayout()
        self.epf_input = QLineEdit()
        self.epf_input.setPlaceholderText("EPF Number")
        epf_layout.addWidget(QLabel("EPF Number:"))
        epf_layout.addWidget(self.epf_input)
        layout.addLayout(epf_layout)

        # --- Role ---
        role_layout = QHBoxLayout()
        self.role_select = QComboBox()
        self.role_select.addItems([
            "Operator",
            "Supervisor",
            "Technician",
            "Quality Controller",
            "Executive"
        ])
        role_layout.addWidget(QLabel("Role:"))
        role_layout.addWidget(self.role_select)
        layout.addLayout(role_layout)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("💾 Save Operator")
        self.save_btn.setStyleSheet("padding: 8px; font-weight: bold;")
        self.back_btn = QPushButton("🔙 Back")
        self.back_btn.setStyleSheet("padding: 8px; font-weight: bold;")
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.back_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # --- Connections ---
        self.save_btn.clicked.connect(self.save_operator)
        self.back_btn.clicked.connect(self.on_back if self.on_back else lambda: None)

    def save_operator(self):
        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        epf_number = self.epf_input.text().strip()
        role = self.role_select.currentText()

        if not name or not username or not password or not epf_number:
            QMessageBox.warning(self, "Missing Info", "Please fill all fields including EPF Number.")
            return

        data = []
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)

        data.append({
            "name": name,
            "username": username,
            "password": password,
            "epf_number": epf_number,
            "role": role
        })

        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=4)

        QMessageBox.information(self, "Success", f"Operator '{name}' saved successfully!")

        # Clear inputs
        self.name_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.epf_input.clear()
