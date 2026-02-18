"""
CIV E 665 - Assignment 5, Question 2
Cantilever Beam FEM Solution (2 Euler-Bernoulli elements, Reddy formulation)
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ==============================================================================
# Parameters
# ==============================================================================
E = 100e9        # Pa
t = 0.1          # m (square cross section)
I_val = t**4/12  # m^4
EI = E * I_val   # N*m^2
L = 1.0          # m
n_elem = 2
Le = L / n_elem  # 0.5 m
F0 = 100.0       # N (point force at free end)
M0 = -10.0       # N*m (point moment at free end, Reddy convention)

C = 2 * EI / Le**3  # stiffness coefficient

print(f"EI = {EI:.4f} N*m^2")
print(f"C  = {C:.4f} N/m")
print(f"Le = {Le} m")

# ==============================================================================
# Element Stiffness Matrix (Reddy formulation)
# ==============================================================================
def elem_stiffness(C, Le):
    return C * np.array([
        [6,      -3*Le,    -6,      -3*Le   ],
        [-3*Le,   2*Le**2,  3*Le,    Le**2   ],
        [-6,      3*Le,     6,       3*Le    ],
        [-3*Le,   Le**2,    3*Le,    2*Le**2 ]
    ])

K_e = elem_stiffness(C, Le)

# ==============================================================================
# Global Assembly (6x6)
# ==============================================================================
K_global = np.zeros((6, 6))
K_global[0:4, 0:4] += K_e   # Element 1 -> DOFs [1,2,3,4]
K_global[2:6, 2:6] += K_e   # Element 2 -> DOFs [3,4,5,6]

# ==============================================================================
# Element Force Vectors (from analytical integration)
# ==============================================================================
# Element 1: q(x) = -100x + 100, x in [0, 0.5]
f1 = np.array([21.25, -5/3, 16.25, 35/24])

# Element 2: q(x) = -100x + 100, x in [0.5, 1.0]
f2 = np.array([8.75, -0.625, 3.75, 5/12])

F_global = np.zeros(6)
F_global[0:4] += f1
F_global[2:6] += f2

# Add point loads at Node 3 (DOFs 5 and 6, indices 4 and 5)
F_global[4] += F0   # Point force
F_global[5] += M0   # Point moment

print(f"\nGlobal Force Vector F = {F_global}")

# ==============================================================================
# Apply Boundary Conditions: W1 = W2 = 0 (fixed at Node 1)
# ==============================================================================
free_dofs = [2, 3, 4, 5]  # DOFs 3,4,5,6
K_red = K_global[np.ix_(free_dofs, free_dofs)]
F_red = F_global[free_dofs]

print(f"\nReduced K (4x4):")
print(K_red)
print(f"\nReduced F = {F_red}")

# ==============================================================================
# Solve
# ==============================================================================
W_red = np.linalg.solve(K_red, F_red)
W = np.zeros(6)
W[free_dofs] = W_red

print(f"\n{'='*60}")
print(f"FEM Nodal Values:")
print(f"{'='*60}")
labels = ['W1 (w₁)', 'W2 (θ₁)', 'W3 (w₂)', 'W4 (θ₂)', 'W5 (w₃)', 'W6 (θ₃)']
for i in range(6):
    print(f"  {labels[i]:12s} = {W[i]: .6e}  {'m' if i%2==0 else 'rad'}")

print(f"\nIn matrix form (scientific notation):")
print(f"  W3 = {W[2]:.10e} m")
print(f"  W4 = {W[3]:.10e} rad")
print(f"  W5 = {W[4]:.10e} m")
print(f"  W6 = {W[5]:.10e} rad")

# ==============================================================================
# Reconstruct w(x) using Hermite shape functions (Reddy formulation)
# ==============================================================================
def psi1(xb, Le):
    xi = xb / Le
    return 1 - 3*xi**2 + 2*xi**3

def psi2(xb, Le):
    return -xb * (1 - xb/Le)**2

def psi3(xb, Le):
    xi = xb / Le
    return 3*xi**2 - 2*xi**3

def psi4(xb, Le):
    xi = xb / Le
    return -xb * (-xi + xi**2)

# Element 1: x in [0, Le], local coords = x
n_pts = 300
x_e1 = np.linspace(0, Le, n_pts)
w_e1 = (W[0]*psi1(x_e1, Le) + W[1]*psi2(x_e1, Le) +
        W[2]*psi3(x_e1, Le) + W[3]*psi4(x_e1, Le))

# Element 2: x in [Le, 2*Le], local coords = x - Le
x_e2_local = np.linspace(0, Le, n_pts)
x_e2 = x_e2_local + Le
w_e2 = (W[2]*psi1(x_e2_local, Le) + W[3]*psi2(x_e2_local, Le) +
        W[4]*psi3(x_e2_local, Le) + W[5]*psi4(x_e2_local, Le))

x_fem = np.concatenate([x_e1, x_e2])
w_fem = np.concatenate([w_e1, w_e2])

# ==============================================================================
# Exact Analytical Solution
# ==============================================================================
# EI w'''' = q(x) = -100x + 100
# BCs: w(0) = 0, w'(0) = 0
# Natural BCs at x=1 (Reddy convention):
#   Q_w = -EI w'''(1) = F0  =>  EI w'''(1) = -F0 = -100
#   Q_θ = -EI w''(1) = M0   =>  EI w''(1) = -M0 = 10
#
# Integrating EI w'''' = -100x + 100:
#   EI w''' = -50x^2 + 100x + C1
#   EI w''  = -50x^3/3 + 50x^2 + C1*x + C2
#   EI w'   = -50x^4/12 + 50x^3/3 + C1*x^2/2 + C2*x + C3
#   EI w    = -50x^5/60 + 50x^4/12 + C1*x^3/6 + C2*x^2/2 + C3*x + C4
#
# From BCs:
#   w(0) = 0 => C4 = 0
#   w'(0) = 0 => C3 = 0
#   EI w'''(1) = -100: -50 + 100 + C1 = -100 => C1 = -150
#   EI w''(1) = 10: -50/3 + 50 - 150 + C2 = 10 => C2 = 110 + 50/3 = 380/3

C1_exact = -150.0
C2_exact = 380.0/3.0

def w_exact(x):
    EI_w = (-50*x**5/60 + 50*x**4/12 + C1_exact*x**3/6 + C2_exact*x**2/2)
    return EI_w / EI

x_exact = np.linspace(0, 1, 500)
w_exact_vals = w_exact(x_exact)

print(f"\n{'='*60}")
print(f"Exact Solution Values:")
print(f"{'='*60}")
print(f"  w_exact(0.5) = {w_exact(0.5):.10e} m")
print(f"  w_exact(1.0) = {w_exact(1.0):.10e} m")
print(f"\n  FEM w(0.5)   = {W[2]:.10e} m")
print(f"  FEM w(1.0)   = {W[4]:.10e} m")

print(f"\n  Error at x=0.5: {abs(W[2] - w_exact(0.5))/abs(w_exact(0.5))*100:.4f}%")
print(f"  Error at x=1.0: {abs(W[4] - w_exact(1.0))/abs(w_exact(1.0))*100:.4f}%")

# ==============================================================================
# Plot
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

# FEM
ax.plot(x_fem, w_fem * 1e3, 'b-', linewidth=2, label='FEM Solution (2 elements)')

# Exact
ax.plot(x_exact, w_exact_vals * 1e3, 'r--', linewidth=1.5, label='Exact Solution')

# Node markers
nodes_x = [0, Le, 2*Le]
nodes_w = [W[0], W[2], W[4]]
ax.plot(nodes_x, np.array(nodes_w)*1e3, 'ko', markersize=8, zorder=5, label='FEM Nodes')

ax.set_xlabel('x (m)', fontsize=13)
ax.set_ylabel('w(x) (mm)', fontsize=13)
ax.set_title('Deflection of Cantilever Beam (Question 2)', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.tick_params(labelsize=11)

fig.tight_layout()
fig.savefig('./assets/q2_deflection.png', dpi=150, bbox_inches='tight')
print(f"\nPlot saved to ./assets/q2_deflection.png")
