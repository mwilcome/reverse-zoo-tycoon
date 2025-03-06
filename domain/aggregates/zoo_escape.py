from domain.entities.zookeeper import Zookeeper
from domain.entities.human import Human
from domain.entities.guard import Guard
from domain.entities.escape_point import EscapePoint
from domain.entities.position import Position
from domain.services.detection_service import DetectionService

class ZooEscape:
    def __init__(self):
        self.zookeeper = Zookeeper(1, Position(200, 300))
        self.humans = [Human(1, Position(600, 300), "caged")]
        self.guards = [Guard(1, Position(400, 300), 1)]
        self.escape_points = [EscapePoint(1, Position(700, 500))]

    def free_human(self, human: Human):
        if (human.state == "caged" and 
            self.zookeeper.pos.distance_to(human.pos) < 50):
            human.state = "following"
            human.follows = self.zookeeper if not self.zookeeper.humans else self.zookeeper.humans[-1]
            self.zookeeper.humans.append(human)

    def escape_human(self, human: Human):
        for ep in self.escape_points:
            if (human.pos.distance_to(ep.pos) < 30 and 
                human.state == "following"):
                human.state = "escaped"
                self.zookeeper.humans.remove(human)
                human.follows = None

    def update(self):
        for guard in self.guards:
            guard.patrol()
        for human in self.humans:
            human.update_position()

    def is_caught(self) -> bool:
        return any(DetectionService.is_detected(guard, self.zookeeper) 
                  for guard in self.guards)