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
    vision_type: str = "radial"  # "radial" or "cone"

    def get_next_position(self):
        if self.patrol_axis == "horizontal":
            next_x = self.pos.x + self.direction * self.speed
            return Position(next_x, self.pos.y)
        else:  # vertical
            next_y = self.pos.y + self.direction * self.speed
            return Position(self.pos.x, next_y)

    def get_facing_angle(self):
        if self.patrol_axis == "horizontal":
            return 0 if self.direction == 1 else 180  # Right: 0°, Left: 180°
        else:  # vertical
            return 90 if self.direction == 1 else 270  # Down: 90°, Up: 270°