# Step 7: Introduce Institution, Investigations, and Social Networks
# Goal: Simulate 7 rounds of interactions with institutional oversight, investigation, and network-based corruption influence.

import random
import sys

def handle_interactions(citizens, bureaucrats, params):
    """
    Each citizen requests service from a randomly assigned bureaucrat.
    Honest citizens expect service; bribe-offering citizens may pay corrupt bureaucrats.
    If a citizen is delayed, they will attempt to get service in the next round.
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
                    bureau['tokens'] += params['bribe_amount']  # Configurable bribe amount
                    citizen['needs_service'] = False
                    citizen['satisfaction'] += 1
                else:
                    # Honest bureaucrat denies bribe, normal service
                    citizen['needs_service'] = False
                    citizen['satisfaction'] += 1
                    bureau['interaction_satisfaction'] += 1

def distribute_salaries(bureaucrats, institution, salary=50):
    """
    Each bureaucrat receives a fixed salary at the end of each round, deducted from the institution's budget.
    """
    total_salary = salary * len(bureaucrats)
    if institution['budget'] >= total_salary:
        institution['budget'] -= total_salary
        for bureau in bureaucrats:
            bureau['tokens'] += salary

def handle_investigations(bureaucrats, institution, params):
    """
    The institution investigates a subset of bureaucrats, confiscating tokens from corrupt ones.
    The investigation costs the institution regardless of outcome.
    """
    num_to_investigate = min(len(bureaucrats), params['investigation_rate'])
    investigation_cost = params['investigation_cost'] * num_to_investigate
    
    if institution['budget'] < investigation_cost:
        return []  # No budget for investigation
    
    institution['budget'] -= investigation_cost
    investigated = random.sample(bureaucrats, num_to_investigate)
    
    for bureau in investigated:
        if bureau['state'] == 'corrupt':
            institution['budget'] += bureau['tokens']  # Confiscate illicit gains
            bureau['tokens'] = 0
            bureau['state'] = 'honest'
    return investigated

def update_social_influence(citizens, bureaucrats):
    """
    Citizens and bureaucrats change behavior based on their network influence.
    - A citizen turns corrupt if 3 out of 5 in their network are corrupt or delayed.
    - A bureaucrat turns honest if 3 in their network were investigated.
    - A bureaucrat turns corrupt if they receive a bribe.
    """
    for citizen in citizens:
        corrupt_neighbors = sum(1 for neighbor in citizen['network'] if citizens[neighbor]['state'] == 'bribe_offering')
        delayed_neighbors = sum(1 for neighbor in citizen['network'] if citizens[neighbor]['waiting_time'] > 0)
        if corrupt_neighbors + delayed_neighbors >= 3:
            citizen['state'] = 'bribe_offering'
    
    for bureau in bureaucrats:
        investigated_neighbors = sum(1 for neighbor in bureau['network'] if bureaucrats[neighbor]['state'] == 'honest')
        if investigated_neighbors >= 3:
            bureau['state'] = 'honest'

# Testing Setup
params = {
    'num_citizens': 100,
    'num_bureaucrats': 50,
    'rounds': 7,  # Number of rounds to simulate
    'salary': 5,  # Fixed salary per round for each bureaucrat
    'bribe_amount': 1,  # Configurable bribe amount
    'investigation_rate': 20,  # Number of bureaucrats investigated per round
    'investigation_cost': 4  # Cost per investigation
}

# Initialize Agents and Institution
citizens, bureaucrats = initialize_simulation(params)
institution = {'budget': 1000}

# Logging Data per Round
log_data = []

total_satisfaction_collected = 0

print("\n--- Simulation Starting ---")
sys.stdout.flush()

for round_num in range(1, params['rounds'] + 1):
    handle_interactions(citizens, bureaucrats, params)
    distribute_salaries(bureaucrats, institution, params['salary'])
    investigated = handle_investigations(bureaucrats, institution, params)
    update_social_influence(citizens, bureaucrats)
    
    total_satisfaction_collected += sum(c['satisfaction'] for c in citizens)
    corruption_level = sum(1 for b in bureaucrats if b['state'] == 'corrupt') / len(bureaucrats)
    avg_satisfaction = sum(c['satisfaction'] for c in citizens) / len(citizens)
    total_tokens = sum(b['tokens'] for b in bureaucrats)
    
    log_data.append({
        'round': round_num,
        'corruption_level': corruption_level,
        'avg_satisfaction': avg_satisfaction,
        'total_tokens': total_tokens,
        'total_satisfaction_collected': total_satisfaction_collected,
        'institution_budget': institution['budget']
    })
    
    print(f"Round {round_num}: Corruption Level: {corruption_level:.2f}, Avg Satisfaction: {avg_satisfaction:.2f}, Total Tokens: {total_tokens}, Institution Budget: {institution['budget']}")
    sys.stdout.flush()

print("\n--- Simulation Complete ---")
sys.stdout.flush()

# Print Logged Data
print("\nSimulation Log:")
for entry in log_data:
    print(entry)
    sys.stdout.flush()
