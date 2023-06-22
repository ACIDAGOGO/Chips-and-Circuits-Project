import time
import sys
sys.path.append("../analysis")
sys.path.append("../classes")
sys.path.append("..")

import copy
import random
from classes.chip import Chip
from classes.wire import Wire
from .random_alg import lay_wire, random_reassign_wire

from analysis.save import save_to_file


class HillClimber:

    def __init__(self, chip_no: int, netlist_no: int, output_filename: str):
        self.chip = Chip(chip_no, f"netlist_{netlist_no}.csv")
        self.costs: int
        self.output_filename: str = output_filename

    def run(self):
        for mother in self.chip.gates.values():
            for father in mother.get_destinations():
                new_wire = Wire(mother, father)
                self.chip.add_wire(new_wire)
                lay_wire(new_wire, self.chip.grid)
                
                while (new_wire.get_current_position() != new_wire.father.get_coords()):
                    random_reassign_wire(new_wire, self.chip.grid)
        self.costs = self.chip.calculate_costs()

        # Writing original chip data to CSV file
        save_to_file(self.chip, self.output_filename)

        iteration: int = 0

        # Start timer
        start_time: float = time.time()

        while (True):
            try:
                for wire in range(len(self.chip.wires)):
                    for _ in range(1000):
                        chip_copy = copy.deepcopy(self.chip)
                        wire_copy = chip_copy.wires[wire]
                        random_reassign_wire(wire_copy, chip_copy.grid)
                        while (wire_copy.get_current_position() != wire_copy.father.get_coords()):
                            random_reassign_wire(wire_copy, chip_copy.grid)
                        
                        copy_cost = chip_copy.calculate_costs()
                        current_cost = self.chip.calculate_costs()
                        
                        if (copy_cost < current_cost):
                            
                            # Update chip to better version
                            self.chip = chip_copy

                            # Update algorithm iteration number
                            iteration += 1

                            # Update chip iteration number
                            self.chip.iteration = iteration

                            # Get time for completed iteration
                            completed_iteration_time = time.time()

                            # Calculate duration of iteration
                            self.chip.iteration_duration = completed_iteration_time - start_time

                            # Update cumulative iteration duration
                            self.chip.cumulative_duration += self.chip.iteration_duration

                            # Reset timer
                            start_time = time.time()

                            # Save relevant chip data to file
                            save_to_file(self.chip, self.output_filename)                  

            except KeyboardInterrupt:
                break

        return self.chip


        # for wire in self.chip.wires:
        #     for _ in range(10):
        #         chip_copy = copy.deepcopy(self.chip)
        #         random_reassign_wire(wire, self.chip.grid)
        #         while (wire.get_current_position() != wire.father.get_coords()):
        #             random_reassign_wire(wire, self.chip.grid)
                
        #         copy_cost = chip_copy.calculate_costs()
        #         print(f'copy: {copy_cost}')
        #         current_cost = self.chip.calculate_costs()

        #         if (current_cost > copy_cost):
        #             self.chip = chip_copy
                
        #         print(f"current: {current_cost}")

                
                
        
        