import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Mice:
    def __init__(self, mice_num, num_frames):
        self.mice_num = mice_num
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()
        self.lines = [self.ax.plot([], [],color='blue', label=f'mouse {i+1}')[0] for i in range(mice_num)]
        #self.line_color = 'blue'
        self.mice_pos = [self.generate_points(np.random.uniform(-5, 5), np.random.uniform(-5, 5)) for _ in range(mice_num)]
        self.init()

    def generate_next_point(self, x, y):
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, 1)
        new_x = x + distance * np.cos(angle)
        new_y = y + distance * np.sin(angle)
        return new_x, new_y

    def generate_points(self, start_x, start_y):
        x_data = np.zeros(self.num_frames)
        y_data = np.zeros(self.num_frames)
        x_data[0] = start_x
        y_data[0] = start_y
        for i in range(1, self.num_frames):
            x_data[i], y_data[i] = self.generate_next_point(x_data[i - 1], y_data[i - 1])
        return x_data, y_data

    def init(self):
        for line in self.lines:
            line.set_data([], [])
        return tuple(self.lines)
        #self.ax.legend()

    def update(self, frame):
        for i in range(self.mice_num):
            self.lines[i].set_data(self.mice_pos[i][0][:frame + 1], self.mice_pos[i][1][:frame + 1])
        return tuple(self.lines)

    def set_axis(self):
        x_min = self.mice_pos[0][0]
        x_max = self.mice_pos[0][0]
        y_min = self.mice_pos[0][1]
        y_max = self.mice_pos[0][1]
        for i in range (self.mice_num):
            if self.mice_pos[i][0] < x_min:
                x_min = self.mice_pos[i][0]
            elif self.mice_pos[i][0] > x_max:
                x_max = self.mice_pos[i][0]
            if self.mice_pos[i][1] < y_min:
                y_min = self.mice_pos[i][1]
            elif self.mice_pos[i][1] > y_max:
                y_max = self.mice_pos[i][1]
        self.ax.set_xlim(x_min - 1, x_max + 1)
        self.ax.set_ylim(y_min - 1, y_max + 1)

    def animate(self):
        animations = [FuncAnimation(self.fig, self.update, frames=self.num_frames, init_func=self.init, blit=True) for _ in range(self.mice_num)]
        self.set_axis()
        plt.legend()
        plt.show()

# Create an instance of the Mice class
mice_simulation = Mice(mice_num=3, num_frames=100)

# Run the animation
mice_simulation.animate()
