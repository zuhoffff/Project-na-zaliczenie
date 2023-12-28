import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

class Simulation:
    def __init__(self, num_frames):
        self.fig, self.ax = plt.subplots()
        self.num_frames = num_frames
        self.lines = []
        mice = Mice('mice.txt')
        average_cats = Average_cats('av_cats.txt')

    def generate_next_point(self, x, y):
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, 1)
        new_x = x + distance * np.cos(angle)
        new_y = y + distance * np.sin(angle)
        return new_x, new_y

    def retrieve(self, file_path):
        mice_pos = []
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                point = [float(words[0]), float(words[1])]
                self.mice_start.append(point)
    def animate(self):
        for i in range (self.num_frames):



class Mice:
    def __init__(self, file_path):
        self.mice_start = []
        self.retrieve(file_path)  # Call retrieve method inside the constructor
        self.draw_circles()


    def init(self):
        # Initialize lines based on the existing mice_pos
        self.lines = [self.ax.plot([], [], color='blue', label='Mice')[0] for _ in range(len(self.mice_pos))]
        return tuple(self.lines)

    def update(self, frame):
        for i in range(len(self.mice_pos)):
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
        self.set_axis()
        # Draw circles before the animation
        for circle in self.circles:
            self.ax.add_patch(circle)
        animations = [FuncAnimation(self.fig, self.update, frames=self.num_frames, init_func=self.init, blit=True, interval=200)]
        plt.legend()
        plt.show()

    def draw_circles(self):
        # Create a single label for all circles
        label = 'Starts'
        # Create circles for each starting point
        self.circles = [Circle((point[0], point[1]), radius=0.1, color='red', label=label) for point in self.mice_start]
        # Set label for all circles
        self.ax.legend([self.circles[0]], [label])

class Average_cats(Mice):

class Lazy_cats():

class Kittens():

# Example usage:
mice_simulation = Mice(file_path='mice.txt', num_frames=100)
mice_simulation.animate()
