import pygame
import time
from store import Store
from utils import Button

class GameGUI:
    def __init__(self, screen, player, game_state):
        self.screen = screen
        self.player = player
        self.game_state = game_state
        self.store = Store()
        self.store_tab = "recovery"
        self.in_store = False
        self.font = pygame.font.SysFont(None, 24)
        self.large_font = pygame.font.SysFont(None, 32)
        self.buttons = []
        self.message = ""
        self.game = None  # Set externally to switch screens

    def draw(self):
        self.screen.fill((30, 30, 30))
        if self.in_store:
            self.draw_store()
        else:
            self.draw_gym()

    def draw_gym(self):
        x, y = 30, 30
        stats = [
            f"Path: {self.player.path}",
            f"Reps: {self.player.reps}",
            f"Total Owned Weight: {self.player.total_weight} lbs",
            f"Barbell Weight: {self.player.barbell_weight} lbs",
            f"Bucks: ${self.player.strength_bucks}",
            f"Cooldown: {round(self.player.get_current_rest_time(), 1)}s",
            f"💰 Bonus per rep: ${self.player.extra_bucks_per_rep}",
            f"Message: {self.message}"
        ]
        for line in stats:
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (x, y))
            y += 28

        self.buttons = []

        cooldown = self.player.get_current_rest_time()
        elapsed = time.time() - self.game_state.last_rep_time
        fill_ratio = min(elapsed / cooldown, 1.0)
        btn_rect = pygame.Rect(100, y + 20, 200, 50)

        rep_btn = Button(btn_rect.x, btn_rect.y, btn_rect.width, btn_rect.height, self.font, "Do Rep", self.do_rep)
        rep_btn.update_cooldown(fill_ratio)
        self.buttons.append(rep_btn)

        self.buttons.append(Button(320, y + 20, 150, 50, self.font, "Open Store", self.go_to_store))
        self.buttons.append(Button(100, y + 90, 100, 40, self.font, "- Weight", self.remove_weight,
                                   disabled=self.player.barbell_weight <= 45))
        self.buttons.append(Button(220, y + 90, 100, 40, self.font, "+ Weight", self.add_weight,
                                   disabled=self.player.barbell_weight >= self.player.total_weight))

        # Save and Exit buttons only (Load removed)
        self.buttons.append(Button(50, y + 140, 100, 40, self.font, "Save Game", self.save_game))
        self.buttons.append(Button(160, y + 140, 150, 40, self.font, "Exit to Menu", self.exit_to_menu))

        for btn in self.buttons:
            btn.draw(self.screen)

    def draw_store(self):
        # Your existing store drawing code here (unchanged)
        pass

    def set_tab(self, tab):
        self.store_tab = tab
        self.message = ""

    def go_to_store(self):
        self.in_store = True
        self.message = ""

    def go_to_gym(self):
        self.in_store = False
        self.message = ""

    def do_rep(self):
        self.message = self.game_state.perform_rep()

    def add_weight(self):
        if self.player.barbell_weight + 5 <= self.player.total_weight:
            self.player.barbell_weight += 5
            self.message = ""
        else:
            self.message = "❌ Not enough weight owned."

    def remove_weight(self):
        if self.player.barbell_weight > 45:
            self.player.barbell_weight -= 5
            self.message = ""
        else:
            self.message = "❌ Barbell can't go lower."

    def purchase(self, item):
        self.message = item.buy(self.player)

    def save_game(self):
        self.player.save()
        self.message = "Game saved!"

    def exit_to_menu(self):
        self.player.save()
        if self.game:
            self.game.current_screen = self.game.home_screen
        self.message = ""

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)
