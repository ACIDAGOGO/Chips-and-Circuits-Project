import sys
sys.path.append("../classes")

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
    
    def check_if_wire_completed(self, current_segment: "WireSegment", father_segment: "WireSegment"):
        wire_path = []
        if current_segment == father_segment:
            segment = current_segment
            while segment is not None:
                wire_path.append(segment.position)
                segment = segment.previous_segment
            return True, wire_path.reverse() # Return reversed path
        else:
            return False, wire_path.reverse()
        
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
            #next_segment_position = (current_segment.get_x() + direction[0], current_segment.get_y() + direction[1], current_segment.get_z() + direction[2])
            next_segment_position = direction

            new_segment = WireSegment(current_segment, next_segment_position)

            next_segments.append(new_segment)

        return next_segments
    
    def assign_next_segment_costs(self, next_segment: "WireSegment", father_coords: tuple[int, int, int]):
        if (self.chip.grid.values[next_segment.get_z()][next_segment.get_y()][next_segment.get_x()] < -1):
            next_segment.wire_cost += 300
        else:
            next_segment.wire_cost += 1
        
        manhattan_distance = abs(next_segment.get_x() - father_coords[0]) + abs(next_segment.get_y() - father_coords[1]) + abs(next_segment.get_z() - father_coords[2])
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

            # Set the current segment to the lowest sum segment
            current_segment = open_list[len(open_list) - 1]

            #print(current_segment.position)

            # Add current lowest value (current) segment to closed list
            open_list.pop()
            closed_list.append(current_segment)

            # Check if father is reached
            completed, wire_path = self.check_if_wire_completed(current_segment, father_segment)
            if (completed == True):
                return wire_path

            # Get all next possible segments
            next_segments = self.create_next_segments(current_segment, father_coords)

            #print(next_segments)

            # 
            for segment in next_segments:
                # Check if segment has not been passed already
                for closed_segment in closed_list:
                    if segment == closed_segment:
                        continue
                
                # Assign costs to the next segment
                self.assign_next_segment_costs(segment, father_coords)

                for open_segment in open_list:
                    if segment == open_segment and segment.wire_cost > open_segment.wire_cost:
                        continue

                # If the segment passes all tests, add it to the open list
                open_list.append(segment)

    def run(self):
        for mother in self.chip.gates.values():
            for father in mother.get_destinations():
                print("Drawing wire")
                wire_path = self.draw_wire(mother, father)
                print(wire_path)
                print("Wire complete")

                new_wire = Wire(mother, father)
                new_wire.pop_unit()
                for segment_coords in wire_path:
                    new_wire.add_unit(segment_coords)

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