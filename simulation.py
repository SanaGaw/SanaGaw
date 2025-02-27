import random

######################################################
# INITIALIZATION
######################################################
def initialize_simulation(params):
    """ Initializes citizens and bureaucrats with their initial states. """
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
            'neighbors': [],
            'was_delayed_this_round': False,
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
            'neighbors': [],
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
    """ Handles interactions between citizens and bureaucrats. """
    for citizen in citizens:
        citizen['was_delayed_this_round'] = False

    for citizen in citizens:
        if citizen['needs_service'] and bureaucrats:
            bureau = random.choice(bureaucrats)
            if citizen['state'] == 'honest':
                if bureau['state'] == 'honest':
                    citizen['needs_service'] = False
                    bureau['satisfaction'] += 1
                else:
                    citizen['waiting_time'] += 1
                    citizen['was_delayed_this_round'] = True
                    bureau['satisfaction'] -= 1
            else:
                if bureau['state'] == 'corrupt':
                    bureau['tokens'] += params['bribe_amount']
                    citizen['needs_service'] = False
                else:
                    citizen['needs_service'] = False
                    bureau['satisfaction'] += 1
                    bureau['state'] = 'corrupt'

######################################################
# SALARY DISTRIBUTION
######################################################
def distribute_salaries(bureaucrats, institution, params):
    """ Pays bureaucrats from the institution budget if possible. """
    total_salary = params['salary'] * len(bureaucrats)
    if institution['budget'] >= total_salary:
        institution['budget'] -= total_salary
        for b in bureaucrats:
            b['tokens'] += params['salary']

######################################################
# INVESTIGATIONS
######################################################
def handle_investigations(bureaucrats, institution, params):
    """ Investigates bureaucrats and confiscates tokens if corrupt. """
    num_to_investigate = min(len(bureaucrats), params['investigation_rate'])
    cost = num_to_investigate * params['investigation_cost']

    if institution['budget'] < cost:
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
    """ Updates corruption trends based on investigations and social influence. """
    for c in citizens:
        corrupt_neighbors = sum(1 for n_id in c['neighbors'] if citizens[n_id]['state'] == 'bribe_offering')
        if corrupt_neighbors >= 3 or c['was_delayed_this_round']:
            c['state'] = 'bribe_offering'

    threshold = len(bureaucrats) * 0.5
    not_enough_pressure = (last_round_investigations < threshold)
    for b in bureaucrats:
        if b['state'] == 'honest' and not_enough_pressure:
            corrupt_neighbors = sum(1 for nb_id in b['neighbors'] if bureaucrats[nb_id]['state'] == 'corrupt')
            if corrupt_neighbors >= 3:
                b['state'] = 'corrupt'

######################################################
# MAIN SIMULATION FUNCTION
######################################################
def run_simulation(params):
    """ Runs the full corruption simulation and returns results. """
    citizens, bureaucrats = initialize_simulation(params)
    institution = {'budget': params['initial_budget']}
    logs = []

    for round_num in range(1, params['rounds'] + 1):
        handle_interactions(citizens, bureaucrats, params)
        distribute_salaries(bureaucrats, institution, params)
        investigated, confiscated = handle_investigations(bureaucrats, institution, params)
        last_round_investigations = len(investigated)
        update_social_influence(citizens, bureaucrats, last_round_investigations, params)

        corruption_level = sum(b['state'] == 'corrupt' for b in bureaucrats) / len(bureaucrats)
        avg_satisfaction = sum(c['satisfaction'] for c in citizens) / len(citizens) if citizens else 0
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

    return logs
