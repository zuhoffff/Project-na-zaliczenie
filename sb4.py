import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

class Animal:
    def __init__(self, file_path, color, label):
        self.start_positions, self.num_animals = self.retrieve(file_path)
        self.lines = [plt.plot([], [], color=color, label=f'{label} {i+1}')[0] for i in range(self.num_animals)]

    def retrieve(self, file_path):
        number = 0
        start = []
        with open(file_path, 'r') as file:
            for line in file:
                number += 1
                words = line.strip().split()
                point = [float(words[0]), float(words[1])]
                start.append(point)
        return start, number

    def generate_next_point(self, x, y, max_distance):
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, max_distance)
        new_x = x + distance * np.cos(angle)
        new_y = y + distance * np.sin(angle)
        return new_x, new_y

    def update(self, frame):
        for i in range(self.num_animals):
            new_point = self.generate_next_point(self.positions[i][-1, 0], self.positions[i][-1, 1], 1.0)
            self.positions[i] = np.vstack([self.positions[i], new_point])
            self.lines[i].set_data(self.positions[i][:, 0], self.positions[i][:, 1])
        return tuple(self.lines)

def main():
    num_frames = 100
    mice = Animal('mice.txt', color='blue', label='Mice')
    average_cats = Animal('average_cats.txt', color='red', label='Average Cats')

    fig, ax = plt.subplots()
    animals = [mice, average_cats]

    def init():
        for animal in animals:
            for line in animal.lines:
                line.set_data([], [])
        return tuple(line for animal in animals for line in animal.lines)

    def animate(frame):
        for animal in animals:
            animal.update(frame)
        return tuple(line for animal in animals for line in animal.lines)

    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    for animal in animals:
        ax.add_patch(Circle((animal.start_positions[0][0], animal.start_positions[0][1]), radius=0.1, color=animal.lines[0].get_color(), label=animal.lines[0].get_label()))

    animation = FuncAnimation(fig, animate, frames=num_frames, init_func=init, blit=True, interval=200)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
