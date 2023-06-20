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
            self.grid_z = 7
        elif self.chip_no == 1:
            self.grid_x = 17
            self.grid_y = 12
            self.grid_z = 7
        elif self.chip_no == 2:
            self.grid_x = 17
            self.grid_y = 16
            self.grid_z = 7

        self.values = self.initialize_grid()

    # Returns the size of the grid in a tuple
    def get_grid_size(self) -> tuple[int, int, int]:
       return (self.grid_x, self.grid_y, self.grid_z)

    # Create grid in 2d array
    def initialize_grid(self) -> Any:

        # Creates grid with zeros with aspect ratio self.x, self.y
        grid = np.zeros((self.grid_z + 1, self.grid_y + 1, self.grid_x + 1))

        #grid = np.flipud(grid)
        return grid

    # Pleur in grid class
    def check_for_illegal_gate(self, position: tuple[int, int, int], father: 'Gate') -> bool:
        if self.values[position[2]][position[1]][position[0]] == father.get_id():
            return False
        elif self.values[position[2]][position[1]][position[0]] > 0:
            return True
        
        return False