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
        self.flags = []  # flags that represent indices of mice that are close to a cat

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

    def init_creature(self, ax):
        raise NotImplementedError("init_creature method must be implemented in each creature class")

    def update_creature(self, frame):
        raise NotImplementedError("update_creature method must be implemented in each creature class")


class Mouse(Creature):
    def __init__(self, file_path='mice.txt', max_distance=2):
        super().__init__(file_path, max_distance)

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

    def init_creature(self, ax):
        lines = [ax.plot([], [], color='blue')[0] for _ in range(self.num)]
        return tuple(lines)

    def update_creature(self, frame):
        for i in range(self.num):
            positions = np.array(self.positions)
            self.lines[i].set_data(positions[:frame + 1, i, 0], positions[:frame + 1, i, 1])
        return tuple(self.lines)


class AverageCat(Creature):
    def __init__(self, file_path='average_cats.txt', max_distance=2):
        super().__init__(file_path, max_distance)

    def init_creature(self, ax):
        lines = [ax.plot([], [], color='red')[0] for _ in range(self.num)]
        return tuple(lines)

    def update_creature(self, frame):
        for i in range(self.num):
            positions = np.array(self.positions)
            self.lines[i].set_data(positions[:frame + 1, i, 0], positions[:frame + 1, i, 1])
        return tuple(self.lines)


class Kitten(Creature):
    def __init__(self, file_path='kittens.txt', max_distance=5):
        super().__init__(file_path, max_distance)

    def generate_points(self):
        next_positions = []
        for i in range(self.num):
            start_x, start_y = self.positions[0][i]
            new_x, new_y = self.generate_next_point(start_x, start_y)

            # Check if the distance exceeds the maximum allowed distance
            distance = np.linalg.norm(np.array([new_x, new_y]) - np.array([start_x, start_y]))

            # Adjust the new point if needed
            if distance > 100:
                angle = np.arctan2(new_y - start_y, new_x - start_x)
                new_x = start_x + 100 * np.cos(angle)
                new_y = start_y + 100 * np.sin(angle)

            next_positions.append([new_x, new_y])

        self.positions.append(next_positions)

    def init_creature(self, ax):
        lines = [ax.plot([], [], color='green')[0] for _ in range(self.num)]
        return tuple(lines)

    def update_creature(self, frame):
        for i in range(self.num):
            positions = np.array(self.positions)
            self.lines[i].set_data(positions[:frame + 1, i, 0], positions[:frame + 1, i, 1])
        return tuple(self.lines)


class Simulation:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()
        self.creatures = [Mouse(), AverageCat(), Kitten()]
        self.render_point()
        self.lines = []
        self.circles = self.draw_circles()

    def render_point(self):
        # iterate through frames
        for i in range(1, self.num_frames):
            for creature in self.creatures:
                creature.generate_points()
                creature.flags.clear()

                # Check for proximity and reset positions of mice if necessary
                for index, mouse in enumerate(creature.positions[i]):
                    for cat in self.creatures[1].positions[i]:  # Assuming the second creature is a cat
                        mouse_arr = np.array(mouse)
                        cat_arr = np.array(cat)
                        distance = np.linalg.norm(mouse_arr - cat_arr)
                        if distance <= 10:
                            creature.flags.append(index)

    def init_creatures(self):
        self.lines = []
        for creature in self.creatures:
            self.lines.extend(creature.init_creature(self.ax))
        return tuple(self.lines)

    def update_creatures(self, frame):
        all_lines = []
        for creature in self.creatures:
            all_lines.extend(creature.update_creature(frame))
        return tuple(all_lines)

    def animate(self):
        for circle in self.circles:
            self.ax.add_patch(circle)
        anim = FuncAnimation(self.fig, self.update_creatures, frames=self.num_frames,
                             init_func=self.init_creatures, blit=False, interval=300)
        self.set_axis()
        plt.show()

    def set_axis(self):
        all_positions = [creature.positions for creature in self.creatures]
        min_x = min(point[0] for frame_positions in all_positions for point in frame_positions)
        max_x = max(point[0] for frame_positions in all_positions for point in frame_positions)
        min_y = min(point[1] for frame_positions in all_positions for point in frame_positions)
        max_y = max(point[1] for frame_positions in all_positions for point in frame_positions)

        self.ax.set_xlim(min_x - 5, max_x + 5)
        self.ax.set_ylim(min_y - 5, max_y + 5)

    def draw_circles(self):
        circles = [Circle((mouse[0], mouse[1]), radius=0.4, color='blue', label='Starting Point') for mouse in
                   self.creatures[0].positions[0]]
        return circles


def main():
    simulation = Simulation(num_frames=100)
    simulation.animate()


if __name__ == '__main__':
    main()