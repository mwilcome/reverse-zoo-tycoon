from dataclasses import dataclass
from .position import Position

@dataclass
class Guard:
    id: int
    pos: Position
    direction: int  # 1 or -1
    speed: int = 2
    patrol_axis: str = "horizontal"  # "horizontal" or "vertical"
    vision_range: float = 100.0

    def get_next_position(self):
        if self.patrol_axis == "horizontal":
            next_x = self.pos.x + self.direction * self.speed
            return Position(next_x, self.pos.y)
        else:  # vertical
            next_y = self.pos.y + self.direction * self.speed
            return Position(self.pos.x, next_y)