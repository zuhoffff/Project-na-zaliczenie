import random

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class mice:
    def __init__(self):
        self.mice_pos = []  # starting coordinates of each
        self.window, self.graph = plt.subplots()
    def retrieve(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                words = line.strip().split()
                self.mice_pos.append(int(words[0].strip()))
                self.mice_pos.append(int(words[1].strip()))

    #def mice_animation(self):
    def mice_plotting(self):
        x = [self.mice_pos[0]]
        y = [self.mice_pos[1]]

        figure, ax = plt.subplots()

        ax.set_xlim(0,40)
        ax.set_ylim(0,40)

        line, = ax.plot(0,0)#mb change arguments

        def animation_function(i):#plot get out of the limited space
            next_x = x[-1] + random.uniform(-1., 1.)
            next_y = y[-1] + random.uniform(-1., 1.)
            x.append(next_x)
            y.append(next_y)

            line.set_xdata(x)
            line.set_ydata(y)
            return line,

        animation = FuncAnimation(figure,
                                  func=animation_function,
                                  frames=np.arange(0, 10, 0.1),
                                  interval=50)

        plt.show()
#main
obj = mice()
obj.retrieve('mice.txt')
obj.mice_plotting()