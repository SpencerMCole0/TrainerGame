import pygame
from utils import Button

class HomeScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 48)
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        w, h = self.screen.get_size()
        mid_x = w // 2
        start_y = h // 3
        gap = 80
        self.buttons = [
            Button(mid_x - 100, start_y, 200, 50, self.font, "Career Path", self.goto_career_path),
            Button(mid_x - 100, start_y + gap, 200, 50, self.font, "Load Game", self.load_game),
            Button(mid_x - 100, start_y + 2 * gap, 200, 50, self.font, "Settings", self.goto_settings),
            Button(mid_x - 100, start_y + 3 * gap, 200, 50, self.font, "How to Play", self.goto_how_to_play),
        ]

    def draw(self):
        self.screen.fill((20, 20, 30))
        title = self.font.render("Trainer Game", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)
        for btn in self.buttons:
            btn.draw(self.screen)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def goto_career_path(self):
        self.game.current_screen = self.game.career_path_screen

    def load_game(self):
        self.game.player.load()
        self.game.current_screen = self.game.gui  # Switch to main game GUI

    def goto_settings(self):
        self.game.current_screen = self.game.settings_screen

    def goto_how_to_play(self):
        self.game.current_screen = self.game.how_to_play_screen

# The rest of your screen classes stay the same
# (CareerPathScreen, SettingsScreen, HowToPlayScreen)
