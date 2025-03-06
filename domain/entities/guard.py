from dataclasses import dataclass
from .position import Position

@dataclass
class Guard:
    id: int
    pos: Position
    direction: int  # 1 = right, -1 = left
    vision_range: float = 100

    def patrol(self):
        self.pos.x += 2 * self.direction
        if self.pos.x < 200 or self.pos.x > 600:
            self.direction *= -1