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
        window, graph = plt.subplots()
        num_points = 5000
        x_increments = np.random.randint(-1, 2, num_points)
        y_increments = np.random.randint(-1, 2, num_points)

        for i in range(num_points):
            # Generate the next point
            x_next = self.mice_pos[0] + x_increments[i]
            y_next = self.mice_pos[1] + y_increments[i]

            # Plot the point
            plt.plot(x_next, y_next, marker='o', linestyle='-', color='blue' if i == 0 else 'green')

            plt.pause(0.05)

            # Update the starting point for the next iteration
            self.mice_pos[0], self.mice_pos[1] = x_next, y_next

        # Use plt methods for labels, title, and legend
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Random Walk')
        plt.legend()

        plt.show()

#main
obj = mice()
obj.retrieve('mice.txt')
obj.mice_plotting()