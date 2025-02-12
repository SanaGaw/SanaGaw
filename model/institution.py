# model/institution.py

from config.parameters import INVESTIGATION_COST, IC_INITIAL, TOKEN_LOSS_CORRUPT

class Institution:
    """
    The institution monitors bureaucrats, conducts investigations,
    and updates institutional credibility (IC).
    """
    def __init__(self, init_ic=IC_INITIAL):
        self.ic = init_ic  # institutional credibility

    def investigate_bureaucrats(self, bureaucrats, strategy_func):
        """
        Investigate bureaucrats using a given strategy (passed as strategy_func).
        The strategy function decides who to investigate.
        Returns the list of investigated bureaucrats for further processing.
        """
        to_investigate = strategy_func(bureaucrats, self.ic)
        # Pay the cost for each investigated bureaucrat
        total_cost = INVESTIGATION_COST * len(to_investigate)

        if self.ic >= total_cost:
            self.ic -= total_cost  # reduce IC by cost
            return to_investigate
        else:
            # Not enough resources (IC) to investigate everyone chosen;
            # investigate fewer or none, as a simple fallback
            return []

    def update_ic(self, citizen_satisfactions):
        """
        Example: Recalculate institutional credibility based on citizen satisfaction.
        The model's formula or approach might vary. This is simplified.
        """
        if not citizen_satisfactions:
            return

        avg_sat = sum(citizen_satisfactions) / len(citizen_satisfactions)
        # Example: average between current IC and average satisfaction (like the given formula)
        self.ic = (self.ic + avg_sat) / 2

    def reactive_mode(self):
        """
        Check if the institution is in reactive mode (IC < threshold).
        """
        return (self.ic < 0.4)
