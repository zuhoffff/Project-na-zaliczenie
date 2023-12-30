import matplotlib
matplotlib.use('Qt5Agg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation

class Creature:
    def __init__(self, file_path, max_distance):
        self.start_positions = self.retrieve(file_path) #are the separete start_positions actually required?
        self.positions = []
        self.max_distance = max_distance
        self.num = len(self.start_positions)
    def retrieve(self, file_path):
        positions = []
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                position = [float(words[0]), float(words[1])]
                positions.append(position)
        return positions
    def generate_next_point(self, x, y):
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, self.max_distance)
        new_x = x + distance * np.cos(angle)
        new_y = y + distance * np.sin(angle)
        return new_x, new_y

class Mouse(Creature):
    def __init__(self, file_path='mice.txt', max_distance=1):
        super().__init__(file_path, max_distance)


class Cat(Creature):
    def __init__(self, file_path='average_cats.txt', max_distance=10):
        super().__init__(file_path, max_distance)


class Simulation: #can be performed within creature class ?
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.fig, self.ax = plt.subplots()
        self.mice = Mouse()
        self.cats = Cat()

    def set_axis(self):

    def init(self):
        self.mouse_lines = [self.ax.plot([], [], color='blue', label='Mice')[0] for _ in range(self.mice.num)]
        self.cat_lines = [self.ax.plot([], [], color='blue', label='Cats')[0] for _ in range(self.cats.num)]
        return tuple(self.mouse_lines), tuple(self.cat_lines)

    def update(self, frame):
        #just assign compete lists to lines instead?

        for mouse in range(self.mice.num):
            self.mouse_lines[mouse].set_data(
                self.mice.positions[mouse][0][:frame+1],
                self.mice.positions[mouse][1][:frame+1]
            )
        for cat in range():
            self.cat_lines[cat].set_data(
                self.cats.positions[cat][0][:frame + 1],
                self.cats.positions[cat][1][:frame + 1]
            )
        return tuple(self.mouse_lines), tuple(self.cat_lines) #can a pair of tuples be returned and used then?


    def check_interaction(self):
        for frame in range (self.num_frames):
            x_values = []
            y_values = []
            for mouse in self.mice.start_positions:
                next_x, next_y = self.mice.generate_next_point(mouse[0], mouse[1])
                x_values.append(next_x)
                y_values.append(next_y)
            self.mice.positions.append(x_values, y_values)


            x_values = []
            y_values = []
            for cat in self.cats.start_positions:
                next_x, next_y = self.cats.generate_next_point(cat[0], cat[1])
                x_values.append(next_x)
                y_values.append(next_y)
            self.cats.positions.append(x_values, y_values)

    def animate(self):
        self.set_axis()
        self.ax.legend()
        mice_anim = FuncAnimation(self.fig, self.update[0], frames=self.num_frames, init_func=self.init, blit=True, interval=200)# can be replaced with one anim obj
        cats_anim = FuncAnimation(self.fig, self.update[1], frames=self.num_frames, init_func=self.init, blit=True, interval=200)
        plt.legend()
        plt.show()

# Example usage:

def main():
    simulation = Simulation(num_frames=100)
    simulation.animate()

if __name__ == '__main__':
    main()