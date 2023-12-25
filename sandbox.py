import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Function to generate new points within a distance of 1 from the previous point
def generate_next_point(x, y):
    angle = np.random.uniform(0, 2 * np.pi)
    distance = np.random.uniform(0, 1)
    new_x = x + distance * np.cos(angle)
    new_y = y + distance * np.sin(angle)
    return new_x, new_y

# Number of frames (points)
num_frames = 100
x_data = np.zeros(num_frames)
y_data = np.zeros(num_frames)

# Generate points
for i in range(1, num_frames):
    x_data[i], y_data[i] = generate_next_point(x_data[i-1], y_data[i-1])

# Set up the figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [], label='Your Data')
ax.legend()

# Function to initialize the plot
def init():
    line.set_data([], [])
    return line,

# Function to update the plot in each animation frame
def update(frame):
    line.set_data(x_data[:frame + 1], y_data[:frame + 1])
    return line,

# Calculate the range of your data for axis limits
x_min, x_max = np.min(x_data), np.max(x_data)
y_min, y_max = np.min(y_data), np.max(y_data)

# Set the axis limits based on the data range
ax.set_xlim(x_min - 1, x_max + 1)
ax.set_ylim(y_min - 1, y_max + 1)

# Create the animation
animation = FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True)

# Show the animation
plt.show()
