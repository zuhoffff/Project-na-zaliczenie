import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

class Creature:
    def __init__(self, file_path, max_distance):
        self.positions = []
        self.positions.append(self.retrieve(file_path))
        self.max_distance = max_distance
        self.num = len(self.positions[0])

    def retrieve(file_path):
        start_positions = []
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                start_position = [float(words[0]), float(words[1])]
                start_positions.append(start_position)
        return start_positions

    def generate_next_point(self, x, y):
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, self.max_distance)
        new_x = x + distance * np.cos(angle)
        new_y = y + distance * np.sin(angle)
        return new_x, new_y

    def generate_points(self):
        next_positions = []
        for i in range(1, self.num):
            next_position = self.generate_next_point(self.positions[-1][i]) #self.positions[-1][i][0], self.poitions[-1][i][1]
            next_positions.append(next_position)
        self.positions.append(next_positions)

class Mouse(Creature):
    def __init__(self, file_path='mice.txt', max_distance=1):
        super().__init__(file_path, max_distance)

class Cat(Creature):
    def __init__(self, file_path='average_cats.txt', max_distance=10):
        super().__init__(file_path, max_distance)

class Simulation:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()
        self.mice = Mouse()
        self.cats = Cat()

    def render_point(self):
        #iterate through frames
        for i in range(self.num_frames):
            self.mice.generate_points()
            self.cats.generate_points()



def main():
    simulation = Simulation(num_frames=100)
    simulation.animate()

if __name__ == '__main__':
    main()