# gui/widgets/engineer_login_screen.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt

class EngineerLoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(50, 20, 50, 20)

        title_label = QLabel("Engineer Login")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #f0f0f0;")
        layout.addWidget(title_label)

        # Username and password
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
        self.login_btn.clicked.connect(self.check_login)

        self.setLayout(layout)

    def check_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Hardcoded engineer credentials (can be extended to JSON later)
        if username == "admin" and password == "admin123":
            print("Engineer login successful!")
            # Navigate to EngineerDashboard (handled in home.py)
        else:
            print("Invalid engineer username or password!")
