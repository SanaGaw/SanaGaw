#######################################
# app_streamlit.py
#######################################
import streamlit as st
import pandas as pd

# Import the ABM logic
from simulation import run_simulation

def main():
    st.title("Corruption Simulation (Streamlit GUI)")
    st.write("Adjust parameters below and click **Run Simulation**.")

    # Layout: Two columns for user inputs side by side
    col1, col2 = st.columns(2)

    # Left column inputs
    with col1:
        num_citizens = st.slider("Number of Citizens", min_value=10, max_value=1000, value=100, step=10)
        num_bureaucrats = st.slider("Number of Bureaucrats", min_value=5, max_value=200, value=20, step=5)
        rounds = st.slider("Number of Rounds", min_value=1, max_value=50, value=7, step=1)
        salary = st.slider("Salary", min_value=1, max_value=50, value=5, step=1)
        bribe_amount = st.slider("Bribe Amount", min_value=1, max_value=50, value=1, step=1)

    # Right column inputs
    with col2:
        investigation_rate = st.slider("Investigation Rate (# Bureaucrats Investigated)", 
                                       min_value=1, max_value=100, value=20, step=1)
        investigation_cost = st.slider("Investigation Cost", min_value=1, max_value=20, value=3, step=1)
        init_corr_cit = st.slider("Initial Corruption (Citizens)", 0.0, 1.0, 0.4, 0.05)
        init_corr_bur = st.slider("Initial Corruption (Bureaucrats)", 0.0, 1.0, 0.4, 0.05)
        initial_budget = st.number_input("Initial Budget", min_value=100, max_value=100000, value=1000, step=100)

    # Button to run
    if st.button("Run Simulation"):
        # Build the params dict
        params = {
            'num_citizens': num_citizens,
            'num_bureaucrats': num_bureaucrats,
            'rounds': rounds,
            'salary': salary,
            'bribe_amount': bribe_amount,
            'investigation_rate': investigation_rate,
            'investigation_cost': investigation_cost,
            'initial_corruption_citizens': init_corr_cit,
            'initial_corruption_bureaucrats': init_corr_bur,
            'initial_budget': initial_budget
        }

        # Run the ABM
        logs = run_simulation(params)  
        # logs is expected to be a list of dicts, e.g.:
        # [
        #   {'round':1, 'institution_budget':..., 'corruption_level':..., ...},
        #   {'round':2, 'institution_budget':..., 'corruption_level':..., ...},
        #   ...
        # ]

        st.subheader("Simulation Results")

        # Convert logs to a DataFrame for easy display
        df_logs = pd.DataFrame(logs)

        # Show as a table
        st.dataframe(df_logs)

        # If we have a 'corruption_level' column, let's plot it
        if 'corruption_level' in df_logs.columns:
            st.line_chart(df_logs['corruption_level'])

        # Similarly, you can line-chart other columns (like budget)
        # st.line_chart(df_logs['institution_budget'])

        st.success("Simulation complete!")

if __name__ == "__main__":
    main()
