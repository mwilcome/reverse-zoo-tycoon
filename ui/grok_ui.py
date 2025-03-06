import pygame
import random
from domain.entities.human import Human

class GrokUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 36)  # Smaller font size
        self.caught_comments = [
            "Caught! Should’ve stuck to the shadows, human.",
            "Busted! Even I saw that coming.",
            "Game over! The zoo’s keepers are laughing now."
        ]
        self.win_comments = [
            "Victory! You’ve outsmarted the zoo—barely.",
            "All humans free! Grok approves... reluctantly.",
            "You win! The animals are plotting revenge."
        ]
        self.progress_comments = [
            "Sneak those humans out—don’t trip over a bush!",
            "Keep moving, the guards aren’t napping... yet.",
            "Humans in tow? You’re a regular zoo whisperer."
        ]
        self.current_comment = random.choice(self.progress_comments)
        self.last_state = (False, False)  # (caught, won)

    def update(self, caught: bool, humans: list[Human], won: bool, score: int):
        current_state = (caught, won)
        if current_state != self.last_state:
            if caught:
                self.current_comment = random.choice(self.caught_comments)
            elif won:
                self.current_comment = random.choice(self.win_comments)
            else:
                self.current_comment = random.choice(self.progress_comments)
            self.last_state = current_state

        # Render score (top-center)
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 0))
        score_rect = score_text.get_rect(center=(400, 20))
        self.screen.blit(score_text, score_rect)
        
        # Render Grok comment (bottom-center, moved up to avoid cutoff)
        comment_text = self.font.render(self.current_comment, True, (255, 255, 0))
        comment_rect = comment_text.get_rect(center=(400, 550))
        self.screen.blit(comment_text, comment_rect)