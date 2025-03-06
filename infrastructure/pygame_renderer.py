import pygame
from domain.aggregates.zoo_escape import ZooEscape

class PygameRenderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Reverse Zoo Tycoon - Grok Edition")
        self.clock = pygame.time.Clock()

    def render(self, zoo: ZooEscape, caught: bool):
        self.screen.fill((0, 0, 0))  # Black background
        # Zookeeper
        color = (0, 0, 100) if zoo.zookeeper.stealth else (0, 0, 255)
        pygame.draw.rect(self.screen, color, (zoo.zookeeper.pos.x, zoo.zookeeper.pos.y, 30, 30))
        # Humans
        for human in zoo.humans:
            color = (255, 0, 0) if human.state == "caged" else (0, 255, 0)
            pygame.draw.rect(self.screen, color, (human.pos.x, human.pos.y, 20, 20))
        # Guards
        for guard in zoo.guards:
            pygame.draw.rect(self.screen, (255, 165, 0), (guard.pos.x, guard.pos.y, 40, 50))
        # Escape Points
        for ep in zoo.escape_points:
            pygame.draw.circle(self.screen, (0, 255, 255), (int(ep.pos.x), int(ep.pos.y)), 20)
        pygame.display.flip()
        self.clock.tick(60)

    def quit(self):
        pygame.quit()