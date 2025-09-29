# gui/widgets/select_mold_screen.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QSpinBox, QPushButton, QDateTimeEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QDateTime
import os, json

class SelectMoldScreen(QWidget):
    def __init__(self, current_job, on_back=None, on_next=None):
        super().__init__()
        self.current_job = current_job
        self.on_back = on_back
        self.on_next = on_next
        self.data_folder = "data/molds"
        os.makedirs(self.data_folder, exist_ok=True)

        self.mold_files = []
        self.molds = []
        self.selected_mold = None

        self.load_molds()
        self.init_ui()

    def init_ui(self):
        main = QVBoxLayout()
        main.setSpacing(12)
        main.setContentsMargins(40, 20, 40, 20)

        # Title
        title = QLabel("Create Job — Step 2: Select Mold & Details")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f0f0f0; padding: 6px;")
        main.addWidget(title)

        # Mold selection
        main.addWidget(QLabel("Select Mold:"))
        self.mold_select = QComboBox()
        self.mold_select.addItems([m.get("mold_name", "Unknown") for m in self.molds])
        main.addWidget(self.mold_select)

        # Quantity / Part count
        main.addWidget(QLabel("Part Count:"))
        self.part_count = QSpinBox()
        self.part_count.setRange(1, 10000)
        self.part_count.setValue(1)
        main.addWidget(self.part_count)

        # Job Start / End DateTime
        main.addWidget(QLabel("Job Start Date & Time:"))
        self.start_dt = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_dt.setCalendarPopup(True)
        main.addWidget(self.start_dt)

        main.addWidget(QLabel("Job End Date & Time:"))
        self.end_dt = QDateTimeEdit(QDateTime.currentDateTime())
        self.end_dt.setCalendarPopup(True)
        main.addWidget(self.end_dt)

        # Buttons
        btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("⬅️ Back")
        self.back_btn.clicked.connect(self.on_back if self.on_back else lambda: None)

        self.next_btn = QPushButton("✅ Start Job")
        self.next_btn.clicked.connect(self.start_job)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.next_btn)
        main.addLayout(btn_layout)

        self.setLayout(main)

    # ---------------- Load molds ----------------
    def load_molds(self):
        """Load all molds from data folder (reusing ViewMoldScreen logic)"""
        self.mold_files = [f for f in os.listdir(self.data_folder) if f.endswith(".json")]
        self.molds = []
        for file in self.mold_files:
            path = os.path.join(self.data_folder, file)
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    if "mold_name" in data:
                        self.molds.append(data)
            except Exception as e:
                print(f"Failed to load mold file {file}: {e}")

    # ---------------- Start Job ----------------
    def start_job(self):
        # Validate selection
        selected_name = self.mold_select.currentText()
        self.selected_mold = next((m for m in self.molds if m.get("mold_name") == selected_name), None)
        if not self.selected_mold:
            QMessageBox.warning(self, "No selection", "Please select a valid mold.")
            return
        if self.start_dt.dateTime() >= self.end_dt.dateTime():
            QMessageBox.warning(self, "Invalid Date", "End date/time must be after start date/time.")
            return

        # Save selection to current job
        self.current_job["mold"] = self.selected_mold
        self.current_job["part_count"] = self.part_count.value()
        self.current_job["start_datetime"] = self.start_dt.dateTime().toString(Qt.DateFormat.ISODate)
        self.current_job["end_datetime"] = self.end_dt.dateTime().toString(Qt.DateFormat.ISODate)

        # Next-step callback
        if self.on_next:
            self.on_next(self.current_job)
        else:
            QMessageBox.information(self, "Job Ready", f"Job details saved:\n{self.current_job}")
