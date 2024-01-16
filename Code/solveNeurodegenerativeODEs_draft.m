function solveNeurodegenerativeODEs_draft()
    % Initial values
    AiBeta = 1e-6;     % Amyloid Beta inside neurons (g/ml)
    AoBeta = 1e-8;     % Amyloid Beta outside neurons (g/ml)
    Tau = 1.37e-10;    % Tan Protein (g/ml)
    Fi = 3.36e-10;     % NFTs inside neurons (g/ml)
    Fo = 3.36e-11;     % NFTs outside neurons (g/ml)
    A = 0.14;          % Astroglias (g/ml)
    M1 = 0.02;         % Proinflammatory Microglias (g/ml)
    M2 = 0.02;         % Anti-inflammatory Microglias (g/ml)
    N = 0.14;          % Neurons (g/ml)

    % Parameters
    lambda_Nd = 0.05365;          % Neuron death rate (1/day)
    lambda_iBeta = 9.51e-6;       % Production rate of Aiβ (g/ml/day)
    lambda_N = 8e-9;              % Production rate of Aoβ by neuron (g/ml/day)
    lambda_MA = 0.045;            % Production rate of astrocytes by M1 (g/ml/day)
    lambda_A = 8e-10;             % Production rate of Aoβ by astrocytes (g/ml/day)
    lambda_tau = 1.35e-11;        % Production rate of Tau proteins by ROS (g/ml/day)
    lambda_F = 1.662e-3;          % Production rate of NFT by Tau (1/day)
    lambda_AA_beta_o = 1.793;     % Production/Activation rate of astrocytes by Aβo (1/day)
    lambda_tau_0 = 8.1e-11;       % Production of Tau proteins (healthy) (1/day)
    lambda_MF = 2e-2;             % Production/Activation rate of Microglias by NFT (1/day)

    % Degradation rates
    d_Fi = 2.77e-3;               % Degradation rate for Fi (1/day)
    d_F0 = 2.77e-4;               % Degradation rate for Fo (1/day)
    d_M1 = 0.015;                 % Degradation rate for M1 (1/day)
    d_M2 = 0.015;                 % Degradation rate for M2 (1/day)
    d_A_beta_o_M = 2e-3;          % Clearance rate of Aoβ by microglia (1/day)
    d_Ai_beta = 9.51;             % Clearance rate of Aiβ (1/day)
    d_A = 1.2e-3;                 % Death rate of astrocytes (1/day)
    d_NF = 3.4e-4;                % Death rate of neurons by NFT (1/day)
    d_tau = 0.277;                % Degradation of τ proteins (1/day)

    % Michaelis-Menten constants
    K_Fi = 3.36e-10;              % Half-saturation of intracellular NFTs (g/ml)
    K_Fo = 2.58e-11;              % Average of extracellular NFTs (g/ml)
    K_Ao_beta = 7e-3;             % Michaelis-Menten coefficient for Aoβ (g/cm3)

    % Other parameters
    M0_G = 0.047;                 % Source of Microglia (g/cm3)
    beta_M1 = 0.9;                % Measure of inflammation for M1
    beta_M2 = 0.09;               % Measure of inflammation for M2
    theta = 0.9;                  % M1/M2 effectivity in clearance of Aoβ
    R0 = 6;                       % Initial inflammation by ROS
    N0 = 0.14;                    % Reference density of neurons (g/cm3)
    A0 = 0.14;                    % Reference density of astrocytes (g/cm3)

    % Define ODEs
    odes = @(t, y) [
        -lambda_Nd * y(1) - lambda_N * y(1) - lambda_F * y(1) * y(5) + d_NF * y(8) * (1 - exp(-beta_M2 * y(7))) * y(1);
        lambda_iBeta - d_Ai_beta * y(2);
        lambda_F * y(1) * y(5) - d_Fi * y(3);
        lambda_F * y(1) * y(5) - d_F0 * y(4);
        lambda_tau * R0 * (1 - exp(-beta_M1 * y(6))) - d_tau * y(5);
        lambda_N * y(1) - d_A_beta_o_M * y(6) * y(8) - lambda_tau * y(5) + d_tau * y(5);
        lambda_MA * (1 - exp(-theta * beta_M1 * y(7))) - d_A * y(7);
        lambda_MA * exp(-theta * beta_M2 * y(7)) - d_A * y(8)
    ];

    % Solve ODEs numerically
    timeSpan = [0 1000];
    initialConditions = [N0; AiBeta; Fi; Fo; Tau; AoBeta; M1; M2];
    [t, solution] = ode45(odes, timeSpan, initialConditions);

    % Plot the results
    figure;

    % Population N over time
    subplot(3, 2, 1);
    plot(t, solution(:, 1), 'LineWidth', 2);
    xlabel('Time');
    ylabel('Population N');
    title('Population N Over Time');

    % Intracellular NFTs (Fi) over time
    subplot(3, 2, 2);
    plot(t, solution(:, 3), 'LineWidth', 2);
    xlabel('Time');
    ylabel('Intracellular NFTs (Fi)');
    title('Intracellular NFTs (Fi) Over Time');

    % Extracellular NFTs (Fo) over time
    subplot(3, 2, 3);
    plot(t, solution(:, 4), 'LineWidth', 2);
    xlabel('Time');
    ylabel('Extracellular NFTs (Fo)');
    title('Extracellular NFTs (Fo) Over Time');

    % Tau proteins over time
    subplot(3, 2, 4);
    plot(t, solution(:, 5), 'LineWidth', 2);
    xlabel('Time');
    ylabel('Tau Proteins');
    title('Tau Proteins Over Time');

    % Astrocytes over time
    subplot(3, 2, 5);
    plot(t, solution(:, 7), 'LineWidth', 2);
    xlabel('Time');
    ylabel('Astrocytes');
    title('Astrocytes Over Time');

    % Microglia (M1 + M2) over time
    subplot(3, 2, 6);
    plot(t, solution(:, 7) + solution(:, 8), 'LineWidth', 2);
    xlabel('Time');
    ylabel('Microglia (M1 + M2)');
    title('Microglia (M1 + M2) Over Time');

    % Adjust layout
    sgtitle('Neurodegenerative Model Simulation');
end
