from gate import Gate
import numpy as np
import matplotlib.pyplot as plt
from typing import Any

class Grid:
    def __init__(self, chip_no: int) -> None:
        self.chip_no = chip_no

        if self.chip_no == 0:
            self.grid_x = 7
            self.grid_y = 6
        elif self.chip_no == 1:
            self.grid_x = 17
            self.grid_y = 12
        elif self.chip_no == 2:
            self.grid_x = 17
            self.grid_y = 16

        self.values = self.initialize_grid()

    # Returns the size of the grid in a tuple
    def get_grid_size(self) -> tuple[int, int]:
       return (self.grid_x, self.grid_y)

    # Create grid in 2d array
    def initialize_grid(self) -> Any:

        # Creates grid with zeros with aspect ratio self.x, self.y
        grid = np.zeros((self.grid_y + 1, self.grid_x + 1))

        #grid = np.flipud(grid)
        return grid

    # Pleur in grid class
    def check_for_illegal_gate(self, position: tuple[int, int], father: 'Gate') -> bool:
        if self.values[position[1]][position[0]] == father.get_id():
            return False
        elif self.values[position[1]][position[0]] > 0:
            return True
        
        return False


    # Visualizes grid in scatterplot
    def visualize_grid(self) -> None:
        fig, ax = plt.subplots()

        # Define colormap
        cmap = plt.cm.gray
        cmap.set_under('red')
        ax.imshow(self.values, cmap=cmap, vmin = 0.01)
        
        ax.set_xticks(range(self.grid_x))
        ax.set_yticks(range(self.grid_y))
        ax.grid(True, color='white', linewidth=0.5)

        plt.show()