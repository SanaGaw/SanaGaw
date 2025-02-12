# gui/main_window.py

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QProgressBar, QHBoxLayout, QFormLayout
)
from PyQt6.QtCore import Qt
from gui.simulation_thread import SimulationThread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Agent-Based Governance Simulation")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        # Form layout for parameter inputs
        form_layout = QFormLayout()
        self.num_bureaucrats_input = QLineEdit("10")
        self.num_citizens_input = QLineEdit("50")
        self.rounds_input = QLineEdit("30")
        
        form_layout.addRow("Number of Bureaucrats:", self.num_bureaucrats_input)
        form_layout.addRow("Number of Citizens:", self.num_citizens_input)
        form_layout.addRow("Simulation Rounds:", self.rounds_input)

        layout.addLayout(form_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_bar)

        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Run Simulation")
        self.start_button.clicked.connect(self.run_simulation)
        button_layout.addWidget(self.start_button)

        self.results_button = QPushButton("Show Results")
        self.results_button.setEnabled(False)  # Initially disabled
        button_layout.addWidget(self.results_button)

        layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        # Simulation thread
        self.simulation_thread = None

    def run_simulation(self):
        """
        Starts the simulation in a separate thread to prevent UI freezing.
        """
        self.start_button.setEnabled(False)
        self.results_button.setEnabled(False)
        self.status_label.setText("Running simulation...")

        # Retrieve user-defined parameters
        num_bureaucrats = int(self.num_bureaucrats_input.text())
        num_citizens = int(self.num_citizens_input.text())
        rounds = int(self.rounds_input.text())

        # Create and start simulation thread
        self.simulation_thread = SimulationThread(num_bureaucrats, num_citizens, rounds)
        self.simulation_thread.progress_update.connect(self.progress_bar.setValue)
        self.simulation_thread.finished.connect(self.on_simulation_complete)
        self.simulation_thread.start()

    def on_simulation_complete(self):
        """
        Called when the simulation finishes.
        """
        self.start_button.setEnabled(True)
        self.results_button.setEnabled(True)
        self.status_label.setText("Simulation Complete!")
