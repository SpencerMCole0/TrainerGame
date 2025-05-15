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

        # Do Rep button with fill cooldown
        btn_rect = pygame.Rect(100, y + 20, 200, 50)
        cooldown = self.player.get_current_rest_time()
        elapsed = time.time() - self.game_state.last_rep_time
        fill_ratio = min(elapsed / cooldown, 1.0)
        fill_width = int(btn_rect.width * fill_ratio)

        # background + cooldown fill
        pygame.draw.rect(self.screen, (100, 100, 100), btn_rect)
        if fill_ratio < 1.0:
            pygame.draw.rect(self.screen, (0, 200, 0), (btn_rect.x, btn_rect.y, fill_width, btn_rect.height))
        else:
            pygame.draw.rect(self.screen, (0, 255, 0), btn_rect)

        pygame.draw.rect(self.screen, (255, 255, 255), btn_rect, 2)
        label = self.font.render("Do Rep", True, (0, 0, 0))
        self.screen.blit(label, label.get_rect(center=btn_rect.center))

        if fill_ratio >= 1.0:
            self.buttons.append(Button(btn_rect.x, btn_rect.y, btn_rect.width, btn_rect.height, self.font, "Do Rep", self.do_rep))

        # Open Store button
        self.buttons.append(Button(320, y + 20, 150, 50, self.font, "Open Store", self.go_to_store))

        # Weight buttons
        self.buttons.append(Button(100, y + 90, 100, 40, self.font, "- Weight", self.remove_weight,
                                   disabled=self.player.barbell_weight <= 45))
        self.buttons.append(Button(220, y + 90, 100, 40, self.font, "+ Weight", self.add_weight,
                                   disabled=self.player.barbell_weight >= self.player.total_weight))

        for btn in self.buttons:
            btn.draw(self.screen)

    def draw_store(self):
        x, y = 30, 30
        self.screen.blit(self.large_font.render("🏪 Store", True, (255, 255, 0)), (x, y))
        y += 40

        self.buttons = []
        self.buttons.append(Button(x, y, "🧃 Recovery", lambda: self.set_tab("recovery"),
                                   highlight=(self.store_tab == "recovery")))
        self.buttons.append(Button(x + 160, y, "📢 Sponsorships", lambda: self.set_tab("sponsorship"),
                                   highlight=(self.store_tab == "sponsorship")))
        self.buttons.append(Button(x + 340, y, "🏋️ Weights", lambda: self.set_tab("weights"),
                                   highlight=(self.store_tab == "weights")))
        y += 50

        grouped = self.store.get_grouped_items()
        all_items = self.store.get_items()

        if self.store_tab == "recovery":
            keys = grouped[0]
        elif self.store_tab == "sponsorship":
            keys = grouped[1]
        else:
            keys = grouped[2]

        items = [all_items[key] for key in keys]

        self.screen.blit(self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0)), (x, y))
        y += 30

        row_height = 90
        col_width = 180
        padding = 30
        screen_width = self.screen.get_width()
        items_per_row = max(1, (screen_width - 2 * padding) // col_width)
        current_y = y + 10

        for i, item in enumerate(items):
            col = i % items_per_row
            row = i // items_per_row
            x = padding + col * col_width
            y = current_y + row * row_height

            maxed = item.limit is not None and item.times_bought >= item.limit
            label = "MAXED" if maxed else f"Buy ({item.times_bought}/{item.limit})"
            disabled = not item.can_buy(self.player)[0] or maxed

            self.screen.blit(self.font.render(item.description, True, (255, 255, 255)), (x, y - 20))
            self.buttons.append(Button(x, y, 160, 40, self.font, label, lambda i=item: self.purchase(i), disabled=disabled))

        self.buttons.append(Button(screen_width // 2 - 80, y + row_height + 20, 160, 40, self.font,
                                   "Back to Gym", self.go_to_gym, color=(255, 100, 100)))

        for btn in self.buttons:
            btn.draw(self.screen)

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

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)
