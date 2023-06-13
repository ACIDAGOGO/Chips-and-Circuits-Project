class Gate:
    def __init__(self, id: int, x: int, y: int) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.destinations: list['Gate'] = []

    def get_id(self) -> int:
        return self.id

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_coords(self) -> tuple[int, int]:
        return (self.x, self.y)

    def add_destinations(self, gate: 'Gate') -> None:
        self.destinations.append(gate)

    def get_destinations(self) -> list['Gate']:
        return self.destinations

    def __repr__(self) -> str:
        return f"GATE {self.id}"