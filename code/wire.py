from gate import Gate

class Wire:
    def __init__(self, mother: 'Gate', father: 'Gate'):
        self.mother = mother
        self.father = father
        self.path: list[tuple[int, int]] = []

    def add_unit(self, x: int, y: int) -> None:
        self.path.append((x, y))

    def pop_unit(self) -> tuple[int, int]:
        return self.path.pop()

    def get_path(self) -> list[tuple[int, int]]:
        return self.path

