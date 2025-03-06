import random
from domain.entities.zookeeper import Zookeeper
from domain.entities.human import Human
from domain.entities.guard import Guard
from domain.entities.escape_point import EscapePoint
from domain.entities.position import Position
from domain.entities.tile import Tile
from domain.services.detection_service import DetectionService
from infrastructure.map_generator import MapGenerator

class ZooEscape:
    def __init__(self):
        map_data = MapGenerator.generate_map()
        self.map = map_data['tiles']
        self.zookeeper = Zookeeper(1, map_data['spawn_pos'])
        self.humans = [Human(i + 1, pos, "caged") for i, pos in enumerate(map_data['cage_positions'])]
        self.guards = [
            Guard(1, map_data['guard_positions'][0], 1, patrol_axis=random.choice(["horizontal", "vertical"]), vision_type="radial"),
            Guard(2, map_data['guard_positions'][1], 1, patrol_axis=random.choice(["horizontal", "vertical"]), vision_type="cone")
        ]
        self.escape_points = [EscapePoint(i + 1, pos) for i, pos in enumerate(map_data['escape_positions'])]
        self.map_width = MapGenerator.WIDTH * MapGenerator.TILE_SIZE
        self.map_height = MapGenerator.HEIGHT * MapGenerator.TILE_SIZE
        self.player_width = 20
        self.player_height = 20
        self.guard_width = 30
        self.guard_height = 30
        self.score = 0

    def free_human(self, human: Human):
        if (human.state == "caged" and 
            self.zookeeper.pos.distance_to(human.pos) < 30):
            human.state = "following"
            human.follows = self.zookeeper if not self.zookeeper.humans else self.zookeeper.humans[-1]
            self.zookeeper.humans.append(human)

    def escape_human(self, human: Human):
        # Check all humans for escape, not just one
        for human in self.humans[:]:  # Use a copy to avoid modifying list during iteration
            for ep in self.escape_points:
                if (human.pos.distance_to(ep.pos) < 30 and 
                    human.state == "following" and 
                    self.zookeeper.pos.distance_to(ep.pos) < 30):
                    human.state = "escaped"
                    self.zookeeper.humans.remove(human)
                    human.follows = None
                    self.score += 100  # Add 100 points for each escaped human

    def check_collision(self, pos: Position) -> bool:
        for tile in self.map:
            if not tile.passable and (
                tile.pos.x <= pos.x + 10 < tile.pos.x + MapGenerator.TILE_SIZE and
                tile.pos.y <= pos.y + 10 < tile.pos.y + MapGenerator.TILE_SIZE
            ):
                return True
        return False

    def update(self):
        for guard in self.guards:
            next_pos = guard.get_next_position()
            if not self.check_collision(next_pos):
                guard.pos = next_pos
            else:
                guard.direction *= -1
            guard.pos.x = max(0, min(guard.pos.x, self.map_width - self.guard_width))
            guard.pos.y = max(0, min(guard.pos.y, self.map_height - self.guard_height))
        for human in self.humans:
            human.update_position()

    def is_caught(self) -> bool:
        return any(DetectionService.is_detected(guard, self.zookeeper) 
                   for guard in self.guards)

    def is_won(self) -> bool:
        return all(human.state == "escaped" for human in self.humans)