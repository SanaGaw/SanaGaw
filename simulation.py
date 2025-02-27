import random
import sys

######################################################
# INITIALIZATION
######################################################
def initialize_simulation(params):
    """
    Initializes citizens and bureaucrats with their initial states.
    Uses 'initial_corruption_citizens' and 'initial_corruption_bureaucrats'
    to define how many start off corrupt.
    """
    num_citizens = params['num_citizens']
    num_bureaucrats = params['num_bureaucrats']

    # Create citizens
    citizens = []
    for i in range(num_citizens):
        is_corrupt = random.random() < params['initial_corruption_citizens']
        citizens.append({
            'id': i,
            'state': 'bribe_offering' if is_corrupt else 'honest',
            'needs_service': True,
            'waiting_time': 0,
            # Will store references to other citizen IDs
            'neighbors': [],
            # Additional flag to mark if they were delayed this round
            'was_delayed_this_round': False,
            # Optional satisfaction tracking
            'satisfaction': 0
        })

    # Create bureaucrats
    bureaucrats = []
    for i in range(num_bureaucrats):
        is_corrupt = random.random() < params['initial_corruption_bureaucrats']
        bureaucrats.append({
            'id': i,
            'state': 'corrupt' if is_corrupt else 'honest',
            'tokens': 0,
            'investigations': 0,
            'neighbors': [],  # <--- MISSING COMMA FIXED
            'satisfaction': 0
        })

    # Assign up to 5 random neighbors for each citizen/bureaucrat
    for c in citizens:
        possible_others = [other['id'] for other in citizens if other['id'] != c['id']]
        c['neighbors'] = random.sample(possible_others, min(5, len(possible_others)))

    for b in bureaucrats:
        possible_others = [other['id'] for other in bureaucrats if other['id'] != b['id']]
        b['neighbors'] = random.sample(possible_others, min(5, len(possible_others)))

    return citizens, bureaucrats

######################################################
# INTERACTIONS
######################################################
def handle_interactions(citizens, bureaucrats, params):
    """
    Each citizen attempts to get service from a random bureaucrat.
    If an honest citizen meets a corrupt bureau => delayed => becomes corrupt NEXT round
    """

    for citizen in citizens:
        citizen['was_delayed_this_round'] = False  # reset each round

    for citizen in citizens:
        if citizen['needs_service'] and bureaucrats:
            bureau = random.choice(bureaucrats)
            if citizen['state'] == 'honest':
                if bureau['state'] == 'honest':
                    # immediate service
                    citizen['needs_service'] = False
                    bureau['satisfaction'] += 1
                else:
                    # corrupt => wait
                    citizen['waiting_time'] += 1
                    citizen['was_delayed_this_round'] = True
                    bureau['satisfaction'] -= 1
            else:  # bribe_offering
                if bureau['state'] == 'corrupt':
                    # bribe occurs
                    bureau['tokens'] += params['bribe_amount']
                    citizen['needs_service'] = False
                    # bureau['satisfaction'] += 0 (if needed)
                else:
                    # honest bureau => serve anyway
                    citizen['needs_service'] = False
                    bureau['satisfaction'] += 1
                    bureau['state'] = 'corrupt'

######################################################
# SALARY
######################################################
def distribute_salaries(bureaucrats, institution, params):
    """
    Pay each bureaucrat from the institution budget if possible.
    """
    total_salary = params['salary'] * len(bureaucrats)
    institution['budget'] -= total_salary
    for b in bureaucrats:
        b['tokens'] += params['salary']
######################################################
# INVESTIGATIONS
######################################################
def handle_investigations(bureaucrats, institution, params):
    """
    Investigate some bureaucrats. If corrupt, confiscate tokens & turn honest.
    """
    num_to_investigate = min(len(bureaucrats), params['investigation_rate'])
    cost = num_to_investigate * params['investigation_cost']

    if institution['budget'] < cost:
        # not enough budget to investigate
        return [], 0

    
    chosen = random.sample(bureaucrats, num_to_investigate)
    confiscated = 0

    for b in chosen:
        b['investigations'] += 1
        if b['state'] == 'corrupt':
            confiscated += b['tokens']
            institution['budget'] += b['tokens']
            institution['budget'] -= cost
            b['tokens'] = 0
            b['state'] = 'honest'

    return chosen, confiscated

