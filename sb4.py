import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
from enum import Enum

class PlotManager:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

class Creature:
    def __init__(self, file_path, max_distance, color, label, plot_manager):
        self.positions = []
        self.positions.append(self.retrieve(file_path))
        self.max_distance = max_distance
        self.color = color
        self.label = label
        self.num = len(self.positions[0])
        self.flags = []
        self.lines = []
        self.anim = []
        self.plot_manager = plot_manager

    def retrieve(self, file_path):
        start_pos = []
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                start_position = [float(words[0]), float(words[1])]
                start_pos.append(start_position)
        return start_pos

    def generate_next_point(self, x, y):
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, self.max_distance)
        new_x = x + distance * np.cos(angle)
        new_y = y + distance * np.sin(angle)
        new_point = [new_x, new_y]
        return new_point

    def generate_points(self):
        next_positions = []
        for i in range(self.num):
            y = self.positions[-1][i][1]
            x = self.positions[-1][i][0]
            next_pos = self.generate_next_point(x, y)
            next_positions.append(next_pos)
        self.positions.append(next_positions)

    def init_plot(self):
        self.lines = [self.plot_manager.ax.plot([], [], color=self.color, label=self.label)[0] for _ in range(self.num)]
        return tuple(self.lines)

    def update(self, frame):
        for i in range(self.num):
            arr_pos = np.array(self.positions)
            self.lines[i].set_data(arr_pos[:frame + 1, i, 0], arr_pos[:frame + 1, i, 1])
        return tuple(self.lines)

    def draw_circles(self):
        self.circles = [Circle((mouse[0], mouse[1]), radius=0.4, color='blue', label='Starting Point') for mouse in
                        self.positions[0]]
        return self.circles

    def animate(self, num_frames):
        for circle in self.draw_circles():
            self.plot_manager.ax.add_patch(circle)

        self.anim = FuncAnimation(
            self.plot_manager.fig, self.update, frames=num_frames, init_func=self.init_plot, blit=False, interval=300
        )

class Mouse(Creature):
    def __init__(self, file_path='mice.txt', max_distance=2, color='blue', label='Mice', plot_manager=None):
        super().__init__(file_path, max_distance, color, label, plot_manager)

    def generate_points(self):
        next_positions = []
        for i in range(self.num):
            if i in self.flags:
                next_positions.append(self.positions[0][i])
            else:
                y = self.positions[-1][i][1]
                x = self.positions[-1][i][0]
                next_pos = self.generate_next_point(x, y)
                next_positions.append(next_pos)
        self.positions.append(next_positions)

class Average_cat(Creature):
    def __init__(self, file_path='average_cats.txt', max_distance=2, color='red', label='average cats', plot_manager=None):
        super().__init__(file_path, max_distance, color, label, plot_manager)

class Simulation:
    def __init__(self, num_frames, plot_manager):
        self.num_frames = num_frames
        self.plot_manager = plot_manager
        self.creatures = [Mouse(plot_manager=plot_manager), Average_cat(plot_manager=plot_manager)]
        self.set_axis()

    def render_point(self):
        for i in range(1, self.num_frames):
            for creature in self.creatures:
                creature.generate_points()
                creature.flags.clear()

            for index, mouse in enumerate(self.creatures[0].positions[i]):
                for cat in self.creatures[1].positions[i]:
                    mouse_arr = np.array(mouse)
                    cat_arr = np.array(cat)
                    distance = np.linalg.norm(mouse_arr - cat_arr)
                    if distance <= 10:
                        creature.flags.append(index)

    def animate(self):
        for creature in self.creatures:
            creature.animate(self.num_frames)

        plt.show()

    def set_axis(self):
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        for creature_type in self.creatures:
            for frame in creature_type.positions:
                for creature in frame:
                    min_x = min(min_x, creature[0])
                    max_x = max(max_x, creature[0])
                    min_y = min(min_y, creature[1])
                    max_y = max(max_y, creature[1])

        self.plot_manager.ax.set_xlim(min_x - 5, max_x + 5)
        self.plot_manager.ax.set_ylim(min_y - 5, max_y + 5)

def main():
    plot_manager = PlotManager()
    simulation = Simulation(num_frames=100, plot_manager=plot_manager)
    simulation.render_point()
    simulation.animate()

if __name__ == '__main__':
    main()
