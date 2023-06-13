import csv
import sys
sys.path.append("../algorithms")
from gate import Gate
from wire import Wire
from random_alg import run
from typing import Any
from grid import Grid


class Chip:
    def __init__(self, chip_no: int, netlist_name: str):
        self.chip_no = chip_no
        self.netlist_name = netlist_name
        self.grid = Grid(chip_no)
        self.gates: dict[str, 'Gate'] = {}
        self.load_gates(f"../../gates&netlists/chip_{chip_no}/print_{chip_no}.csv")
        self.load_connections(f"../../gates&netlists/chip_{chip_no}/{netlist_name}")
        self.fill_grid()
        self.wires: list['Wire'] = []
        

    # Create grid in 2d array
    def fill_grid(self) -> None:
        for gate in self.gates.values():
            self.grid.values[gate.get_y(), gate.get_x()] = gate.get_id()


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
        for row in self.grid.values:
            for value in row:
                if value < -1:
                    intersections = abs(value) - 1
                else:
                    intersections = 0
                
                cost += 1 * abs(value) + 300 * intersections

        # Add 1 per wire, because in the grid, a wire on top of a father gate is not represented
        cost += len(self.wires)

        return int(cost)



if __name__ == "__main__":

    total_costs = 10000

    while (total_costs > 1000):
        chip = Chip(0, "netlist_1.csv")

        for mother in chip.gates.values():
            for father in mother.get_destinations():
                new_wire = Wire(mother, father)
                chip.add_wire(new_wire)
                # print(f'WIRE ORIGIN: {new_wire.mother.get_id()} DESTINATION: {new_wire.father.get_id()}')
                run(new_wire, chip.grid)

                # Reset wire and its path on the grid and find new path until wire has found father
                while (new_wire.get_current_position() != new_wire.father.get_coords()):

                    # Trace back wire
                    for unit in range(len(new_wire.get_path()) - 1):
                        coords = new_wire.pop_unit()

                        # Reset grid on traced back route
                        chip.grid.values[coords[1]][coords[0]] += 1

                    # Start a new wire
                    run(new_wire, chip.grid)
        
        total_costs = chip.calculate_costs()
        print(f'TOTAL COSTS: ${total_costs}')

    for gate in chip.gates.values():
        print(gate)
        print(f'CONNECTIONS: {gate.get_destinations()}')

    print(chip.grid.values)
    chip.grid.visualize_grid()

    for wire in chip.wires:
        if wire.get_current_position() == wire.father.get_coords():
            print(f'WIRE {wire.mother.get_id()} FOUND FATHER')
        else:
            print(f'WIRE {wire.mother.get_id()} DID NOT FIND FATHER')