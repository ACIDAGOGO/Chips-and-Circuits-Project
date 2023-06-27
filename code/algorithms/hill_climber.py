import time
import sys
sys.path.append("../analysis")
sys.path.append("../classes")
sys.path.append("..")

import copy
from classes.chip import Chip
from classes.wire import Wire
from .random_alg import lay_wire, random_reassign_wire

from analysis.save import save_to_file


class HillClimber:

    def __init__(self, chip_no: int, netlist_no: int, output_filename: str):
        self.chip = Chip(chip_no, f"netlist_{netlist_no}.csv")
        self.costs: int
        self.output_filename: str = output_filename

    def make_random_valid_solution(self) -> 'Chip':
        """
        Create one randomly solved chip for hill_climber to improve upon.
        """
        # Create the wires
        for mother in self.chip.gates.values():
            for father in mother.get_destinations():
                new_wire = Wire(mother, father)
                self.chip.add_wire(new_wire)
                lay_wire(new_wire, self.chip.grid)
                # Randomly lay wires until father gate is found
                while (new_wire.get_current_position() != new_wire.father.get_coords()):
                    random_reassign_wire(new_wire, self.chip.grid)
        return (self.chip)

    def check_score(self, chip_copy: "Chip") -> bool:
        """
        Checks and updates a better chip and thus a better score
        """
        # Cost of the chip after placing a new wire
        copy_cost = chip_copy.calculate_costs()
        # Update cost of the original chip
        self.costs = self.chip.calculate_costs()

        if (copy_cost < self.costs):
            # Update chip to better version
            self.chip = chip_copy
            return True

        return False

    def run(self):
        # Get one valid solution
        self.make_random_valid_solution()

        # Update the first score
        self.chip.calculate_costs()

        # Writing original solved chip data to CSV file
        save_to_file(self.chip, self.output_filename)
        iteration: int = 0

        # Start timer
        start_time: float = time.time()

        while (True):
            try:
                # Go through all the wires
                for wire in range(len(self.chip.wires)):

                    # Try and improve the wire a thousand times
                    for _ in range(1000):

                        # Copy the original chip
                        chip_copy = copy.deepcopy(self.chip)

                        # Copy the current wire
                        wire_copy = chip_copy.wires[wire]

                        # Randomly replace the wire
                        random_reassign_wire(wire_copy, chip_copy.grid)
                        
                        # Find a new valid solution
                        while (wire_copy.get_current_position() != wire_copy.father.get_coords()):
                            random_reassign_wire(wire_copy, chip_copy.grid)

                        # Check for a better solution
                        if (self.check_score(chip_copy)):

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

        print(f"\nRuntime: {round(self.chip.cumulative_duration, 3)} seconds.")
        return self.chip
