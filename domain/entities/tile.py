from dataclasses import dataclass
from .position import Position

@dataclass
class Tile:
    pos: Position
    type: str  # "path", "wall", "bush", "cage", "escape"
    passable: bool