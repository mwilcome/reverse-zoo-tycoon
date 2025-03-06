from dataclasses import dataclass
from typing import List
from .position import Position

@dataclass
class Zookeeper:
    id: int
    pos: Position
    stealth: bool = False
    humans: List['Human'] = None  # Forward reference, defined later

    def __post_init__(self):
        if self.humans is None:
            self.humans = []