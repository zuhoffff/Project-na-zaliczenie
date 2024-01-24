import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.animation import FuncAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class PlotManager:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def set_axis(self, all_positions):
        min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')

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
        self.valid_data = bool(self.positions[0])

    def retrieve(self, file_path):
        start_pos = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    words = line.strip().split()
                    start_position = [float(words[0]), float(words[1])]
                    start_pos.append(start_position)
        except (FileNotFoundError, IndexError, ValueError):
            print(f"Error reading {file_path}. Skipping creature type.")
            self.valid_data = False
            return []
        return start_pos

    def generate_next_point(self, x, y, angle=None):
        if angle is None:
            angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, self.max_distance)
        new_x = x + distance * np.cos(angle)
        new_y = y + distance * np.sin(angle)
        return [new_x, new_y]

    def generate_points(self):
        next_positions = [self.generate_next_point(x, y) for x, y in self.positions[-1]]
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
        circles = [Circle((creature[0], creature[1]), radius=self.radius, color=self.color) for creature in self.positions[0]]
        if label:
            circles[0].set_label(label)
        return circles

    def animate(self, num_frames):
        for circle in self.draw_circles(self.label):
            self.plot_manager.ax.add_patch(circle)

        self.anim = FuncAnimation(
            self.plot_manager.fig, self.update, frames=num_frames, init_func=self.init_plot, blit=False, interval=300
        )

class Mouse(Creature):
    def __init__(self, plot_manager, file_path='mice.txt', max_distance=2, color='blue', label='Mice', radius=0.5):
        super().__init__(plot_manager, file_path, max_distance, color, label, radius)
        self.flags = []

    def interact(self, other):
        for index, mouse in enumerate(self.positions[-1]):
            for creature in other.positions[-1]:
                mouse_arr, creature_arr = np.array(mouse), np.array(creature)
                distance = np.linalg.norm(mouse_arr - creature_arr)
                if distance <= 10:
                    self.flags.append(index)

    def generate_points(self):
        next_positions = [self.positions[0][i] if i in self.flags else self.generate_next_point(x, y)
                          for i, (x, y) in enumerate(self.positions[-1])]
        self.positions.append(next_positions)

class AverageCat(Creature):
    def __init__(self, plot_manager, file_path='average_cats.txt', max_distance=10, color='red', label='Average cats',
                 radius=0):
        super().__init__(plot_manager, file_path, max_distance, color, label, radius)

class Kitten(Creature):
    def __init__(self, plot_manager, file_path='kittens.txt', max_distance=5, color='purple', label='Kittens',
                 radius=0.5):
        super().__init__(plot_manager, file_path, max_distance, color, label, radius)
        self.flags = []

    def interact(self, other):
        for index, kitten in enumerate(self.positions[-1]):
            kitten_start_arr = np.array(self.positions[0][index])
            for other_index, creature in enumerate(other.positions[-1]):
                kitten_arr, creature_arr = np.array(kitten), np.array(creature)
                distance = np.linalg.norm(kitten_arr - creature_arr)
                if distance <= 10:
                    dist_to_home = np.linalg.norm(kitten_arr - kitten_start_arr)
                    if dist_to_home > 50:
                        self.flags.append(index)
                    else:
                        other.flags.append(other_index)

    def generate_points(self):
        next_positions = [self.positions[0][i] if i in self.flags else self.generate_next_point(x, y)
                          for i, (x, y) in enumerate(self.positions[-1])]

        start_positions = np.array(self.positions[0])
        current_positions = np.array(self.positions[-1])

        # Check if the distance exceeds the maximum allowed distance
        distances = np.linalg.norm(current_positions - start_positions, axis=1)
        exceed_distance_indices = np.where(distances > 100)[0]

        for i in exceed_distance_indices:
            angle = np.arctan2(current_positions[i, 1] - start_positions[i, 1],
                              current_positions[i, 0] - start_positions[i, 0])
            new_x = start_positions[i, 0] + 100 * np.cos(angle)
            new_y = start_positions[i, 1] + 100 * np.sin(angle)
            next_positions[i] = [new_x, new_y]

        self.positions.append(next_positions)

class LazyCat(Creature):
    def __init__(self, plot_manager, file_path='lazy_cats.txt', max_distance=10, color='green', label='Lazy cats', radius=0):
        super().__init__(plot_manager, file_path, max_distance, color, label, radius)
        self.streak = 0
        self.interaction_probability = 1 / (1 + np.exp(-0.1 * self.streak))

    def interact(self, other):
        for index, mouse in enumerate(other.positions[-1]):
            for lazy_cat in self.positions[-1]:
                lazy_cat, mouse = np.array(lazy_cat), np.array(mouse)
                distance = np.linalg.norm(lazy_cat - mouse)
                if self.interaction_probability and distance <= 10:
                    other.flags.append(index)

class Simulation:
    def __init__(self, plot_manager, num_frames):
        self.plot_manager = plot_manager
        self.creatures = [
            Mouse(plot_manager),  # 0
            AverageCat(plot_manager),  # 1
            Kitten(plot_manager),  # 2
            LazyCat(plot_manager)  # 3
        ]
        self.num_frames = num_frames
        self.render_points()

    def interact(self, creature1, creature2):
        creature1.interact(creature2)

    def render_points(self):
        all_positions = [creature.positions for creature in self.creatures]
        for _ in range(1, self.num_frames):
            for creature in self.creatures:
                if creature.valid_data:
                    creature.generate_points()

            self.creatures[0].flags.clear()
            self.creatures[2].flags.clear()

            # Interactions todo: handle the priority of interactions
            self.interact(self.creatures[0], self.creatures[1])
            self.interact(self.creatures[2], self.creatures[0])
            self.interact(self.creatures[3], self.creatures[0])

        self.plot_manager.set_axis(all_positions)

    def animate(self):
        for creature in self.creatures:
            if creature.valid_data:
                creature.animate(self.num_frames)
        plt.legend()
        plt.show()

class CustomMainWindow(QMainWindow):
    def __init__(self, plot_manager, simulation):
        super(CustomMainWindow, self).__init__()

        self.plot_manager = plot_manager
        self.simulation = simulation

        # Set up the main window
        self.setWindowTitle("Mice & Cats")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Add a layout to the central widget
        layout = QVBoxLayout(central_widget)

        # Embed the matplotlib figure in the Qt window
        canvas = FigureCanvas(self.plot_manager.fig)
        layout.addWidget(canvas)

        # Add a button to start the animation
        self.start_button = QPushButton("Start Animation", self)
        self.start_button.clicked.connect(self.start_animation)
        layout.addWidget(self.start_button)

    def start_animation(self):
        self.simulation.animate()
        self.start_button.hide()

def main():
    plot_manager = PlotManager()
    simulation = Simulation(plot_manager, num_frames=100)

    # Create the Qt application and window
    app = QApplication([])
    window = CustomMainWindow(plot_manager, simulation)

    # Show the window
    window.show()

    # Start the Qt application event loop
    app.exec_()

if __name__ == '__main__':
    main()