from domain.entities.guard import Guard
from domain.entities.zookeeper import Zookeeper
from domain.entities.human import Human

class DetectionService:
    @staticmethod
    def is_detected(guard: Guard, zookeeper: Zookeeper) -> bool:
        if not zookeeper.stealth and guard.pos.distance_to(zookeeper.pos) < guard.vision_range:
            return True
        for human in zookeeper.humans:
            if not human.stealth and guard.pos.distance_to(human.pos) < guard.vision_range:
                return True
        return False