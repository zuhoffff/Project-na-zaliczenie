import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

class PlotManager:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def set_axis(self, all_positions):
        min_x = min(point[0] for frame_positions in all_positions for point in frame_positions)
        max_x = max(point[0] for frame_positions in all_positions for point in frame_positions)
        min_y = min(point[1] for frame_positions in all_positions for point in frame_positions)
        max_y = max(point[1] for frame_positions in all_positions for point in frame_positions)

        self.ax.set_xlim(min_x - 5, max_x + 5)
        self.ax.set_ylim(min_y - 5, max_y + 5)

class Creature:
    def __init__(self, plot_manager, file_path, max_distance, color, label):
        self.plot_manager = plot_manager
        self.positions = [self.retrieve(file_path)]
        self.max_distance = max_distance
        self.color = color
        self.label = label
        self.num = len(self.positions[0])
        self.lines = []
        self.anim = []

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
        arr_pos = np.array(self.positions)
        for i in range(self.num):
            self.lines[i].set_data(arr_pos[:frame + 1, i, 0], arr_pos[:frame + 1, i, 1])
        return tuple(self.lines)

    def draw_circles(self):

        #todo: color and radius needs to be changed for diff spicies
        self.circles = [Circle((mouse[0], mouse[1]), radius=0.15, color='blue', label='Starting Point') for mouse in
                        self.positions[0]]
        return self.circles

    def animate(self, num_frames):
        for circle in self.draw_circles():
            self.plot_manager.ax.add_patch(circle)

        self.anim = FuncAnimation(
            self.plot_manager.fig, self.update, frames=num_frames, init_func=self.init_plot, blit=False, interval=300
        )

class Mouse(Creature):
    def __init__(self, plot_manager, file_path='mice.txt', max_distance=2, color='blue', label='Mice'):
        super().__init__(plot_manager, file_path, max_distance, color, label)
        self.flags = []

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

class AverageCat(Creature):
    def __init__(self, plot_manager, file_path='average_cats.txt', max_distance=2, color='red', label='average cats'):
        super().__init__(plot_manager, file_path, max_distance, color, label)

    def interact(self, other_creature):
        for index, mouse in enumerate(other_creature.positions[-1]):
            for cat in self.positions[-1]:
                mouse_arr = np.array(mouse)
                cat_arr = np.array(cat)
                distance = np.linalg.norm(mouse_arr - cat_arr)
                if distance <= 10:
                    other_creature.flags.append(index)

class Simulation:
    def __init__(self, plot_manager, num_frames):
        self.plot_manager = plot_manager
        self.mice = Mouse(plot_manager)
        self.cats = AverageCat(plot_manager)
        self.num_frames = num_frames
        self.render_points()

    def render_points(self):
        all_positions = self.mice.positions + self.cats.positions
        for i in range(1, self.num_frames):
            self.mice.generate_points()
            self.cats.generate_points()
            self.mice.flags.clear()
            self.cats.interact(self.mice)

        self.plot_manager.set_axis(all_positions)

    def animate(self):
        self.mice.animate(self.num_frames)
        self.cats.animate(self.num_frames)
        plt.legend()
        plt.show()

def main():
    plot_manager = PlotManager()
    simulation = Simulation(plot_manager, num_frames=100)
    simulation.animate()

if __name__ == '__main__':
    main()
