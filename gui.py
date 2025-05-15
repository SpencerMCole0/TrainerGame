import pygame
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
        self.buttons = []
        self.font = pygame.font.SysFont(None, 24)
        self.large_font = pygame.font.SysFont(None, 32)
        self.message = ""

    def draw(self):
        self.screen.fill((30, 30, 30))
        if self.in_store:
            self.draw_store()
        else:
            self.draw_gym()

    def draw_gym(self):
        x, y = 30, 30
        line_height = 25
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
            y += line_height

        # Draw Do Rep button with cooldown fill
        rep_btn_rect = pygame.Rect(100, y + 40, 200, 50)
        can_rep = self.game_state.can_rep()
        cooldown_time = self.player.get_current_rest_time()
        time_since_last = pygame.time.get_ticks() / 1000 - self.game_state.last_rep_time
        fill_ratio = min(time_since_last / cooldown_time, 1.0)

        # Background gray
        pygame.draw.rect(self.screen, (100, 100, 100), rep_btn_rect)
        # Filled progress
        if not can_rep:
            fill_width = int(rep_btn_rect.width * fill_ratio)
            fill_rect = pygame.Rect(rep_btn_rect.x, rep_btn_rect.y, fill_width, rep_btn_rect.height)
            pygame.draw.rect(self.screen, (0, 200, 0), fill_rect)
        else:
            pygame.draw.rect(self.screen, (0, 200, 0), rep_btn_rect)

        # Border and label
        pygame.draw.rect(self.screen, (255, 255, 255), rep_btn_rect, 2)
        label = self.font.render("Do Rep", True, (0, 0, 0))
        self.screen.blit(label, label.get_rect(center=rep_btn_rect.center))

        # Other gym buttons
        self.buttons = []
        self.buttons.append(Button(320, y + 40, "Open Store", self.go_to_store))
        self.buttons.append(Button(100, y + 100, "- Weight", self.remove_weight,
                                   disabled=(self.player.barbell_weight <= 45)))
        self.buttons.append(Button(240, y + 100, "+ Weight", self.add_weight,
                                   disabled=(self.player.barbell_weight >= self.player.total_weight)))

        for btn in self.buttons:
            btn.draw(self.screen)

    def draw_store(self):
        x, y = 30, 30
        self.screen.blit(self.large_font.render("🏪 Store", True, (255, 255, 0)), (x, y))
        y += 40

        self.buttons = []

        self.buttons.append(Button(x, y, "🧃 Recovery", lambda: self.set_tab("recovery"),
                                   highlight=(self.store_tab == "recovery")))
        self.buttons.append(Button(x + 150, y, "📢 Sponsorships", lambda: self.set_tab("sponsorship"),
                                   highlight=(self.store_tab == "sponsorship")))
        self.buttons.append(Button(x + 330, y, "🏋️ Weights", lambda: self.set_tab("weights"),
                                   highlight=(self.store_tab == "weights")))

        y += 50
        self.screen.blit(self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0)), (x, y))
        y += 30

        grouped = self.store.get_grouped_items()
        all_items = self.store.get_items()

        if self.store_tab == "recovery":
            keys = grouped[0]
        elif self.store_tab == "sponsorship":
            keys = grouped[1]
        else:
            keys = grouped[2]

        items = [all_items[key] for key in keys]

        padding = 20
        row_height = 90
        col_width = 180
        screen_width = self.screen.get_width()
        current_x = padding
        current_y = y + 20
        items_per_row = max(1, (screen_width - padding * 2) // col_width)

        for i, item in enumerate(items):
            can_afford = item.can_buy(self.player)[0]
            maxed = item.limit is not None and item.times_bought >= item.limit
            label = "MAXED" if maxed else f"Buy ({item.times_bought}/{item.limit})" if item.limit else f"Buy (${item.cost})"
            effect = item.description
            disabled = not can_afford or maxed

            col = i % items_per_row
            row = i // items_per_row
            x = padding + col * col_width
            y = current_y + row * row_height

            self.screen.blit(self.font.render(effect, True, (255, 255, 255)), (x, y - 20))
            self.buttons.append(Button(x, y, label, lambda i=item: self.purchase(i), disabled=disabled))

        # Back button
        self.buttons.append(Button(screen_width // 2 - 60, y + row_height + 10, "Back to Gym", self.go_to_gym, color=(255, 100, 100)))

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
        return_msg = item.buy(self.player)
        self.message = return_msg

    def handle_event(self, event):
        if not self.in_store and event.type == pygame.MOUSEBUTTONDOWN:
            rep_btn_rect = pygame.Rect(100, 255, 200, 50)
            if rep_btn_rect.collidepoint(event.pos) and self.game_state.can_rep():
                self.do_rep()

        for btn in self.buttons:
            btn.handle_event(event)
