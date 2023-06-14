import sys
sys.path.append("../classes")

import random
import matplotlib.pyplot as plt
from grid import Grid
from wire import Wire
from chip import Chip

max_tries: int = 1000
counter: int = 0
tries_counter: int = 0
iteration_counter: int = 0

def is_move_valid(wire: 'Wire', grid: 'Grid', desired_position: tuple[int, int, int]) -> bool:
    global counter
    global tries_counter

    previous_position = wire.get_previous_position()
    grid_upperbounds = grid.get_grid_size()

    if desired_position[0] > grid_upperbounds[0] or desired_position[1] > grid_upperbounds[1] or desired_position[2] > grid_upperbounds[2] or desired_position[0] < 0 or desired_position[1] < 0 or desired_position[2] < 0:
            counter += 1
            tries_counter += 1
            return False

    foreign_gate: bool = grid.check_for_illegal_gate(desired_position, wire.father)

    if desired_position == previous_position:
        counter += 1
        tries_counter += 1
        return False
    elif desired_position in wire.path:
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
    current_position = wire.get_current_position()
    current_position_x = current_position[0]
    current_position_y = current_position[1]
    current_position_z = current_position[2]

    possible_directions: list[tuple[int, int, int]] = [(current_position_x + 1, current_position_y, current_position_z), (current_position_x - 1, current_position_y, current_position_z), (current_position_x, current_position_y + 1, current_position_z), (current_position_x, current_position_y - 1, current_position_z), (current_position_x, current_position_y, current_position_z + 1), (current_position_x, current_position_y, current_position_z - 1)]

    random_direction: tuple[int, int] = random.choice(possible_directions)

    return random_direction

def lay_wire(wire: 'Wire', grid: 'Grid') -> None:
    global counter
    counter = 0

    while (counter <= max_tries and wire.check_for_father() == False):
        random_direction = get_random_direction(wire)
        if (is_move_valid(wire, grid, random_direction)):
            wire.add_unit(random_direction)
            if (random_direction != wire.father.get_coords()):
                grid.values[random_direction[2]][random_direction[1]][random_direction[0]] -= 1

def run_random() -> None:
    costs_list: list[int] = []

    global iteration_counter
    total_costs = 100


    while (iteration_counter < 100):
        iteration_counter += 1
        chip = Chip(0, "netlist_1.csv")

        for mother in chip.gates.values():
            for father in mother.get_destinations():
                new_wire = Wire(mother, father)
                chip.add_wire(new_wire)
                # print(f'WIRE ORIGIN: {new_wire.mother.get_id()} DESTINATION: {new_wire.father.get_id()}')
                lay_wire(new_wire, chip.grid)

                # Reset wire and its path on the grid and find new path until wire has found father
                while (new_wire.get_current_position() != new_wire.father.get_coords()):

                    # Trace back wire
                    for unit in range(len(new_wire.get_path()) - 1):
                        coords = new_wire.pop_unit()

                        # Reset grid on traced back route
                        chip.grid.values[coords[2]][coords[1]][coords[0]] += 1

                    # Start a new wire
                    lay_wire(new_wire, chip.grid)
        
        total_costs = chip.calculate_costs()
        costs_list.append(total_costs)


        #print(f'TOTAL COSTS: ${total_costs}')
        print(iteration_counter)

    # for gate in chip.gates.values():
    #     print(gate)
    #     print(f'CONNECTIONS: {gate.get_destinations()}')

    # print(chip.grid.values)
    # chip.grid.visualize_grid()

    # for wire in chip.wires:
    #     if wire.get_current_position() == wire.father.get_coords():
    #         print(f'WIRE {wire.mother.get_id()} FOUND FATHER')
    #     else:
    #         print(f'WIRE {wire.mother.get_id()} DID NOT FIND FATHER')


    plt.hist(total_costs, 21)
    plt.show()
