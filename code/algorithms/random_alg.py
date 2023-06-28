import sys
import random
import copy
import time
from classes.grid import Grid
from classes.wire import Wire
from classes.chip import Chip
from analysis.save import save_to_file
sys.path.append("../analysis")
sys.path.append("../classes")

random.seed(a=1)
max_tries: int = 1000
counter: int = 0
tries_counter: int = 0


def is_move_valid(wire: 'Wire', grid: 'Grid',
                  desired_position: tuple[int, int, int]) -> bool:
    """
    Checks if a given move is a valid move.
    """

    global counter
    global tries_counter

    grid_upperbounds = grid.get_grid_size()

    # Check if move is out of bounds
    if desired_position[0] > grid_upperbounds[0] or\
       desired_position[1] > grid_upperbounds[1] or\
       desired_position[2] > grid_upperbounds[2] or\
       desired_position[0] < 0 or\
       desired_position[1] < 0 or\
       desired_position[2] < 0:
        counter += 1
        tries_counter += 1
        return False

    foreign_gate: bool =\
        grid.check_for_illegal_gate(desired_position, wire.father)

    # Check for all illegal moves
    if desired_position in wire.path:
        counter += 1
        tries_counter += 1
        return False
    elif foreign_gate:
        counter += 1
        tries_counter += 1
        return False
    else:
        counter = 0
        return True


def get_random_direction(wire: 'Wire') -> tuple[int, int, int]:
    """
    Defines a random direction for a wire to base its next move on.
    """

    current_position = wire.get_current_position()
    current_position_x = current_position[0]
    current_position_y = current_position[1]
    current_position_z = current_position[2]

    possible_directions: list[tuple[int, int, int]] =\
        [(current_position_x + 1, current_position_y, current_position_z),
         (current_position_x - 1, current_position_y, current_position_z),
         (current_position_x, current_position_y + 1, current_position_z),
         (current_position_x, current_position_y - 1, current_position_z),
         (current_position_x, current_position_y, current_position_z + 1),
         (current_position_x, current_position_y, current_position_z - 1)]

    random_direction: tuple[int, int, int] = random.choice(possible_directions)

    return random_direction


def lay_wire(wire: 'Wire', grid: 'Grid') -> None:
    """
    Inserts wires into the 3D grid.
    """

    global counter
    counter = 0

    while (counter <= max_tries and not wire.check_for_father()):
        random_direction = get_random_direction(wire)
        if (is_move_valid(wire, grid, random_direction)):
            wire.add_unit(random_direction)
            if (random_direction != wire.father.get_coords()):
                grid.values[random_direction[2]][random_direction[1]]\
                           [random_direction[0]] -= 1


def random_reassign_wire(new_wire: "Wire", grid: "Grid"):
    """
    Removes a wire and create a new one.
    """

    # Trace back wire and remove
    for unit in range(len(new_wire.get_path()) - 1):
        coords = new_wire.pop_unit()

        # Reset grid on traced back route
        if grid.values[coords[2]][coords[1]][coords[0]] !=\
           new_wire.father.get_id():
            grid.values[coords[2]][coords[1]][coords[0]] += 1

    # Start a new wire
    lay_wire(new_wire, grid)


def run_random(chip_no: int, netlist_no: int, output_filename: str) -> 'Chip':
    """
    Runs random algorithm.
    """
    
    iteration = 0
    cumulative_duration: float = 0.0

    # Start timer
    start_time: float = time.time()

    while (True):
        try:
            chip = Chip(chip_no, f"netlist_{netlist_no}.csv")

            # Loop through all mother gates and lay wires to father
            for mother in chip.gates.values():
                for father in mother.get_destinations():
                    new_wire = Wire(mother, father)
                    chip.add_wire(new_wire)
                    lay_wire(new_wire, chip.grid)

                    # Reset wire and its path on the grid
                    # and find new path until wire has found father
                    while (new_wire.get_current_position() !=
                           new_wire.father.get_coords()):
                        random_reassign_wire(new_wire, chip.grid)

            # Calculate total cost of chip
            total_costs = chip.calculate_costs()

            # Remeber cheapest chip configuration
            if (iteration == 0):
                best_chip = copy.deepcopy(chip)
            else:
                if (total_costs < best_chip.calculate_costs()):
                    best_chip = copy.deepcopy(chip)

            # Count chip iteration number
            chip.iteration = iteration
            iteration += 1

            # Get time for completed iteration
            completed_iteration_time = time.time()

            # Calculate duration of iteration
            chip.iteration_duration = completed_iteration_time - start_time

            # Update cumulative iteration duration
            cumulative_duration += chip.iteration_duration
            chip.cumulative_duration = cumulative_duration

            # Reset timer
            start_time = time.time()

            # Save relevant chip data to file
            save_to_file(chip, output_filename)

        except KeyboardInterrupt:
            break
    print(f"\nRuntime: {round(cumulative_duration, 3)} seconds.")
    return best_chip
