# Step 1: Define and Initialize Agents
# Goal: Represent citizens, bureaucrats, and the institution as data structures.

import random

# Parameters
params = {
    'num_citizens': 10,  # Adjust based on scenario
    'num_bureaucrats': 5, # Adjust based on scenario
    'initial_budget': 1000, # Placeholder for the institution's budget
    'default_strategy': 'none' # No investigation strategy yet
}

# Initialize Citizens
citizens = []
for i in range(params['num_citizens']):
    citizens.append({
        'id': i,
        'state': 'honest',  # Can later become 'bribe_offering'
        'satisfaction': 0,   # Tracks how happy they are with the system
        'needs_service': True, # Tracks if they still require bureaucratic assistance
        'interaction_count': 0, # Number of times they have interacted
        'waiting_time': 0 # How many rounds they have waited for service
    })

# Initialize Bureaucrats
bureaucrats = []
for i in range(params['num_bureaucrats']):
    bureaucrats.append({
        'id': i,
        'state': 'honest',  # Can later become 'corrupt'
        'tokens': 0,        # Tracks bribery income
        'investigations': 0, # Tracks number of times investigated
        'interaction_satisfaction': 0, # Satisfaction score from handling citizens
    })

# Initialize Institution
institution = {
    'budget': params['initial_budget'],
    'strategy': params['default_strategy'],
}

# Testing Initialization
print("Citizens:")
for citizen in citizens:
    print(citizen)

print("\nBureaucrats:")
for bureaucrat in bureaucrats:
    print(bureaucrat)

print("\nInstitution:")
print(institution)

# Verify if sizes and initial states are correct
assert len(citizens) == params['num_citizens'], "Mismatch in citizen count"
assert len(bureaucrats) == params['num_bureaucrats'], "Mismatch in bureaucrat count"
