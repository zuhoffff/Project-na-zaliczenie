import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

class Simulation:
    def __init__(self, num_frames):
        self.fig, self.ax = plt.subplots()
        self.num_frames = num_frames
        self.lines = []
        self.mice = Mice('mice.txt')
        self.average_cats = Average_cats('av_cats.txt')

    def generate_next_point(x, y):
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, 1)
        new_x = x + distance * np.cos(angle)
        new_y = y + distance * np.sin(angle)
        return new_x, new_y

    def retrieve(file_path): #return 2d list of start points retrieved from file
        number = 0
        start = []
        with open(file_path, 'r') as file:
            for line in file:
                number += 1
                words = line.strip().split()
                point = [float(words[0]), float(words[1])]
                start.append(point)
        return start, number

    def render_and_animate(self):

        #loop to iterate through the frames
        for i in range (self.num_frames):

                #loop iteration through anumals
                for animal in range():



class Mice:
    def __init__(self, file_path):
        self.mice_start = []
        self.mice_num = 0
        self.retrieve(file_path)  # Call retrieve method inside the constructor
        self.draw_circles()
        self.lines = []
        self.mice_pos = []


    def init(self):
        # Initialize lines based on the existing mice_pos
        self.lines = [plt.plot([], [], color='blue', label='Mice')[0] for _ in range(self.mice_num)]
        return tuple(self.lines)

    def update(self, frame):
        for i in range(self.mice_num):
            self.lines[i].set_data(self.mice_pos[i][0][:frame + 1], self.mice_pos[i][1][:frame + 1])
        return tuple(self.lines)

    def set_axis(self):
        x_min = np.min([np.min(mouse[0]) for mouse in self.mice_pos])
        x_max = np.max([np.max(mouse[0]) for mouse in self.mice_pos])
        y_min = np.min([np.min(mouse[1]) for mouse in self.mice_pos])
        y_max = np.max([np.max(mouse[1]) for mouse in self.mice_pos])
        self.ax.set_xlim(x_min - 1, x_max + 1)
        self.ax.set_ylim(y_min - 1, y_max + 1)

    def animate(self):
        self.set_axis()
        # Draw circles before the animation
        for circle in self.circles:
            self.ax.add_patch(circle)
        animations = [FuncAnimation(self.fig, self.update, frames=self.num_frames, init_func=self.init, blit=True, interval=200)]
        plt.legend()
        plt.show()

    def draw_circles(self):
        # Create a single label for all circles
        label = 'Starts'
        # Create circles for each starting point
        self.circles = [Circle((point[0], point[1]), radius=0.1, color='red', label=label) for point in self.mice_start]
        # Set label for all circles
        self.ax.legend([self.circles[0]], [label])

class Average_cats(Mice):

# class Lazy_cats():
#
# class Kittens():

# Example usage:
