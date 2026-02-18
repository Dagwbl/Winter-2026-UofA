% CIV E 665 - Assignment 5, Question 2
% Cantilever Beam FEM Solution (2 Euler-Bernoulli elements, Reddy formulation)
clear; clc;

%% Parameters
E = 100e9;        % Pa
t = 0.1;          % m (square cross section)
I_val = t^4/12;   % m^4
EI = E * I_val;   % N*m^2
L = 1.0;          % m
n_elem = 2;
Le = L / n_elem;  % 0.5 m
F0 = 100.0;       % N (point force at free end)
M0 = -10.0;       % N*m (point moment at free end, Reddy convention)

C = 2 * EI / Le^3;

fprintf('EI = %.4f N*m^2\n', EI);
fprintf('C  = %.4f N/m\n', C);
fprintf('Le = %.1f m\n', Le);

%% Element Stiffness Matrix (Reddy formulation)
K_e = C * [ 6,      -3*Le,    -6,      -3*Le;
           -3*Le,    2*Le^2,   3*Le,    Le^2;
           -6,       3*Le,     6,       3*Le;
           -3*Le,    Le^2,     3*Le,    2*Le^2];

%% Global Assembly (6x6)
K_global = zeros(6, 6);
K_global(1:4, 1:4) = K_global(1:4, 1:4) + K_e;  % Element 1
K_global(3:6, 3:6) = K_global(3:6, 3:6) + K_e;  % Element 2

%% Element Force Vectors
f1 = [21.25; -5/3; 16.25; 35/24];
f2 = [8.75; -0.625; 3.75; 5/12];

F_global = zeros(6, 1);
F_global(1:4) = F_global(1:4) + f1;
F_global(3:6) = F_global(3:6) + f2;
F_global(5) = F_global(5) + F0;   % Point force
F_global(6) = F_global(6) + M0;   % Point moment

fprintf('\nGlobal Force Vector F =\n');
disp(F_global');

%% Apply BCs: W1 = W2 = 0 (fixed at Node 1)
free = 3:6;
K_red = K_global(free, free);
F_red = F_global(free);

fprintf('Reduced K (4x4):\n');
disp(K_red);
fprintf('Reduced F:\n');
disp(F_red');

%% Solve
W = zeros(6, 1);
W(free) = K_red \ F_red;

fprintf('\n%s\n', repmat('=', 1, 60));
fprintf('FEM Nodal Values:\n');
fprintf('%s\n', repmat('=', 1, 60));
labels = {'W1 (w1)', 'W2 (th1)', 'W3 (w2)', 'W4 (th2)', 'W5 (w3)', 'W6 (th3)'};
units  = {'m', 'rad', 'm', 'rad', 'm', 'rad'};
for i = 1:6
    fprintf('  %-12s = % .6e  %s\n', labels{i}, W(i), units{i});
end

%% Reconstruct w(x) using Hermite shape functions
psi1 = @(xb) 1 - 3*(xb/Le).^2 + 2*(xb/Le).^3;
psi2 = @(xb) -xb .* (1 - xb/Le).^2;
psi3 = @(xb) 3*(xb/Le).^2 - 2*(xb/Le).^3;
psi4 = @(xb) -xb .* (-(xb/Le) + (xb/Le).^2);

n_pts = 300;

% Element 1
x_e1 = linspace(0, Le, n_pts);
w_e1 = W(1)*psi1(x_e1) + W(2)*psi2(x_e1) + W(3)*psi3(x_e1) + W(4)*psi4(x_e1);

% Element 2
x_e2_local = linspace(0, Le, n_pts);
x_e2 = x_e2_local + Le;
w_e2 = W(3)*psi1(x_e2_local) + W(4)*psi2(x_e2_local) + W(5)*psi3(x_e2_local) + W(6)*psi4(x_e2_local);

x_fem = [x_e1, x_e2];
w_fem = [w_e1, w_e2];

%% Exact Analytical Solution
C1_exact = -150.0;
C2_exact = 380.0/3.0;

w_exact = @(x) (-50*x.^5/60 + 50*x.^4/12 + C1_exact*x.^3/6 + C2_exact*x.^2/2) / EI;

x_exact = linspace(0, 1, 500);
w_exact_vals = w_exact(x_exact);

fprintf('\n%s\n', repmat('=', 1, 60));
fprintf('Exact Solution Values:\n');
fprintf('%s\n', repmat('=', 1, 60));
fprintf('  w_exact(0.5) = %.10e m\n', w_exact(0.5));
fprintf('  w_exact(1.0) = %.10e m\n', w_exact(1.0));
fprintf('  FEM w(0.5)   = %.10e m\n', W(3));
fprintf('  FEM w(1.0)   = %.10e m\n', W(5));
fprintf('  Error at x=0.5: %.4f%%\n', abs(W(3) - w_exact(0.5))/abs(w_exact(0.5))*100);
fprintf('  Error at x=1.0: %.4f%%\n', abs(W(5) - w_exact(1.0))/abs(w_exact(1.0))*100);

%% Plot
figure;
plot(x_fem, w_fem*1e3, 'b-', 'LineWidth', 2); hold on;
plot(x_exact, w_exact_vals*1e3, 'r--', 'LineWidth', 1.5);
plot([0, Le, 2*Le], [W(1), W(3), W(5)]*1e3, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'k');

xlabel('x (m)', 'FontSize', 13);
ylabel('w(x) (mm)', 'FontSize', 13);
title('Deflection of Cantilever Beam (Question 2)', 'FontSize', 14);
legend('FEM Solution (2 elements)', 'Exact Solution', 'FEM Nodes', 'FontSize', 11);
grid on;
set(gca, 'FontSize', 11);

saveas(gcf, './assets/q2_deflection_matlab.png');
fprintf('\nPlot saved to ./assets/q2_deflection_matlab.png\n');
