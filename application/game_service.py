from domain.aggregates.zoo_escape import ZooEscape
from infrastructure.pygame_renderer import PygameRenderer
from infrastructure.input_handler import InputHandler
from ui.grok_ui import GrokUI

class GameService:
    def __init__(self):
        self.zoo = ZooEscape()
        self.renderer = PygameRenderer()
        self.input_handler = InputHandler()
        self.ui = GrokUI()

    def run(self):
        running = True
        while running:
            running = self.input_handler.handle_input(self.zoo)
            self.zoo.update()
            caught = self.zoo.is_caught()
            won = self.zoo.is_won()
            self.renderer.render(self.zoo, caught)
            self.ui.update(caught, self.zoo.zookeeper.humans)
            if caught:
                print("Game Over! You were caught.")
                running = False
            elif won:
                print("You win! All humans escaped.")
                running = False