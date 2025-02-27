# Agent-Based Simulation of Corruption and Institutional Governance

## Abstract
This simulation is an agent-based model (ABM) designed to explore the dynamics of corruption and governance within public institutions. It simulates interactions between citizens, bureaucrats, and an overseeing institution to capture how corruption emerges, evolves, and can be controlled through various enforcement strategies. By adjusting parameters such as bribe amounts, investigation rates, salaries, and initial corruption levels, users can simulate different regional or historical governance scenarios—ranging from a high-integrity, low-corruption environment to settings where corruption is deeply entrenched yet managed for results. The model offers a flexible framework for understanding the interplay between institutional credibility, citizen satisfaction, and bureaucratic behavior.

## Detailed Description

### Purpose and Scope
This simulation provides a virtual environment to analyze how corruption develops and is mitigated within bureaucratic institutions. It is aimed at researchers, policymakers, and educators interested in:
- **Investigating Corruption Dynamics:** Understand how dishonest practices emerge among citizens and bureaucrats.
- **Evaluating Institutional Responses:** Explore how an overseeing institution can allocate resources to distribute salaries and conduct investigations.
- **Comparing Governance Strategies:** Simulate different anti-corruption approaches (e.g., proactive versus reactive enforcement) and regional governance models.

### Core Entities and Their Roles
The model consists of three primary types of agents:

1. **Citizens**
   - **Role:** Service users who can behave honestly or engage in corrupt practices by offering bribes.
   - **Behavior:** Request services, experience delays when interacting with corrupt bureaucrats, and may change behavior based on personal experiences and social influence from neighbors.

2. **Bureaucrats**
   - **Role:** Public officials responsible for service delivery.
   - **Behavior:** Operate honestly (delivering prompt service and earning standard tokens) or corruptly (accepting bribes and delaying services). Their state can shift depending on investigation risks and peer influence.

3. **Institution**
   - **Role:** The governing body that oversees bureaucratic operations.
   - **Functions:** Distributes salaries, manages an institutional budget, and conducts investigations to detect and penalize corrupt behavior. Institutional credibility is central to its capacity to enforce rules and maintain public trust.

### Simulation Mechanics and Workflow
The simulation operates in discrete rounds, each representing a cycle of interactions and institutional actions:

1. **Initialization**
   - **Agent Creation:** Citizens and bureaucrats are created based on user-defined parameters, with initial corruption levels determining their starting states.
   - **Social Networks:** Each agent is assigned a set of random neighbors to simulate social influence, which will affect future behavior.

2. **Citizen–Bureaucrat Interactions**
   - **Service Delivery:** Citizens request services and are randomly paired with bureaucrats.
   - **Outcome Determination:** 
     - If both citizen and bureaucrat are honest, the service is delivered promptly.
     - If a corrupt bureaucrat interacts with an honest citizen, the service is delayed (resulting in decreased satisfaction).
     - If both are corrupt, bribes are exchanged, reinforcing corrupt behavior.

3. **Salary Distribution**
   - The institution pays salaries to bureaucrats using its available budget, reinforcing honest behavior when funds are sufficient.

4. **Investigations**
   - **Enforcement Mechanism:** A subset of bureaucrats is randomly selected for investigation at a cost. If a bureaucrat is found corrupt, their accumulated tokens are confiscated and the bureaucrat's state resets to honest.

5. **Social Influence and Behavioral Updates**
   - **Dynamic Adaptation:** Both citizens and bureaucrats adjust their behavior based on experiences (such as delays or successful bribe exchanges) and the influence of their neighbors.

6. **Metric Logging**
   - After each round, key metrics are logged:
     - Overall corruption level among bureaucrats.
     - Institutional budget.
     - Average citizen satisfaction.
     - Total tokens accumulated by bureaucrats.
   - These metrics facilitate detailed analysis post-simulation.

### Parameterization and Governance Strategies
The simulation is highly configurable. Key parameters include:
- **Agent Counts:** Number of citizens and bureaucrats.
- **Economic Variables:** Salary levels, bribe amounts, and investigation costs.
- **Corruption Settings:** Initial corruption rates for citizens and bureaucrats.
- **Institutional Settings:** Investigation rate and starting budget.
- **Simulation Duration:** Total number of rounds.

Additionally, synthetic regional scenarios (e.g., Scandinavian, South American, Middle Eastern, South Korean) are provided as baselines. These offer historical and anthropological rationales for various parameter settings, enabling the simulation of distinct governance models.

### Simulating Different Governance Models
By modifying key parameters, the model can emulate various strategies:
- **Pragmatic Approach:** Focuses on investigating bureaucrats when citizen satisfaction falls, prioritizing those with high token reserves.
- **Corruption-Minimizing Approach:** Targets bureaucrats with high bribe acceptance rates to systematically reduce corruption.
- **Firefighting Approach:** Triggers intensive investigations only when institutional credibility drops below a threshold or overall corruption exceeds a predefined limit.

These strategies allow users to explore how different enforcement policies impact corruption dynamics and institutional performance over time.

### User Interface and Execution
A Streamlit-based GUI provides an intuitive interface for:
- **Interactive Parameter Adjustment:** Modify simulation settings using sliders and input fields.
- **Real-Time Visualization:** View simulation outcomes as tables and charts, showcasing trends in corruption levels, institutional budgets, and satisfaction metrics.
- **Result Analysis:** Easily interpret how parameter changes affect the system, aiding in hypothesis testing and policy simulation.

## Conclusion
This agent-based simulation model provides a robust platform for exploring the complex interplay between corruption, bureaucratic behavior, and institutional governance. It not only enables the simulation of various corruption scenarios but also allows for comparative studies of different governance strategies across diverse regional contexts. By understanding the relationships among citizens, bureaucrats, and the overseeing institution, users can gain deep insights into how policies and cultural factors interact to shape the integrity and efficiency of public administration.

## Getting Started
1. **Setup Parameters:** Adjust simulation parameters (e.g., number of agents, corruption rates) via the provided GUI or configuration files.
2. **Choose a Strategy:** Select the desired governance strategy either through the main simulation script or via command-line arguments.
3. **Run the Simulation:** Execute the simulation (e.g., `python run.py`) to generate outputs such as logs and visualizations.
4. **Analyze Results:** Use the built-in plotting tools to visualize trends in corruption, satisfaction, and institutional performance over time.

## Extending the Model
- **Parameter Sweeps:** Run multiple simulations varying key parameters to explore different outcomes.
- **Additional Metrics:** Extend logging to include more detailed measures, such as the distribution of citizen satisfaction or inequality in bureaucrat earnings.
- **Custom Governance Strategies:** Implement new strategies to explore alternative approaches to corruption management.

## Contributing
Contributions are welcome! Please submit pull requests, open issues for feature proposals, or bug reports. For major changes, please discuss via an issue first.
