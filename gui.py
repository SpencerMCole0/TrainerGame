import pygame
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
        self.mode = "gym"
        self.store_tab = "recovery"
        self.buttons = []
        self.store = Store()

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
            f"Cooldown: {round(self.player.base_rest_time, 1)}s",
            f"Message: {self.message}"
        ]
        for label in labels:
            self.screen.blit(self.font.render(label, True, (255, 255, 255)), (x, y))
            y += line_height

        self.buttons = []
        self.buttons.append(Button(50, y + 40, "Do Rep", self.do_rep))
        self.buttons.append(Button(170, y + 40, "Open Store", self.go_to_store))
        self.buttons.append(Button(50, y + 80, "- Weight", self.remove_weight,
                                   disabled=(self.player.barbell_weight <= 45)))
        self.buttons.append(Button(170, y + 80, "+ Weight", self.add_weight,
                                   disabled=(self.player.barbell_weight >= self.player.total_weight)))

        for btn in self.buttons:
            btn.draw(self.screen)

    def draw_store(self):
        x, y = 30, 30
        self.screen.blit(self.large_font.render("🟨 Store", True, (255, 255, 0)), (x, y))
        y += 40

        self.buttons = []
        self.buttons.append(Button(x, y, "🧃 Recovery", lambda: self.set_tab("recovery"),
                                   highlight=(self.store_tab == "recovery")))
        self.buttons.append(Button(x + 150, y, "📢 Sponsorships", lambda: self.set_tab("sponsorship"),
                                   highlight=(self.store_tab == "sponsorship")))
        self.buttons.append(Button(x + 320, y, "🏋️ Weights", lambda: self.set_tab("weights"),
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

        for item in items:
            self.screen.blit(self.font.render(f"{item.name} - ${item.cost}", True, (255, 255, 255)), (x, y))
            self.screen.blit(self.font.render(item.description, True, (180, 180, 180)), (x + 10, y + 22))
            y += 50

        self.screen.blit(self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0)), (x, y))
        y += 25

        if self.message:
            self.screen.blit(self.font.render(self.message, True, (255, 255, 255)), (x, y))
            y += 30

        screen_width = self.screen.get_width()
        current_x = 20
        current_y = y + 30
        row_height = 50
        padding = 15

        for item in items:
            label = f"Buy {item.name} (${item.cost})"
            text_width = self.font.size(label)[0] + 20
            can_afford = item.can_buy(self.player)[0]
            disabled = not can_afford

            if current_x + text_width > screen_width - padding:
                current_x = padding
                current_y += row_height + 10

            self.buttons.append(Button(current_x, current_y, label,
                                       lambda i=item: self.purchase(i),
                                       disabled=disabled))
            current_x += text_width + 10

        self.buttons.append(Button(screen_width // 2 - 60, current_y + row_height + 20, "Back to Gym", self.go_to_gym, color=(255, 100, 100)))

        for btn in self.buttons:
            btn.draw(self.screen)

    def set_tab(self, tab):
        self.store_tab = tab
        self.message = ""

    def go_to_store(self):
        self.mode = "store"
        self.message = ""

    def go_to_gym(self):
        self.mode = "gym"
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
        for btn in self.buttons:
            btn.handle_event(event)
