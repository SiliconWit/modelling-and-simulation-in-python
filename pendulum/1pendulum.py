import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

m = 1                    # kg (bob mass)
L = 1                    # m (pendulum lenth)
g = 9.81                 # m/s/s
angle_0 = np.radians(60) # deg to rad (initial angular displacement)
v_0 = 0                  # m/s (tangential vel)
step = 0                 # starting simulation time step 
dt = 0.01                # time step for integration calculation
angle = [angle_0]        # prepare array for angle data
v = [v_0]                # prepare array for vel data
angle_old = angle_0

# Period calculation 
T = 2 * np.pi * np.sqrt(L / g)

while 1==1:
    step += 1
    t = step * dt

    angle_old, v_old = angle[-1], v[-1]
    arc_lenth = v_old * dt
    angle_change = arc_lenth/L
    angle_new = angle_old - angle_change

    acc = -g * np.sin(angle_old)
    v_new = v_old - acc * dt

    if t > T:
        # end
        break

    angle.append(angle_new)
    v.append(v_new)

x0 = L * np.sin(angle_old)
y0 = -L * np.cos(angle_old)

fig, ax = plt.subplots()
ax.set_xlim(-L*1.15, L*1.15)
ax.set_ylim(-L*1.15, L*1.15)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_aspect('equal')
ax.text(0.5, 0.5, 'orcid.org/0000-0002-7326-7502', transform=ax.transAxes, fontsize=8, color='gray', alpha=0.5, ha='center', va='center', rotation=0)
graph = ax.plot([0, x0], [0, y0], lw=2, color='grey')[0]

bob = ax.add_patch(plt.Circle((x0,y0), 0.08,
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
#anim.save('1pendulum.gif', writer='PillowWriter', fps=40)
plt.show()
