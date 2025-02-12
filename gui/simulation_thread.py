# gui/simulation_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
from model.simulation import Simulation
from strategies.strategies import pragmatic_strategy

class SimulationThread(QThread):
    progress_update = pyqtSignal(int)  # Signal to update progress bar

    def __init__(self, num_bureaucrats, num_citizens, rounds):
        super().__init__()
        self.num_bureaucrats = num_bureaucrats
        self.num_citizens = num_citizens
        self.rounds = rounds
        self.results = None

    def run(self):
        """
        Runs the simulation in a loop, updating progress after each round.
        """
        sim = Simulation(governance_strategy=pragmatic_strategy,
                         num_bureaucrats=self.num_bureaucrats,
                         num_citizens=self.num_citizens,
                         rounds=self.rounds)

        for i in range(self.rounds):
            sim.run()
            progress = int(((i + 1) / self.rounds) * 100)
            self.progress_update.emit(progress)

        self.results = sim.get_results()
