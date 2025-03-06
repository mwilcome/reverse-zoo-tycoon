from dataclasses import dataclass
from .position import Position

@dataclass
class EscapePoint:
    id: int
    pos: Position