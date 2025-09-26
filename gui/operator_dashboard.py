from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class OperatorDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("👷 Operator Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #f0f0f0;")
        layout.addWidget(title)

        self.view_jobs_btn = QPushButton("📋 View Assigned Jobs")
        self.mold_details_btn = QPushButton("🛠️ View Mold Details")
        self.back_btn = QPushButton("⬅️ Back to Home")

        for btn in [self.view_jobs_btn, self.mold_details_btn, self.back_btn]:
            btn.setFixedWidth(240)
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)
