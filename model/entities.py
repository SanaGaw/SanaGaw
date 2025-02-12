# model/entities.py

import random
from config.parameters import BRIBE_AMOUNT, HONEST_EARNING

class Citizen:
    """
    Citizens may be honest or corrupt.
    They seek services from bureaucrats and provide satisfaction feedback.
    """
    def __init__(self, citizen_id, is_corrupt=False):
        self.id = citizen_id
        self.is_corrupt = is_corrupt
        self.satisfaction = 0  # track satisfaction from each interaction

    def request_service(self, bureaucrat):
        """
        Interact with a bureaucrat, attempt to bribe if corrupt,
        or expect fair service if honest.
        Returns satisfaction outcome (e.g., +1, 0, -1).
        """
        if self.is_corrupt:
            # Attempt to bribe
            success = bureaucrat.accept_bribe()
            if success:
                # Service provided quickly, satisfaction = 0 (as per the model)
                return 0
            else:
                # Bribe failed, might reduce satisfaction further
                return -1
        else:
            # Honest citizen expects fair service
            # Bureaucrat might delay or provide normal service
            delayed = bureaucrat.process_honest_request()
            if delayed:
                # If delayed or poorly served
                return -1
            else:
                # Correctly served
                return +1

    def maybe_switch_behavior(self, service_outcomes):
        """
        Optional logic: If honest citizen gets -1 repeatedly, might turn corrupt.
        If corrupt citizen fails bribes repeatedly, might revert to honesty.
        For simplicity, we just show a placeholder.
        """
        # Example logic:
        if not self.is_corrupt:
            if service_outcomes.count(-1) > 2:  # got delayed 3+ times
                self.is_corrupt = True
        else:
            if service_outcomes.count(-1) > 2:  # bribes failed multiple times
                self.is_corrupt = False


class Bureaucrat:
    """
    Bureaucrats can be honest or corrupt.
    They earn tokens from honest work or bribes.
    They can also switch behavior if risk or earnings push them.
    """
    def __init__(self, bureaucrat_id, is_corrupt=False):
        self.id = bureaucrat_id
        self.is_corrupt = is_corrupt
        self.tokens = 0.0
        self.reported = False  # will be set if found corrupt in investigations

    def accept_bribe(self):
        """
        If corrupt, accept bribe and add tokens. Return True if successful, False otherwise.
        """
        if self.is_corrupt:
            self.tokens += BRIBE_AMOUNT
            # In a real model, might factor in chance of detection here
            return True
        else:
            # Honest bureaucrat does not accept bribes
            return False

    def process_honest_request(self):
        """
        Handle service for an honest citizen.
        Return True if there's a delay (corrupt bureaucrat might deprioritize),
        False if served properly.
        """
        if self.is_corrupt:
            # Possibly delay honest citizens
            # For simplicity, let's assume a 50% chance of delay
            delayed = random.random() < 0.5
            if not delayed:
                # If not delayed, no tokens earned from an honest request
                # (the model says a corrupt bureaucrat doesn't earn standard token from honest service)
                pass
            return delayed
        else:
            # Honest bureaucrat: gain small token earning
            self.tokens += HONEST_EARNING
            return False

    def lose_tokens_if_reported(self, fraction):
        """
        If reported as corrupt, bureaucrat loses a fraction of accumulated tokens.
        """
        if self.is_corrupt and self.reported:
            self.tokens *= (1 - fraction)

    def maybe_switch_behavior(self, peers_investigated, avg_corrupt_earnings):
        """
        Corrupt -> Honest switch if many peers are investigated (risk is high).
        Honest -> Corrupt switch if corrupt peers earn significantly more.
        """
        # If corrupt and the number of investigated peers is high, switch to honest
        if self.is_corrupt and peers_investigated >= 3:
            self.is_corrupt = False

        # If honest and the average corrupt earnings is significantly higher, switch to corrupt
        if not self.is_corrupt and self.tokens < avg_corrupt_earnings:
            self.is_corrupt = True
