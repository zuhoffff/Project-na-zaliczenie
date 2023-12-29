import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

class AnimalSimulation:
    def __init__(self, file_path, num_frames, color, label, max_distance=1.0):
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()
        self.lines = []
        self.positions = self.retrieve(file_path)
        self.circles = self.draw_circles(color)
        self.max_distance = max_distance  # Include max_distance in the __init__ method

    def generate_next_point(self, x, y):
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, self.max_distance)
        new_x = x + distance * np.cos(angle)
        new_y = y + distance * np.sin(angle)
        return new_x, new_y

    def generate_points(self, start_x, start_y):
        x_data = [start_x]
        y_data = [start_y]
        for _ in range(1, self.num_frames):
            x, y = self.generate_next_point(x_data[-1], y_data[-1])
            x_data.append(x)
            y_data.append(y)
        return x_data, y_data

    def init(self):
        self.lines = [self.ax.plot([], [], color='blue', label=self.label)[0] for _ in range(len(self.positions))]
        return tuple(self.lines)

    def update(self, frame):
        for i in range(len(self.positions)):
            new_point = self.generate_next_point(self.positions[i][0][-1], self.positions[i][1][-1])
            self.positions[i][0].append(new_point[0])
            self.positions[i][1].append(new_point[1])
            self.lines[i].set_data(self.positions[i][0][:frame + 1], self.positions[i][1][:frame + 1])
        return tuple(self.lines)

    def set_axis(self):
        x_min = np.min([np.min(animal[0]) for animal in self.positions])
        x_max = np.max([np.max(animal[0]) for animal in self.positions])
        y_min = np.min([np.min(animal[1]) for animal in self.positions])
        y_max = np.max([np.max(animal[1]) for animal in self.positions])
        self.ax.set_xlim(x_min - 1, x_max + 1)
        self.ax.set_ylim(y_min - 1, y_max + 1)

    def animate(self):
        self.set_axis()
        for circle in self.circles:
            self.ax.add_patch(circle)
        animations = [
            FuncAnimation(self.fig, self.update, frames=self.num_frames, init_func=self.init, blit=True, interval=200)]
        plt.legend()
        plt.show()

    def retrieve(self, file_path):
        animal_positions = []
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                start_x, start_y = float(words[0]), float(words[1])
                animal_positions.append(self.generate_points(start_x, start_y))
        return animal_positions

    def draw_circles(self, color):
        label = 'Starts'
        circles = [Circle((animal[0][0], animal[1][0]), radius=0.1, color='red', label=label) for animal in
                   self.positions]
        self.ax.legend([circles[0]], [label])
        return circles

# Example usage for Mice
mice_simulation = AnimalSimulation(file_path='mice.txt', num_frames=100, color='blue', label='Mice')
mice_simulation.animate()

# Example usage for Cats
cats_simulation = AnimalSimulation(file_path='cats.txt', num_frames=100, color='orange', label='Cats', max_distance=10.0)
cats_simulation.animate()
