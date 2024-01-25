try:
    from scipy.integrate import odeint
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import questionary
except ImportError:
    print("One or more required libraries are not installed.")
    install_choice = input("Do you want to install them? (yes/no): ").lower()

    if install_choice == "yes":
        try:
            # Use pip to install the libraries
            import subprocess
            subprocess.check_call(['pip', 'install', 'scipy', 'numpy', 'matplotlib', 'seaborn', 'pandas', 'questionary'])
            print("Libraries installed successfully.")
        except Exception as e:
            print(f"Error installing libraries: {e}")
    else:
        print("You chose not to install the libraries.")

#############################################################################################################

def sir_model(y, t, params):
    """ODE system for the SIR model.

    Parameters:
    - y (list): List of S, I, R values.
    - t (float): Time.
    - params (dict): Dictionary containing model parameters.

    Returns:
    - list: List of derivatives [dS/dt, dI/dt, dR/dt].
    """
    S, I, R = y

    beta = params['b0'] * (1 + params['b1'] * np.cos(2 * np.pi * t + params['phi']))

    dSdt = params['mu'] - params['mu'] * S - beta * S * I + params['gamma'] * R
    dIdt = beta * S * I - params['ni'] * I - params['mu'] * I
    dRdt = params['ni'] * I - params['mu'] * R - params['gamma'] * R

    return [dSdt, dIdt, dRdt]

def solve_sir_model(initial_conditions, t, params):
    """Solves the SIR model ODE using odeint.

    Parameters:
    - initial_conditions (list): List of initial conditions [S0, I0, R0].
    - t (numpy.ndarray): Time array.
    - params (dict): Dictionary containing model parameters.

    Returns:
    - numpy.ndarray: Solution of the ODE.
    """
    solution = odeint(sir_model, initial_conditions, t, args=(params,))
    return solution

def simulate_and_plot(t, parameters, initial_conditions):
    """Simulates and plots multiple SIR model simulations.

    Parameters:
    - t (numpy.ndarray): Time array.
    - parameters (dict): Dictionary containing model parameters.
    - initial_conditions (dict): Dictionary containing initial conditions.

    Returns:
    - str: Message if no simulations are performed.
    """
    num_simulations = int(questionary.text("Enter the number of simulations:", validate=lambda val: val.isdigit(), default="1").ask())
    plural = "simulations"
    if num_simulations < 2:
        plural = "simulation"
    plt.figure(figsize=(10, 6))
    lables_on_y = {0: "Susceptible S(t)",
                   1: "Infectives I(t)",
                   2: "Recovered R(t)"}
    for n in range(0, 3):
        if num_simulations > 0:
            for r in range(num_simulations):
                np.random.seed(r)
                solution = solve_sir_model([initial_conditions['S0'], initial_conditions['I0'], initial_conditions['R0']], t, parameters)
                plt.plot(t, solution[:, n], linewidth=0.9, label=f'Simulation {r + 1}')

            plt.title(f'Adaptive step-size Runge-Kutta, {num_simulations} {plural}')
            plt.xlabel('Time t (years)')
            plt.ylabel(lables_on_y[n])
            plt.show()
        else:
            return "You chose not to simulate :)"

def modify_input():
    """Prompts the user to modify simulation inputs or use default values."""
    modify_input_question = questionary.select(f"Do you want to modify the inputs?",choices=["Yes", "No"],default="No").ask()

    if modify_input_question == "Yes":
        # Time vector, adjust the time range as needed
        t = np.linspace(int(questionary.text("Enter initial time:", validate=lambda val: val.isdigit(), default="0").ask()), 
                        int(questionary.text("Enter end time:", validate=lambda val: val.isdigit(), default="5").ask()), 
                        int(questionary.text("Enter number of steps:", validate=lambda val: val.isdigit(), default="5000").ask()))  
        parameters = {
            'mu': float(questionary.text("Enter value for mu:", validate=lambda val: not val.isdigit(), default="0.009").ask()),
            'b0': float(questionary.text("Enter value for b0:", validate=lambda val: not val.isdigit(), default="36.4").ask()),
            'b1': float(questionary.text("Enter value for b1:", validate=lambda val: not val.isdigit(), default="0.38").ask()),
            'phi': float(questionary.text("Enter value for phi:", validate=lambda val: not val.isdigit(), default="1.07").ask()),
            'gamma': float(questionary.text("Enter value for gamma:", validate=lambda val: not val.isdigit(), default="1.8").ask()),
            'ni': int(questionary.text("Enter value for ni:", validate=lambda val: val.isdigit(), default="36").ask()),
        }

        # Initial conditions
        initial_conditions = {
            'S0': float(questionary.text("Enter value for S0:", validate=lambda val: not val.isdigit(), default="0.9988").ask()),
            'I0': float(questionary.text("Enter value for I0:", validate=lambda val: not val.isdigit(), default="0.0012").ask()),
            'R0': float(questionary.text("Enter value for R0:", validate=lambda val: not val.isdigit(), default="0.0").ask())
            }

        # Call the function to simulate and plot
        simulate_and_plot(t,parameters,initial_conditions)
            
    else:
        # Time vector
        t = np.linspace(0, 4, 5000)  # Adjust the time range as needed
        # Define parameters
        # Parameters
        parameters = {
            'b0': 36.4,
            'b1': 0.38,
            'phi': 1.07,
            'mu': 0.009,
            'gamma': 1.8,
            'ni': 36,
        }

        # Initial conditions
        initial_conditions = {
            'S0': 0.9988,
            'I0': 0.0015,
            'R0': 0.0,
        }
        # Call the function to simulate and plot
        simulate_and_plot(t,parameters,initial_conditions)

modify_input()

def real_data():
    """Plots real data using Matplotlib."""
    data = {
        'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        '2001': [414, 272, 137, 22, 17, 2, 0, 1, 17, 1, 9, 127],
        '2002': [454, 301, 160, 55, 25, 11, 7, 1, 17, 32, 86, 417],
        '2003': [382, 138, 120, 50, 2, 10, 4, 4, 31, 64, 284, 607],
        '2004': [348, 145, 129, 9, 6, 4, 0, 0, 15, 28, 88, 373]
    }

    Empirical_data = pd.DataFrame(data)

    # Sum values for each year
    sum_by_year = Empirical_data.sum(numeric_only=True)

    # Matplotlib Bar Plot
    plt.style.use("ggplot")
    plt.figure(figsize=(10, 5))
    plt.bar(x=sum_by_year.index, height=sum_by_year.values)
    plt.title('Sum of Values for Each Year')
    plt.xlabel('Year')
    plt.ylabel('Sum')
    plt.tight_layout()
    plt.show()

real_data()
