import random
import sys

######################################################
# INITIALIZATION
######################################################
def initialize_simulation(params):
    """
    Initializes citizens and bureaucrats with their initial states and networks.
    Uses 'initial_corruption_citizens' and 'initial_corruption_bureaucrats' to set corruption fraction.
    """
    num_citizens = params['num_citizens']
    num_bureaucrats = params['num_bureaucrats']

    # Create citizens
    citizens = []
    for i in range(num_citizens):
        is_corrupt = (random.random() < params['initial_corruption_citizens'])
        citizens.append({
            'id': i,
            'state': 'bribe_offering' if is_corrupt else 'honest',
            'satisfaction': 0,
            'needs_service': True,
            'interaction_count': 0,
            'waiting_time': 0,
            'network': []
        })

    # Create bureaucrats
    bureaucrats = []
    for i in range(num_bureaucrats):
        is_corrupt = (random.random() < params['initial_corruption_bureaucrats'])
        bureaucrats.append({
            'id': i,
            'state': 'corrupt' if is_corrupt else 'honest',
            'interaction_satisfaction': 0,   # immediate round-based satisfaction
            'tokens': 0,
            'network': [],
            'investigations': 0,            # how many times they've been investigated
            'accumulated_satisfaction': 0   # total citizen satisfaction credited
        })

    # Assign up to 5 random same-type neighbors as their "network"
    for c in citizens:
        others = [x for x in citizens if x['id'] != c['id']]
        c['network'] = random.sample(others, min(5, len(others)))

    for b in bureaucrats:
        others = [x for x in bureaucrats if x['id'] != b['id']]
        b['network'] = random.sample(others, min(5, len(others)))

    return citizens, bureaucrats


######################################################
# INTERACTIONS
######################################################
def handle_interactions(citizens, bureaucrats, params):
    """
    Each citizen requests service from a randomly assigned bureaucrat.
    Honest citizens expect service; bribe-offering citizens may pay corrupt bureaucrats.
    If a citizen is delayed, they will attempt to get service in the next round.
    """
    for citizen in citizens:
        if citizen['needs_service'] and bureaucrats:
            bureau = random.choice(bureaucrats)
            # if citizen is honest
            if citizen['state'] == 'honest':
                if bureau['state'] == 'honest':
                    # service is immediate
                    citizen['needs_service'] = False
                    citizen['satisfaction'] += 1
                    bureau['interaction_satisfaction'] += 1
                    bureau['accumulated_satisfaction'] += 1
                else:
                    # citizen must wait if bureau is corrupt
                    citizen['waiting_time'] += 1
                    bureau['interaction_satisfaction'] -= 1
            else:
                # citizen is bribe_offering
                if bureau['state'] == 'corrupt':
                    # bribe transaction
                    bureau['tokens'] += params['bribe_amount']
                    citizen['needs_service'] = False
                    citizen['satisfaction'] += 1
                else:
                    # honest bureaucrat denies bribe, but grants service
                    citizen['needs_service'] = False
                    citizen['satisfaction'] += 1
                    bureau['interaction_satisfaction'] += 1
                    bureau['accumulated_satisfaction'] += 1


######################################################
# SALARIES
######################################################
def distribute_salaries(bureaucrats, institution, salary=50):
    """
    Deduct from institution's budget and pay each bureaucrat a fixed salary.
    """
    total_salary = salary * len(bureaucrats)
    if institution['budget'] >= total_salary:
        institution['budget'] -= total_salary
        for bureau in bureaucrats:
            bureau['tokens'] += salary


######################################################
# INVESTIGATIONS
######################################################
def handle_investigations(bureaucrats, institution, params):
    """
    Investigate a subset of bureaucrats, confiscate tokens from corrupt ones.
    Cost is deducted from institution's budget.
    """
    num_to_investigate = min(len(bureaucrats), params['investigation_rate'])
    investigation_cost = params['investigation_cost'] * num_to_investigate

    if institution['budget'] < investigation_cost:
        return [], 0  # no budget for investigations

    institution['budget'] -= investigation_cost
    investigated = random.sample(bureaucrats, num_to_investigate)
    confiscated_tokens = 0

    for bureau in investigated:
        bureau['investigations'] += 1  # track that they've been investigated
        if bureau['state'] == 'corrupt':
            confiscated_tokens += bureau['tokens']
            institution['budget'] += bureau['tokens']
            bureau['tokens'] = 0
            bureau['state'] = 'honest'

    return investigated, confiscated_tokens


