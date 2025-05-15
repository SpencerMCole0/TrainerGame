import pygame
from store import Store
from utils import Button

class GameGUI:
    def __init__(self, screen, player, game_state):
        self.screen = screen
        self.player = player
        self.game_state = game_state
        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 32)
        self.message = ""
        self.mode = "recovery"
        self.store_tab = "recovery"
        self.buttons = []

    def draw(self):
        self.screen.fill((30, 30, 30))
        if self.mode == "store":
            self.draw_store()
        else:
            self.draw_gym()

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
            f"💪 Bonus per rep: ${self.player.extra_bucks_per_rep}",
            f"Message: {self.message}"
        ]

        for label in labels:
            self.screen.blit(self.font.render(label, True, (255, 255, 255)), (x, y))
            y += line_height

        self.buttons = []
        # Draw rep button with cooldown bar
        button_width, button_height = 200, 40
        rep_btn_x, rep_btn_y = 100, y + 10
        rep_ready = self.player.can_rep(self.game_state.current_time)

        rep_progress = self.player.rep_progress(self.game_state.current_time)
        btn_color = (0, 255, 0) if rep_ready else (50, 50, 50)
        fill_width = int(button_width * rep_progress)

        rep_rect = pygame.Rect(rep_btn_x, rep_btn_y, button_width, button_height)
        pygame.draw.rect(self.screen, (100, 100, 100), rep_rect)
        pygame.draw.rect(self.screen, btn_color, (rep_btn_x, rep_btn_y, fill_width, button_height))
        text = self.big_font.render("Do Rep", True, (0, 0, 0))
        text_rect = text.get_rect(center=rep_rect.center)
        self.screen.blit(text, text_rect)
        self.buttons.append(Button(rep_btn_x, rep_btn_y, button_width, button_height, "Do Rep", self.do_rep))

        # Store button
        self.buttons.append(Button(rep_btn_x + 220, rep_btn_y, 120, button_height, "Open Store", self.open_store))

        # Add/subtract weight buttons
        add_btn = Button(rep_btn_x + 120, rep_btn_y + 50, 100, 40, "+ Weight", self.add_weight)
        sub_btn = Button(rep_btn_x, rep_btn_y + 50, 100, 40, "- Weight", self.remove_weight)
        sub_btn.disabled = self.player.barbell_weight <= 45
        self.buttons.extend([sub_btn, add_btn])

    def draw_store(self):
        x, y = 30, 30
        header = self.big_font.render("🛒 Store", True, (255, 255, 0))
        self.screen.blit(header, (x, y))

        y += 40
        self.buttons = []
        tabs = [("Recovery", "recovery"), ("Sponsorships", "sponsorships"), ("Weights", "weights")]
        for i, (name, tab) in enumerate(tabs):
            tab_btn = Button(x + i * 160, y, 150, 30, f"🗂 {name}", lambda t=tab: self.set_store_tab(t))
            tab_btn.color = (180, 255, 180) if self.store_tab == tab else (200, 200, 200)
            self.buttons.append(tab_btn)

        y += 50
        self.screen.blit(self.font.render(f"Your Bucks: ${self.player.strength_bucks}", True, (0, 255, 0)), (x, y))
        y += 20

        # Show items from selected store tab
        category = store_items.get(self.store_tab, {})
        row = 0
        col = 0
        for key, item in category.items():
            if item.hidden:
                continue
            label = f"{item.label}"
            owned = self.player.inventory.get(key, 0)
            maxed = owned >= item.max_quantity
            desc = f"{item.description}"
            short = f"Buy ({owned}/{item.max_quantity})"
            text_color = (255, 255, 255)

            label_surf = self.font.render(desc, True, text_color)
            self.screen.blit(label_surf, (x + col * 220, y + row * 80))

            btn = Button(x + col * 220, y + row * 80 + 20, 150, 40, short,
                         lambda i=item: self.purchase(i), disabled=not item.can_afford(self.player) or maxed)
            self.buttons.append(btn)

            col += 1
            if col >= 4:
                col = 0
                row += 1

        self.buttons.append(Button(330, y + row * 80 + 60, 150, 40, "Back to Gym", self.close_store))

    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event)

    def do_rep(self):
        self.game_state.perform_rep(self.player)

    def open_store(self):
        self.mode = "store"

    def close_store(self):
        self.mode = "gym"

    def set_store_tab(self, tab):
        self.store_tab = tab

    def purchase(self, item):
        if item.purchase(self.player):
            self.message = f"✅ Purchased {item.label}"
        else:
            self.message = "❌ Not enough bucks or already maxed"

    def add_weight(self):
        self.player.total_weight += 5
        self.player.barbell_weight += 5

    def remove_weight(self):
        if self.player.barbell_weight > 45:
            self.player.barbell_weight -= 5
