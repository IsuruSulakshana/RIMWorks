# gui/widgets/create_job_screen.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit,
    QListWidget, QPushButton, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
import json
import os
from datetime import datetime

class CreateJobScreen(QWidget):
    """Step 1 of Create Job: assign an operator.
    Next step will be selecting mold, mixing ratio, etc.
    """
    ROLE_OPTIONS = [
        "All Roles",
        "Operator",
        "Supervisor",
        "Technician",
        "Quality Controller",
        "Executive"
    ]

    def __init__(self, on_back=None, on_next=None):
        super().__init__()
        self.on_back = on_back
        self.on_next = on_next
        self.operators_file = "data/operators/operators.json"
        os.makedirs(os.path.dirname(self.operators_file), exist_ok=True)

        # current_job will collect partial job details across steps
        self.current_job = {"job_id": self._generate_job_id()}
        self.operators = []            # loaded operator dictionaries
        self.selected_operator = None  # selected operator dict

        self.init_ui()
        self.load_operators()
        self.refresh_operator_list()

    # ---------------- UI ----------------
    def init_ui(self):
        main = QVBoxLayout()
        main.setSpacing(12)
        main.setContentsMargins(40, 20, 40, 20)

        # Title
        title = QLabel("Create Job — Step 1: Assign Operator")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f0f0f0; padding: 6px;")
        main.addWidget(title)

        # Filters row: Role select + search
        filters = QHBoxLayout()
        self.role_select = QComboBox()
        self.role_select.addItems(self.ROLE_OPTIONS)
        self.role_select.currentTextChanged.connect(self.refresh_operator_list)
        filters.addWidget(QLabel("Operator Role:"))
        filters.addWidget(self.role_select)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by username...")
        self.search_input.textChanged.connect(self.refresh_operator_list)
        filters.addWidget(QLabel("Search:"))
        filters.addWidget(self.search_input)

        # Optional sort selector (by username or name)
        self.sort_select = QComboBox()
        self.sort_select.addItems(["Sort: Username", "Sort: Name"])
        self.sort_select.currentTextChanged.connect(self.refresh_operator_list)
        filters.addWidget(self.sort_select)

        main.addLayout(filters)

        # Body: left = list, right = details
        body = QHBoxLayout()

        # Operator list
        left = QVBoxLayout()
        self.operator_list = QListWidget()
        self.operator_list.setMaximumHeight(200)
        self.operator_list.itemSelectionChanged.connect(self.on_operator_selected)
        left.addWidget(self.operator_list)
        body.addLayout(left, 40)  # ratio

        # Details panel (read-only)
        right = QVBoxLayout()
        details_frame = QFrame()
        details_frame.setFrameShape(QFrame.Shape.StyledPanel)
        details_layout = QVBoxLayout(details_frame)

        self.detail_name = QLabel("Name: ")
        self.detail_username = QLabel("Username: ")
        self.detail_epf = QLabel("EPF Number: ")
        self.detail_role = QLabel("Role: ")

        for w in (self.detail_name, self.detail_username, self.detail_epf, self.detail_role):
            w.setStyleSheet("font-size: 14px; color: #f0f0f0; padding: 4px;")
            details_layout.addWidget(w)

        right.addWidget(details_frame)
        body.addLayout(right, 60)

        main.addLayout(body)

        # Buttons
        buttons = QHBoxLayout()
        self.assign_btn = QPushButton("✅ Assign Operator")
        self.assign_btn.setEnabled(False)
        self.assign_btn.clicked.connect(self.assign_operator)

        self.next_btn = QPushButton("➡️ Next (Select Mold)")
        self.next_btn.clicked.connect(self.goto_next)
        self.next_btn.setEnabled(False)  # enabled once operator assigned

        self.back_btn = QPushButton("⬅️ Back")
        self.back_btn.clicked.connect(self.on_back if self.on_back else lambda: None)

        buttons.addWidget(self.assign_btn)
        buttons.addWidget(self.next_btn)
        buttons.addWidget(self.back_btn)
        main.addLayout(buttons)

        self.setLayout(main)

    # ---------------- Data Loading ----------------
    def load_operators(self):
        """Load operators from JSON file safely."""
        self.operators = []
        if not os.path.exists(self.operators_file):
            return
        try:
            with open(self.operators_file, "r") as f:
                data = json.load(f)
            if isinstance(data, list):
                # Expecting list of dicts
                for entry in data:
                    if isinstance(entry, dict) and "username" in entry:
                        self.operators.append(entry)
            else:
                # handle when file contains None or unexpected structure
                print("Operators file has unexpected structure — ignoring.")
        except Exception as e:
            print(f"Failed to load operators: {e}")
            # don't crash; operators stays empty

    # ---------------- List / Filter / Sort ----------------
    def refresh_operator_list(self):
        """Refresh the list widget based on role filter, search and sort."""
        self.operator_list.clear()
        role_filter = self.role_select.currentText()
        q = self.search_input.text().strip().lower()
        sort_mode = self.sort_select.currentText()

        filtered = []
        for op in self.operators:
            # role filter
            if role_filter != "All Roles" and op.get("role", "") != role_filter:
                continue
            # search by username (partial)
            if q and q not in op.get("username", "").lower():
                continue
            filtered.append(op)

        # sorting
        if sort_mode == "Sort: Name":
            filtered.sort(key=lambda x: x.get("name", "").lower())
        else:
            filtered.sort(key=lambda x: x.get("username", "").lower())

        # populate list widget
        for op in filtered:
            display = f"{op.get('username','')}  —  {op.get('name','')}"
            self.operator_list.addItem(display)

        # clear details & disable assignment until selection
        self.clear_details()
        self.assign_btn.setEnabled(False)

    # ---------------- Selection & Details ----------------
    def on_operator_selected(self):
        selected = self.operator_list.selectedItems()
        if not selected:
            self.selected_operator = None
            self.clear_details()
            self.assign_btn.setEnabled(False)
            return

        text = selected[0].text()
        # text format: "username  —  name"
        username = text.split("—")[0].strip()
        # find operator dict
        self.selected_operator = next((o for o in self.operators if o.get("username") == username), None)
        if not self.selected_operator:
            self.clear_details()
            self.assign_btn.setEnabled(False)
            return

        # populate details
        self.detail_name.setText(f"Name: {self.selected_operator.get('name','')}")
        self.detail_username.setText(f"Username: {self.selected_operator.get('username','')}")
        self.detail_epf.setText(f"EPF Number: {self.selected_operator.get('epf_number','')}")
        self.detail_role.setText(f"Role: {self.selected_operator.get('role','')}")

        self.assign_btn.setEnabled(True)

    def clear_details(self):
        self.detail_name.setText("Name: ")
        self.detail_username.setText("Username: ")
        self.detail_epf.setText("EPF Number: ")
        self.detail_role.setText("Role: ")

    # ---------------- Actions ----------------
    def assign_operator(self):
        """Attach selected operator to current_job and enable Next."""
        if not self.selected_operator:
            QMessageBox.warning(self, "No selection", "Please select an operator first.")
            return

        # attach operator to job
        self.current_job["operator"] = {
            "username": self.selected_operator.get("username"),
            "name": self.selected_operator.get("name"),
            "epf_number": self.selected_operator.get("epf_number"),
            "role": self.selected_operator.get("role")
        }
        QMessageBox.information(self, "Assigned", f"Operator '{self.selected_operator.get('name')}' assigned to job.")
        self.next_btn.setEnabled(True)

    def goto_next(self):
        """Proceed to next step (select mold). Calls on_next callback if provided."""
        if "operator" not in self.current_job:
            QMessageBox.warning(self, "Not assigned", "Please assign an operator before proceeding.")
            return
        # call the next-step callback and pass current_job dict
        if self.on_next:
            self.on_next(self.current_job)
        else:
            QMessageBox.information(self, "Next", "Proceed to mold selection (not implemented).")

    # ---------------- Utility ----------------
    def _generate_job_id(self):
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"JOB_{now}"
