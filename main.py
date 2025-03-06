from application.game_service import GameService

if __name__ == "__main__":
    game = GameService()
    game.run()
    game.renderer.quit()