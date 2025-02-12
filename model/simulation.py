# model/simulation.py

import random
from config.parameters import (
    NUM_BUREAUCRATS, NUM_CITIZENS, INITIAL_CORRUPTION_RATE,
    INITIAL_CORRUPT_CITIZEN_RATE, ROUNDS, TOKEN_LOSS_CORRUPT
)
from .entities import Citizen, Bureaucrat
from .institution import Institution

class Simulation:
    def __init__(self, governance_strategy, 
                 num_bureaucrats=NUM_BUREAUCRATS,
                 num_citizens=NUM_CITIZENS,
                 init_corr_rate=INITIAL_CORRUPTION_RATE,
                 init_corr_cit_rate=INITIAL_CORRUPT_CITIZEN_RATE,
                 rounds=ROUNDS):
        """
        governance_strategy: a function that the institution uses to decide who to investigate
        """
        self.governance_strategy = governance_strategy
        self.num_bureaucrats = num_bureaucrats
        self.num_citizens = num_citizens
        self.init_corr_rate = init_corr_rate
        self.init_corr_cit_rate = init_corr_cit_rate
        self.rounds = rounds

        # Create agent lists
        self.bureaucrats = self._init_bureaucrats()
        self.citizens = self._init_citizens()

        # Create institution
        self.institution = Institution()

        # For tracking
        self.history_ic = []
        self.history_corruption_rate = []
        self.history_satisfaction = []

    def _init_bureaucrats(self):
        bureaus = []
        for i in range(self.num_bureaucrats):
            is_corr = (random.random() < self.init_corr_rate)
            bureaus.append(Bureaucrat(bureaucrat_id=i, is_corrupt=is_corr))
        return bureaus

    def _init_citizens(self):
        cits = []
        for i in range(self.num_citizens):
            is_corr = (random.random() < self.init_corr_cit_rate)
            cits.append(Citizen(citizen_id=i, is_corrupt=is_corr))
        return cits

    def run(self):
        """
        Run the simulation for the specified number of rounds.
        """
        for round_idx in range(self.rounds):
            # 1. Citizen-Bureaucrat Interactions
            citizen_satisfactions = self._run_interactions()

            # 2. Update Institutional Credibility
            self.institution.update_ic(citizen_satisfactions)

            # 3. Investigate Bureaucrats
            investigated = self.institution.investigate_bureaucrats(
                self.bureaucrats, 
                strategy_func=self.governance_strategy
            )

            # 4. If found corrupt, they lose tokens
            for b in investigated:
                if b.is_corrupt:
                    b.reported = True
                    b.lose_tokens_if_reported(TOKEN_LOSS_CORRUPT)

            # 5. Bureaucrats adapt behavior (switch to honest/corrupt)
            self._adapt_bureaucrats(investigated)

            # 6. Calculate metrics & record history
            self.history_ic.append(self.institution.ic)
            self.history_corruption_rate.append(self._compute_corruption_rate())
            self.history_satisfaction.append(sum(citizen_satisfactions)/len(citizen_satisfactions)
                                             if len(citizen_satisfactions) > 0 else 0)

    def _run_interactions(self):
        """
        Simulate citizen-bureaucrat interactions for this round.
        Returns a list of satisfaction scores from all citizen interactions.
        """
        satisfactions = []
        # Shuffle or randomize interactions
        random.shuffle(self.citizens)

        # Each bureaucrat can serve up to 5 interactions (as per the original model)
        # We'll do a simple chunk-based approach
        chunk_size = 5

        for i, b in enumerate(self.bureaucrats):
            # For the current bureaucrat, pick a subset of citizens
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size
            relevant_citizens = self.citizens[start_idx:end_idx] if end_idx <= len(self.citizens) else []

            # Each citizen interacts with bureaucrat
            for c in relevant_citizens:
                result = c.request_service(b)
                satisfactions.append(result)

        return satisfactions

    def _adapt_bureaucrats(self, investigated_bureaucrats):
        """
        Update each bureaucrat's corrupt/honest state based on investigations & earnings logic.
        """
        # For demonstration, let's compute the average tokens of corrupt bureaucrats
        corrupt_bureaucrats = [b for b in self.bureaucrats if b.is_corrupt]
        if len(corrupt_bureaucrats) > 0:
            avg_corrupt_earnings = sum([b.tokens for b in corrupt_bureaucrats]) / len(corrupt_bureaucrats)
        else:
            avg_corrupt_earnings = 0.0

        investigated_ids = {b.id for b in investigated_bureaucrats}

        for b in self.bureaucrats:
            # How many peers were investigated?
            # For simplicity, let's pass the total number of investigated peers
            peers_investigated = len(investigated_ids) if b.id not in investigated_ids else len(investigated_ids) - 1

            b.maybe_switch_behavior(peers_investigated, avg_corrupt_earnings)
            # Reset reported status each round
            b.reported = False

    def _compute_corruption_rate(self):
        corr_count = sum(1 for b in self.bureaucrats if b.is_corrupt)
        return corr_count / len(self.bureaucrats)

    def get_results(self):
        """
        Return final or historical data for analysis or plotting.
        """
        return {
            "ic_history": self.history_ic,
            "corruption_history": self.history_corruption_rate,
            "satisfaction_history": self.history_satisfaction
        }
