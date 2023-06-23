import sys
import random
import math
import time

from .hill_climber import HillClimber
sys.path.append("../analysis")
sys.path.append("../classes")
sys.path.append("..")

import copy
import random
from classes.chip import Chip
from classes.wire import Wire
from .random_alg import lay_wire, random_reassign_wire

from analysis.save import save_to_file



class SimulatedAnnealing(HillClimber):


    def __init__(self, chip_no: int, netlist_no: int, output_filename: str, temp: int = 1000):
        # Use init of hill_climber class
        super().__init__(chip_no, netlist_no, output_filename)
        #self.chip = Chip(chip_no, f"netlist_{netlist_no}.csv")

        # Starting and current temperature
        self.start_temp = temp
        self.current_temp = temp
        self.amount_of_tries: int = 30

    def cool_down(self, amount_of_tries: int):
        """
        This function will make the temperature gradually cool down eventually becoming zero. 
        When this has become zero, the function will just run like a regular hillclimber would.
        """

        self.current_temp -= (self.start_temp / amount_of_tries)
        print(self.current_temp)
    

    def check_solution_not_perfect(self, chip_copy: "Chip"):
        """
        Checks for a better solution and updates the chip likewise.
        Will sometimes accept a worse chip, depending on the current temperature.
        A higher temperature will increase the chances of accepting a worse chip.
        """

        # Cost of the chip after placing a new wire
        copy_cost = chip_copy.calculate_costs()
        # Update cost of the original chip
        self.costs = self.chip.calculate_costs()

        # difference between the new and old chip's costs
        difference: int = copy_cost - self.costs

        if (difference < 0):
            self.chip = chip_copy
            return True

        if (self.current_temp <= 0):
            chance = 0
        else:
            # Calculate probability of accepting new graph;
            # the larger the difference the smaller the chance
            chance = math.exp(- difference / self.current_temp)

        # Note that if the difference is positive and the costs are worse,
        # chance will become small.
        # A negative difference will result in a chance greater than 1
        # and will therefore always be accepted.

        # Turn the temperature down
        self.cool_down(self.amount_of_tries)

        # Amount of tries goes down by one
        if (self.amount_of_tries != 1):
            self.amount_of_tries -= 1

        # randomly choose whether we will accept the chip
        print(chance)
        if random.random() < chance:
            print(f"random {random.random()}")
            self.chip = chip_copy
            return True
        
        return False
    
    def run_sim_annealing(self):
        # Get one valid solution
        self.make_random_valid_solution()

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
                        if (self.check_solution_not_perfect(chip_copy)):

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
        
        
        

