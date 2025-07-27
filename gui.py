import pygame
import time
from store import Store
from utils import Button

class GameGUI:
    def open_save_slots(self):
        if self.game:
            self.game.current_screen = self.game.save_slots_screen

    def __init__(self, screen, player, game_state):
        self.screen     = screen
        self.player     = player
        self.game_state = game_state
        self.store      = Store()
        self.store_tab  = "recovery"
        self.in_store   = False
        self.font       = pygame.font.SysFont(None, 24)
        self.large_font = pygame.font.SysFont(None, 32)
        self.buttons    = []
        self.message    = ""
        self.game       = None  # will be set in main

        # Slider state
        self.slider_dragging = False
        self.slider_track    = None
        self.slider_handle   = None

    def draw(self):
        self.screen.fill((30, 30, 30))
        if self.in_store:
            self.draw_store()
        else:
            self.draw_gym()

    def draw_gym(self):
        self.buttons = []
        self.screen.fill((30, 30, 30))

        padding = 30
        x, y = padding, padding
        line_height = 25

        labels = [
            f"Path: {self.player.path}",
            f"Reps: {self.player.reps}",
            f"Total Owned Weight: {self.player.total_weight:.1f} kg",
            f"Barbell Weight: {self.player.barbell_weight:.1f} kg",
            f"Bucks: ${self.player.strength_bucks}",
            f"Cooldown: {round(self.player.get_current_rest_time(), 1)}s",
            f"Sponsor Money per Rep: ${self.player.get_sponsorship_bonus()}",
            f"Message: {self.message}",
        ]
        for label in labels:
            self.screen.blit(self.font.render(label, True, (255, 255, 255)), (x, y))
            y += line_height

        y += 20  # extra space

        # Draw weight slider
        slider_x, slider_y = padding, y
        slider_w, slider_h = 200, 8
        min_wt = self.player.base_bar_weight
        max_wt = self.player.total_weight

        # Track
        pygame.draw.rect(self.screen, (100, 100, 100), (slider_x, slider_y, slider_w, slider_h))

        # Handle
        t = (self.player.barbell_weight - min_wt) / (max_wt - min_wt) if max_wt > min_wt else 0
        handle_x = slider_x + t * slider_w
        handle_y = slider_y + slider_h // 2
        pygame.draw.circle(self.screen, (200, 200, 0), (int(handle_x), int(handle_y)), 12)

        self.slider_track = pygame.Rect(slider_x, slider_y, slider_w, slider_h)
        self.slider_handle = pygame.Rect(int(handle_x) - 12, int(handle_y) - 12, 24, 24)

        wt_label = self.font.render(f"Barbell Weight: {self.player.barbell_weight:.1f} kg", True, (255, 255, 255))
        self.screen.blit(wt_label, (slider_x, slider_y - 30))

        y = slider_y + 60  # Move down for barbell drawing
        self.draw_barbell(slider_x, y)

        # Buttons below barbell
        btn_y = y + 100
        btn_x = padding
        btn_w, btn_h = 120, 40
        gap = 20

        self.buttons.append(Button(btn_x, btn_y, btn_w, btn_h, self.font, "Do Rep", self.do_rep))
        self.buttons.append(Button(btn_x + btn_w + gap, btn_y, btn_w, btn_h, self.font, "Open Store", self.open_store))
        self.buttons.append(Button(btn_x, btn_y + btn_h + gap, btn_w, btn_h, self.font, "Save & Exit", self.save_and_exit))
        self.buttons.append(Button(btn_x + btn_w + gap, btn_y + btn_h + gap, btn_w, btn_h, self.font, "Exit to Menu", self.exit_to_menu))

        for btn in self.buttons:
            btn.draw(self.screen)

    def draw_store(self):
        padding = 30
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        # Title
        self.screen.blit(self.large_font.render("🏪 Store", True, (255, 255, 0)), (padding, padding))
        # Bucks top-right
        bucks = self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0))
        self.screen.blit(bucks, (screen_w - padding - bucks.get_width(), padding))

        extra_v = 20
        tabs_y = padding + self.large_font.get_height() + extra_v
        self.buttons = [
            Button(padding, tabs_y, 150, 40, self.font, "🧃 Recovery",
                   callback=lambda: self.set_tab("recovery"),
                   highlight=(self.store_tab == "recovery")),
            Button(padding + 160, tabs_y, 150, 40, self.font, "📢 Sponsorships",
                   callback=lambda: self.set_tab("sponsorship"),
                   highlight=(self.store_tab == "sponsorship")),
            Button(padding + 320, tabs_y, 150, 40, self.font, "🏋️ Weights",
                   callback=lambda: self.set_tab("weights"),
                   highlight=(self.store_tab == "weights")),
        ]
        items_start_y = tabs_y + 40 + extra_v

        all_items = self.store.get_items()
        rec, spon, wts = self.store.get_grouped_items()
        keys = {"recovery": rec, "sponsorship": spon, "weights": wts}[self.store_tab]
        items = [all_items[k] for k in keys]

        cols = 4
        col_width = (screen_w - 2 * padding) // cols
        row_height = 120

        for idx, item in enumerate(items):
            col = idx % cols
            row = idx // cols
            x = padding + col * col_width
            y = items_start_y + row * row_height

            cost_surf = self.font.render(f"Cost: ${item.cost}", True, (255, 255, 0))
            self.screen.blit(cost_surf, (x, y - 50))
            desc_surf = self.font.render(item.description, True, (255, 255, 255))
            self.screen.blit(desc_surf, (x, y - 30))

            maxed = item.limit is not None and item.times_bought >= item.limit
            label = "MAXED" if maxed else f"Buy ({item.times_bought}/{item.limit})"
            disabled = maxed or not item.can_buy(self.player)[0]
            self.buttons.append(
                Button(x, y, 160, 40, self.font, label,
                       callback=lambda it=item: self.purchase(it),
                       disabled=disabled)
            )

        # Back to Gym button
        back_w, back_h = 160, 40
        bx = screen_w - back_w - padding
        by = screen_h - back_h - padding
        self.buttons.append(
            Button(bx, by, back_w, back_h, self.font, "Back to Gym",
                   callback=self.go_to_gym, color=(255, 100, 100))
        )

        for btn in self.buttons:
            btn.draw(self.screen)

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
        pygame.draw.rect(self.screen, BASE_BAR_COLOR, (x, y, BAR_LENGTH, BAR_HEIGHT))
        collar_w, collar_h = 40, 60
        pygame.draw.rect(self.screen, COLLAR_COLOR, (x - collar_w, y - 20, collar_w, collar_h))
        pygame.draw.rect(self.screen, COLLAR_COLOR, (x + BAR_LENGTH, y - 20, collar_w, collar_h))
        plate_x = x - collar_w
        for weight in sorted(self.player.plates.keys(), reverse=True):
            count = self.player.plates[weight]
            for _ in range(count):
                plate_x -= PLATE_WIDTH
                color = PLATE_COLORS.get(weight, (100, 100, 100))
                pygame.draw.rect(self.screen, color, (plate_x, y - (PLATE_HEIGHT - BAR_HEIGHT) // 2, PLATE_WIDTH, PLATE_HEIGHT))
        plate_x = x + BAR_LENGTH + collar_w
        for weight in sorted(self.player.plates.keys(), reverse=True):
            count = self.player.plates[weight]
            for _ in range(count):
                color = PLATE_COLORS.get(weight, (100, 100, 100))
                pygame.draw.rect(self.screen, color, (plate_x, y - (PLATE_HEIGHT - BAR_HEIGHT) // 2, PLATE_WIDTH, PLATE_HEIGHT))
                plate_x += PLATE_WIDTH

    def handle_event(self, event):
        # Slider drag logic
        if event.type == pygame.MOUSEBUTTONDOWN and self.slider_handle and self.slider_handle.collidepoint(event.pos):
            self.slider_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.slider_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.slider_dragging:
            mx, _ = event.pos
            if self.slider_track:
                clamped = max(self.slider_track.x, min(mx, self.slider_track.x + self.slider_track.w))
                t = (clamped - self.slider_track.x) / self.slider_track.w
                min_wt = self.player.base_bar_weight
                max_wt = self.player.total_weight
                new_wt = min_wt + t * (max_wt - min_wt)
                snapped = round((new_wt - min_wt) / 5) * 5 + min_wt
                self.player.barbell_weight = max(min_wt, min(snapped, max_wt))
        # Button events
        for btn in self.buttons:
            btn.handle_event(event)

    def do_rep(self):
        self.message = self.game_state.perform_rep()

    def purchase(self, item):
        self.message = item.buy(self.player)

    def save_and_exit(self):
        if self.game:
            self.game.current_screen = self.game.save_slots_screen
        self.message = ""

    def open_store(self):
        self.in_store = True
        self.message = ""

    def exit_to_menu(self):
        if self.game:
            self.game.current_screen = self.game.home_screen
        self.message = ""

    def set_tab(self, tab):
        self.store_tab = tab
        self.message = ""

    def go_to_gym(self):
        self.in_store = False
        self.message = ""
