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

# Generate points
def generate_points(num_frames):
    x_data = np.zeros(num_frames)
    y_data = np.zeros(num_frames)
    for i in range(1, num_frames):
        x_data[i], y_data[i] = generate_next_point(x_data[i - 1], y_data[i - 1])
    return x_data, y_data

#initial values
mice_num = 3
num_frames = 100

# Set up the figure and axis
fig, ax = plt.subplots()
ax.legend()

# Function to initialize the plot
def init():
    for line in lines:
        line.set_data([], [])
    return tuple(lines)

# Function to update the plot in each animation frame
def update(frame):
    lines[frame].set_data(mice_pos[frame][:frame + 1], mice_pos[frame+1][:frame + 1])
    return lines[frame],

#initialize arrays
mice_pos = []
lines = []
animations = []

#main programm
for i in range (mice_num):
        mice_pos.append(generate_points(num_frames))
        lines.append(ax.plot([], [], label=f'mouse {i+1}')[0])
        #init(i)

        # rewrite this part so that global maximum,minimum is determined for all the subplots
        # x_min, x_max = np.min(mice_pos[-2]), np.max(mice_pos[-1])
        # y_min, y_max = np.min(mice_pos[-2]), np.max(mice_pos[-1])ax.set_xlim(x_min, x_max)
        # ax.set_ylim(y_min, y_max)
        # ax.set_xlim(x_min - 1, x_max + 1)
        # ax.set_ylim(y_min - 1, y_max + 1)

        animations.append(FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=True))

# Show the animation
plt.show()
