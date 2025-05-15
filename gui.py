import pygame
import time
from store import Store
from utils import Button

class GameGUI:
    def __init__(self, screen, player, game_state):
        self.screen = screen
        self.player = player
        self.game_state = game_state
        self.font = pygame.font.SysFont(None, 24)
        self.large_font = pygame.font.SysFont(None, 32)
        self.message = ""
        self.mode = "gym"  # gym or store
        self.store_tab = "recovery"  # recovery, sponsorships, weights
        self.buttons = []

    def draw(self):
        self.screen.fill((30, 30, 30))
        if self.mode == "gym":
            self.draw_gym()
        elif self.mode == "store":
            self.draw_store()

    def draw_gym(self):
        x, y = 30, 30
        line_height = 25
        labels = [
            f"Path: {self.player.path}",
            f"Reps: {self.player.reps}",
            f"Total Owned Weight: {self.player.total_weight} lbs",
            f"Barbell Weight: {self.player.barbell_weight} lbs",
            f"Bucks: ${self.player.strength_bucks}",
            f"Cooldown: {round(self.player.get_current_cooldown(), 1)}s",
            f"💪 Bonus per rep: ${self.player.bonus_per_rep}",
            f"Message: {self.message}",
        ]
        for label in labels:
            self.screen.blit(self.font.render(label, True, (255, 255, 255)), (x, y))
            y += line_height

        self.buttons = []
        # Do Rep button with cooldown fill
        rep_btn_text = "Do Rep"
        rep_btn_rect = pygame.Rect(50, y + 40, 200, 40)
        elapsed = time.time() - self.player.last_rep_time
        cooldown = self.player.get_current_cooldown()
        fill_ratio = min(elapsed / cooldown, 1.0)
        fill_width = int(rep_btn_rect.width * fill_ratio)
        pygame.draw.rect(self.screen, (0, 255, 0) if fill_ratio >= 1 else (100, 100, 100), rep_btn_rect)
        pygame.draw.rect(self.screen, (0, 200, 0), (rep_btn_rect.x, rep_btn_rect.y, fill_width, rep_btn_rect.height))
        rep_text_surface = self.font.render(rep_btn_text, True, (0, 0, 0))
        rep_text_rect = rep_text_surface.get_rect(center=rep_btn_rect.center)
        self.screen.blit(rep_text_surface, rep_text_rect)
        self.buttons.append(Button(rep_btn_rect.x, rep_btn_rect.y, rep_btn_rect.width, rep_btn_rect.height, self.font, "Do Rep", self.do_rep))

        # Open Store button
        self.buttons.append(Button(270, y + 40, 150, 40, self.font, "Open Store", self.open_store))
        self.buttons.append(Button(50, y + 90, 90, 40, self.font, "- Weight", self.remove_weight))
        self.buttons.append(Button(150, y + 90, 90, 40, self.font, "+ Weight", self.add_weight))

    def draw_store(self):
        # placeholder safe rendering for store screen
        pass

    def do_rep(self):
        self.message = self.game_state.perform_rep()

    def open_store(self):
        self.mode = "store"

    def remove_weight(self):
        self.message = self.game_state.remove_weight()

    def add_weight(self):
        self.message = self.game_state.add_weight()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttons:
                btn.handle_event(event)
