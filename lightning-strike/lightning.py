import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def generate_lightning(x, y, angle, length, branching_factor, decay_factor, depth, max_depth, seed):
    if length < 1 or depth > max_depth:
        return []
    
    np.random.seed(seed)
    x_new = x + length * np.cos(angle)
    y_new = y + length * np.sin(angle)
    segments = [((x, y), (x_new, y_new))]
    
    if depth == 0:
        branching_factor = 1
    
    for i in range(branching_factor):
        angle_branch = angle + np.random.uniform(-np.pi/4, np.pi/4)
        length_branch = length * decay_factor
        child_seed = seed * 10 + i + 1
        segments += generate_lightning(x_new, y_new, angle_branch, length_branch, 2, decay_factor, depth + 1, max_depth, child_seed)
    
    return segments

def update(frame):
    plt.gca().clear()
    plt.gca().set_xlim(-100, 100)
    plt.gca().set_ylim(0, 200)
    segments = generate_lightning(0, 200, -np.pi/2, 100, 2, 0.5, 0, frame, 0)
    for segment in segments:
        plt.plot(*zip(*segment), color='blue', linewidth=0.8)
    return []

fig = plt.figure()
ani = FuncAnimation(fig, update, frames=range(10), interval=200, blit=True)
writer = PillowWriter(fps=5)
ani.save('lightning.gif', writer=writer)
plt.show()

