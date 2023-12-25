import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Generate random data for illustration
np.random.seed(42)
x_data = np.random.rand(100)
y_data = np.random.rand(100)

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
    line.set_data(x_data[:frame], y_data[:frame])
    return line,

# Calculate the range of your data for axis limits
x_min, x_max = np.min(x_data), np.max(x_data)
y_min, y_max = np.min(y_data), np.max(y_data)

# Set the axis limits based on the data range
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

# Create the animation
animation = FuncAnimation(fig, update, frames=len(x_data), init_func=init, blit=True)

# Show the animation
plt.show()
