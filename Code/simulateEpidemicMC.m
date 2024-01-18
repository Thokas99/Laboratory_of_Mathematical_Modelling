function simulateEpidemicMC(c, beta, gamma, nu, a, T, dt, numPaths)
    figure;

    for path = 1:numPaths
        [~, I, ~, t] = simulateEpidemicSDE(c, beta, gamma, nu, a, T, dt);
        % Plot each realization
        plot(t, I, 'r');
        hold on;
    end

    xlabel('Time');
    ylabel('Population of Infected (I(t))');
    %legend('Realization 1', 'Realization 2', 'Realization 3', 'Realization 4','Realization 5');  % Add legend for each path
    title('Monte Carlo Simulation of Epidemic with Birth Rate Perturbation');
end

function [S, I, R, t] = simulateEpidemicSDE(c, beta, gamma, nu, a, T, dt)
    % Parameters
    t = 0:dt:T;
    n = length(t);
    
    % Initialize arrays
    S = zeros(1, n);
    I = zeros(1, n);
    R = zeros(1, n);
    
    % Initial conditions
    S(1) = 0.8;
    I(1) = 0.2;
    R(1) = 0.0;

    % Simulation using Euler-Maruyama method
    for i = 2:n
        dW = sqrt(dt) * randn();
        
        % Birth rate perturbation
        c_tilde = c + a * dW;
        
        % Update equations
        dS = (c_tilde - c * S(i-1) - beta * S(i-1) * I(i-1) + gamma * R(i-1)) * dt + a * (1 - S(i-1)) * dW;
        dI = (beta * S(i-1) * I(i-1) - nu * I(i-1) - c_tilde * I(i-1)) * dt - a * I(i-1) * dW;
        dR = (nu * I(i-1) - c * R(i-1) - gamma * R(i-1)) * dt - a * R(i-1) * dW;

        % Update states
        S(i) = S(i-1) + dS;
        I(i) = I(i-1) + dI;
        R(i) = R(i-1) + dR;
    end

    % Plot the results
    %plotEpidemicResults(t, I);
end



