import random
from grid import Grid
from wire import Wire

max_tries: int = 1000
counter: int = 0
tries_counter: int = 0

def is_move_valid(wire: 'Wire', grid: 'Grid', desired_position: tuple[int, int]) -> bool:
    global counter
    global tries_counter

    previous_position = wire.get_previous_position()
    grid_upperbounds = grid.get_grid_size()

    if desired_position[0] > grid_upperbounds[0] or desired_position[1] > grid_upperbounds[1] or desired_position[0] < 0 or desired_position[1] < 0:
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

def get_random_direction(wire: 'Wire') -> tuple[int, int]:
    current_position = wire.get_current_position()
    current_position_x = current_position[0]
    current_position_y = current_position[1]

    possible_directions: list[tuple[int, int]] = [(current_position_x + 1, current_position_y), (current_position_x - 1, current_position_y), (current_position_x, current_position_y + 1), (current_position_x, current_position_y - 1)]

    random_direction: tuple[int, int] = random.choice(possible_directions)

    return random_direction

def run(wire: 'Wire', grid: 'Grid'):
    global counter
    counter = 0

    while (counter <= max_tries and wire.check_for_father() == False):
        random_direction = get_random_direction(wire)
        if (is_move_valid(wire, grid, random_direction)):
            wire.add_unit(random_direction)
            if (random_direction != wire.father.get_coords()):
                grid.values[random_direction[1]][random_direction[0]] -= 1