######################################################
# SOCIAL INFLUENCE
######################################################
def update_social_influence(citizens, bureaucrats):
    """
    Citizens and bureaucrats change behavior based on network influence.
    - Citizen: If 3 out of 5 in their network are corrupt or delayed, becomes bribe_offering.
    - Bureaucrat: If 3 in network were investigated, becomes honest.
    """
    # Citizens
    for citizen in citizens:
        corrupt_neighbors = sum(1 for neigh in citizen['network']
                                if neigh['state'] == 'bribe_offering')
        delayed_neighbors = sum(1 for neigh in citizen['network']
                                if neigh['waiting_time'] > 0)

        if corrupt_neighbors + delayed_neighbors >= 3:
            citizen['state'] = 'bribe_offering'

    # Bureaucrats
    for bureau in bureaucrats:
        invests = sum(1 for neigh in bureau['network']
                      if neigh['investigations'] > 0)
        if invests >= 3:
            bureau['state'] = 'honest'


######################################################
# MAIN EXECUTION
######################################################
if __name__ == '__main__':
    params = {
        'num_citizens': 100,
        'num_bureaucrats': 20,
        'rounds': 7,                # Number of rounds to simulate
        'salary': 5,                # Salary each bureaucrat gets each round
        'bribe_amount': 1,          # Bribe exchanged if both are corrupt
        'investigation_rate': 20,   # Number of bureaucrats investigated each round
        'investigation_cost': 3,    # Cost per investigated bureaucrat
        'initial_corruption_citizens': 0.8,
        'initial_corruption_bureaucrats': 0.4
    }

    # Initialize Agents & Institution
    citizens, bureaucrats = initialize_simulation(params)
    institution = {'budget': 1000}

    log_data = []
    total_satisfaction_collected = 0

    print("\n--- Simulation Starting ---")
    sys.stdout.flush()

    for round_num in range(1, params['rounds'] + 1):
        # 1. Interactions
        handle_interactions(citizens, bureaucrats, params)

        # 2. Distribute Salaries
        distribute_salaries(bureaucrats, institution, params['salary'])

        # 3. Investigations
        investigated, confiscated_tokens = handle_investigations(bureaucrats, institution, params)

        # 4. Social Influence
        update_social_influence(citizens, bureaucrats)

        # Evaluate Metrics
        total_satisfaction_collected += sum(c['satisfaction'] for c in citizens)
        corruption_level = sum(1 for b in bureaucrats if b['state'] == 'corrupt') / len(bureaucrats)
        avg_satisfaction = sum(c['satisfaction'] for c in citizens) / len(citizens)
        total_tokens = sum(b['tokens'] for b in bureaucrats)

        # Extended stats for bureaucrats
        total_investigation_count = sum(b['investigations'] for b in bureaucrats)
        total_bureaucrat_satisfaction = sum(b['accumulated_satisfaction'] for b in bureaucrats)

        log_data.append({
            'round': round_num,
            'corruption_level': corruption_level,
            'avg_satisfaction': avg_satisfaction,
            'total_tokens': total_tokens,
            'total_satisfaction_collected': total_satisfaction_collected,
            'institution_budget': institution['budget'],
            'confiscated_tokens': confiscated_tokens,
            'num_investigated': len(investigated),
            'total_investigation_count': total_investigation_count,
            'total_bureaucrat_satisfaction': total_bureaucrat_satisfaction
        })

        print(f"Round {round_num}: "
              f"Corruption={corruption_level:.2f}, "
              f"AvgSat={avg_satisfaction:.2f}, "
              f"Budget={institution['budget']}, "
              f"Tokens={total_tokens}, "
              f"Confiscated={confiscated_tokens}, "
              f"Investigated={len(investigated)}, "
              f"BureaucratInvestigations={total_investigation_count}, "
              f"BureaucratSat={total_bureaucrat_satisfaction}")
        sys.stdout.flush()

    print("\n--- Simulation Complete ---")
    sys.stdout.flush()

    # Print Logged Data
    print("\nSimulation Log:")
    for entry in log_data:
        print(entry)
        sys.stdout.flush()
