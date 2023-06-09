import csv
from gate import Gate
from wire import Wire
from random import run
import numpy as np
import matplotlib.pyplot as plt
from typing import Any

class Chip:
    def __init__(self, chip_no: int, netlist_name: str):
        self.chip_no = chip_no
        self.netlist_name = netlist_name
        self.grid_x: int
        self.grid_y: int
        self.gates: dict[str, 'Gate'] = {}
        self.load_gates(f"../gates&netlists/chip_{chip_no}/print_{chip_no}.csv")
        self.load_connections(f"../gates&netlists/chip_{chip_no}/{netlist_name}")
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
    
    def get_grid_upperbounds(self) -> tuple[int, int]:
        return (self.grid_x, self.grid_y)


    # Create grid in 2d array
    def initialize_grid(self) -> Any:
        self.get_grid_size()
        grid = np.zeros((self.grid_y, self.grid_x))
        for gate in self.gates.values():
            grid[gate.get_y(), gate.get_x()] = gate.get_id()
        
        #grid = np.flipud(grid)
        return grid
    


    def visualize_grid(self) -> None:
        fig, ax = plt.subplots()

        # Define colormap
        cmap = plt.cm.gray
        cmap.set_under('red')
        ax.imshow(self.grid, cmap=cmap, vmin = 0.01)
        
        ax.set_xticks(range(self.grid_x))
        ax.set_yticks(range(self.grid_y))
        ax.grid(True, color='white', linewidth=0.5)

        plt.show()

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
                self.gates[row[0]] = new_gate

    # Loads all gates from CSV into memory
    def load_connections(self, filename: str) -> None:
         with open(filename) as file:
            netlist = csv.reader(file)

            # Skip the first line
            next(netlist)
            
            # Iterate over the csv file
            for row in netlist:
                
                # Set origin and destination gates
                origin_gate = self.gates[row[0]]
                destination_gate = self.gates[row[1]]

                # Add destination gate to origin gate's destination list
                origin_gate.add_destinations(destination_gate)

    # Pleur in grid class
    def check_for_illegal_gate(self, position: tuple[int, int], father: 'Gate') -> bool:
        if self.grid[position[1]][position[0]] == father.get_id():
            return False
        elif self.grid[position[1]][position[0]] > 0:
            return True
        
        return False


if __name__ == "__main__":

    chip = Chip(0, "netlist_1.csv")
    for mother in chip.gates.values():
        for father in gate.get_destinations():
            new_wire = Wire(mother, father)
            run(new_wire, chip)
            

        print(gate)
        print(f'CONNECTIONS: {gate.get_destinations()}')


    print(chip.grid)
    chip.visualize_grid()