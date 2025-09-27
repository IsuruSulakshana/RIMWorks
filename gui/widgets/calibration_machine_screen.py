# gui/widgets/calibration_machine_screen.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
import os, json
from datetime import datetime

class CalibrationMachineScreen(QWidget):
    RATIOS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

    def __init__(self, on_back=None):
        super().__init__()
        self.on_back = on_back
        self.data_folder = "data/calibration"
        os.makedirs(self.data_folder, exist_ok=True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        # Title
        title = QLabel("Calibration Machine")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #f0f0f0;")
        layout.addWidget(title)

        # --- Mixing Ratio Inputs ---
        self.ratio_inputs = {}
        for ratio in self.RATIOS:
            row_layout = QHBoxLayout()
            row_layout.addWidget(QLabel(f"{ratio}:"))

            min_input = QLineEdit()
            min_input.setPlaceholderText("Min")
            min_input.setMaximumWidth(80)
            row_layout.addWidget(min_input)

            max_input = QLineEdit()
            max_input.setPlaceholderText("Max")
            max_input.setMaximumWidth(80)
            row_layout.addWidget(max_input)

            layout.addLayout(row_layout)
            self.ratio_inputs[ratio] = (min_input, max_input)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save Calibration")
        self.back_btn = QPushButton("⬅️ Back")

        save_btn.clicked.connect(self.save_calibration)
        self.back_btn.clicked.connect(self.on_back if self.on_back else lambda: None)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(self.back_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def save_calibration(self):
        data = {}
        for ratio, (min_input, max_input) in self.ratio_inputs.items():
            min_val = min_input.text().strip()
            max_val = max_input.text().strip()
            if not min_val or not max_val:
                QMessageBox.warning(self, "Missing Info", f"Please enter values for {ratio}.")
                return
            try:
                min_val = float(min_val)
                max_val = float(max_val)
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", f"{ratio} values must be numbers.")
                return
            data[ratio] = {"min": min_val, "max": max_val}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.data_folder, f"calibration_{timestamp}.json")
        try:
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Saved", f"Calibration saved:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save calibration:\n{str(e)}")
