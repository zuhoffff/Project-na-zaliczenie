import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
from enum import Enum

class Creature:
    def __init__(self, file_path, max_distance, color, label):
        self.positions = []
        self.positions.append(self.retrieve(file_path))
        self.max_distance = max_distance
        self.color = color
        self.label = label
        self.num = len(self.positions[0])
        self.flags = [] #flags that represent indecies of mice that's close to cat
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
        #todo: maybe ax should be used instead of plt, in this case it needs to be passed to this method or class
        self.lines = [self.ax.plot([], [], color=self.color, label=self.label)[0] for _ in range(self.num)] #ax instead of plt
        return tuple(self.lines)

    def update(self, frame):
        for i in range(self.num):
            arr_pos = np.array(self.positions)
            self.lines[i].set_data(arr_pos[:frame + 1, i, 0], arr_pos[:frame + 1, i, 1])
        return tuple(self.lines)

    def draw_circles(self):
        #todo: rewrite method for new class, call method in subclass  (?)
        self.circles = []
        #Create circles for each starting point
        circles = [Circle((mouse[0], mouse[1]), radius=0.4, color='blue', label='Starting Point') for mouse in
                   self.positions[0]]
        return circles

    def animate(self, ax, fig, num_frames):
        for circle in self.draw_circles():
            ax.add_patch(circle)

        self.anim = FuncAnimation(
            fig, self.update, frames=num_frames, init_func=self.init_plot, blit=False, interval=300
        )


class Mouse(Creature):
    def __init__(self, file_path='mice.txt', max_distance=2, color = 'blue', label = 'Mice'):
        super().__init__(file_path, max_distance, color,label)
    def generate_points(self):
        next_positions = []
        for i in range(self.num):
            #TODO: move flags feature to the Mouse class (DONE)
            if i in self.flags:
                next_positions.append(self.positions[0][i])
            else:
                y = self.positions[-1][i][1]
                x = self.positions[-1][i][0]
                next_pos = self.generate_next_point(x, y)
                next_positions.append(next_pos)
        self.positions.append(next_positions)

#TODO: create classes for all types of cats
class Average_cat(Creature):
    def __init__(self, file_path='average_cats.txt', max_distance=2, color='red',label='average cats'):
        super().__init__(file_path, max_distance, color, label)

# TODO: override method for some creatures if needed
class Kitten(Creature):
    def __init__(self,file_path='kittens.txt', max_distance=5):
        super().__init__(file_path, max_distance)

    #TODO: next point isn't 100p further from startpos
    def generate_points(self):
        next_positions = []
        for i in range(self.num):
            y = self.positions[-1][i][1]
            x = self.positions[-1][i][0]
            next_pos = self.generate_next_point(x, y)
            next_positions.append(next_pos)
        self.positions.append(next_positions)
#
# class Lazy_cats(Creature):
#     def __init__(self,file_path='lazy_cat.txt', max_distance=10):
#         super().__init__(file_path, max_distance)

class CreatureType(Enum):
    MICE = 0
    CATS = 1

class Simulation:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()

        # creatures -> creature_type -> frame -> creature -> x or y
        self.creatures = {CreatureType.MICE: Mouse(), CreatureType.CATS: Average_cat()}
        self.set_axis()

    def render_point(self):
        for i in range(1, self.num_frames):
            for creature_type, creature in self.creatures.items():
                creature.generate_points()
                creature.flags.clear()

                # Check for proximity and reset positions if necessary
                for idx, mouse in enumerate(self.creatures[CreatureType.MICE].positions[i]):
                    for cat in self.creatures[CreatureType.CATS].positions[i]:
                        mouse_arr = np.array(mouse)
                        cat_arr = np.array(cat)
                        distance = np.linalg.norm(mouse_arr - cat_arr)
                        if distance <= 10:
                            creature.flags.append(idx)

    def animate(self):
        for creature_type, creature in self.creatures.items():
            creature.animate(self.ax, self.fig, self.num_frames, creature_type)

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

        self.ax.set_xlim(min_x - 5, max_x + 5)
        self.ax.set_ylim(min_y - 5, max_y + 5)

def main():
    simulation = Simulation(num_frames=100)
    simulation.render_point()
    simulation.animate()

if __name__ == '__main__':
    main()