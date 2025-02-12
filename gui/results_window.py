# gui/results_window.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class ResultsWindow(QWidget):
    def __init__(self, results):
        super().__init__()

        self.setWindowTitle("Simulation Results")
        self.setGeometry(250, 250, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Simulation Outcomes")
        layout.addWidget(self.label)

        # Create table
        self.table = QTableWidget()
        self.table.setRowCount(3)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Metric", "Value"])

        # Fill table
        data = [
            ("Final Institutional Credibility", results["ic_history"][-1]),
            ("Final Corruption Rate", results["corruption_history"][-1]),
            ("Final Average Satisfaction", results["satisfaction_history"][-1])
        ]

        for row, (metric, value) in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(metric))
            self.table.setItem(row, 1, QTableWidgetItem(str(value)))

        layout.addWidget(self.table)
        self.setLayout(layout)
