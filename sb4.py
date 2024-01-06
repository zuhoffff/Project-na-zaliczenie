import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

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
        self.lines = [self.plt.plot([], [], color=self.color, label=self.label)[0] for _ in range(self.num)] #ax instead of plt
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

    def animate(self):
        #todo: pass ax and fig to the class OR move their initialization to this class
        #todo: call the animate in the simulation class or in the creature class itself
        for circle in self.circles:
            self.ax.add_patch(circle)
        cat_anim = [FuncAnimation(self.fig, self.cats.update(), frames=self.num_frames, init_func=self.cats.init, blit=False, interval=300)]
        mouse_anim = [FuncAnimation(self.fig, self.mice.update(), frames=self.num_frames, init_func=self.mice.init, blit=False, interval=300)]
        # plt.legend()
        # self.set_axis()
        plt.show()


class Mouse(Creature):
    def __init__(self, file_path='mice.txt', max_distance=2, color = 'blue', label = 'Mice'):
        super().__init__(file_path, max_distance)
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
        super().__init__(file_path, max_distance)

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

class Simulation:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()
        self.mice = Mouse()
        self.cats = Average_cat()
        self.render_point()
        #self.circles = self.draw_circles()
        self.set_axis()

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
                        self.mice.flags.append(index)

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


def main():
    simulation = Simulation(num_frames=100)
    simulation.animate()

if __name__ == '__main__':
    main()
