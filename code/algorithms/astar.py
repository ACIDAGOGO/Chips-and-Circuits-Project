import sys
sys.path.insert(0, "../classes")

import time

from typing import Optional
import operator

from classes.chip import Chip
from classes.gate import Gate
from classes.wire import Wire
from analysis.save import save_to_file

class WireSegment:
    """ Implements a wire segment. A wire segment is a node which is initialized with a previous wire segment this
        one is connected to and the position of the segment. Furthermore it contains the wire cost of laying a wire to the position
        of this segment, the manhattan distance cost between this segment and destination segment and the sum of these costs.
        Wire segments are used in the A* algorithm to determine the cheapest wire path possible between two points.
    """

    def __init__(self, previous_segment: "WireSegment" = None, position: tuple[int, int, int] = None):
        self.previous_segment = previous_segment
        self.position = position

        self.wire_cost = 0
        self.manhattan_cost = 0
        self.total_cost = 0

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_z(self):
        return self.position[2]

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self) -> str:
        return f"{self.position}"
    

class Heuristics:
    """ Implements an easy way to apply extra heurstics to the A* algorithm. These heuristics influence which paths
        are prioritized (seen as "cheaper") when laying wire segments by setting the cost of making certain moves 
    """

    def __init__(self, heuristic: str = None):
        self.heuristic = heuristic

    def calculate_manhattan_distance(self, segment_coords: tuple[int, int, int], father_coords: tuple[int, int, int]):
        """ Returns the manhattan distance between two points """

        manhattan_distance = abs(segment_coords[0] - father_coords[0]) + abs(segment_coords[1] - father_coords[1]) + abs(segment_coords[2] - father_coords[2])

        return manhattan_distance
    
    def default(self, chip: "Chip", current_segment: "WireSegment", next_segment: "WireSegment", father_coords: tuple[int, int, int]):
        """ Default A*, only takes wire intersection costs into account """

        # Check if position already contains a wire segment and assign wire cost
        if (chip.grid.values[next_segment.get_z()][next_segment.get_y()][next_segment.get_x()] <= -1):
            # next_segment.wire_cost += 300
            next_segment.wire_cost = current_segment.wire_cost + 300
        else:
            # next_segment.wire_cost += 1
            next_segment.wire_cost = current_segment.wire_cost + 1
        
        # Assign manhattan distance cost
        manhattan_distance = self.calculate_manhattan_distance(next_segment.position, father_coords)
        next_segment.manhattan_cost = manhattan_distance

        # Assign total cost
        next_segment.total_cost = next_segment.wire_cost + manhattan_distance

    def avoid_gates(self, chip: "Chip", next_segment: "WireSegment", mother_coords: tuple[int, int, int], father_coords: tuple[int, int, int]):
        segment_position = next_segment.position
        grid_size = chip.grid.get_grid_size()
        
        avoid_distance = 1
        for z in range(segment_position[2], segment_position[2] + avoid_distance + 1):
            for y in range(segment_position[1], segment_position[1] + avoid_distance + 1):
                for x in range(segment_position[0], segment_position[0] + avoid_distance + 1):
                    if (x < grid_size[0] and y < grid_size[1] and z < grid_size[2]):
                        if (chip.grid.values[z][y][x] > 0 and not (x,y,z) == mother_coords and not (x,y,z) == father_coords):
                            next_segment.wire_cost += 50

    def avoid_low_layers(self, next_segment: "WireSegment"):
        layer_costs = [7,6,5,4,3,2,1,0]
        z = next_segment.get_z()

        next_segment.wire_cost += layer_costs[z]

    def assign_next_segment_costs(self, chip: "Chip", current_segment: "WireSegment", next_segment: "WireSegment", mother_coords: tuple[int, int, int], father_coords: tuple[int, int, int]):
        """ Determines and assigns the cost of using a wire segment to the object """

        # Apply different costs based on chosen heuristic
        self.default(chip, current_segment, next_segment, father_coords)
        if (self.heuristic == "avoid_gates"):
            self.avoid_gates(chip, next_segment, mother_coords, father_coords)
            next_segment.total_cost = next_segment.wire_cost + next_segment.manhattan_cost
        elif (self.heuristic == "avoid_low"):
            self.avoid_low_layers(next_segment)
            next_segment.total_cost = next_segment.wire_cost + next_segment.manhattan_cost
        elif (self.heuristic == "all"):
            self.avoid_gates(chip, next_segment, mother_coords, father_coords)
            self.avoid_low_layers(next_segment)
            next_segment.total_cost = next_segment.wire_cost + next_segment.manhattan_cost


