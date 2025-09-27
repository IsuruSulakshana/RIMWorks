# gui/home.py
from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from gui.widgets.home_screen import HomeScreenUI
from gui.engineer_dashboard import EngineerDashboard
from gui.operator_dashboard import OperatorDashboard
from gui.widgets.create_operator_screen import CreateOperatorScreen
from gui.widgets.create_mold_screen import CreateMoldScreen
from gui.widgets.operator_login_screen import OperatorLoginScreen
from gui.widgets.engineer_login_screen import EngineerLoginScreen
from gui.widgets.calibration_machine_screen import CalibrationMachineScreen  # New import
from gui.widgets.view_mold_screen import ViewMoldScreen  # New import

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
        self.calibration_machine_screen = CalibrationMachineScreen()  # New screen
        self.view_mold_screen = ViewMoldScreen(on_back=lambda: self.switch_screen("engineer_dashboard"))  # New screen

        # Add screens to stack
        for screen in [
            self.home_ui, self.engineer_login_screen, self.operator_login_screen,
            self.engineer_dashboard, self.operator_dashboard,
            self.create_operator_screen, self.create_mold_screen,
            self.calibration_machine_screen, self.view_mold_screen
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
        self.engineer_dashboard.calibration_btn.clicked.connect(
            lambda: self.switch_screen("calibration_machine")
        )
        self.engineer_dashboard.view_molds_btn.clicked.connect(
            lambda: self.switch_screen("view_mold_screen")
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
            "view_mold_screen": self.view_mold_screen
        }
        if screen_name in mapping:
            self.stack.setCurrentWidget(mapping[screen_name])

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
