import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Double pendulum equations
def double_pendulum_equations(t, y, L1, L2, m1, m2, g):
    theta1, theta2, p1, p2 = y
    cos_diff = np.cos(theta1 - theta2)
    sin_diff = np.sin(theta1 - theta2)
    
    # Angular velocities
    theta1_dot = (L2 * p1 - L1 * p2 * cos_diff) / (L1 ** 2 * L2 * (m1 + m2 * sin_diff ** 2))
    theta2_dot = (-L1 * m1 * p1 - L1 * m2 * p1 * cos_diff + (m1 + m2) * L2 * p2) / (L1 * L2 ** 2 * (m1 + m2 * sin_diff ** 2))
    
    # Time derivatives of momenta
    p1_dot = - (m1 + m2) * g * L1 * np.sin(theta1) - m2 * L1 * L2 * theta2_dot * theta1_dot * sin_diff
    p2_dot = - m2 * g * L2 * np.sin(theta2) + m2 * L1 * L2 * theta1_dot * theta2_dot * sin_diff
    
    return [theta1_dot, theta2_dot, p1_dot, p2_dot]

# Animation function
def animate(i):
    ax.clear()
    ax.set_xlim(-L1 - L2, L1 + L2)
    ax.set_ylim(-L1 - L2, L1 + L2)
    
    x1 = L1 * np.sin(sol.y[0][i])
    y1 = -L1 * np.cos(sol.y[0][i])
    x2 = x1 + L2 * np.sin(sol.y[1][i])
    y2 = y1 - L2 * np.cos(sol.y[1][i])
    
    ax.plot([0, x1], [0, y1], 'r-', linewidth=2)
    ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2)
    ax.plot([x1], [y1], 'ro', markersize=12)
    ax.plot([x2], [y2], 'bo', markersize=12)
    ax.plot([x2], [y2], 'ko', markersize=4)
    
    ax.text(0.5, 0.5, 'orcid.org/0000-0002-7326-7502', transform=ax.transAxes, fontsize=8, color='gray', alpha=0.5, ha='center', va='center', rotation=0)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

# Parameters
L1, L2 = 1, 1
m1, m2 = 1, 1
g = 9.81
t_span = (0, 20)
t_eval = np.linspace(t_span[0], t_span[1], 500)

# Initial conditions [theta1, theta2, p1, p2]
y0 = [np.pi / 2, np.pi, 0, 0]
sol = solve_ivp(double_pendulum_equations, t_span, y0, args=(L1, L2, m1, m2, g), t_eval=t_eval, rtol=1e-8, atol=1e-8)

# Set up the plot
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')

# Create the animation
anim = FuncAnimation(fig, animate, frames=len(t_eval), interval=40, blit=False)

# Display the animation
#anim.save('2pendulum.gif', writer='PillowWriter', fps=40)
plt.show()