class AstarAlg:
    """ Implements the A* pathfinding algorithms, this algrotihm determines the cheapest path between two gates in on the grid of a chip.
        AstarAlg is initialized with a chip numbr, netlist number and filename to output to.
    """

    def __init__(self, chip_no: int, netlist_no: int, output_filename: str, heuristic: str):
        self.chip = Chip(chip_no, f"netlist_{netlist_no}.csv")
        self.output_filename = output_filename
        self.heuristic = Heuristics(heuristic)
        self.run()

    def create_parent_segments(self, mother_coords: tuple[int, int, int], father_coords: tuple[int, int, int]) -> tuple["WireSegment", "WireSegment"]:
        """ Returns the origin and destination segment of a wire """

        mother_segment = WireSegment(None, mother_coords)
        father_segment = WireSegment(None, father_coords)

        return mother_segment, father_segment
    
    def update_grid(self, wire_path: list[tuple[int, int, int]]) -> None:
        """ Updates the grid (3D array) if a coordinate contains a wire """

        for coordinate in wire_path[1:-1]:
                self.chip.grid.values[coordinate[2]][coordinate[1]][coordinate[0]] -= 1
    
    def check_if_wire_completed(self, current_segment: "WireSegment", father_segment: "WireSegment") -> tuple[bool, Optional[list[tuple[int, int, int]]]]:
        """ Determines if a wire had reached its destination and if so retuns its path"""

        wire_path = []
        if current_segment == father_segment:
            segment = current_segment

            # Create path
            while segment is not None:
                wire_path.append(segment.position)
                segment = segment.previous_segment

            # Update 3D array
            self.update_grid(wire_path)

            return True, wire_path
        else:
            return False, None
        
    def get_all_directions(self, current_segment: "WireSegment") -> list[tuple[int, int, int]]:
        """ Retuns all possible directions in the grid from a wire segments' position"""

        x = current_segment.get_x()
        y = current_segment.get_y()
        z = current_segment.get_z()

        directions = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]

        return directions
    
    def get_possible_directions(self, current_segment: "WireSegment", father_coords: tuple[int, int, int]) -> list[tuple[int, int, int]]:
        """ Returns all possible directions in the grid from a wire segemnt's position """

        possible_directions = []

        # Get all directions
        directions = self.get_all_directions(current_segment)

        # Iterate through all directions
        for direction in directions:
            # Get grid bounds
            grid_upperbounds = self.chip.grid.get_grid_size()

            # Check if this direction is outside the grid, proceed if not
            if direction[0] > grid_upperbounds[0] or direction[1] > grid_upperbounds[1] or direction[2] > grid_upperbounds[2] or direction[0] < 0 or direction[1] < 0 or direction[2] < 0:
                continue

            # Check if this direction contains a gate other than the father gate, proceed if not 
            if self.chip.grid.values[direction[2]][direction[1]][direction[0]] > 0 and direction != father_coords:
                continue

            # If all checks passed, append direction to possible directions
            possible_directions.append(direction)

        return possible_directions

    def create_next_segments(self, current_segment: "WireSegment", father_coords: tuple[int, int, int]) -> list["WireSegment"]:
        """ Create and return a wire segment for each possible direction from the current wire segment """

        next_segments = []
        
        # Get possible directions
        possible_directions = self.get_possible_directions(current_segment, father_coords)

        # Iterate through possible directions
        for direction in possible_directions:
            next_segment_position = direction

            # Create new wire segment
            new_segment = WireSegment(current_segment, next_segment_position)

            # Append new segment to list
            next_segments.append(new_segment)

        return next_segments
    
    # def calculate_manhattan_distance(self, segment_coords: tuple[int, int, int], father_coords: tuple[int, int, int]):
    #     """ Returns the manhattan distance between two points """

    #     manhattan_distance = abs(segment_coords[0] - father_coords[0]) + abs(segment_coords[1] - father_coords[1]) + abs(segment_coords[2] - father_coords[2])

    #     return manhattan_distance
    
    # def assign_next_segment_costs(self, next_segment: "WireSegment", father_coords: tuple[int, int, int]):
    #     """ Determines and assigns the cost of using a wire segment to the object """

    #     # Check if position already contains a wire segment and assign wire cost
    #     if (self.chip.grid.values[next_segment.get_z()][next_segment.get_y()][next_segment.get_x()] <= -1):
    #         next_segment.wire_cost += 300
    #     else:
    #         next_segment.wire_cost += 1
        
    #     # Assign manhattan distance cost
    #     manhattan_distance = self.calculate_manhattan_distance(next_segment.position, father_coords)
    #     next_segment.manhattan_cost = manhattan_distance

    #     # Assign total cost
    #     next_segment.total_cost = next_segment.wire_cost + manhattan_distance

    def draw_wire(self, mother: "Gate", father: "Gate"):
        """ Determines the shortest path between two points and draws the wire """

        # Create lists which keep track of checked and not-checked possible segments
        open_list = []
        closed_list = []
        next_segments = []

        # Initialize mother and father segments
        mother_coords = mother.get_coords()
        father_coords = father.get_coords()
        mother_segment, father_segment = self.create_parent_segments(mother_coords, father_coords)

        # Initialize open list with mother segment
        open_list.append(mother_segment)

        # Repeat while there open paths
        while len(open_list) > 0:
            # Sort open list on segment cost 
            open_list.sort(key=lambda x: x.total_cost, reverse = True)

            # Set the current segment to the lowest sum segment
            current_segment = open_list[len(open_list) - 1]

            # Add current lowest value (current) segment to closed list
            open_list.pop()
            closed_list.append(current_segment)

            # current_segment = open_list[0]
            # current_index = 0
            # for index, item in enumerate(open_list):
            #     if item.total_cost < current_segment.total_cost:
            #         current_segment = item
            #         current_index = index

            # open_list.pop(current_index)
            # closed_list.append(current_segment)


            # Check if father is reached
            completed, wire_path = self.check_if_wire_completed(current_segment, father_segment)
            if (completed):
                return wire_path

            # Get all next possible segments
            next_segments = self.create_next_segments(current_segment, father_coords)

            # Loop through possible next segments to see if they are valid and better
            for segment in next_segments:
                go_next = False

                # Skip segment if it has already been passed
                for closed_segment in closed_list:
                    if segment == closed_segment:
                        go_next = True
                if go_next:
                    continue

                # Assign costs to the next segment
                self.heuristic.assign_next_segment_costs(self.chip, current_segment, segment, mother_coords, father_coords)

                # Check if possible next segment already in open list
                for index, open_segment in enumerate(open_list):
                    if segment == open_segment:
                        # Skip segment if there already is a segment on the same position with a cheaper path, else add segment and remove more expensive path
                        if segment.wire_cost > open_segment.wire_cost:
                            go_next = True
                        else:
                            closed_list.append(open_segment)
                            open_list.pop(index)
                if go_next:
                    continue

                # Add the segment to the open list
                open_list.append(segment)

        # Exit if open list is empty and father was not found
        print("Can't lay wire")
        sys.exit(1)

    def sort_desired_connections(self):
        """ Sort mother-father connections which have to be made (currently sorts on shortest to longest manhattan distance) """

        connections: list[tuple["Gate", "Gate", int]] = []
        for mother in self.chip.gates.values():
            for father in mother.get_destinations():
                manhattan_distance = self.heuristic.calculate_manhattan_distance(mother.get_coords(), father.get_coords())
                connections.append((mother, father, manhattan_distance))

        connections.sort(key=operator.itemgetter(2))
        
        return connections[::-1]

    def run(self):
        """ Lay all wires and return chip """

        # Start timer
        start_time: float = time.time()

        # Get sorted connections
        sorted_connections = self.sort_desired_connections()
        
        # Draw and add all wires to chip
        wires_drawn = 1
        for connection in sorted_connections:
                mother = connection[0]
                father = connection[1]

                # Draw wire and get path
                print(f"Drawing wire {wires_drawn}")
                wire_path = self.draw_wire(mother, father)
                wires_drawn += 1

                # Create new wire object
                new_wire = Wire(mother, father)
                new_wire.pop_unit()

                # Add found path to wire object
                for segment_coords in wire_path:
                    new_wire.add_unit(segment_coords)

                # Add wire object to chip
                self.chip.add_wire(new_wire)

        # Determine duration of algorithm
        total_time = time.time() - start_time
        print(total_time)

        # Assing duration to chip
        self.chip.iteration_duration = total_time
        self.chip.cumulative_duration += self.chip.iteration_duration

        # Determine chip cost
        self.chip.calculate_costs()

        # Save relevant chip data to file
        save_to_file(self.chip, self.output_filename)
