import pygame
import sys
from player import Player
from game_state import GameState
from gui import GameGUI
from utils import Button

# Import your screen classes
from screens import HomeScreen, CareerPathScreen, SettingsScreen, HowToPlayScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Trainer Game")

    # Initialize player, game state, and main GUI
    player = Player("No Path")
    game_state = GameState(player)
    gui = GameGUI(screen, player, game_state)

    # Create screen instances
    home_screen = HomeScreen(screen, None)
    career_path_screen = CareerPathScreen(screen, None)
    settings_screen = SettingsScreen(screen, None)
    how_to_play_screen = HowToPlayScreen(screen, None)

    # Create a dummy game object to hold shared state and screen references
    class GameContext:
        pass

    game = GameContext()
    game.player = player
    game.game_state = game_state
    game.gui = gui
    game.home_screen = home_screen
    game.career_path_screen = career_path_screen
    game.settings_screen = settings_screen
    game.how_to_play_screen = how_to_play_screen
    game.current_screen = home_screen

    # Assign game context to each screen for navigation and shared state
    home_screen.game = game
    career_path_screen.game = game
    settings_screen.game = game
    how_to_play_screen.game = game
    gui.game = game  # if needed in gui

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.current_screen.handle_event(event)

        game.current_screen.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
