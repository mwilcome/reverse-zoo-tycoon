import pygame
from domain.entities.human import Human

class GrokUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def update(self, caught: bool, humans: list[Human]):
        screen = pygame.display.get_surface()
        if caught:
            text = self.font.render("Caught! Zoo wins!", True, (255, 255, 255))
        elif any(h.state == "following" for h in humans):
            text = self.font.render("Lead those humans to freedom!", True, (255, 255, 255))
        else:
            text = self.font.render("Sneak those humans out!", True, (255, 255, 255))
        screen.blit(text, (10, 10))