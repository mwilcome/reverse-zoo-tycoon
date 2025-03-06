from dataclasses import dataclass
from .position import Position

@dataclass
class Human:
    id: int
    pos: Position
    state: str  # "caged", "following", "escaped"
    stealth: bool = False
    follows: 'Zookeeper | Human | None' = None

    def update_position(self):
        if self.follows and self.state == "following":
            target_pos = self.follows.pos
            dist = self.pos.distance_to(target_pos)
            if dist > 20:  # Tighter chain
                self.pos.x += (target_pos.x - self.pos.x) * 0.1
                self.pos.y += (target_pos.y - self.pos.y) * 0.1