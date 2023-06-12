from gate import Gate

class Wire:
    def __init__(self, mother: 'Gate', father: 'Gate'):
        self.mother = mother
        self.father = father
        self.start_position: tuple[int, int] = mother.get_coords()
        self.path: list[tuple[int, int]] = [self.start_position]

    def add_unit(self, position: tuple[int, int]) -> None:
        self.path.append(position)

    def pop_unit(self) -> tuple[int, int]:
        return self.path.pop()

    def reset_path(self) -> None:
        self.path = [self.start_position]

    def get_path(self) -> list[tuple[int, int]]:
        return self.path
    
    def get_current_position(self) -> tuple[int, int]:
        wire_length = len(self.path)
        return self.path[wire_length - 1]

    def get_previous_position(self) -> tuple[int, int]:
        wire_length = len(self.path)

        if (wire_length > 1):
            return self.path[wire_length - 2]
        
        return self.get_current_position()
    
    def check_for_father(self) -> bool:
        if self.get_current_position() == self.father.get_coords():
            return True
        
        return False

