# gui/widgets/select_mold_screen.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QSpinBox, QDateTimeEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QDateTime
from gui.widgets.view_mold_screen import ViewMoldScreen  # Your existing view screen
import os, json, uuid


class SelectMoldScreen(QWidget):
    def __init__(self, current_job, on_back=None, on_next=None):
        super().__init__()
        self.current_job = current_job
        self.on_back = on_back
        self.on_next = on_next
        self.selected_mold = None
        self.init_ui()

    # ---------------- UI Setup ----------------
    def init_ui(self):
        main = QVBoxLayout()
        main.setSpacing(12)
        main.setContentsMargins(40, 20, 40, 20)

        # --- Title ---
        title = QLabel("Create Job — Step 2: Select Mold")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f0f0f0; padding: 6px;")
        main.addWidget(title)

        # --- Select Mold Button ---
        self.select_mold_btn = QPushButton("🔍 Select Mold")
        self.select_mold_btn.clicked.connect(self.open_view_mold_screen)
        main.addWidget(self.select_mold_btn)

        # --- Selected Mold Preview ---
        self.selected_label = QLabel("Selected Mold: None")
        self.selected_label.setStyleSheet("font-size: 14px; color: #f0f0f0;")
        main.addWidget(self.selected_label)

        # --- Job Details ---
        main.addWidget(QLabel("Part Count:"))
        self.part_count = QSpinBox()
        self.part_count.setRange(1, 10000)
        self.part_count.setValue(1)
        main.addWidget(self.part_count)

        main.addWidget(QLabel("Job Start Date & Time:"))
        self.start_dt = QDateTimeEdit(QDateTime.currentDateTime())
        self.start_dt.setCalendarPopup(True)
        main.addWidget(self.start_dt)

        main.addWidget(QLabel("Job End Date & Time:"))
        self.end_dt = QDateTimeEdit(QDateTime.currentDateTime())
        self.end_dt.setCalendarPopup(True)
        main.addWidget(self.end_dt)

        # --- Buttons ---
        self.back_btn = QPushButton("⬅️ Back")
        self.back_btn.clicked.connect(self.on_back if self.on_back else lambda: None)

        self.next_btn = QPushButton("✅ Start Job")
        self.next_btn.clicked.connect(self.start_job)

        main.addWidget(self.back_btn)
        main.addWidget(self.next_btn)

        self.setLayout(main)

    # ---------------- Open View Mold Screen ----------------
    def open_view_mold_screen(self):
        # Callback when mold is selected in ViewMoldScreen
        def mold_selected_callback(selected_data):
            if selected_data:
                self.selected_mold = selected_data
                mold_name = selected_data.get("mold_name", "Unknown")
                self.selected_label.setText(f"Selected Mold: {mold_name}")
            self.view_screen.hide()

        # Show ViewMoldScreen with selection callback
        self.view_screen = ViewMoldScreen(
            on_back=lambda: self.view_screen.hide(),
            on_select=mold_selected_callback
        )
        self.view_screen.show()

    # ---------------- Start Job ----------------
    def start_job(self):
        if not self.selected_mold:
            QMessageBox.warning(self, "No selection", "Please select a mold first.")
            return
        if self.start_dt.dateTime() >= self.end_dt.dateTime():
            QMessageBox.warning(self, "Invalid Date", "End date/time must be after start date/time.")
            return

        # Generate unique job ID
        job_id = f"JOB-{uuid.uuid4().hex[:6].upper()}"

        # Save job details
        self.current_job["job_id"] = job_id
        self.current_job["mold"] = self.selected_mold
        self.current_job["part_count"] = self.part_count.value()
        self.current_job["start_datetime"] = self.start_dt.dateTime().toString(Qt.DateFormat.ISODate)
        self.current_job["end_datetime"] = self.end_dt.dateTime().toString(Qt.DateFormat.ISODate)
        self.current_job["status"] = "Not Started"  # default status

        # Save to file
        os.makedirs("data/jobs", exist_ok=True)
        job_file = os.path.join("data/jobs", f"{job_id}.json")
        with open(job_file, "w") as f:
            json.dump(self.current_job, f, indent=4)

        # Callback or confirmation
        if self.on_next:
            self.on_next(self.current_job)
        else:
            QMessageBox.information(self, "Job Ready", f"Job saved:\n{self.current_job}")
