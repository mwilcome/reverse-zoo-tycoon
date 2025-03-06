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
        self.guards = [Guard(i + 1, pos, 1, patrol_axis=random.choice(["horizontal", "vertical"])) 
                       for i, pos in enumerate(map_data['guard_positions'])]
        self.escape_points = [EscapePoint(i + 1, pos) for i, pos in enumerate(map_data['escape_positions'])]

    def free_human(self, human: Human):
        if (human.state == "caged" and 
            self.zookeeper.pos.distance_to(human.pos) < 30):
            human.state = "following"
            human.follows = self.zookeeper if not self.zookeeper.humans else self.zookeeper.humans[-1]
            self.zookeeper.humans.append(human)

    def escape_human(self, human: Human):
        for ep in self.escape_points:
            if (human.pos.distance_to(ep.pos) < 30 and 
                human.state == "following" and 
                self.zookeeper.pos.distance_to(ep.pos) < 30):
                human.state = "escaped"
                self.zookeeper.humans.remove(human)
                human.follows = None

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
        for human in self.humans:
            human.update_position()

    def is_caught(self) -> bool:
        return any(DetectionService.is_detected(guard, self.zookeeper) 
                   for guard in self.guards)

    def is_won(self) -> bool:
        return all(human.state == "escaped" for human in self.humans)