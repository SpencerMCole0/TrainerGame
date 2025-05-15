import pygame
from store import store_items
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
        self.store_tab = "recovery"  # or 'training'
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

        # Tabs
        self.buttons = []
        self.buttons.append(Button(x, y, "🟩 Recovery", lambda: self.set_tab("recovery"),
                                   highlight=(self.store_tab == "recovery")))
        self.buttons.append(Button(x + 130, y, "☑ Training", lambda: self.set_tab("training"),
                                   highlight=(self.store_tab == "training")))
        y += 50

        # Filter items by tab
        items = [item for item in store_items if item["category"] == self.store_tab]

        # Draw item descriptions
        for item in items:
            lines = item["description"].split("\n")
            self.screen.blit(self.font.render(f"{item['name']} - ${item['cost']}", True, (255, 255, 255)), (x, y))
            y += 22
            for line in lines:
                self.screen.blit(self.font.render(line, True, (180, 180, 180)), (x + 10, y))
                y += 20
            y += 5

        # Your bucks
        self.screen.blit(self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0)), (x, y))
        y += 25

        # Message
        if self.message:
            self.screen.blit(self.font.render(self.message, True, (255, 255, 255)), (x, y))
            y += 30

        # Calculate layout
        padding = 15
        screen_width = self.screen.get_width()
        current_x = padding
        current_y = y + 30
        max_button_height = 40
        row_height = max_button_height + 10

        for item in items:
            text = f"Buy {item['name']} (${item['cost']})"
            text_width = self.font.size(text)[0] + 20
            disabled = not item["available"](self.player)
            if current_x + text_width > screen_width - padding:
                current_x = padding
                current_y += row_height
            self.buttons.append(Button(current_x, current_y, text, lambda i=item: self.purchase(i), disabled=disabled))
            current_x += text_width + 10

        # Back button (its own row, red)
        back_y = current_y + row_height
        self.buttons.append(Button(screen_width // 2 - 60, back_y, "Back to Gym", self.go_to_gym, color=(255, 100, 100)))

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
        success, msg = item["on_purchase"](self.player)
        self.message = msg

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)
