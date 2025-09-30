# gui/home.py
from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from gui.widgets.home_screen import HomeScreenUI
from gui.engineer_dashboard import EngineerDashboard
from gui.operator_dashboard import OperatorDashboard
from gui.widgets.create_operator_screen import CreateOperatorScreen
from gui.widgets.create_mold_screen import CreateMoldScreen
from gui.widgets.operator_login_screen import OperatorLoginScreen
from gui.widgets.engineer_login_screen import EngineerLoginScreen
from gui.widgets.calibration_machine_screen import CalibrationMachineScreen
from gui.widgets.view_mold_screen import ViewMoldScreen
from gui.widgets.create_job_screen import CreateJobScreen
from gui.widgets.select_mold_screen import SelectMoldScreen
from gui.widgets.job_status_screen import JobStatusScreen  # NEW

import os, json, uuid
from PyQt6.QtCore import Qt, QDateTime

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RIMWorks")
        self.setGeometry(400, 200, 600, 600)
        self.setMinimumSize(500, 400)

        # Stack to manage screens
        self.stack = QStackedWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.stack)
        self.setLayout(self.layout)

        # Screens
        self.home_ui = HomeScreenUI()
        self.engineer_login_screen = EngineerLoginScreen()
        self.operator_login_screen = OperatorLoginScreen()
        self.engineer_dashboard = EngineerDashboard()
        self.operator_dashboard = OperatorDashboard()
        self.create_operator_screen = CreateOperatorScreen()
        self.create_mold_screen = CreateMoldScreen()
        self.calibration_machine_screen = CalibrationMachineScreen()
        self.view_mold_screen = ViewMoldScreen(on_back=lambda: self.switch_screen("engineer_dashboard"))

        self.create_job_screen = CreateJobScreen(
            on_back=lambda: self.switch_screen("engineer_dashboard"),
            on_next=self.goto_select_mold
        )

        self.job_status_screen = JobStatusScreen(on_back=lambda: self.switch_screen("engineer_dashboard"))

        # Add base screens to stack
        for screen in [
            self.home_ui, self.engineer_login_screen, self.operator_login_screen,
            self.engineer_dashboard, self.operator_dashboard,
            self.create_operator_screen, self.create_mold_screen,
            self.calibration_machine_screen, self.view_mold_screen,
            self.create_job_screen, self.job_status_screen
        ]:
            self.stack.addWidget(screen)

        # --- Home buttons ---
        self.home_ui.engineer_btn.clicked.connect(lambda: self.switch_screen("engineer_login"))
        self.home_ui.operator_btn.clicked.connect(lambda: self.switch_screen("operator_login"))

        # --- Engineer login validation ---
        self.engineer_login_screen.login_btn.clicked.connect(self.engineer_login)

        # --- Operator login validation ---
        self.operator_login_screen.login_btn.clicked.connect(self.operator_login)

        # --- Engineer Dashboard navigation ---
        self.engineer_dashboard.create_operator_btn.clicked.connect(
            lambda: self.switch_screen("create_operator")
        )
        self.engineer_dashboard.create_mold_btn.clicked.connect(
            lambda: self.switch_screen("create_mold")
        )
        self.engineer_dashboard.create_job_btn.clicked.connect(
            lambda: self.switch_screen("create_job")
        )
        self.engineer_dashboard.calibration_btn.clicked.connect(
            lambda: self.switch_screen("calibration_machine")
        )
        self.engineer_dashboard.view_molds_btn.clicked.connect(
            lambda: self.switch_screen("view_mold_screen")
        )
        self.engineer_dashboard.job_status_btn.clicked.connect(  # add button in EngineerDashboard UI
            lambda: self.switch_screen("job_status")
        )
        self.engineer_dashboard.back_btn.clicked.connect(lambda: self.switch_screen("home"))

        # --- Operator Dashboard navigation ---
        self.operator_dashboard.back_btn.clicked.connect(lambda: self.switch_screen("home"))

        # --- Create Operator navigation ---
        self.create_operator_screen.back_btn.clicked.connect(
            lambda: self.switch_screen("engineer_dashboard")
        )

        # --- Create Mold navigation ---
        self.create_mold_screen.back_btn.clicked.connect(
            lambda: self.switch_screen("engineer_dashboard")
        )

        # --- Calibration Machine navigation ---
        self.calibration_machine_screen.back_btn.clicked.connect(
            lambda: self.switch_screen("engineer_dashboard")
        )

    # ------------------- Screen switching -------------------
    def switch_screen(self, screen_name):
        mapping = {
            "home": self.home_ui,
            "engineer_login": self.engineer_login_screen,
            "operator_login": self.operator_login_screen,
            "engineer_dashboard": self.engineer_dashboard,
            "operator_dashboard": self.operator_dashboard,
            "create_operator": self.create_operator_screen,
            "create_mold": self.create_mold_screen,
            "calibration_machine": self.calibration_machine_screen,
            "view_mold_screen": self.view_mold_screen,
            "create_job": self.create_job_screen,
            "job_status": self.job_status_screen
        }
        if screen_name in mapping:
            self.stack.setCurrentWidget(mapping[screen_name])
            # auto-refresh job status
            if screen_name == "job_status":
                self.job_status_screen.load_jobs()

    # ------------------- Login handlers -------------------
    def engineer_login(self):
        username = self.engineer_login_screen.username_input.text()
        password = self.engineer_login_screen.password_input.text()
        if username == "admin" and password == "admin123":
            print("Engineer login successful!")
            self.switch_screen("engineer_dashboard")
        else:
            print("Invalid engineer credentials!")

    def operator_login(self):
        if self.operator_login_screen.validate_login():
            print("Operator login successful!")
            self.switch_screen("operator_dashboard")

    # ------------------- Create Job → Select Mold flow -------------------
    def goto_select_mold(self, current_job):
        """Callback after operator assigned: open SelectMoldScreen."""
        self.select_screen = SelectMoldScreen(
            current_job=current_job,
            on_back=lambda: self.switch_screen("create_job"),
            on_next=self.job_started
        )
        self.stack.addWidget(self.select_screen)
        self.stack.setCurrentWidget(self.select_screen)

    def job_started(self, job_data):
        """Callback after Start Job pressed in SelectMoldScreen."""
        print("Job started:", job_data)

        # Ensure jobs folder exists
        os.makedirs("data/jobs", exist_ok=True)

        # Assign unique job_id if missing
        if "job_id" not in job_data:
            job_data["job_id"] = f"JOB-{uuid.uuid4().hex[:6].upper()}"

        # Save job JSON
        job_file = os.path.join("data/jobs", f"{job_data['job_id']}.json")
        with open(job_file, "w") as f:
            json.dump(job_data, f, indent=4)

        # Navigate to Job Status screen
        self.switch_screen("job_status")
