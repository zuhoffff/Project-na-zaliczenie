import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

#todo: craches if there is no creatures of any type
class PlotManager:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def set_axis(self, all_positions):
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        for creature_type in all_positions:
            for frame in creature_type:
                for creature in frame:
                    min_x = min(min_x, creature[0])
                    max_x = max(max_x, creature[0])
                    min_y = min(min_y, creature[1])
                    max_y = max(max_y, creature[1])

        self.ax.set_xlim(min_x - 5, max_x + 5)
        self.ax.set_ylim(min_y - 5, max_y + 5)

class Creature:
    def __init__(self, plot_manager, file_path, max_distance, color, label, radius):
        self.plot_manager = plot_manager
        self.positions = [self.retrieve(file_path)]
        self.max_distance = max_distance
        self.color = color
        self.label = label
        self.num = len(self.positions[0])
        self.lines = []
        self.anim = []
        self.radius = radius

    def retrieve(self, file_path):
        start_pos = []
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                start_position = [float(words[0]), float(words[1])]
                start_pos.append(start_position)
        return start_pos

    def generate_next_point(self, x, y, angle=None):
        if angle is None:
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

    def draw_circles(self, label=None):
        self.circles = [Circle((creature[0], creature[1]), radius=self.radius, color=self.color) for creature in
                        self.positions[0]]
        if label:
            self.circles[0].set_label(label)

        return self.circles

    def animate(self, num_frames):
        for circle in self.draw_circles(self.label):
            self.plot_manager.ax.add_patch(circle)

        self.anim = FuncAnimation(
            self.plot_manager.fig, self.update, frames=num_frames, init_func=self.init_plot, blit=False, interval=300
        )

class Mouse(Creature):
    def __init__(self, plot_manager, file_path='mice.txt', max_distance=2, color='blue', label='Mice', radius=0.15):
        super().__init__(plot_manager, file_path, max_distance, color, label, radius)
        self.flags = []

    def interact(self, other):
        for index, mouse in enumerate(self.positions[-1]):
            for creature in other.positions[-1]:
                mouse_arr = np.array(mouse)
                creature_arr = np.array(creature)
                distance = np.linalg.norm(mouse_arr - creature_arr)
                if distance <= 10:
                    self.flags.append(index)

        return None

    def generate_points(self):
        next_positions = []
        for i in range(self.num):
            if i in self.flags:
                next_positions.append(self.positions[0][i])
            else:
                x = self.positions[-1][i][0]
                y = self.positions[-1][i][1]
                next_pos = self.generate_next_point(x, y)
                next_positions.append(next_pos)
        self.positions.append(next_positions)

class AverageCat(Creature):
    def __init__(self, plot_manager, file_path='average_cats.txt', max_distance=10, color='red', label='average cats',
                 radius=0):
        super().__init__(plot_manager, file_path, max_distance, color, label, radius)

class Kitten(Creature):
    def __init__(self, plot_manager, file_path='kittens.txt', max_distance=5, color='purple', label='kittens',
                 radius=0.15):
        super().__init__(plot_manager, file_path, max_distance, color, label, radius)
        self.flags = []

    def interact(self, other):
        for index, kitten in enumerate(self.positions[-1]):
            kitten_start_arr = np.array(self.positions[0][index])
            for other_index, creature in enumerate(other.positions[-1]):
                kitten_arr = np.array(kitten)
                creature_arr = np.array(creature)
                distance = np.linalg.norm(kitten_arr - creature_arr)
                #check the proximity of kitten and mouse
                if distance <= 10:
                    dist_to_home = np.linalg.norm(kitten_arr - kitten_start_arr)
                    if dist_to_home > 50:
                        self.flags.append(index)
                    else:
                        other.flags.append(other_index)


        return None

    def generate_points(self):
        next_positions = []
        for i in range(self.num):
            if i in self.flags:
                next_positions.append(self.positions[0][i])
            start_x, start_y = self.positions[0][i]
            x = self.positions[-1][i][0]
            y = self.positions[-1][i][1]
            new_x, new_y = self.generate_next_point(x, y)

            # Check if the distance exceeds the maximum allowed distance
            distance = np.linalg.norm(np.array([new_x, new_y]) - np.array([start_x, start_y]))

            # Adjust the new point if needed
            if distance > 100:
                angle = np.arctan2(new_y - start_y, new_x - start_x)
                new_x = start_x + 100 * np.cos(angle)
                new_y = start_y + 100 * np.sin(angle)

            next_positions.append([new_x, new_y])

        self.positions.append(next_positions)

class Simulation:
    def __init__(self, plot_manager, num_frames):
        self.plot_manager = plot_manager
        self.mice = Mouse(plot_manager)
        self.cats = AverageCat(plot_manager)
        self.kittens = Kitten(plot_manager)
        self.num_frames = num_frames
        self.render_points()

    def interact(self, creature1, creature2):
        interaction_index = creature1.interact(creature2)

    def render_points(self):
        all_positions = [self.mice.positions, self.cats.positions, self.kittens.positions]
        for i in range(1, self.num_frames):
            self.mice.generate_points()
            self.cats.generate_points()
            self.kittens.generate_points()
            self.mice.flags.clear()

            # Interactions  todo: handle the priority of interactions
            self.interact(self.mice, self.cats)
            self.interact(self.kittens, self.mice) ##works correctly only in such order!

        self.plot_manager.set_axis(all_positions)

    def animate(self):
        self.mice.animate(self.num_frames)
        self.cats.animate(self.num_frames)
        self.kittens.animate(self.num_frames)
        plt.legend()
        plt.show()

def main():
    plot_manager = PlotManager()
    simulation = Simulation(plot_manager, num_frames=100)
    simulation.animate()

if __name__ == '__main__':
    main()
