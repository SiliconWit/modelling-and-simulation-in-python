import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Function to create lightning bolt segments recursively
def create_segments(segments, generations, max_offset, decay_factor):
    # If there are no more generations left, return the segments
    if generations == 0:
        return segments

    # Create an empty list to store new segments
    new_segments = []
    
    # Loop through the existing segments
    for segment in segments:
        # Unpack the segment start and end points
        start, end = segment
        
        # Calculate the midpoint of the segment
        mid = 0.5 * (start + end)
        
        # Calculate the normal vector (perpendicular) to the segment
        normal = np.array([-(end[1] - start[1]), end[0] - start[0]], dtype=float)
        
        # Normalize the normal vector
        normal /= np.linalg.norm(normal)
        
        # Calculate a random offset for the midpoint
        offset = np.random.uniform(-max_offset, max_offset)
        
        # Apply the offset to the midpoint along the normal
        mid += normal * offset

        # Add two new segments with the new midpoint
        new_segments.append((start, mid))
        new_segments.append((mid, end))

        # Occasionally create a branch from the midpoint
        if np.random.rand() < 0.3:
            # Calculate the direction vector of the segment
            direction = end - start
            direction /= np.linalg.norm(direction)

            # Calculate a random angle for the branch
            angle = np.random.uniform(-np.pi / 4, np.pi / 4)

            # Create a rotation matrix for the angle
            rot_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

            # Rotate the direction vector to create the branch
            direction = rot_matrix.dot(direction)

            # Add the branch to the new segments
            new_segments.append((mid, mid + direction * decay_factor))

    # Recursively create more segments with decreased max_offset and generations
    return create_segments(new_segments, generations - 1, max_offset / 2, decay_factor)

# Function to update the animation frame
def update(frame):
    # Clear the current plot
    plt.gca().clear()

    # Set the plot limits
    plt.gca().set_xlim(-100, 100)
    plt.gca().set_ylim(0, 200)

    # Set the number of lightning strikes
    n_strikes = 2

    # Loop through the lightning strikes
    for _ in range(n_strikes):
        # Occasionally create a new strike
        if np.random.rand() < 0.5:
            # Calculate a random initial angle for the bolt
            initial_bolt_angle = np.random.uniform(-np.pi / 12, np.pi / 12)

            # Calculate the initial bolt end point
            initial_bolt_end = np.array([100 * np.sin(initial_bolt_angle), 200 - 100 * np.cos(initial_bolt_angle)], dtype=float)

            # Create the initial segments for the bolt
            segments = [(np.array([0, 200], dtype=float), initial_bolt_end)]

            # Generate the lightning bolt segments
            segments = create_segments(segments, 6, 50, 0.7)

            # Loop through the segments and plot them
            for i, segment in enumerate(segments):
                # Plot main bolt with thicker lines
                if i < 2:
                    plt.plot(*zip(*segment), color='black', linewidth=3.5)  # black outline
                    plt.plot(*zip(*segment), color='blue', linewidth=2.5)  # colored line
                else:  # branches
                    plt.plot(*zip(*segment), color='black', linewidth=1.5)  # black outline
                    plt.plot(*zip(*segment), color='lightblue', linewidth=0.8)  # colored line

    # Add ORCID and SiliconWit to the plot
    plt.gca().text(0.5, 0.5, 'orcid.org/0000-0002-7326-7502', transform=plt.gca().transAxes, fontsize=8, color='gray', alpha=0.5, ha='center', va='center', rotation=0)
    plt.gca().text(0.95, 0.05, 'SiliconWit.com', transform=plt.gca().transAxes, fontsize=10, color='gray', alpha=0.5, ha='right', va='bottom')

    return []

# Create the figure for the animation
fig = plt.figure()

# Create the animation
ani = FuncAnimation(fig, update, frames=range(20), interval=200, blit=True)

# Set up the writer for saving the animation as a GIF
writer = PillowWriter(fps=5)

# Save the animation as a GIF
# ani.save('lightning-strike.gif', writer=writer)

# Show the animation
plt.show()

