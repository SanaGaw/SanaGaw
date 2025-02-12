# config/parameters.py

# Basic model parameters
NUM_BUREAUCRATS = 10
NUM_CITIZENS = 50

# Initial fractions or probabilities
INITIAL_CORRUPTION_RATE = 0.3  # fraction of bureaucrats initially corrupt
INITIAL_CORRUPT_CITIZEN_RATE = 0.2  # fraction of citizens initially corrupt

# Economic parameters
INVESTIGATION_COST = 0.7       # cost in tokens to investigate one bureaucrat
BRIBE_AMOUNT = 0.2             # tokens gained by corrupt bureaucrat per bribe
HONEST_EARNING = 0.05          # tokens earned by honest bureaucrat per service

# Satisfaction & Institutional Credibility
IC_INITIAL = 1.0               # initial institutional credibility
IC_THRESHOLD = 0.4             # credibility threshold for reactive measures
SATISFACTION_TARGET = 0.8      # target average satisfaction (0 - 1 scale)

# Behavioral switching
PEER_INVESTIGATIONS_THRESHOLD = 3  # # of peers investigated before switching
TOKEN_LOSS_CORRUPT = 1.0           # fraction of corrupt bureaucrat's tokens lost if caught

# Simulation controls
ROUNDS = 30  # default number of rounds to run in the simulation

