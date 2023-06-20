import csv
from gate import Gate
from wire import Wire
from typing import Any
from grid import Grid


class Chip:
    def __init__(self, chip_no: int, netlist_name: str):
        self.chip_no = chip_no
        self.netlist_name = netlist_name
        self.grid = Grid(chip_no)
        self.gates: dict[str, 'Gate'] = {}
        self.load_gates(f"./../data/chip_{chip_no}/print_{chip_no}.csv")
        self.load_connections(f"./../data/chip_{chip_no}/{netlist_name}")
        self.fill_grid()
        self.wires: list['Wire'] = []

        # Data for analysis
        self.iteration: int = 0
        self.cost: int = 0
        self.intersectioncount: int = 0
        self.wirecount: int = 0
        

    # Create grid in 2d array
    def fill_grid(self) -> None:
        for gate in self.gates.values():
            self.grid.values[gate.get_z(), gate.get_y(), gate.get_x()] = gate.get_id()


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

    # Adds wire to list of wires on the chip
    def add_wire(self, wire: 'Wire') -> None:
        self.wires.append(wire)

    # Calculates total cost of chip
    def calculate_costs(self) -> int:
        cost = 0

        # Loop through grid
        for layer in self.grid.values:    
            for row in layer:
                for value in row:
                    if value < -1:
                        intersections = abs(value) - 1
                        self.intersectioncount += intersections
                    else:
                        intersections = 0

                    # Add every wire and intersection to the total count
                    if value < 0:
                        self.wirecount += abs(value)
                        cost += (abs(value) + (300 * intersections))

        # Add 1 per wire, because in the grid, a wire on top of a father gate is not represented
        cost += len(self.wires)
        self.wirecount += len(self.wires)

        # Save cost to chip
        self.cost = int(cost)

        return int(cost)