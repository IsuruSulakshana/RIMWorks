# gui/engineer_dashboard.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QFrame
from PyQt6.QtCore import Qt

class EngineerDashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 20)

        # Title Container
        title_frame = QFrame()
        title_frame.setFrameShape(QFrame.Shape.Box)
        title_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #555;
                border-radius: 10px;
                background-color: #2e2f33;
            }
        """)
        title_layout = QVBoxLayout()
        title_label = QLabel("Engineer Dashboard")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px; color: #f0f0f0;")
        title_layout.addWidget(title_label)
        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)

        # Buttons
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

        self.create_operator_btn = QPushButton("👤 Create Operator")
        self.create_mold_btn = QPushButton("🛠️ Create Mold")
        self.create_job_btn = QPushButton("📋 Create Job")
        self.view_molds_btn = QPushButton("🔍 View Mold Details")
        self.job_status_btn = QPushButton("📊 Job Status")
        self.calibration_btn = QPushButton("⚙️ Calibration Machine")  # New button
        self.back_btn = QPushButton("⬅️ Back to Home")

        for btn in [self.create_operator_btn, self.create_mold_btn, self.create_job_btn,
                    self.view_molds_btn, self.job_status_btn, self.calibration_btn, self.back_btn]:
            btn.setStyleSheet(button_style)
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)
