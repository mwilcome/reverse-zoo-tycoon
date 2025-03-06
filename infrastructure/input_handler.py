import pygame
from domain.aggregates.zoo_escape import ZooEscape
from domain.services.stealth_service import StealthService

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
                        zoo.escape_human(human)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: zoo.zookeeper.pos.x -= 4
        if keys[pygame.K_RIGHT]: zoo.zookeeper.pos.x += 4
        if keys[pygame.K_UP]: zoo.zookeeper.pos.y -= 4
        if keys[pygame.K_DOWN]: zoo.zookeeper.pos.y += 4
        return True