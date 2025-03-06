from domain.entities.zookeeper import Zookeeper

class StealthService:
    @staticmethod
    def toggle_stealth(zookeeper: Zookeeper):
        zookeeper.stealth = not zookeeper.stealth
        for human in zookeeper.humans:
            human.stealth = zookeeper.stealth