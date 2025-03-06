import pygame
from domain.aggregates.zoo_escape import ZooEscape
from domain.services.stealth_service import StealthService
from domain.entities.position import Position

class InputHandler:
    def handle_input(self, zoo: ZooEscape) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    StealthService.toggle_stealth(zoo.zookeeper)
                if event.key == pygame.K_e:
                    for human in zoo.humans:
                        zoo.free_human(human)
                    for human in zoo.humans:
                        zoo.escape_human(human)
        keys = pygame.key.get_pressed()
        new_pos = Position(zoo.zookeeper.pos.x, zoo.zookeeper.pos.y)
        if keys[pygame.K_a]: new_pos.x -= 4  # Left
        if keys[pygame.K_d]: new_pos.x += 4  # Right
        if keys[pygame.K_w]: new_pos.y -= 4  # Up
        if keys[pygame.K_s]: new_pos.y += 4  # Down
        if not zoo.check_collision(new_pos):
            zoo.zookeeper.pos = new_pos
        # Clamp player position to map boundaries
        zoo.zookeeper.pos.x = max(0, min(zoo.zookeeper.pos.x, zoo.map_width - zoo.player_width))
        zoo.zookeeper.pos.y = max(0, min(zoo.zookeeper.pos.y, zoo.map_height - zoo.player_height))
        return True