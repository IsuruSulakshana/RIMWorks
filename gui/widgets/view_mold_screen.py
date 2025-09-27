from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit,
    QListWidget, QPushButton, QMessageBox, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
import json
import os
from datetime import date, datetime

class ViewMoldScreen(QWidget):
    def __init__(self, on_back=None):
        super().__init__()
        self.on_back = on_back
        self.data_folder = "data/molds"
        os.makedirs(self.data_folder, exist_ok=True)
        self.mold_files = []
        self.selected_mold_data = None
        self.init_ui()
        self.refresh_filters()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(40, 20, 40, 20)

        # --- Filters Row ---
        filters_layout = QHBoxLayout()

        self.vehicle_filter = QComboBox()
        self.vehicle_filter.addItem("All Vehicles")
        self.vehicle_filter.currentTextChanged.connect(self.refresh_mold_list)
        filters_layout.addWidget(QLabel("Vehicle:"))
        filters_layout.addWidget(self.vehicle_filter)

        self.system_filter = QComboBox()
        self.system_filter.addItem("All Systems")
        self.system_filter.addItems(["Steering", "Braking", "Suspension", "Other"])
        self.system_filter.currentTextChanged.connect(self.refresh_mold_list)
        filters_layout.addWidget(QLabel("System:"))
        filters_layout.addWidget(self.system_filter)

        self.mold_type_filter = QComboBox()
        self.mold_type_filter.addItem("All Mold Types")
        self.mold_type_filter.addItems(["Soft Silicon", "Hard Silicon"])
        self.mold_type_filter.currentTextChanged.connect(self.refresh_mold_list)
        filters_layout.addWidget(QLabel("Mold Type:"))
        filters_layout.addWidget(self.mold_type_filter)

        self.chemical_filter = QComboBox()
        self.chemical_filter.addItem("All Chemicals")
        self.chemical_filter.addItems(["A","B","C","D"])
        self.chemical_filter.currentTextChanged.connect(self.refresh_mold_list)
        filters_layout.addWidget(QLabel("Chemical:"))
        filters_layout.addWidget(self.chemical_filter)

        self.mixing_filter = QComboBox()
        self.mixing_filter.addItem("All Mixing Ratios")
        self.mixing_filter.addItems(["A","B","C","D","E","F","G","H","I","J"])
        self.mixing_filter.currentTextChanged.connect(self.refresh_mold_list)
        filters_layout.addWidget(QLabel("Mixing Ratio:"))
        filters_layout.addWidget(self.mixing_filter)

        self.date_filter = QComboBox()
        self.date_filter.addItem("All Dates")
        self.date_filter.currentTextChanged.connect(self.refresh_mold_list)
        filters_layout.addWidget(QLabel("Date:"))
        filters_layout.addWidget(self.date_filter)

        layout.addLayout(filters_layout)

        # --- Search Bar ---
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Part Number...")
        self.search_input.textChanged.connect(self.refresh_mold_list)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # --- Mold List ---
        self.mold_list_widget = QListWidget()
        self.mold_list_widget.setMaximumHeight(200)  # Reduced height
        self.mold_list_widget.itemSelectionChanged.connect(self.display_selected_mold)
        layout.addWidget(self.mold_list_widget)

        # --- Mold Details Frame ---
        self.details_frame = QFrame()
        self.details_layout = QVBoxLayout()
        self.details_frame.setLayout(self.details_layout)
        layout.addWidget(self.details_frame)

        # --- Action Buttons ---
        button_layout = QHBoxLayout()
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.clicked.connect(self.delete_selected_mold)
        self.back_btn = QPushButton("⬅️ Back")
        self.back_btn.clicked.connect(self.on_back if self.on_back else lambda: None)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.back_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    # ------------------ Load filters ------------------
    def refresh_filters(self):
        vehicles = set()
        dates = set()
        self.mold_files = [f for f in os.listdir(self.data_folder) if f.endswith(".json")]
        for file in self.mold_files:
            path = os.path.join(self.data_folder, file)
            with open(path, "r") as f:
                data = json.load(f)
                vehicles.add(data.get("vehicle", ""))
                date = data.get("created_at", "")
                if date:
                    dates.add(date)
        # Update dropdowns
        self.vehicle_filter.clear()
        self.vehicle_filter.addItem("All Vehicles")
        self.vehicle_filter.addItems(sorted(vehicles))

        self.date_filter.clear()
        self.date_filter.addItem("All Dates")
        self.date_filter.addItems(sorted(dates))

        # Refresh list
        self.refresh_mold_list()

    # ------------------ Mold List ------------------
    def refresh_mold_list(self):
        self.mold_list_widget.clear()
        for file in self.mold_files:
            path = os.path.join(self.data_folder, file)
            with open(path, "r") as f:
                data = json.load(f)
            # Apply filters
            if self.vehicle_filter.currentText() != "All Vehicles" and data.get("vehicle") != self.vehicle_filter.currentText():
                continue
            if self.system_filter.currentText() != "All Systems" and data.get("system") != self.system_filter.currentText():
                continue
            if self.mold_type_filter.currentText() != "All Mold Types" and data.get("mold_type") != self.mold_type_filter.currentText():
                continue
            if self.chemical_filter.currentText() != "All Chemicals" and data.get("chemical_type") != self.chemical_filter.currentText():
                continue
            if self.mixing_filter.currentText() != "All Mixing Ratios" and data.get("mixing_ratio") != self.mixing_filter.currentText():
                continue
            if self.date_filter.currentText() != "All Dates" and data.get("created_at") != self.date_filter.currentText():
                continue
            if self.search_input.text().strip() and self.search_input.text().strip().lower() not in data.get("part_number", "").lower():
                continue
            self.mold_list_widget.addItem(data.get("mold_name"))

    # ------------------ Display Selected Mold ------------------
    def display_selected_mold(self):
        # Clear previous widgets without removing layout
        for i in reversed(range(self.details_layout.count())):
            widget = self.details_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        selected_items = self.mold_list_widget.selectedItems()
        if not selected_items:
            return

        selected_name = selected_items[0].text()
        self.selected_mold_data = None
        for file in self.mold_files:
            path = os.path.join(self.data_folder, file)
            with open(path, "r") as f:
                data = json.load(f)
            if data.get("mold_name") == selected_name:
                self.selected_mold_data = data
                break

        if not self.selected_mold_data:
            return

        # Display all mold info
        for key, value in self.selected_mold_data.items():
            self.details_layout.addWidget(QLabel(f"{key}: {value}"))

    # ------------------ Delete Mold ------------------
    def delete_selected_mold(self):
        if not self.selected_mold_data:
            QMessageBox.warning(self, "No selection", "Please select a mold to delete.")
            return
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete mold '{self.selected_mold_data.get('mold_name')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            file_path = os.path.join(self.data_folder, f"{self.selected_mold_data.get('mold_name')}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
            self.selected_mold_data = None
            self.refresh_filters()
            # Clear details layout
            for i in reversed(range(self.details_layout.count())):
                widget = self.details_layout.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            QMessageBox.information(self, "Deleted", "Mold deleted successfully.")
            with open(file_path, "w") as f:
                json.dump(self.selected_mold_data, f, indent=4)