######################################################
# SOCIAL INFLUENCE & RE-CORRUPTION
######################################################
def update_social_influence(citizens, bureaucrats, last_round_investigations, params):
    """
    CITIZENS:
      - If delayed => becomes corrupt in NEXT round
      - If 3 out of 5 neighbors are corrupt => immediate corrupt

    BUREAUCRATS:
      - If not enough investigations => revert to corrupt if 3 neighbors are corrupt
    """

    # 1) CITIZENS
    for c in citizens:
        # immediate corruption if 3/5 neighbors are bribe_offering
        corrupt_neighbors = 0
        for n_id in c['neighbors']:
            if n_id < len(citizens):
                if citizens[n_id]['state'] == 'bribe_offering':
                    corrupt_neighbors += 1
        if corrupt_neighbors >= 3:
            c['state'] = 'bribe_offering'

        # if delayed, become corrupt next round
        if c['was_delayed_this_round']:
            c['state'] = 'bribe_offering'

    # 2) BUREAUCRATS REVERT
    threshold = len(bureaucrats) * 0.5
    not_enough_pressure = (last_round_investigations < threshold)
    for b in bureaucrats:
        if b['state'] == 'honest' and not_enough_pressure:
            # count corrupt neighbors
            corrupt_neighbors = sum(1 for nb_id in b['neighbors']
                                    if nb_id < len(bureaucrats)
                                    and bureaucrats[nb_id]['state'] == 'corrupt')
            if corrupt_neighbors >= 3:
                b['state'] = 'corrupt'

######################################################
# MAIN
######################################################
if __name__ == '__main__':
    params = {
        'num_citizens': 100,
        'num_bureaucrats': 20,
        'rounds': 12,
        'salary': 5,
        'bribe_amount': 1,
        'investigation_rate': 13,
        'investigation_cost': 3,
        'initial_corruption_citizens': 0.3,
        'initial_corruption_bureaucrats': 0.3,
        'initial_budget': 1000
    }

    # Initialize
    citizens, bureaucrats = initialize_simulation(params)
    institution = {'budget': params['initial_budget']}

    logs = []

    print("\n--- Simulation Starting ---")
    sys.stdout.flush()

    for round_num in range(1, params['rounds'] + 1):
        handle_interactions(citizens, bureaucrats, params)
        distribute_salaries(bureaucrats, institution, params)
        investigated, confiscated = handle_investigations(bureaucrats, institution, params)
        last_round_investigations = len(investigated)
        update_social_influence(citizens, bureaucrats, last_round_investigations, params)

        corruption_level = sum(b['state'] == 'corrupt' for b in bureaucrats) / len(bureaucrats)
        avg_satisfaction = (sum(c['satisfaction'] for c in citizens) / len(citizens)) if citizens else 0
        total_tokens = sum(b['tokens'] for b in bureaucrats)

        logs.append({
            'round': round_num,
            'institution_budget': institution['budget'],
            'corruption_level': corruption_level,
            'confiscated_tokens': confiscated,
            'investigated_count': last_round_investigations,
            'avg_satisfaction': avg_satisfaction,
            'bureaucrat_tokens': total_tokens
        })

        print(f"Round {round_num}: Budget={institution['budget']}, "
              f"Corruption={corruption_level:.2f}, "
              f"Confiscated={confiscated}, Investigated={last_round_investigations}, "
              f"AvgSatisfaction={avg_satisfaction:.2f}, BureauTokens={total_tokens}")
        sys.stdout.flush()

    print("\n--- Simulation Complete ---")
    sys.stdout.flush()

    # Print final log
    print("\nSimulation Log:")
    for row in logs:
        print(row)
        sys.stdout.flush()
