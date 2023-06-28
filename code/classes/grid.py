from .gate import Gate
import numpy as np
from typing import Any


class Grid:
    """
    Class used to create a grid for storing wire and gate locations in 3D space.
    """

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

    def get_grid_size(self) -> tuple[int, int, int]:
        """
        Returns the size of the grid in a tuple.
        """

        return (self.grid_x, self.grid_y, self.grid_z)

    def initialize_grid(self) -> Any:
        """
        Create grid in 3d array.
        """

        # Creates grid with zeros with aspect ratio self.x, self.y
        grid = np.zeros((self.grid_z + 1, self.grid_y + 1, self.grid_x + 1))

        return grid

    def check_for_illegal_gate(self, position: tuple[int, int, int],
                               father: 'Gate') -> bool:
        """
        Checks for a foreign, illegal gate.
        """
        
        if self.values[position[2]][position[1]][position[0]] == father.get_id():
            return False
        elif self.values[position[2]][position[1]][position[0]] > 0:
            return True

        return False
