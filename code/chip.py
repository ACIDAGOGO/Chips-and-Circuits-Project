import csv
from gate import Gate
import numpy as np
from typing import Any

class Chip:
    def __init__(self, chip_no: int, netlist_name: str):
        self.chip_no = chip_no
        self.netlist_name = netlist_name
        self.grid_x: int
        self.grid_y: int
        self.gates: dict[int, 'Gate'] = {}
        self.load_gates(f"../gates&netlists/chip_{chip_no}/print_{chip_no}.csv")
        self.grid = self.initialize_grid()

    # Set the grid size to the right aspect ratio
    def get_grid_size(self) -> None:
        if self.chip_no == 0:
            self.grid_x = 8
            self.grid_y = 7
        elif self.chip_no == 1:
            self.grid_x = 18
            self.grid_y = 13
        elif self.chip_no == 2:
            self.grid_x = 18
            self.grid_y = 17

    # Create grid in 2d array
    def initialize_grid(self) -> Any:
        self.get_grid_size()
        grid = np.zeros((self.grid_y, self.grid_x))
        for gate in self.gates.values():
            grid[gate.get_y(), gate.get_x()] = gate.get_id()
        
        grid = np.flipud(grid)
        return grid


    # Loads all gates from CSV into memory
    def load_gates(self, filename: str) -> None:
        with open(filename) as file:
            printlist = csv.reader(file)

            # Skip the first line
            next(printlist)
            
            # Iterate over the csv file
            for row in printlist:
                
                # Create gates
                new_gate = Gate(int(row[0]), int(row[1]), int(row[2]))
                self.gates[int(row[0])] = new_gate


if __name__ == "__main__":

    chip = Chip(0, "netlist_1.csv")
    for gate in chip.gates.values():
        print(gate)

    print(chip.grid)