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

    def add_destinations(self, gate: 'Gate') -> None:
        self.destinations.append(gate)

    def get_destinations(self, gate: 'Gate') -> list['Gate']:
        return self.destinations

    def __repr__(self) -> str:
        return f"ID: {self.id}, X: {self.x}, Y: {self.y}"