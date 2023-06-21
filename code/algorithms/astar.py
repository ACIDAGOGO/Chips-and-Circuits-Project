import sys
sys.path.append("../classes")

from chip import Chip

class WireSegment:
    
    def __init__(self, previous_segment: "WireSegment" = None, position: tuple[int, int, int]):
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


class AstarAlg:

    def __init__(self, chip_no: int, netlist_no: int):
        self.chip = Chip(chip_no, f"netlist_{netlist_no}.csv")

    def create_parent_segments(self, mother_coords: tuple[int, int, int], father_coords: tuple[int, int, int]) -> tuple["WireSegment", "WireSegment"]:
        mother_segment = WireSegment(None, mother_coords)
        father_segement = WireSegment(None, father_coords)

        return mother_segment, father_segement

    def get_possible_directions(self, current_segment: "WireSegment"):
        x = current_segment.get_x()
        y = current_segment.get_y()
        z = current_segment.get_z()

        possible_directions = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]
        # check if valid
        return possible_directions


    def draw_wire(self, mother: "Gate", father: "Gate"):
        # Create lists which keep track of checked and not-checked possible segments
        open_list = []
        closed_list = []

        # Initialize mother and father segments
        mother_coords = mother.get_coords()
        father_coords = father.get_coords()
        mother_segment, father_segement = self.create_parent_segments(mother_coords, father_coords)

        # Initialize open list with mother segment
        open_list.append(mother_segment)

        while len(open_list) > 0:

            # Sort open list on segment cost 
            open_list.sort(key=lambda x: x.total_cost, reverse = True)

            # Set the current segment to the lowest sum segment
            current_segment = open_list[len(open_list) - 1]

            open_list.pop()
            closed_list.append(current_segment)



    def run(self):
        for mother in self.chip.gates.values():
            for father in self.chip.gates.values():
                draw_wire(mother, father)





1. Add the starting square (or node) to the open list.

2. Repeat the following:

A) Look for the lowest F cost square on the open list. We refer to this as the current square.

B). Switch it to the closed list.

C) For each of the 8 squares adjacent to this current square …

If it is not walkable or if it is on the closed list, ignore it. Otherwise do the following.
If it isn’t on the open list, add it to the open list. Make the current square the parent of this square. Record the F, G, and H costs of the square.
If it is on the open list already, check to see if this path to that square is better, using G cost as the measure. A lower G cost means that this is a better path. If so, change the parent of the square to the current square, and recalculate the G and F scores of the square. If you are keeping your open list sorted by F score, you may need to resort the list to account for the change.
D) Stop when you:

Add the target square to the closed list, in which case the path has been found, or
Fail to find the target square, and the open list is empty. In this case, there is no path.
3. Save the path. Working backwards from the target square, go from each square to its parent square until you reach the starting square. That is your path.