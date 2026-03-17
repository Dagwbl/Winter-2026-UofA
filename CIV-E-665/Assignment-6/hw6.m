clear; clc; close all;

%% Shape function coefficients
E1 = [1,0,0; 1,5,0; 1,5,1];
E2 = [1,0,1; 1,0,0; 1,5,1];
psi1 = inv(E1)
psi2 = inv(E2)

%% B matrices (strain-displacement)
% Element 1: local nodes (1,2,3) -> global nodes (2,3,4)
% psi1 betas: [-0.2, 0.2, 0], gammas: [0, -1, 1]
B1 = [
    -0.2,    0,  0.2,    0,   0,   0;
       0,    0,    0, -1.0,   0, 1.0;
       0, -0.2, -1.0,  0.2, 1.0,   0
];

% Element 2: local nodes (1,2,3) -> global nodes (1,2,4)
% psi2 betas: [-0.2, 0, 0.2], gammas: [1, -1, 0]
B2 = [
   -0.2,    0,    0,    0,  0.2,   0;
      0,  1.0,    0, -1.0,    0,   0;
    1.0, -0.2, -1.0,    0,    0, 0.2
];

%% Material properties
E_mod = 100e9;  % Young's modulus (Pa)
nu = 0.3;       % Poisson's ratio
t = 0.2;        % Thickness (m)

% Material constants for plane stress condition
c11 = E_mod / (1 - nu^2);
c22 = c11;
c12 = E_mod * nu / (1 - nu^2);
c66 = E_mod / (2 * (1 + nu));

C1 = [c11 c12 0; c12 c22 0; 0 0 c66]
C2 = C1;

%% Element stiffness matrices: K^e = B^T * C * B * t * A
K1 = 0.5 * B1' * C1 * B1 * t * det(E1)
K2 = 0.5 * B2' * C2 * B2 * t * det(E2)

%% Assemble global stiffness matrix (8x8)
% Global DOF ordering: [u1x, u1y, u2x, u2y, u3x, u3y, u4x, u4y]
% Element 1: local (1,2,3) -> global (2,3,4) -> DOFs [3,4,5,6,7,8]
% Element 2: local (1,2,3) -> global (1,2,4) -> DOFs [1,2,3,4,7,8]
K_global = zeros(8, 8);

e1_dofs = [3, 4, 5, 6, 7, 8];
for i = 1:6
    for j = 1:6
        K_global(e1_dofs(i), e1_dofs(j)) = K_global(e1_dofs(i), e1_dofs(j)) + K1(i, j);
    end
end

e2_dofs = [1, 2, 3, 4, 7, 8];
for i = 1:6
    for j = 1:6
        K_global(e2_dofs(i), e2_dofs(j)) = K_global(e2_dofs(i), e2_dofs(j)) + K2(i, j);
    end
end

disp('Global K (8x8) / 1e10 =');
disp(K_global / 1e10);

%% Apply boundary conditions and solve
% Nodes 1,2 fixed -> DOFs 1,2,3,4 = 0
% Free DOFs: 5,6,7,8 -> [u3x, u3y, u4x, u4y]
free_dofs = [5, 6, 7, 8];
K_reduced = K_global(free_dofs, free_dofs);

disp('Reduced K (4x4) / 1e10 =');
disp(K_reduced / 1e10);

% Force: 1000 N in x-direction at nodes 3 and 4
F_reduced = [1000; 0; 1000; 0];

U_active = K_reduced \ F_reduced;

disp('Nodal Displacements [u3x; u3y; u4x; u4y] (in meters):');
disp(U_active);

% Full global displacement vector
U_global = zeros(8, 1);
U_global(free_dofs) = U_active;
disp('Full Global Displacement Vector:');
disp(U_global);
