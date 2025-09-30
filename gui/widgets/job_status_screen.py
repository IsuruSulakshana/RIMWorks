# gui/widgets/job_status_screen.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QHeaderView
)
from PyQt6.QtCore import Qt
import os, json

STATUS_COLORS = {
    "Not Started": "#ff4d4d",    # Red
    "In Progress": "#ffd633",    # Yellow
    "Completed": "#4dff4d"       # Green
}

class JobStatusScreen(QWidget):
    def __init__(self, on_back=None):
        super().__init__()
        self.on_back = on_back
        self.data_folder = "data/jobs"
        os.makedirs(self.data_folder, exist_ok=True)
        self.jobs = []
        self.init_ui()
        self.load_jobs()

    def init_ui(self):
        main = QVBoxLayout()
        main.setSpacing(12)
        main.setContentsMargins(40, 20, 40, 20)

        # Title
        title = QLabel("Job Status Overview")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f0f0f0; padding: 6px;")
        main.addWidget(title)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Job ID", "Mold Name", "Vehicle", "System",
            "Part Count", "Status", "Start Date/Time", "End Date/Time"
        ])
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.table.setStyleSheet(
            "QTableWidget {background-color: #2b2b2b; color: #f0f0f0; gridline-color: #444;}"
            "QHeaderView::section {background-color: #3c3f41; color: #f0f0f0; font-weight: bold;}"
        )

        # Adjust column widths and resize behavior
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Job ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Mold Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Vehicle
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # System
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Part Count
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Status
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Start Date
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # End Date

        main.addWidget(self.table)

        # Buttons
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_jobs)
        self.back_btn = QPushButton("⬅️ Back")
        self.back_btn.clicked.connect(self.on_back if self.on_back else lambda: None)
        btn_layout.addWidget(self.back_btn)
        btn_layout.addWidget(self.refresh_btn)
        main.addLayout(btn_layout)

        self.setLayout(main)

    def load_jobs(self):
        self.jobs = []
        self.table.setRowCount(0)

        # Load all jobs
        for file in os.listdir(self.data_folder):
            if not file.endswith(".json"):
                continue
            try:
                with open(os.path.join(self.data_folder, file), "r") as f:
                    data = json.load(f)
                    self.jobs.append(data)
            except Exception as e:
                print(f"Failed to load job {file}: {e}")

        # Group by chemical type
        jobs_by_chemical = {}
        for job in self.jobs:
            chem = job.get("mold", {}).get("chemical_type", "Unknown")
            if chem not in jobs_by_chemical:
                jobs_by_chemical[chem] = []
            jobs_by_chemical[chem].append(job)

        # Fill table
        for chem, jobs in sorted(jobs_by_chemical.items()):
            # Insert chemical type as a spanning row
            row_idx = self.table.rowCount()
            self.table.insertRow(row_idx)
            header_item = QTableWidgetItem(f"Chemical Type: {chem}")
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            header_item.setBackground(Qt.GlobalColor.darkGray)
            header_item.setForeground(Qt.GlobalColor.white)
            self.table.setItem(row_idx, 0, header_item)
            self.table.setSpan(row_idx, 0, 1, self.table.columnCount())

            for job in jobs:
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                mold = job.get("mold", {})
                status = job.get("status", "Not Started")
                color = STATUS_COLORS.get(status, "#ffffff")

                cells = [
                    job.get("job_id", "N/A"),
                    mold.get("mold_name", "N/A"),
                    mold.get("vehicle", "N/A"),
                    mold.get("system", "N/A"),
                    str(job.get("part_count", 0)),
                    status,
                    job.get("start_datetime", "N/A"),
                    job.get("end_datetime", "N/A")
                ]

                for col, value in enumerate(cells):
                    item = QTableWidgetItem(value)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    # Color status column
                    if col == 5:
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.lightGray)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.lightGray)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.lightGray)
                        # Apply status color
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                        item.setBackground(Qt.GlobalColor.transparent)
                    self.table.setItem(row_idx, col, item)
