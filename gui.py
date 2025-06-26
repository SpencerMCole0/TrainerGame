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
            f"Total Owned Weight: {self.player.total_weight} kg",
            f"Barbell Weight: {self.player.barbell_weight} kg",
            f"Bucks: ${self.player.strength_bucks}",
            f"Cooldown: {round(self.player.get_current_rest_time(), 1)}s",
            f"Sponsor Money per Rep: ${self.player.get_sponsorship_bonus()}",
            f"Message: {self.message}",
        ]
        for label in labels:
            self.screen.blit(self.font.render(label, True, (255, 255, 255)), (x, y))
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
        padding = 30
        extra_vspace = 100
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        # Title
        title_x, title_y = padding, padding
        self.screen.blit(
            self.large_font.render("🏪 Store", True, (255, 255, 0)),
            (title_x, title_y)
        )
        # Bucks top-right
        bucks_surf = self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0))
        self.screen.blit(
            bucks_surf,
            (screen_w - padding - bucks_surf.get_width(), title_y)
        )

        # Tabs row, pushed down by another padding
        tab_y = title_y + self.large_font.get_height() + padding + extra_vspace
        self.buttons = [
            Button(padding, tab_y, 150, 40, self.font, "🧃 Recovery",
                   callback=lambda: self.set_tab("recovery"),
                   highlight=(self.store_tab == "recovery")),
            Button(padding + 160, tab_y, 150, 40, self.font, "📢 Sponsorships",
                   callback=lambda: self.set_tab("sponsorship"),
                   highlight=(self.store_tab == "sponsorship")),
            Button(padding + 320, tab_y, 150, 40, self.font, "🏋️ Weights",
                   callback=lambda: self.set_tab("weights"),
                   highlight=(self.store_tab == "weights")),
        ]

        # Now leave a full "padding" below tabs before drawing items
        items_start_y = tab_y + 40 + padding + extra_vspace

        # Pick the right items
        all_items = self.store.get_items()
        rec, spon, wts = self.store.get_grouped_items()
        keys = {"recovery": rec, "sponsorship": spon, "weights": wts}[self.store_tab]
        items = [all_items[k] for k in keys]

        # Grid layout
        desired_cols = 4
        col_width = (screen_w - 2 * padding) // desired_cols
        row_height = 120
        per_row = desired_cols

        for idx, item in enumerate(items):
            col = idx % per_row
            row = idx // per_row
            x = padding + col * col_width
            y = items_start_y + row * row_height

            # Cost (yellow)
            cost = self.font.render(f"Cost: ${item.cost}", True, (255, 255, 0))
            self.screen.blit(cost, (x, y - 50))

            # Description (white)
            desc = self.font.render(item.description, True, (255, 255, 255))
            self.screen.blit(desc, (x, y - 30))

            # Buy button
            maxed = item.limit is not None and item.times_bought >= item.limit
            label = "MAXED" if maxed else f"Buy ({item.times_bought}/{item.limit})"
            disabled = maxed or not item.can_buy(self.player)[0]
            self.buttons.append(
                Button(x, y, 160, 40, self.font, label,
                       callback=lambda it=item: self.purchase(it),
                       disabled=disabled)
            )

        # Back to Gym
        back_w, back_h = 160, 40
        bx = screen_w - back_w - padding
        by = screen_h - back_h - padding
        self.buttons.append(
            Button(bx, by, back_w, back_h, self.font, "Back to Gym",
                   self.go_to_gym, color=(255, 100, 100))
        )

        # Finally, draw all the buttons
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
        # Just go back to the main menu—no auto-save
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
        self.in_store = True
        self.message = ""

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
    
    def change_mode(self, mode: str):
        self.mode = mode
        self.buttons.clear()
