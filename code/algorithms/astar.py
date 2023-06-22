import sys
sys.path.append("../classes")

from typing import Optional
import operator

from chip import Chip
from gate import Gate
from wire import Wire


class WireSegment:
    
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
        return f"Previous: ({self.previous_segment}), Position: ({self.position})"


class AstarAlg:

    def __init__(self, chip_no: int, netlist_no: int):
        self.chip = Chip(chip_no, f"netlist_{netlist_no}.csv")
        self.run()

    def create_parent_segments(self, mother_coords: tuple[int, int, int], father_coords: tuple[int, int, int]) -> tuple["WireSegment", "WireSegment"]:
        mother_segment = WireSegment(None, mother_coords)
        father_segment = WireSegment(None, father_coords)

        return mother_segment, father_segment
    
    def update_grid(self, wire_path: list[tuple[int, int, int]]) -> None:
        for coordinate in wire_path[1:-1]:
                self.chip.grid.values[coordinate[2]][coordinate[1]][coordinate[0]] -= 1
    
    def check_if_wire_completed(self, current_segment: "WireSegment", father_segment: "WireSegment") -> tuple[bool, Optional[list[tuple[int, int, int]]]]:
        wire_path = []
        if current_segment == father_segment:
            segment = current_segment
            while segment is not None:
                wire_path.append(segment.position)
                segment = segment.previous_segment

            self.update_grid(wire_path)

            return True, wire_path
        else:
            return False, None
        
    def get_all_directions(self, current_segment: "WireSegment") -> list[tuple[int, int, int]]:
        x = current_segment.get_x()
        y = current_segment.get_y()
        z = current_segment.get_z()

        directions = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]

        return directions
    
    def get_possible_directions(self, current_segment: "WireSegment", father_coords: tuple[int, int, int]) -> list[tuple[int, int, int]]:
        directions = self.get_all_directions(current_segment)
        possible_directions = []

        for direction in directions:
            grid_upperbounds = self.chip.grid.get_grid_size()

            # Check if this direction is within the grid
            if direction[0] > grid_upperbounds[0] or direction[1] > grid_upperbounds[1] or direction[2] > grid_upperbounds[2] or direction[0] < 0 or direction[1] < 0 or direction[2] < 0:
                continue

            # Check if this direction does not contain a gate other than the father gate
            if self.chip.grid.values[direction[2]][direction[1]][direction[0]] > 0 and direction != father_coords:
                continue

            # If all checks passed, append direction to possible directions
            possible_directions.append(direction)

        return possible_directions

    def create_next_segments(self, current_segment: "WireSegment", father_coords: tuple[int, int, int]) -> list["WireSegment"]:
        next_segments = []
        
        possible_directions = self.get_possible_directions(current_segment, father_coords)
        for direction in possible_directions:
            next_segment_position = direction

            new_segment = WireSegment(current_segment, next_segment_position)

            next_segments.append(new_segment)

        return next_segments
    
    def calculate_manhattan_distance(self, segment_coords: tuple[int, int, int], father_coords: tuple[int, int, int]):
        manhattan_distance = abs(segment_coords[0] - father_coords[0]) + abs(segment_coords[1] - father_coords[1]) + abs(segment_coords[2] - father_coords[2])

        return manhattan_distance
    
    def assign_next_segment_costs(self, next_segment: "WireSegment", father_coords: tuple[int, int, int]):
        if (self.chip.grid.values[next_segment.get_z()][next_segment.get_y()][next_segment.get_x()] <= -1):
            next_segment.wire_cost += 300
        else:
            next_segment.wire_cost += 1
        
        manhattan_distance = self.calculate_manhattan_distance(next_segment.position, father_coords)
        next_segment.manhattan_cost = manhattan_distance

        next_segment.total_cost = next_segment.wire_cost + manhattan_distance

    def draw_wire(self, mother: "Gate", father: "Gate"):
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

        while len(open_list) > 0:
            # Sort open list on segment cost 
            open_list.sort(key=lambda x: x.total_cost, reverse = True)

            #     print(f"Lowest {open_list[len(open_list) - 1].total_cost}")

            # Set the current segment to the lowest sum segment
            current_segment = open_list[len(open_list) - 1]

            #print(current_segment.position)

            # Add current lowest value (current) segment to closed list
            open_list.pop()
            closed_list.append(current_segment)

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
                self.assign_next_segment_costs(segment, father_coords)

                # Skip segment if it is already in open list and has a higher cost
                for open_segment in open_list:
                    if segment == open_segment and segment.wire_cost > open_segment.wire_cost:
                        go_next = True
                if go_next:
                    continue

                # Add the segment to the open list
                open_list.append(segment)

            # # Check if segment has not been passed already
            # go_next = False
            # for closed_segment in closed_list:
            #     if segment == closed_segment:
            #         go_next = True
            # if go_next:
            #     continue

            # # Assign costs to the next segment
            # self.assign_next_segment_costs(segment, father_coords)

            # for open_segment in open_list:
            #     if segment == open_segment and segment.wire_cost < open_segment.wire_cost:
            #         print(segment)
            #         print(open_segment)
            #         open_segment.wire_cost = segment.wire_cost
            #         open_segment.previous_segment = current_segment
            #         go_next = True
            
            # if go_next:
            #     continue

            # # If the segment passes all tests, add it to the open list
            # open_list.append(segment)

            # print(f"Open list {open_list}")
            # print(f"Closed list {closed_list}")

        # Exit if open list is empty and father was not found
        print("Can't lay wire")
        sys.exit(1)

    def sort_desired_connections(self):
        # Sort mother-father connections which have to be made (currently sorts on shortest to longest distance)
        connections: list[tuple["Gate", "Gate", int]] = []
        for mother in self.chip.gates.values():
            for father in mother.get_destinations():
                manhattan_distance = self.calculate_manhattan_distance(mother.get_coords(), father.get_coords())
                connections.append((mother, father, manhattan_distance))

        connections.sort(key=operator.itemgetter(2))
        
        return connections

    def run(self):
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
                print("Wire complete")

                # Create new wire object
                new_wire = Wire(mother, father)
                new_wire.pop_unit()

                # Add found path to wire object
                for segment_coords in wire_path:
                    new_wire.add_unit(segment_coords)

                # Add wire object to chip
                self.chip.add_wire(new_wire)

# 1. Add the starting square (or node) to the open list.

# 2. Repeat the following:

# A) Look for the lowest F cost square on the open list. We refer to this as the current square.

# B). Switch it to the closed list.

# C) For each of the 8 squares adjacent to this current square …

# If it is not walkable or if it is on the closed list, ignore it. Otherwise do the following.
# If it isn’t on the open list, add it to the open list. Make the current square the parent of this square. Record the F, G, and H costs of the square.
# If it is on the open list already, check to see if this path to that square is better, using G cost as the measure. A lower G cost means that this is a better path. If so, change the parent of the square to the current square, and recalculate the G and F scores of the square. If you are keeping your open list sorted by F score, you may need to resort the list to account for the change.
# D) Stop when you:

# Add the target square to the closed list, in which case the path has been found, or
# Fail to find the target square, and the open list is empty. In this case, there is no path.
# 3. Save the path. Working backwards from the target square, go from each square to its parent square until you reach the starting square. That is your path.