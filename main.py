import pygame
import sys
from player import Player
from game_state import GameState
from gui import GameGUI
from utils import Button

# Import your new screens (adjust path if needed)
from screens import HomeScreen, CareerPathScreen, SettingsScreen, HowToPlayScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Trainer Game")

    # Initialize player, game state, GUI
    player = Player("No Path")
    game_state = GameState(player)
    gui = GameGUI(screen, player, game_state)

    # Instantiate screens
    home_screen = HomeScreen(screen, None)  # pass None first, will update below
    career_path_screen = CareerPathScreen(screen, None)
    settings_screen = SettingsScreen(screen, None)
    how_to_play_screen = HowToPlayScreen(screen, None)

    # Reference back to game for screens
    home_screen.game = career_path_screen.game = settings_screen.game = how_to_play_screen.game = type('', (), {})()
    home_screen.game.player = player
    home_screen.game.current_screen = home_screen
    home_screen.game.career_path_screen = career_path_screen
    home_screen.game.settings_screen = settings_screen
    home_screen.game.how_to_play_screen = how_to_play_screen
    home_screen.game.gui = gui

    current_screen = home_screen
    home_screen.game.current_screen = current_screen

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            current_screen.handle_event(event)

        current_screen = home_screen.game.current_screen  # update current screen pointer
        current_screen.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
