import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class MiceSimulation:
    def __init__(self, file_path, num_frames):
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()
        self.lines = []
        self.mice_pos = []  # Initialize an empty list for mouse positions
        self.mice_num = 0  # Initialize mice_num
        self.retrieve(file_path)  # Call retrieve method inside the constructor

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
        # Initialize lines based on the existing mice_pos
        self.lines = [self.ax.plot([], [], color='blue', label=f'mouse {i+1}')[0] for i in range(self.mice_num)]
        return tuple(self.lines)

    def update(self, frame):
        for i in range(self.mice_num):
            self.lines[i].set_data(self.mice_pos[i][0][:frame + 1], self.mice_pos[i][1][:frame + 1])
        return tuple(self.lines)

    def set_axis(self):
        x_min = np.min([np.min(mouse[0]) for mouse in self.mice_pos])
        x_max = np.max([np.max(mouse[0]) for mouse in self.mice_pos])
        y_min = np.min([np.min(mouse[1]) for mouse in self.mice_pos])
        y_max = np.max([np.max(mouse[1]) for mouse in self.mice_pos])
        self.ax.set_xlim(x_min - 1, x_max + 1)
        self.ax.set_ylim(y_min - 1, y_max + 1)

    def animate(self):
        animations = [FuncAnimation(self.fig, self.update, frames=self.num_frames, init_func=self.init, blit=True, interval=200)]
        self.set_axis()
        plt.legend()
        plt.show()

    def retrieve(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                start_x, start_y = float(words[0]), float(words[1])
                # Add the initial point for each mouse to mice_pos
                self.mice_pos.append(self.generate_points(start_x, start_y))
        self.mice_num = len(self.mice_pos)

# Example usage:
mice_simulation = MiceSimulation(file_path='mice.txt', num_frames=100)
mice_simulation.animate()
