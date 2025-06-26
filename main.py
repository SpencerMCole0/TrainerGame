import pygame
import sys
from player import Player
from game_state import GameState
from gui import GameGUI
from utils import Button
from screens import HomeScreen, CareerPathScreen, SettingsScreen, HowToPlayScreen
from SaveSlotsScreen import SaveSlotsScreen
from LoadSlotsScreen import LoadSlotsScreen

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    # grab your monitor's current resolution
    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h
    # start window at full resolution, and let user resize
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
    
    while running:
            for event in pygame.event.get():
    +            # if the user drags to resize, update our surface & pass to game
                if event.type == pygame.VIDEORESIZE:
    -                screen = pygame.display.set_mode((event.w, event.h))
    +                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    +                game.screen = screen
                elif event.type == pygame.QUIT:
                    running = False

    pygame.display.set_caption("Trainer Game")

    # Initialize core game objects
    player = Player("No Path")
    game_state = GameState(player)
    gui = GameGUI(screen, player, game_state)

    # Instantiate all screens
    home_screen = HomeScreen(screen, None)
    career_path_screen = CareerPathScreen(screen, None)
    settings_screen = SettingsScreen(screen, None)
    how_to_play_screen = HowToPlayScreen(screen, None)
    save_slots_screen = SaveSlotsScreen(screen, None)
    load_slots_screen = LoadSlotsScreen(screen, None)

    # Game context to hold shared state and screen refs
    class GameContext:
        def __init__(self):
            self._current_screen = None

        @property
        def current_screen(self):
            return self._current_screen

        @current_screen.setter
        def current_screen(self, screen):
            self._current_screen = screen
            # Only call on_show if screen.game is assigned
            if hasattr(screen, "on_show") and getattr(screen, "game", None) is not None:
                screen.on_show()


    game = GameContext()
    game.player = player
    game.game_state = game_state
    game.gui = gui
    game.home_screen = home_screen
    game.career_path_screen = career_path_screen
    game.settings_screen = settings_screen
    game.how_to_play_screen = how_to_play_screen
    game.save_slots_screen = save_slots_screen
    game.load_slots_screen = load_slots_screen
    game.current_screen = home_screen

    # Pass game context to all screens and GUI
    home_screen.game = game
    career_path_screen.game = game
    settings_screen.game = game
    how_to_play_screen.game = game
    save_slots_screen.game = game
    load_slots_screen.game = game
    gui.game = game

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
