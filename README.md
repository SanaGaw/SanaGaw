### Agent-Based Simulation of Corruption and Institutional Governance
## Overview
This simulation is an agent-based model (ABM) designed to explore the dynamics of corruption and governance within public institutions. It simulates interactions between citizens, bureaucrats, and an overseeing institution to capture how corruption emerges, evolves, and can be controlled through various enforcement strategies. By adjusting parameters such as bribe amounts, investigation rates, salaries, and initial corruption levels, users can simulate different regional or historical governance scenarios—ranging from a high-integrity, low-corruption environment to settings where corruption is deeply entrenched yet managed for results. The model offers a flexible framework for understanding the interplay between institutional credibility, citizen satisfaction, and bureaucratic behavior.

## Detailed Description
# Purpose and Scope
This simulation provides a virtual environment to analyze how corruption develops and is mitigated within bureaucratic institutions. It is aimed at researchers, policymakers, and educators interested in:

Investigating Corruption Dynamics: Understanding how dishonest practices emerge among citizens and bureaucrats.
Evaluating Institutional Responses: Exploring how an overseeing institution can allocate resources to distribute salaries and conduct investigations.
Comparing Governance Strategies: Simulating different anti-corruption approaches (e.g., proactive versus reactive enforcement) and regional governance models.
Core Entities and Their Roles
The model consists of three primary types of agents, each with distinct roles and interactions:

# Citizens

Role: Citizens are service users who may either behave honestly or engage in corrupt practices by offering bribes.
Behavior: They request services, experience delays when interacting with corrupt bureaucrats, and can change their behavior based on their personal experiences and the influence of their social network (neighbors).
# Bureaucrats

Role: Bureaucrats are the public officials responsible for providing services.
Behavior: They can act honestly—delivering prompt service and earning standard tokens—or corruptly—accepting bribes, delaying services, and earning extra tokens from illicit transactions. Their state (honest vs. corrupt) can shift based on the risk of investigations and social influences from their peers.
Institution

Role: The institution represents the governing body overseeing bureaucratic operations.
Functions: It distributes salaries to bureaucrats, manages an institutional budget, and conducts investigations to detect and penalize corrupt behavior. The institution’s credibility is central to its ability to enforce rules and maintain public trust.
Simulation Mechanics and Workflow
The simulation runs in discrete rounds, each capturing a cycle of interactions and institutional actions:

# Initialization

Agent Creation: Citizens and bureaucrats are created based on user-defined parameters, with initial corruption levels determining their starting states.
Social Networks: Each agent is assigned a set of random “neighbors” to simulate social influence, affecting future behavior changes.
Citizen–Bureaucrat Interactions

Service Delivery: Citizens request services and are randomly paired with bureaucrats.
Outcome Determination: If both citizen and bureaucrat are honest, the service is delivered promptly. However, if a corrupt bureaucrat interacts with an honest citizen, the service is delayed (with negative impacts on satisfaction). In cases where both are corrupt, bribes are exchanged, reinforcing corrupt behavior.
Salary Distribution

Institutional Payment: The institution uses its budget to pay salaries to bureaucrats, which reinforces honest behavior when sufficient funds are available.
Investigations

Enforcement Mechanism: A subset of bureaucrats is randomly selected for investigation. Each investigation has an associated cost, and if a bureaucrat is found to be corrupt, their accumulated tokens (representing illicit gains) are confiscated. This process not only punishes corruption but also resets the bureaucrat’s state to honest.
Social Influence and Behavioral Updates

Dynamic Adaptation: Both citizens and bureaucrats adjust their behavior based on social influence—observing the state of their neighbors—and based on their experiences (such as delays or successful bribe exchanges). This mechanism captures the real-world notion that behavior can spread through communities.
Metric Logging

Outcome Recording: After each round, the simulation logs key metrics including the overall corruption level among bureaucrats, institutional budget, average citizen satisfaction, and total tokens accumulated by bureaucrats. These metrics facilitate detailed post-simulation analysis.
Parameterization and Governance Strategies
The simulation is highly configurable, allowing users to tailor scenarios by adjusting parameters such as:

Agent Counts: Number of citizens and bureaucrats.
Economic Variables: Salary levels, bribe amounts, and investigation costs.
Corruption Settings: Initial corruption rates for both citizens and bureaucrats.
Institutional Settings: Investigation rate and starting budget.
Simulation Duration: Total number of rounds.
Additionally, a supplemental parameter table provides synthetic regional scenarios (e.g., Scandinavian, South American, Middle Eastern, South Korean) that offer historical and anthropological rationales for different parameter settings. These baselines enable users to simulate and compare how various regions might experience and control corruption differently.

Simulating Different Governance Models
By modifying key parameters, the model can mimic various governance strategies:

Pragmatic Approach: The institution focuses on investigating bureaucrats when citizen satisfaction dips, prioritizing those with high token reserves.
Corruption-Minimizing Approach: Investigations target bureaucrats with a high rate of bribe acceptance, regardless of their token balance, to systematically reduce corruption.
Firefighting Approach: Intensive investigations are triggered only when institutional credibility falls below a threshold or when overall corruption exceeds a predefined limit.
Such flexibility allows users to explore the impact of different enforcement strategies on corruption dynamics and institutional performance over time.

User Interface and Execution
A Streamlit-based GUI offers an intuitive front-end for:

Interactive Parameter Adjustment: Users can modify simulation settings via sliders and input fields.
Real-Time Visualization: Simulation outcomes are displayed as tables and charts, illustrating trends in corruption levels, institutional budgets, and satisfaction metrics.
Result Analysis: The interface enables easy interpretation of how changes in parameters affect the system, providing valuable insights for hypothesis testing and policy simulation.
Conclusion
This agent-based simulation model provides a robust platform for exploring the complex interplay between corruption, bureaucratic behavior, and institutional governance. It not only offers a means to simulate various corruption scenarios but also enables comparative studies of different governance strategies across diverse regional contexts. By understanding the relationships among citizens, bureaucrats, and the governing institution, users can gain deep insights into how policies and cultural factors interact to shape the integrity and efficiency of public administration.