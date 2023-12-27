import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Mice:
    def __init__(self, file_path, num_frames):
        self.mice_num = 0
        self.mice_pos = []
        self.retrieve()
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()
        self.lines = [self.ax.plot([], [], color='blue', label=f'mouse {i+1}')[0] for i in range(self.mice_num)]
        self.mice_pos = [self.generate_points(self.mice_pos[i][0], self.mice_pos[i][1]) for i in range(self.mice_num)]#tuple is immutable!
        #and the mice_pos is list of tuples of arrays (array is mutalbe structure os the fixed size)
        self.init()

    def retrieve(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                self.mice_num += 1
                words = line.strip().split()
                self.mice_pos[0].append(int(words[0].strip()))
                self.mice_pos[1].append(int(words[1].strip()))

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
        x_min = np.min([np.min(self.mice_pos[i][0]) for i in range(self.mice_num)])
        x_max = np.max([np.max(self.mice_pos[i][0]) for i in range(self.mice_num)])
        y_min = np.min([np.min(self.mice_pos[i][1]) for i in range(self.mice_num)])
        y_max = np.max([np.max(self.mice_pos[i][1]) for i in range(self.mice_num)])
        self.ax.set_xlim(x_min - 1, x_max + 1)
        self.ax.set_ylim(y_min - 1, y_max + 1)

    def animate(self):
        animations = [FuncAnimation(self.fig, self.update, frames=self.num_frames, init_func=self.init, blit=True, interval = 200) for _ in range(self.mice_num)]
        self.set_axis()
        plt.legend()
        plt.show()

# Create an instance of the Mice class
mice_simulation = Mice(mice_num=3, num_frames=100)

# Run the animation
mice_simulation.animate()
