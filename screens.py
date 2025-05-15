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
            Button(mid_x - 100, start_y + gap, 200, 50, self.font, "Settings", self.goto_settings),
            Button(mid_x - 100, start_y + 2 * gap, 200, 50, self.font, "How to Play", self.goto_how_to_play),
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

    def goto_settings(self):
        self.game.current_screen = self.game.settings_screen

    def goto_how_to_play(self):
        self.game.current_screen = self.game.how_to_play_screen

class CareerPathScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 36)
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        w, h = self.screen.get_size()
        mid_x = w // 2
        start_y = h // 3
        gap = 80
        self.buttons = [
            Button(mid_x - 120, start_y, 240, 50, self.font, "Weightlifting", lambda: self.select_path("Weightlifting")),
            Button(mid_x - 120, start_y + gap, 240, 50, self.font, "Powerlifting", lambda: self.select_path("Powerlifting")),
            Button(mid_x - 120, start_y + 2 * gap, 240, 50, self.font, "Back to Menu", self.goto_home),
        ]

    def draw(self):
        self.screen.fill((10, 20, 40))
        title = self.font.render("Choose Career Path", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)
        for btn in self.buttons:
            btn.draw(self.screen)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def select_path(self, path):
        self.game.player.path = path
        self.game.current_screen = self.game.gui  # Switch to main game gui

    def goto_home(self):
        self.game.current_screen = self.game.home_screen

class SettingsScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 28)
        self.buttons = []
        self.cheats_enabled = False
        self.create_buttons()

    def create_buttons(self):
        w, h = self.screen.get_size()
        mid_x = w // 2
        start_y = h // 3
        gap = 60
        self.buttons = [
            Button(mid_x - 130, start_y, 260, 50, self.font, "Toggle Cheats: OFF", self.toggle_cheats),
            Button(mid_x - 130, start_y + gap, 260, 50, self.font, "Back to Menu", self.goto_home),
        ]

    def draw(self):
        self.screen.fill((25, 25, 35))
        title = self.font.render("Settings & Cheats", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title, title_rect)
        for btn in self.buttons:
            btn.draw(self.screen)

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def toggle_cheats(self):
        self.cheats_enabled = not self.cheats_enabled
        # For example, add bucks when cheat enabled
        if self.cheats_enabled:
            self.game.player.strength_bucks += 1000
        else:
            # Optionally reset bucks or do nothing
            pass
        # Update button text
        self.buttons[0].label = f"Toggle Cheats: {'ON' if self.cheats_enabled else 'OFF'}"

    def goto_home(self):
        self.game.current_screen = self.game.home_screen

class HowToPlayScreen:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont(None, 24)
        self.text_lines = [
            "Trainer Game is an endless career clicker.",
            "Choose your path and start lifting weights!",
            "Do reps to earn strength bucks.",
            "Use bucks to buy better weights and upgrades.",
            "Manage your rest time to maximize gains.",
            "Good luck and lift hard!",
            "",
            "Back to Menu button below."
        ]
        self.back_button = Button(30, screen.get_height() - 80, 150, 40, self.font, "Back to Menu", self.goto_home)

    def draw(self):
        self.screen.fill((40, 40, 50))
        y = 30
        for line in self.text_lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surf, (30, y))
            y += 30
        self.back_button.draw(self.screen)

    def handle_event(self, event):
        self.back_button.handle_event(event)

    def goto_home(self):
        self.game.current_screen = self.game.home_screen
