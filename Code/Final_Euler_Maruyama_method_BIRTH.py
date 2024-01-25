try:
    import questionary
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError:
    print("One or more required libraries are not installed.")
    install_choice = input("Do you want to install it? (yes/no): ").lower()

    if install_choice == "yes":
        try:
            # Use pip to install the library
            import subprocess
            subprocess.check_call(['pip', 'install', 'questionary','numpy','matplotlib'])
            print("Required libraries installed successfully.")
        except Exception as e:
            print(f"Error installing the required libraries: {e}")
    else:
        print("You chose not to install the required libraries.")

#############################################################################################################
# Perturbation BIRTH
# Euler-Maruyama

def dW(delta_t: float) -> float:
    """Sample a random number at each call.

    Parameters:
    - delta_t (float): Time step.

    Returns:
    - float: Random number sampled from a normal distribution.
    """
    return np.random.normal(loc=0.0, scale=np.sqrt(delta_t))

def Euler_Maruyama_method(t_in, t_end, N, mu, b0, b1, phi, gamma, ni, alpha, S_in, I_in, R_in):
    """Simulate the SIR model using Euler-Maruyama method with birth rate perturbation.

    Parameters:
    - t_in (int): Initial time.
    - t_end (int): End time.
    - N (int): Number of steps.
    - mu (float): Parameter mu.
    - b0 (float): Parameter b0.
    - b1 (float): Parameter b1.
    - phi (float): Parameter phi.
    - gamma (float): Parameter gamma.
    - ni (int): Parameter ni.
    - alpha (float): Perturbation strength.
    - S_in (float): Initial susceptible population.
    - I_in (float): Initial infected population.
    - R_in (float): Initial recovered population.

    Returns:
    - Time steps and simulated populations.
    """
    dt = float((t_end - t_in) / N)
    TS = np.arange(t_in, t_end + dt, dt)
    assert TS.size == N + 1
    Ss = np.zeros(TS.size)
    Is = np.zeros(TS.size)
    Rs = np.zeros(TS.size)

    Ss[0] = S_in
    Is[0] = I_in
    Rs[0] = R_in

    for i in range(1, TS.size):
        t = t_in + (i - 1) * dt

        S = Ss[i - 1]
        I = Is[i - 1]
        R = Rs[i - 1]

        b0_tilde = b0 + alpha * dW(dt)
        beta = b0_tilde * (1 + b1 * np.cos(2 * np.pi * t + phi))
        mu_tilde = mu + alpha*dW(dt)

        Ss[i] = S + ( (mu_tilde - mu*S - beta*S*I + gamma*R) * dt + alpha*(1-S) * dW(dt) )
        Is[i] = I +( (beta*S*I - ni*I - mu*I) * dt - alpha*I * dW(dt) )
        Rs[i] = R + ( (ni*I - mu*R - gamma*R) * dt - alpha*R * dW(dt) )

    return TS, [Ss, Is, Rs]

# Function to simulate and plot multiple simulations
def simulate_and_plot(parameters):
    """Simulate and plot multiple SIR model simulations.

    Parameters:
    - parameters (dict): Dictionary containing simulation parameters.

    Returns:
    - None
    """
    num_simulations = int(questionary.text("Enter the number of simulations:", validate=lambda val: val.isdigit(), default="10").ask())
    plural = "simulations"
    if num_simulations < 2:
        plural = "simulation"
    plt.figure(figsize=(10, 6))
    lables_on_y = {0: "Susceptible S(t)",
            1:"Infectives I(t)",
            2: "Recovered R(t)"}
    for n in range(0,3):
        for r in range(num_simulations):
            np.random.seed(r)
            ts, results = Euler_Maruyama_method(**parameters)
            plt.plot(ts, results[n], linewidth=0.9, label=f'Simulation {r + 1}')

        plt.title(f'Euler-Maruyama, {num_simulations} {plural} with birth rate perturbation')
        plt.xlabel('Time t (years)')
        plt.ylabel(lables_on_y[n])
        plt.tight_layout()
        plt.show()

def modify_input():
    """Modify the input parameters and run the simulation.

    Returns:
    - None
    """
    modify_input_question = questionary.select(
        f"Do you want to modify the inputs?",
        choices=["Yes", "No"],
        default="No"
    ).ask()

    if modify_input_question == "Yes":
        parameters = {
            't_in': int(questionary.text("Enter initial time:", validate=lambda val: val.isdigit(), default="0").ask()),
            't_end': int(questionary.text("Enter end time:", validate=lambda val: val.isdigit(), default="5").ask()),
            'N': int(questionary.text("Enter number of steps:", validate=lambda val: val.isdigit(), default="5000").ask()),
            'mu': float(questionary.text("Enter value for mu:", validate=lambda val: not val.isdigit(), default="0.009").ask()),
            'b0': float(questionary.text("Enter value for b0:", validate=lambda val: not val.isdigit(), default="36.4").ask()),
            'b1': float(questionary.text("Enter value for b1:", validate=lambda val: not val.isdigit(), default="0.38").ask()),
            'phi': float(questionary.text("Enter value for phi:", validate=lambda val: not val.isdigit(), default="1.07").ask()),
            'gamma': float(questionary.text("Enter value for gamma:", validate=lambda val: not val.isdigit(), default="1.8").ask()),
            'ni': int(questionary.text("Enter value for ni:", validate=lambda val: val.isdigit(), default="36").ask()),
            'alpha': float(questionary.text("Enter value for alpha:", validate=lambda val: not val.isdigit(), default="0.009").ask()),
            'S_in': float(questionary.text("Enter value for S_in:", validate=lambda val: not val.isdigit(), default="0.9988").ask()),
            'I_in': float(questionary.text("Enter value for I_in:", validate=lambda val: not val.isdigit(), default="0.0012").ask()),
            'R_in': float(questionary.text("Enter value for R_in:", validate=lambda val: not val.isdigit(), default="0.0").ask())
            }

        # Call the function to simulate and plot
        simulate_and_plot(parameters)
            
    else:
        
        # Define parameters
        parameters = {
            't_in' : 0,
            't_end': 5,
            'N': 5000,
            'mu': 0.009,
            'b0': 36.4,
            'b1': 0.38,
            'phi': 1.07,
            'gamma': 1.8,
            'ni': 36,
            'alpha': 0.009,
            'S_in': 0.9988,
            'I_in': 0.0012,
            'R_in': 0
            }
        # Call the function to simulate and plot
        simulate_and_plot(parameters)

modify_input()
