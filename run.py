# run.py

import sys
from model.simulation import Simulation
from strategies.strategies import (
    pragmatic_strategy,
    corruption_minimizing_strategy,
    firefighting_strategy
)

def main():
    # Example usage: 
    # python run.py pragmatic
    # python run.py corruption_minimizing
    # python run.py firefighting

    if len(sys.argv) > 1:
        strategy_name = sys.argv[1].lower()
    else:
        # Default
        strategy_name = "pragmatic"

    if strategy_name == "pragmatic":
        chosen_strategy = pragmatic_strategy
    elif strategy_name == "corruption_minimizing":
        chosen_strategy = corruption_minimizing_strategy
    elif strategy_name == "firefighting":
        chosen_strategy = firefighting_strategy
    else:
        print("Unknown strategy. Defaulting to pragmatic.")
        chosen_strategy = pragmatic_strategy

    # Create and run simulation
    sim = Simulation(governance_strategy=chosen_strategy)
    sim.run()

    # Retrieve and print results
    results = sim.get_results()
    print("Final Institutional Credibility:", results["ic_history"][-1])
    print("Final Corruption Rate:", results["corruption_history"][-1])
    print("Final Average Satisfaction:", results["satisfaction_history"][-1])

    # Optional: Plot or save results here (requires matplotlib or similar)

if __name__ == "__main__":
    main()
