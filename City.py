import random

class City:
    name: str
    x: float
    y: float
    cluster_id: int

    def __init__(self, x: float, y: float, name: str = None) -> None:
        self.name = name if isinstance(name, str) else f"{random.randint(1,100)}"
        self.x = x
        self.y = y
        self.cluster_id = -1
    
    def __repr__(self) -> str:
        return f"{self.name}: {self.x} - {self.y}"