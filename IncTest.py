# Step 6: Full Interaction Logging Over Multiple Rounds
# Goal: Simulate 7 rounds of interactions where bureaucrats receive salaries and corrupt ones collect bribes.

import random
import sys

def handle_interactions(citizens, bureaucrats):
    """
    Each citizen requests service from a randomly assigned bureaucrat.
    Honest citizens expect service; bribe-offering citizens may pay corrupt bureaucrats.
    """
    for citizen in citizens:
        if citizen['needs_service']:
            # Assign a random bureaucrat
            bureau = random.choice(bureaucrats)
            
            if citizen['state'] == 'honest':
                if bureau['state'] == 'honest':
                    # Citizen gets service immediately
                    citizen['needs_service'] = False
                    citizen['satisfaction'] += 1
                    bureau['interaction_satisfaction'] += 1
                else:
                    # Citizen must wait if the bureaucrat is corrupt
                    citizen['waiting_time'] += 1
                    bureau['interaction_satisfaction'] -= 1
            else:  # bribe_offering citizen
                if bureau['state'] == 'corrupt':
                    # Bribe transaction occurs
                    bureau['tokens'] += 10  # Arbitrary bribe amount
                    citizen['needs_service'] = False
                    citizen['satisfaction'] += 1
                else:
                    # Honest bureaucrat denies bribe, normal service
                    citizen['needs_service'] = False
                    citizen['satisfaction'] += 1
                    bureau['interaction_satisfaction'] += 1

def distribute_salaries(bureaucrats, salary=50):
    """
    Each bureaucrat receives a fixed salary at the end of each round.
    """
    for bureau in bureaucrats:
        bureau['tokens'] += salary

def initialize_simulation(params):
    """
    Initializes citizens and bureaucrats based on given parameters.
    """
    citizens = [{
        'id': i,
        'state': random.choice(['honest', 'bribe_offering']),
        'satisfaction': 0,
        'needs_service': True,
        'interaction_count': 0,
        'waiting_time': 0
    } for i in range(params['num_citizens'])]

    bureaucrats = [{
        'id': i,
        'state': random.choice(['honest', 'corrupt']),
        'interaction_satisfaction': 0,
        'tokens': 0  # Bureaucrats start with zero tokens
    } for i in range(params['num_bureaucrats'])]

    return citizens, bureaucrats

# Testing Setup
params = {
    'num_citizens': 10,
    'num_bureaucrats': 5,
    'rounds': 7,  # Number of rounds to simulate
    'salary': 50  # Fixed salary per round for each bureaucrat
}

# Initialize Agents
citizens, bureaucrats = initialize_simulation(params)

# Logging Data per Round
log_data = []

print("\n--- Simulation Starting ---")
sys.stdout.flush()

for round_num in range(1, params['rounds'] + 1):
    handle_interactions(citizens, bureaucrats)
    distribute_salaries(bureaucrats, params['salary'])
    
    corruption_level = sum(1 for b in bureaucrats if b['state'] == 'corrupt') / len(bureaucrats)
    avg_satisfaction = sum(c['satisfaction'] for c in citizens) / len(citizens)
    total_tokens = sum(b['tokens'] for b in bureaucrats)
    
    log_data.append({
        'round': round_num,
        'corruption_level': corruption_level,
        'avg_satisfaction': avg_satisfaction,
        'total_tokens': total_tokens
    })
    
    print(f"Round {round_num}: Corruption Level: {corruption_level:.2f}, Avg Satisfaction: {avg_satisfaction:.2f}, Total Tokens: {total_tokens}")
    sys.stdout.flush()

print("\n--- Simulation Complete ---")
sys.stdout.flush()

# Print Logged Data
print("\nSimulation Log:")
for entry in log_data:
    print(entry)
    sys.stdout.flush()

# Ensure no negative tokens exist
assert all(bureaucrat['tokens'] >= 0 for bureaucrat in bureaucrats), "Error: Negative token count found."

# Ensure satisfaction is within logical bounds
assert all(0 <= citizen['satisfaction'] <= params['rounds'] for citizen in citizens), "Error: Invalid satisfaction values."

# Ensure waiting times are not negative
assert all(citizen['waiting_time'] >= 0 for citizen in citizens), "Error: Negative waiting time detected."
