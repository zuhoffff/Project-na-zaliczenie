import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
        #x =[self.mice_pos[0]]
        #y = [self.mice_pos[1]]
        number=100
        for i in range(number):
            self.mice_pos.append()

#main
obj = mice()
obj.retrieve('mice.txt')
obj.mice_plotting()