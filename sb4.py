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
        self.flags = [] #flags that represent indecies of mice that's close to cat

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
            if i in self.flags:
                next_positions.append(self.positions[0][i])
            else:
                y = self.positions[-1][i][1]
                x = self.positions[-1][i][0]
                next_pos = self.generate_next_point(x, y)
                next_positions.append(next_pos)
        self.positions.append(next_positions)

class Mouse(Creature):
    def __init__(self, file_path='mice.txt', max_distance=2):
        super().__init__(file_path, max_distance)

#TODO: create classes for all types of cats
class Cat(Creature):
    def __init__(self, file_path='average_cats.txt', max_distance=2):
        super().__init__(file_path, max_distance)

class Simulation:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()
        self.mice = Mouse()
        self.cats = Cat()
        self.render_point()
        self.mice_lines = []
        self.cats_lines = []
        self.circles = self.draw_circles()

    def render_point(self):
        #iterate through frames
        for i in range(1, self.num_frames):

            self.mice.generate_points()
            self.cats.generate_points()
            self.mice.flags.clear()

            # Check for proximity and reset positions of mice if necessary
            # distance = np.linalg.norm(mouse - cat) #calculating the normal
            for index, mouse in enumerate(self.mice.positions[i]):
                #index represents the current mouse
                for cat in self.cats.positions[i]:
                    mouse_arr = np.array(mouse)
                    cat_arr = np.array(cat)
                    distance = np.linalg.norm(mouse_arr - cat_arr)
                    if distance <= 10:

                        # TODO: Set next point to start or even sever the chain to a new one (DONE: teleportation line is invisible)
                        self.mice.flags.append(index)

    def init_mice(self): #it d be better to init different creatures separately, also labels need to be repaired
        self.mice_lines = [self.ax.plot([], [], color='blue', label='Mice')[0] for _ in range(self.mice.num)]
        return tuple(self.mice_lines)

    def init_cats(self): #it d be better to init different creatures separately, also labels need to be repaired
        self.cats_lines = [self.ax.plot([], [], color='red', label='Cats')[0] for _ in range(self.cats.num)]
        return tuple(self.cats_lines)

    def update_mice(self, frame):
        for i in range(self.mice.num):
            positions = np.array(self.mice.positions)
            self.mice_lines[i].set_data(positions[:frame+1, i, 0], positions[:frame+1, i, 1])
        return tuple(self.mice_lines)

    def update_cats(self, frame):
        for i in range(self.cats.num):
            positions = np.array(self.cats.positions)
            self.cats_lines[i].set_data(positions[:frame+1, i, 0], positions[:frame+1, i, 1])
        return tuple(self.cats_lines)

    def animate(self):
        for circle in self.circles:
            self.ax.add_patch(circle)
        cat_anim = [FuncAnimation(self.fig, self.update_mice, frames=self.num_frames, init_func=self.init_mice, blit=False, interval=300)]
        mouse_anim = [FuncAnimation(self.fig, self.update_cats, frames=self.num_frames, init_func=self.init_cats, blit=False, interval=300)]
        # plt.legend()
        self.set_axis()
        plt.show()

    def set_axis(self):
        # Extract all positions of mice and cats
        all_positions = self.mice.positions + self.cats.positions

        # Find the minimum and maximum values in x and y directions
        min_x = min(point[0] for frame_positions in all_positions for point in frame_positions)
        max_x = max(point[0] for frame_positions in all_positions for point in frame_positions)
        min_y = min(point[1] for frame_positions in all_positions for point in frame_positions)
        max_y = max(point[1] for frame_positions in all_positions for point in frame_positions)

        # Set the axis limits based on the min and max values
        self.ax.set_xlim(min_x - 5, max_x + 5)
        self.ax.set_ylim(min_y - 5, max_y + 5)

    def draw_circles(self):
        # Create circles for each starting point
        circles = [Circle((mouse[0], mouse[1]), radius=0.4, color='blue', label='Starting Point') for mouse in self.mice.positions[0]]
        return circles

def main():
    simulation = Simulation(num_frames=100)
    simulation.animate()

if __name__ == '__main__':
    main()
