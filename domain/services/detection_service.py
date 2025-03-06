import math
from domain.entities.guard import Guard
from domain.entities.zookeeper import Zookeeper

class DetectionService:
    @staticmethod
    def is_detected(guard: Guard, zookeeper: Zookeeper) -> bool:
        def check_target(target_pos, is_stealth):
            if is_stealth:
                return False
            if guard.vision_type == "radial":
                return guard.pos.distance_to(target_pos) < guard.vision_range
            elif guard.vision_type == "cone":
                dx = target_pos.x - guard.pos.x
                dy = target_pos.y - guard.pos.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance >= guard.vision_range:
                    return False
                target_angle = math.degrees(math.atan2(dy, dx))
                facing_angle = guard.get_facing_angle()
                angle_diff = (target_angle - facing_angle + 180) % 360 - 180
                return abs(angle_diff) <= 30  # Within ±30° (60° cone)

        if check_target(zookeeper.pos, zookeeper.stealth):
            return True
        for human in zookeeper.humans:
            if check_target(human.pos, human.stealth):
                return True
        return False