import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

m = 1                    # kg (bob mass)
L = 1                    # m (pendulum length)
g = 9.81                 # m/s^2
angle_0 = np.radians(60) # deg to rad (initial angular displacement)
v_0 = 0                  # m/s (tangential vel)
step = 0                 # starting simulation time step 
dt = 0.01                # time step for integration calculation
angle = [angle_0]        # prepare array for angle data
v = [v_0]                # prepare array for vel data

def pendulum_acceleration(angle):
    return -g/L * np.sin(angle)

def rk4_step(angle, v, dt):
    k1_a = pendulum_acceleration(angle)
    k1_v = v

    k2_a = pendulum_acceleration(angle + k1_v * dt / 2)
    k2_v = v + k1_a * dt / 2

    k3_a = pendulum_acceleration(angle + k2_v * dt / 2)
    k3_v = v + k2_a * dt / 2

    k4_a = pendulum_acceleration(angle + k3_v * dt)
    k4_v = v + k3_a * dt

    angle_new = angle + (k1_v + 2 * k2_v + 2 * k3_v + k4_v) * dt / 6
    v_new = v + (k1_a + 2 * k2_a + 2 * k3_a + k4_a) * dt / 6

    return angle_new, v_new

# Simulate for a desired number of steps
num_steps = 1000

for _ in range(num_steps):
    angle_new, v_new = rk4_step(angle[-1], v[-1], dt)
    angle.append(angle_new)
    v.append(v_new)

x0 = L * np.sin(angle[-1])
y0 = -L * np.cos(angle[-1])

fig, ax = plt.subplots()
ax.set_xlim(-L*1.15, L*1.15)
ax.set_ylim(-L*1.15, L*1.15)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_aspect('equal')
ax.text(0.5, 0.5, 'orcid.org/0000-0002-7326-7502', transform=ax.transAxes, fontsize=8, color='gray', alpha=0.5, ha='center', va='center', rotation=0)
graph = ax.plot([0, x0], [0, y0], lw=2, color='grey')[0]

bob = ax.add_patch(plt.Circle((x0, y0), 0.08,
                      color='red', zorder=2))

def animate(frame_i):
    x, y = L * np.sin(angle[frame_i]), -L * np.cos(angle[frame_i])
    graph.set_data([0, x], [0, y])
    bob.set_center((x, y))

anim = FuncAnimation(fig, 
                    animate, 
                    frames=len(angle), 
                    interval=2,
                    repeat=True,
                    )

#anim.save(r'1pendulum.mp4')
#anim#anim.save('1pendulum.gif', writer='PillowWriter', fps=40)
plt.show()

