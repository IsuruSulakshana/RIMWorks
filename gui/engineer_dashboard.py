# gui/engineer_dashboard.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt

class EngineerDashboard(QWidget):
    def __init__(self, parent=None, callbacks=None):
        """
        callbacks: optional dict to assign functions to buttons
        Example: {"create_operator": func, "create_job": func, ...}
        """
        super().__init__(parent)
        self.callbacks = callbacks or {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(40, 20, 40, 20)

        # Title
        title_label = QLabel("Engineer Dashboard")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #f0f0f0;
            padding: 10px;
        """)
        layout.addWidget(title_label)

        # Button style
        button_style = """
            QPushButton {
                font-size: 16px;
                padding: 12px 20px;
                min-width: 240px;
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

        # Buttons
        self.create_operator_btn = QPushButton("👤 Create Operator")
        self.create_mold_btn = QPushButton("🛠️ Create Mold")
        self.create_job_btn = QPushButton("📋 Create Job")
        self.view_molds_btn = QPushButton("🔍 View Mold Details")
        self.job_status_btn = QPushButton("📊 Job Status")
        self.calibration_btn = QPushButton("⚙️ Calibration Machine")
        self.back_btn = QPushButton("⬅️ Back to Home")

        buttons = [
            self.create_operator_btn,
            self.create_mold_btn,
            self.create_job_btn,
            self.view_molds_btn,
            self.job_status_btn,
            self.calibration_btn,
            self.back_btn
        ]

        for btn in buttons:
            btn.setStyleSheet(button_style)
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Connect buttons to callbacks if provided
        btn_map = {
            "create_operator": self.create_operator_btn,
            "create_mold": self.create_mold_btn,
            "create_job": self.create_job_btn,
            "view_molds": self.view_molds_btn,
            "job_status": self.job_status_btn,
            "calibration": self.calibration_btn,
            "back": self.back_btn
        }

        for key, button in btn_map.items():
            if key in self.callbacks and callable(self.callbacks[key]):
                button.clicked.connect(self.callbacks[key])

        self.setLayout(layout)
