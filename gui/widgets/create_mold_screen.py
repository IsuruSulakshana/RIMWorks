# gui/widgets/create_mold_screen.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QSpinBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
import json, os, datetime

class CreateMoldScreen(QWidget):
    SYSTEMS = ["Steering", "Braking", "Suspension", "Other"]
    MOLD_TYPES = ["Soft Silicon", "Hard Silicon"]
    CREATION_TYPES = ["Previous mold life complete", "New part"]

    def __init__(self, on_back=None):
        super().__init__()
        self.on_back = on_back
        self.data_folder = "data/molds"
        os.makedirs(self.data_folder, exist_ok=True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        # --- Vehicle ---
        vehicle_layout = QHBoxLayout()
        self.vehicle_input = QLineEdit()
        self.vehicle_input.setPlaceholderText("brand|model|gen")
        vehicle_layout.addWidget(QLabel("Vehicle:"))
        vehicle_layout.addWidget(self.vehicle_input)

        # System selection
        self.system_input = QComboBox()
        self.system_input.addItems(self.SYSTEMS)
        self.system_input.currentTextChanged.connect(self.update_mold_name)
        vehicle_layout.addWidget(QLabel("System:"))
        vehicle_layout.addWidget(self.system_input)
        layout.addLayout(vehicle_layout)

        # --- Mold Type ---
        mold_type_layout = QHBoxLayout()
        self.mold_type_input = QComboBox()
        self.mold_type_input.addItems(self.MOLD_TYPES)
        mold_type_layout.addWidget(QLabel("Mold Type:"))
        mold_type_layout.addWidget(self.mold_type_input)
        layout.addLayout(mold_type_layout)

        # --- Mold Name (auto-generated) ---
        mold_name_layout = QHBoxLayout()
        self.mold_name_input = QLineEdit()
        self.mold_name_input.setPlaceholderText("Mold Name (auto-generated)")
        mold_name_layout.addWidget(QLabel("Mold Name:"))
        mold_name_layout.addWidget(self.mold_name_input)
        layout.addLayout(mold_name_layout)

        # --- Mold Number ---
        mold_number_layout = QHBoxLayout()
        self.mold_number_input = QLineEdit()
        self.mold_number_input.setPlaceholderText("Mold Number")
        mold_number_layout.addWidget(QLabel("Mold Number:"))
        mold_number_layout.addWidget(self.mold_number_input)
        layout.addLayout(mold_number_layout)

        # --- Life Span ---
        life_layout = QHBoxLayout()
        self.life_input = QSpinBox()
        self.life_input.setRange(1, 10000)
        life_layout.addWidget(QLabel("Life Span (cycles):"))
        life_layout.addWidget(self.life_input)
        layout.addLayout(life_layout)

        # --- Part Number ---
        part_layout = QHBoxLayout()
        self.part_input = QLineEdit()
        self.part_input.setPlaceholderText("Part Number")
        part_layout.addWidget(QLabel("Part Number:"))
        part_layout.addWidget(self.part_input)
        layout.addLayout(part_layout)

        # --- Mixing Ratio ---
        mixing_layout = QHBoxLayout()
        self.mixing_ratio_input = QComboBox()
        # temp values until calibration machine integration
        self.mixing_ratio_input.addItems(["A","B","C","D","E","F","G","H","I","J"])
        mixing_layout.addWidget(QLabel("Mixing Ratio:"))
        mixing_layout.addWidget(self.mixing_ratio_input)
        layout.addLayout(mixing_layout)

        # --- Chemical Type ---
        chemical_layout = QHBoxLayout()
        self.chemical_type_input = QComboBox()
        self.chemical_type_input.addItems(["A", "B", "C", "D"])
        chemical_layout.addWidget(QLabel("Chemical Type:"))
        chemical_layout.addWidget(self.chemical_type_input)
        layout.addLayout(chemical_layout)

        # --- Creation Type ---
        creation_layout = QHBoxLayout()
        self.creation_type_input = QComboBox()
        self.creation_type_input.addItems(self.CREATION_TYPES)
        creation_layout.addWidget(QLabel("Creation Type:"))
        creation_layout.addWidget(self.creation_type_input)
        layout.addLayout(creation_layout)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save Mold")
        save_btn.clicked.connect(self.save_mold)

        # BACK BUTTON
        self.back_btn = QPushButton("🔙 Back")
        self.back_btn.clicked.connect(self.on_back if self.on_back else lambda: None)

        button_layout.addWidget(save_btn)
        button_layout.addWidget(self.back_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.vehicle_input.textChanged.connect(self.update_mold_name)

    def update_mold_name(self):
        vehicle = self.vehicle_input.text().strip()
        system = self.system_input.currentText().strip()
        if vehicle and system:
            self.mold_name_input.setText(f"{vehicle}_{system}")

    def save_mold(self):
        vehicle = self.vehicle_input.text().strip()
        system = self.system_input.currentText().strip()
        mold_name = self.mold_name_input.text().strip()
        mold_type = self.mold_type_input.currentText().strip()
        mold_number = self.mold_number_input.text().strip()
        life_span = self.life_input.value()
        part_number = self.part_input.text().strip()
        creation_type = self.creation_type_input.currentText().strip()
        mixing_ratio = self.mixing_ratio_input.currentText()
        chemical_type = self.chemical_type_input.currentText()

        if not all([vehicle, system, mold_name, mold_type, mold_number, part_number]):
            QMessageBox.warning(self, "Missing Info", "Please fill all mandatory fields.")
            return

        # Save with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{mold_name}_{timestamp}.json"

        data = {
            "vehicle": vehicle,
            "system": system,
            "mold_name": mold_name,
            "mold_type": mold_type,
            "mold_number": mold_number,
            "life_span": life_span,
            "part_number": part_number,
            "creation_type": creation_type,
            "mixing_ratio": mixing_ratio,
            "chemical_type": chemical_type,
            "timestamp": timestamp
        }

        try:
            file_path = os.path.join(self.data_folder, file_name)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
            QMessageBox.information(self, "Success", f"Mold saved:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save mold:\n{str(e)}")
