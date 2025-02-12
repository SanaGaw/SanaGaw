# Agent-Based Simulation of Institutional Governance and Bureaucratic Behavior

## 1. Overview
This repository contains an agent-based model (ABM) that simulates interactions between citizens, bureaucrats, and an overseeing institution. The model focuses on how corruption emerges or is contained, how institutional credibility evolves, and how different governance strategies impact overall outcomes.

### Core Features
- Dynamic decision-making by bureaucrats (corrupt vs. honest) based on investigations and earnings.
- Citizens who can be honest or corrupt, offering or refusing bribes.
- An institution that adapts its investigation strategy to manage resources and limit corruption.

## 2. Conceptual Model

### 2.1 Entities
1. **Citizens**
   - May be honest or corrupt.
   - Provide feedback (satisfaction) based on service quality.
   - Switch behavior type (honest ↔ corrupt) under certain conditions (e.g., repeated delays or failed bribes).

2. **Bureaucrats**
   - Can be honest (reject bribes) or corrupt (accept bribes, delay honest citizens).
   - Earn tokens through honest service or bribes.
   - Switch behavior if investigations increase perceived risk or if corrupt earnings outpace honest earnings.

3. **Institution**
   - Maintains an “Institutional Credibility” (IC) score.
   - Conducts investigations at a cost of tokens.
   - Confiscates ill-gotten gains if corrupt bureaucrats are reported.
   - Shifts enforcement strategies according to resource availability and corruption levels.

### 2.2 Key Parameters
- **Num_Bureaucrats:** Total number of bureaucrats in the system.
- **Num_Citizens:** Total number of citizens requesting services each round.
- **Initial_Corruption_Rate:** Fraction of bureaucrats (and/or citizens) starting out corrupt.
- **Investigation_Cost:** The token cost of investigating one bureaucrat.
- **Bribe_Amount:** The token amount a corrupt bureaucrat receives from a bribing citizen.
- **Honest_Earning:** The token amount an honest bureaucrat earns per successful service.
- **Satisfaction_Target:** Initial satisfaction level the institution aims to maintain.
- **IC_Threshold (0.4):** Institutional credibility cutoff that triggers more reactive enforcement.

### 2.3 Simulation Flow (Each Round)
1. **Citizen-Bureaucrat Interactions:**
   - Citizens queue for service; bureaucrats handle up to 5 interactions per round.
   - Corrupt bureaucrats may delay honest citizens or take bribes from corrupt citizens.
   - Satisfaction is calculated (+1, 0, or -1) and used to update Institutional Credibility.

2. **Institutional Enforcement:**
   - Institution checks available resources (IC) and decides how many bureaucrats to investigate.
   - Bureaucrats under investigation and found corrupt lose tokens; the institution recoups some resources (unless the bureaucrat is falsely accused).

3. **Adaptation & Strategy Updates:**
   - **Bureaucrats:** May switch between honest/corrupt behavior based on investigatory risk or peer investigations.
   - **Institution:** Adjusts strategy (pragmatic, corruption-minimizing, firefighting) depending on scenario or policy setting.
   - **Satisfaction Target:** Adjusted by ±3% if average satisfaction is above/below the current target.

4. **Update Metrics:**
   - Institutional Credibility (IC) is recalculated.
   - Overall corruption rate, average satisfaction, and resource usage are recorded for analysis.

### 2.4 Governance Strategies
1. **Pragmatic:** 
   - Investigate bureaucrats below satisfaction targets, prioritize confiscating high token reserves.

2. **Corruption-Minimizing:**
   - Investigate all bureaucrats with bribe acceptance rates > 10%, ignoring token reserves.

3. **Firefighting:**
   - Investigate only if **IC < 0.4** or **corruption > 30%**. Otherwise, minimize spending on investigations.

## 3. Usage Instructions
1. **Setup Parameters:** Edit the `config.py` (or wherever you store parameters) to define your scenario (e.g., number of bureaucrats, initial corruption rate, etc.).
2. **Choose a Strategy:** Set the governance strategy in the main simulation file or via a command-line argument.
3. **Run the Simulation:** Execute the main simulation script (e.g., `python run.py`) to generate outputs (e.g., logs, CSV results).
4. **Analyze Results:** Use the built-in plotting or analysis tools to visualize changes in corruption, satisfaction, and institutional credibility over time.

## 4. Extending the Model
- **Parameter Sweeps:** You can run multiple simulations, varying parameters such as `Investigation_Cost` or `Bribe_Amount` to see how outcomes shift.
- **Additional Metrics:** Track more nuanced measures like the distribution of citizen satisfaction or the Gini coefficient of bureaucrat earnings.

## 5. License
(Include your chosen license here, e.g., MIT License, GPLv3, etc.)

## 6. Contributing
- Pull requests and bug fixes are welcome.
- Please open an issue for major feature proposals or questions.

## 7. Contact
(Include your email or relevant contact info if desired.)

