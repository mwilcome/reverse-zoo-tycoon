import pygame
from domain.aggregates.zoo_escape import ZooEscape
from infrastructure.map_generator import MapGenerator

class PygameRenderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Reverse Zoo Tycoon - Grok Edition")
        self.clock = pygame.time.Clock()
        self.camera_x, self.camera_y = 0, 0

    def render(self, zoo: ZooEscape, caught: bool):
        self.screen.fill((0, 0, 0))
        self.camera_x = max(0, min(zoo.zookeeper.pos.x - 400, MapGenerator.WIDTH * MapGenerator.TILE_SIZE - 800))
        self.camera_y = max(0, min(zoo.zookeeper.pos.y - 300, MapGenerator.HEIGHT * MapGenerator.TILE_SIZE - 600))

        for tile in zoo.map:
            x, y = tile.pos.x - self.camera_x, tile.pos.y - self.camera_y
            if -MapGenerator.TILE_SIZE <= x < 800 and -MapGenerator.TILE_SIZE <= y < 600:
                if tile.type == "wall":
                    pygame.draw.rect(self.screen, (100, 100, 100), (x, y, MapGenerator.TILE_SIZE, MapGenerator.TILE_SIZE))
                elif tile.type == "bush":
                    pygame.draw.rect(self.screen, (0, 100, 0), (x, y, MapGenerator.TILE_SIZE, MapGenerator.TILE_SIZE))
                elif tile.type == "cage" and not any(h.state == "caged" and h.pos == tile.pos for h in zoo.humans):
                    pygame.draw.rect(self.screen, (150, 150, 150), (x, y, MapGenerator.TILE_SIZE, MapGenerator.TILE_SIZE))

        for ep in zoo.escape_points:
            x, y = ep.pos.x - self.camera_x, ep.pos.y - self.camera_y
            pygame.draw.circle(self.screen, (0, 255, 255), (int(x + MapGenerator.TILE_SIZE / 2), int(y + MapGenerator.TILE_SIZE / 2)), 10)

        color = (0, 0, 100) if zoo.zookeeper.stealth else (0, 0, 255)
        pygame.draw.rect(self.screen, color, (zoo.zookeeper.pos.x - self.camera_x, zoo.zookeeper.pos.y - self.camera_y, 20, 20))  # Smaller player
        for human in zoo.humans:
            color = (255, 0, 0) if human.state == "caged" else (0, 255, 0)
            pygame.draw.rect(self.screen, color, (human.pos.x - self.camera_x, human.pos.y - self.camera_y, 15, 15))  # Smaller humans
        for guard in zoo.guards:
            pygame.draw.rect(self.screen, (255, 165, 0), (guard.pos.x - self.camera_x, guard.pos.y - self.camera_y, 30, 30))  # Smaller guard

        pygame.display.flip()
        self.clock.tick(60)

    def quit(self):
        pygame.quit()