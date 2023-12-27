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

# Generate points with random starting coordinates
def generate_points(num_frames, start_x, start_y):
    x_data = np.zeros(num_frames)
    y_data = np.zeros(num_frames)
    x_data[0] = start_x
    y_data[0] = start_y
    for i in range(1, num_frames):
        x_data[i], y_data[i] = generate_next_point(x_data[i - 1], y_data[i - 1])
    return x_data, y_data

# Number of mice
mice_num = 2
num_frames = 100

# Set up the figure and axis
fig, ax = plt.subplots()

# Initialize arrays with random starting coordinates
mice_pos = [generate_points(num_frames, np.random.uniform(-5, 5), np.random.uniform(-5, 5)) for _ in range(mice_num)]
lines = [ax.plot([], [],color = 'blue', label=f'mouse {i+1}')[0] for i in range(mice_num)]

# Function to initialize the plot
def init():
    for line in lines:
        line.set_data([], [])
    return tuple(lines)

# Function to update the plot in each animation frame
def update(frame):
    for i in range(mice_num):
        lines[i].set_data(mice_pos[i][0][:frame + 1], mice_pos[i][1][:frame + 1])
    return tuple(lines)

# Set appropriate axis limits based on the generated data
x_min = np.min([np.min(mice_pos[i][0]) for i in range(mice_num)])
x_max = np.max([np.max(mice_pos[i][0]) for i in range(mice_num)])
y_min = np.min([np.min(mice_pos[i][1]) for i in range(mice_num)])
y_max = np.max([np.max(mice_pos[i][1]) for i in range(mice_num)])

ax.set_xlim(x_min - 1, x_max + 1)
ax.set_ylim(y_min - 1, y_max + 1)

# Create animations
animations = [FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True) for _ in range(mice_num)]

# Show the animation
plt.legend()
plt.show()
