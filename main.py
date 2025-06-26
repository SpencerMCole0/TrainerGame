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

    # Grab full monitor size for fullscreen mode
    info = pygame.display.Info()
    max_w, max_h = info.current_w, info.current_h
    windowed_size = (1024, 768)
    fullscreen = False

    # Start windowed/resizable
    screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)
    pygame.display.set_caption("Trainer Game")

    # Core game objects
    player     = Player("No Path")
    game_state = GameState(player)
    gui        = GameGUI(screen, player, game_state)

    # Screens
    home_screen         = HomeScreen(screen, None)
    career_path_screen  = CareerPathScreen(screen, None)
    settings_screen     = SettingsScreen(screen, None)
    how_to_play_screen  = HowToPlayScreen(screen, None)
    save_slots_screen   = SaveSlotsScreen(screen, None)
    load_slots_screen   = LoadSlotsScreen(screen, None)

    # Keep a list for easy bulk updates
    all_screens = [
        home_screen, career_path_screen, settings_screen,
        how_to_play_screen, save_slots_screen, load_slots_screen
    ]

    # Game context to hold shared state
    class GameContext:
        def __init__(self):
            self._current_screen = None

        @property
        def current_screen(self):
            return self._current_screen

        @current_screen.setter
        def current_screen(self, screen_obj):
            self._current_screen = screen_obj
            if hasattr(screen_obj, "on_show") and getattr(screen_obj, "game", None):
                screen_obj.on_show()

    game = GameContext()
    game.player        = player
    game.game_state    = game_state
    game.gui           = gui
    game.home_screen         = home_screen
    game.career_path_screen  = career_path_screen
    game.settings_screen     = settings_screen
    game.how_to_play_screen  = how_to_play_screen
    game.save_slots_screen   = save_slots_screen
    game.load_slots_screen   = load_slots_screen
    game.current_screen      = home_screen

    # Hook up game reference in all screens and GUI
    for scr in all_screens:
        scr.game = game
    gui.game = game

    clock = pygame.time.Clock()

    # Define fullscreen toggle logic
    def toggle_fullscreen():
        nonlocal fullscreen, screen
        fullscreen = not fullscreen
        if fullscreen:
            screen = pygame.display.set_mode((max_w, max_h), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)
        # Propagate new surface
        gui.screen = screen
        for scr in all_screens:
            scr.screen = screen
        # Refresh the SettingsScreen buttons to update the label
        settings_screen.create_buttons()

    # Attach it to the game context
    game.toggle_fullscreen = toggle_fullscreen

    # Monkey‐patch SettingsScreen to insert our Toggle button
    original_create = settings_screen.create_buttons
    def create_with_fullscreen_toggle():
        original_create()  # build its normal buttons
        w, h = settings_screen.screen.get_size()
        mid_x    = w // 2
        start_y  = h // 3
        gap      = 60
        label    = f"Fullscreen: {'ON' if fullscreen else 'OFF'}"
        btn = Button(
            mid_x - 100,
            start_y + gap * 2,
            200, 40,
            settings_screen.font,
            label,
            callback=toggle_fullscreen
        )
        # insert it just before the "Back" button
        # (assumes Back is the last in settings_screen.buttons)
        settings_screen.buttons.insert(-1, btn)

    settings_screen.create_buttons = create_with_fullscreen_toggle
    settings_screen.create_buttons()  # build them now

    # Main loop
    while True:
        for event in pygame.event.get():
            # F11 = fullscreen toggle
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                toggle_fullscreen()

            # window resize (only when not fullscreen)
            elif event.type == pygame.VIDEORESIZE and not fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                gui.screen = screen
                for scr in all_screens:
                    scr.screen = screen

            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            game.current_screen.handle_event(event)

        game.current_screen.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
