import pygame
import time
from store import Store
from utils import Button

class GameGUI:
    def open_save_slots(self):
        if self.game:
            self.game.current_screen = self.game.save_slots_screen

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
        self.game = None  # Set externally for screen transitions

    def draw(self):
        self.screen.fill((30, 30, 30))
        if self.in_store:
            self.draw_store()
        else:
            self.draw_gym()

    def draw_gym(self):
        x, y = 30, 30
        line_height = 25

        labels = [
            f"Path: {self.player.path}",
            f"Reps: {self.player.reps}",
            f"Total Owned Weight: {round(self.player.total_weight, 1)} kg",
            f"Barbell Weight: {round(self.player.barbell_weight, 1)} kg",
            f"Bucks: ${self.player.strength_bucks}",
            f"Cooldown: {round(self.player.get_current_rest_time(), 1)}s",
            f"🏆 Bonus per rep: ${self.player.bucks_per_rep}",
            f"Message: {self.message}",
        ]

        self.screen.fill((30, 30, 30))  # Clear once

        for label in labels:
            text = self.font.render(label, True, (255, 255, 255))
            self.screen.blit(text, (x, y))
            y += line_height

        self.buttons = []

        btn_y = y + 20
        # Temporarily force all buttons enabled
        self.buttons.append(Button(50, btn_y, 100, 40, self.font, "Do Rep", self.do_rep, disabled=False))
        self.buttons.append(Button(170, btn_y, 100, 40, self.font, "Open Store", self.open_store, disabled=False))
        self.buttons.append(Button(50, btn_y + 50, 100, 40, self.font, "- Weight", self.remove_weight, disabled=False))
        self.buttons.append(Button(170, btn_y + 50, 100, 40, self.font, "+ Weight", self.add_weight, disabled=False))
        self.buttons.append(Button(50, btn_y + 100, 100, 40, self.font, "Save & Exit", self.save_and_exit, disabled=False))
        self.buttons.append(Button(170, btn_y + 100, 100, 40, self.font, "Exit to Menu", self.exit_to_menu, disabled=False))

        for btn in self.buttons:
            btn.draw(self.screen)

        self.draw_barbell(80, btn_y + 160)

    def draw_store(self):
        x, y = 30, 30
        self.screen.blit(self.large_font.render("🏪 Store", True, (255, 255, 0)), (x, y))
        y += 40

        self.buttons = []
        self.buttons.append(Button(x, y, 150, 40, self.font, "🧃 Recovery",
                                callback=lambda: self.set_tab("recovery"),
                                highlight=(self.store_tab == "recovery")))
        self.buttons.append(Button(x + 160, y, 150, 40, self.font, "📢 Sponsorships",
                                callback=lambda: self.set_tab("sponsorship"),
                                highlight=(self.store_tab == "sponsorship")))
        self.buttons.append(Button(x + 320, y, 150, 40, self.font, "🏋️ Weights",
                                callback=lambda: self.set_tab("weights"),
                                highlight=(self.store_tab == "weights")))
        y += 50

        all_items = self.store.get_items()
        grouped = self.store.get_grouped_items()

        if self.store_tab == "recovery":
            keys = grouped[0]
        elif self.store_tab == "sponsorship":
            keys = grouped[1]
        elif self.store_tab == "weights":
            keys = grouped[2]
        else:
            keys = []

        items = [all_items[key] for key in keys]

        self.screen.blit(self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0)), (x, y))
        y += 30

        row_height = 90
        col_width = 180
        padding = 30
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        items_per_row = max(1, (screen_width - 2 * padding) // col_width)
        current_y = y + 10

        for i, item in enumerate(items):
            col = i % items_per_row
            row = i // items_per_row
            item_x = padding + col * col_width
            item_y = current_y + row * row_height

            maxed = item.limit is not None and item.times_bought >= item.limit
            label = "MAXED" if maxed else f"Buy ({item.times_bought}/{item.limit})"
            disabled = not item.can_buy(self.player)[0] or maxed

            self.screen.blit(self.font.render(item.description, True, (255, 255, 255)), (item_x, item_y - 20))
            self.buttons.append(Button(item_x, item_y, 160, 40, self.font, label, lambda i=item: self.purchase(i), disabled=disabled))

        # Position Back to Gym button bottom-right corner
        btn_width = 160
        btn_height = 40
        padding = 20
        back_x = screen_width - btn_width - padding
        back_y = screen_height - btn_height - padding

        self.buttons.append(Button(
            back_x,
            back_y,
            btn_width,
            btn_height,
            self.font,
            "Back to Gym",
            self.go_to_gym,
            color=(255, 100, 100)
        ))

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

    def save_and_exit(self):
    # Instead of immediate save, open SaveSlotsScreen to pick a slot
        if self.game:
            self.game.current_screen = self.game.save_slots_screen
        self.message = ""

    def open_store(self):
        self.change_mode("store")

    def draw_barbell(self, x, y):
        BAR_LENGTH = 300
        BAR_HEIGHT = 20
        BASE_BAR_COLOR = (180, 180, 180)
        COLLAR_COLOR = (120, 120, 120)
        PLATE_COLORS = {
            0.5: (150, 150, 150),
            1: (100, 100, 255),
            2: (255, 255, 100),
            2.5: (255, 165, 0),
            5: (255, 0, 0),
            10: (0, 0, 255),
            15: (0, 255, 0),
            20: (255, 255, 255),
            25: (0, 0, 0)
        }
        PLATE_WIDTH = 15
        PLATE_HEIGHT = 50

        # Draw bar
        pygame.draw.rect(self.screen, BASE_BAR_COLOR, (x, y, BAR_LENGTH, BAR_HEIGHT))

        # Draw collars
        collar_w, collar_h = 40, 60
        pygame.draw.rect(self.screen, COLLAR_COLOR, (x - collar_w, y - 20, collar_w, collar_h))
        pygame.draw.rect(self.screen, COLLAR_COLOR, (x + BAR_LENGTH, y - 20, collar_w, collar_h))

        # Draw plates on left side
        plate_x = x - collar_w
        for weight in sorted(self.player.plates.keys(), reverse=True):
            count = self.player.plates[weight]
            for _ in range(count):
                plate_x -= PLATE_WIDTH
                color = PLATE_COLORS.get(weight, (100, 100, 100))
                pygame.draw.rect(self.screen, color, (plate_x, y - (PLATE_HEIGHT - BAR_HEIGHT) // 2, PLATE_WIDTH, PLATE_HEIGHT))

        # Draw plates on right side
        plate_x = x + BAR_LENGTH + collar_w
        for weight in sorted(self.player.plates.keys(), reverse=True):
            count = self.player.plates[weight]
            for _ in range(count):
                color = PLATE_COLORS.get(weight, (100, 100, 100))
                pygame.draw.rect(self.screen, color, (plate_x, y - (PLATE_HEIGHT - BAR_HEIGHT) // 2, PLATE_WIDTH, PLATE_HEIGHT))
                plate_x += PLATE_WIDTH