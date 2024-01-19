import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def dW(delta_t: float) -> float:
    """Sample a random number at each call."""
    return np.random.normal(loc=0.0, scale=np.sqrt(delta_t))

def simulate_epidemic(mu, b0, b1, phi, gamma, ni, alpha, S0, I0, R0, t_in, t_end, num_steps):
    dt = (t_end - t_in) / num_steps
    TS = np.linspace(t_in, t_end, num_steps + 1)

    S, I, R = np.zeros(num_steps + 1), np.zeros(num_steps + 1), np.zeros(num_steps + 1)
    S[0], I[0], R[0] = S0, I0, R0

    for i in range(1, num_steps + 1):
        t = t_in + (i - 1) * dt
        beta = b0 * (1 + b1 * np.cos(2 * np.pi * t + phi))
        mu_tilde = mu + alpha * dW(dt)

        # Update equations using Euler-Maruyama method
        dS = (mu_tilde - mu * S[i - 1] - beta * S[i - 1] * I[i - 1] + gamma * R[i - 1]) * dt + alpha * (1 - S[i - 1]) * dW(dt)
        dI = (beta * S[i - 1] * I[i - 1] - ni * I[i - 1] - mu_tilde * I[i - 1]) * dt - alpha * I[i - 1] * dW(dt)
        dR = (ni * I[i - 1] - mu * R[i - 1] - gamma * R[i - 1]) * dt - alpha * R[i - 1] * dW(dt)

        # Update states
        S[i] = S[i - 1] + dS
        I[i] = I[i - 1] + dI
        R[i] = R[i - 1] + dR

    return pd.DataFrame({'Time': TS, 'Susceptible': S, 'Infected': I, 'Recovered': R})

def plot_epidemic_results(data):
    sns.set_style('whitegrid')
    plt.figure(figsize=(10, 6))

    # Plot the results
    sns.lineplot(x='Time', y='Infected', data=data, label='Infected', color='red')
    plt.xlabel('Time')
    plt.ylabel('Population of Infected (I(t))')
    plt.title('Epidemic Simulation with Birth Rate Perturbation')
    plt.legend()
    plt.show()

# Parameters
mu_val, b0_val, b1_val, phi_val, gamma_val, ni_val, alpha_val = 0.015, 36.4, 0.38, 1.07, 1.8, 36, 0.009
S0_val, I0_val, R0_val = 0.9988, 0.0012, 0.0
t_initial, t_final, num_steps_val = 0, 10, 50000

# Run simulation
epidemic_data = simulate_epidemic(mu_val, b0_val, b1_val, phi_val, gamma_val, ni_val, alpha_val,
                                  S0_val, I0_val, R0_val, t_initial, t_final, num_steps_val)

# Plot results
plot_epidemic_results(epidemic_data)
